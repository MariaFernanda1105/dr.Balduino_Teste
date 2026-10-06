"""Rotas administrativas."""
import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, jsonify
from flask_login import login_required, current_user
from datetime import datetime, timezone
import bleach
from bleach.css_sanitizer import CSSSanitizer
from models.article import Article
from models.article_view import ArticleView
from models import db
from utils.helpers import save_upload

admin_bp = Blueprint("admin", __name__)

ALLOWED_TAGS = [
    "p", "br", "strong", "b", "em", "i", "u", "h1", "h2", "h3", "h4",
    "ul", "ol", "li", "a", "blockquote", "img"
    , "figure", "figcaption", "table", "thead", "tbody", "tfoot", "tr", "th", "td", "span", "div", "hr", "sub", "sup", "s", "mark"
]
ALLOWED_ATTRS = {
    "a": ["href", "title", "target", "rel"],
    "img": ["src", "alt", "title", "width", "height"],
    "figure": ["class"],
    "div": ["class"],
    "span": ["class", "style"],
    "p": ["style"],
    "h1": ["style"],
    "h2": ["style"],
    "h3": ["style"],
    "h4": ["style"],
    "blockquote": ["style"],
    "table": ["class"],
    "th": ["colspan", "rowspan"],
    "td": ["colspan", "rowspan"],
}
CSS_SANITIZER = CSSSanitizer(allowed_css_properties={"color", "background-color", "font-size", "font-family", "text-align", "width", "height", "float", "margin", "display"})

def sanitize_content(content):
    return bleach.clean(content, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS, css_sanitizer=CSS_SANITIZER, strip=True)

@admin_bp.route("/upload-image", methods=["POST"])
@login_required
def upload_image():
    """Recebe imagens inseridas no editor e devolve a URL pública segura."""
    file = request.files.get("upload")
    if not file or not file.filename:
        return jsonify({"error": {"message": "Nenhuma imagem foi enviada."}}), 400

    filename = save_upload(file)
    if not filename:
        return jsonify({"error": {"message": "Formato de imagem não permitido."}}), 400

    return jsonify({"url": url_for("static", filename=f"uploads/{filename}")})

@admin_bp.route("/dashboard")
@login_required
def dashboard():
    published_count = Article.query.filter_by(status="publicado").count()
    draft_count = Article.query.filter_by(status="rascunho").count()
    total_views = db.session.query(ArticleView).count()
    recent_articles = Article.query.order_by(Article.updated_at.desc()).limit(5).all()

    # Artigos mais visualizados
    top_articles = db.session.query(
        Article, db.func.count(ArticleView.id).label("view_count")
    ).join(ArticleView).group_by(Article.id).order_by(db.desc("view_count")).limit(5).all()

    return render_template("admin/dashboard.html",
                         published_count=published_count,
                         draft_count=draft_count,
                         total_views=total_views,
                         recent_articles=recent_articles,
                         top_articles=top_articles)

@admin_bp.route("/artigos")
@login_required
def admin_artigos():
    articles = Article.query.order_by(Article.updated_at.desc()).all()
    return render_template("admin/artigos.html", articles=articles)

@admin_bp.route("/artigos/novo", methods=["GET", "POST"])
@login_required
def novo_artigo():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        summary = request.form.get("summary", "").strip()
        content = sanitize_content(request.form.get("content", ""))
        status = request.form.get("status", "rascunho")

        if not title or not summary or not content:
            flash("Preencha todos os campos obrigatórios.", "warning")
            return render_template("admin/artigo_form.html")

        article = Article(
            title=title,
            summary=summary,
            content=content,
            status=status,
            author_id=current_user.id
        )
        article.generate_slug()

        if status == "publicado":
            article.published_at = datetime.now(timezone.utc)

        # Upload de imagem
        if "cover_image" in request.files:
            file = request.files["cover_image"]
            if file.filename:
                filename = save_upload(file)
                if filename:
                    article.cover_image = filename
                else:
                    flash("Formato de imagem não permitido.", "warning")

        db.session.add(article)
        db.session.commit()
        flash("Artigo criado com sucesso!", "success")
        return redirect(url_for("admin.admin_artigos"))

    return render_template("admin/artigo_form.html")

@admin_bp.route("/artigos/<int:id>/editar", methods=["GET", "POST"])
@login_required
def editar_artigo(id):
    article = Article.query.get_or_404(id)

    if request.method == "POST":
        article.title = request.form.get("title", "").strip()
        article.summary = request.form.get("summary", "").strip()
        article.content = sanitize_content(request.form.get("content", ""))
        new_status = request.form.get("status", "rascunho")

        if not article.title or not article.summary or not article.content:
            flash("Preencha todos os campos obrigatórios.", "warning")
            return render_template("admin/artigo_form.html", article=article)

        # Se mudou para publicado e não tinha data
        if new_status == "publicado" and article.status != "publicado":
            article.published_at = datetime.now(timezone.utc)

        article.status = new_status

        # Upload de nova imagem
        if "cover_image" in request.files:
            file = request.files["cover_image"]
            if file.filename:
                filename = save_upload(file)
                if filename:
                    # Remover imagem antiga
                    if article.cover_image:
                        old_path = os.path.join(current_app.config["UPLOAD_FOLDER"], article.cover_image)
                        if os.path.exists(old_path):
                            os.remove(old_path)
                    article.cover_image = filename
                else:
                    flash("Formato de imagem não permitido.", "warning")

        db.session.commit()
        flash("Artigo atualizado com sucesso!", "success")
        return redirect(url_for("admin.admin_artigos"))

    return render_template("admin/artigo_form.html", article=article)

@admin_bp.route("/artigos/<int:id>/excluir", methods=["POST"])
@login_required
def excluir_artigo(id):
    article = Article.query.get_or_404(id)

    # Remover imagem
    if article.cover_image:
        img_path = os.path.join(current_app.config["UPLOAD_FOLDER"], article.cover_image)
        if os.path.exists(img_path):
            os.remove(img_path)

    db.session.delete(article)
    db.session.commit()
    flash("Artigo excluído com sucesso!", "success")
    return redirect(url_for("admin.admin_artigos"))

@admin_bp.route("/artigos/<int:id>/publicar", methods=["POST"])
@login_required
def publicar_artigo(id):
    article = Article.query.get_or_404(id)
    article.status = "publicado"
    if not article.published_at:
        article.published_at = datetime.now(timezone.utc)
    db.session.commit()
    flash("Artigo publicado!", "success")
    return redirect(url_for("admin.admin_artigos"))

@admin_bp.route("/artigos/<int:id>/despublicar", methods=["POST"])
@login_required
def despublicar_artigo(id):
    article = Article.query.get_or_404(id)
    article.status = "rascunho"
    db.session.commit()
    flash("Artigo movido para rascunhos.", "info")
    return redirect(url_for("admin.admin_artigos"))
