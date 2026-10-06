"""Modelo de artigo."""
from datetime import datetime, timezone
from slugify import slugify as python_slugify
from models import db


class Article(db.Model):
    __tablename__ = "articles"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(250), unique=True, nullable=False, index=True)
    summary = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    cover_image = db.Column(db.String(250), nullable=True)
    status = db.Column(db.String(20), default="rascunho", nullable=False)  # rascunho, publicado
    
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    author = db.relationship("User", back_populates="articles")
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), 
                           onupdate=lambda: datetime.now(timezone.utc))
    published_at = db.Column(db.DateTime, nullable=True)
    
    # Relacionamento com visualizações
    views = db.relationship("ArticleView", back_populates="article", 
                           cascade="all, delete-orphan", lazy="dynamic")
    
    def generate_slug(self):
        base_slug = python_slugify(self.title)
        slug = base_slug
        counter = 1
        while Article.query.filter_by(slug=slug).first():
            slug = f"{base_slug}-{counter}"
            counter += 1
        self.slug = slug
    
    @property
    def view_count(self):
        return self.views.count()
    
    def __repr__(self):
        return f"<Article {self.title}>"