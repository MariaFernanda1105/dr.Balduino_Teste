"""Aplicação principal — Application Factory."""
import os
import click
from urllib.parse import quote_plus
from flask import Flask, request
from werkzeug.middleware.proxy_fix import ProxyFix
from config import Config
from models import db, login_manager
from models.user import User
from models.article import Article
from models.article_view import ArticleView
from routes import register_blueprints

def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(config_class)
    # Atrás de proxy (Render, Railway, Fly.io...) o esquema/host corretos vêm dos cabeçalhos X-Forwarded-*
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)
    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    @app.context_processor
    def inject_site_settings():
        site_url = (app.config.get("SITE_URL") or request.url_root).rstrip("/")
        return {
            "site_url": site_url,
            "physician_schema": build_physician_schema(app.config, site_url),
            "site_name": "Dr. Balduino Andrade",
            "site_specialty": "Nefrologista",
            "whatsapp_number": app.config.get("WHATSAPP_NUMBER", "5563984668607"),
            "appointment_url": app.config.get("APPOINTMENT_URL", "https://www.doctoralia.com.br/balduino-andrade/nefrologista/palmas2"),
            "clinic_name": app.config.get("CLINIC_NAME", "DaVita Tratamento Renal"),
            "clinic_subtitle": app.config.get("CLINIC_SUBTITLE", "Consultório e tratamento renal em Palmas"),
            "clinic_address": app.config.get("CLINIC_ADDRESS", "Av. Teotônio Segurado, Quadra 201 Sul, Cj 1 Lt 5"),
            "clinic_city": app.config.get("CLINIC_CITY", "DaVita Tratamento Renal · Palmas, Tocantins"),
            "clinic_hours": app.config.get("CLINIC_HOURS", "Atendimento sob agendamento"),
            "clinic_phone": app.config.get("CLINIC_PHONE", ""),
            "clinic_email": app.config.get("CLINIC_EMAIL", ""),
            "clinic_instagram": app.config.get("CLINIC_INSTAGRAM", ""),
            "clinic_map_url": app.config.get("CLINIC_MAP_URL") or "https://www.google.com/maps/search/?api=1&query=" + quote_plus("{} {}, {}".format(app.config.get("CLINIC_NAME", "Clínica de Nefrologia"), app.config.get("CLINIC_ADDRESS", ""), app.config.get("CLINIC_CITY", ""))),
            "doctor_crm": app.config.get("DOCTOR_CRM", ""),
            "doctor_rqe": app.config.get("DOCTOR_RQE", ""),
            "doctor_training": app.config.get("DOCTOR_TRAINING", "Formação e registros profissionais em atualização"),
        }

    db.init_app(app)
    login_manager.init_app(app)

    register_blueprints(app)

    @app.cli.command("create-admin")
    @click.option("--username", default="admin")
    @click.option("--password", prompt=True, hide_input=True)
    def create_admin(username, password):
        """Cria um usuário administrador."""
        with app.app_context():
            if User.query.filter_by(username=username).first():
                click.echo(f"Usuário '{username}' já existe.")
                return

            user = User(username=username, is_active=True)
            user.set_password(password)

            db.session.add(user)
            db.session.commit()

            click.echo(f"Administrador '{username}' criado com sucesso!")

    @app.cli.command("init-db")
    def init_db():
        """Cria as tabelas do banco de dados."""
        with app.app_context():
            db.create_all()
            click.echo("Banco de dados inicializado com sucesso!")

    @app.cli.command("seed")
    def seed():
        """Popula o banco com dados de demonstração."""
        with app.app_context():
            seed_demo_data()
            click.echo("Dados de demonstração inseridos.")

    return app

def build_physician_schema(cfg, site_url):
    """Dados estruturados (schema.org) do médico e do local de atendimento, para SEO local."""
    same_as = [u for u in (cfg.get("CLINIC_INSTAGRAM"), cfg.get("APPOINTMENT_URL")) if u]
    schema = {
        "@context": "https://schema.org",
        "@type": ["Physician", "MedicalBusiness"],
        "@id": site_url + "/#medico",
        "name": "Dr. Balduino Andrade",
        "description": "Nefrologista em Palmas, Tocantins. Prevenção, diagnóstico e acompanhamento da saúde renal.",
        "url": site_url + "/",
        "image": site_url + "/static/images/doctor-portrait.jpeg",
        "medicalSpecialty": "Nephrology",
        "areaServed": {"@type": "City", "name": "Palmas"},
        "address": {
            "@type": "PostalAddress",
            "streetAddress": cfg.get("CLINIC_ADDRESS") or "",
            "addressLocality": "Palmas",
            "addressRegion": "TO",
            "addressCountry": "BR",
        },
        "location": {"@type": "MedicalClinic", "name": cfg.get("CLINIC_NAME") or ""},
    }
    if cfg.get("CLINIC_PHONE"):
        schema["telephone"] = cfg["CLINIC_PHONE"]
    if cfg.get("CLINIC_EMAIL"):
        schema["email"] = cfg["CLINIC_EMAIL"]
    if same_as:
        schema["sameAs"] = same_as
    return schema


def seed_demo_data():
    """Insere artigos de demonstração."""
    # Criar usuário demo se não existir
    admin = User.query.filter_by(username="admin").first()
    if not admin:
        admin = User(username="admin", is_active=True)
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()

    demo_articles = [
        {
            "title": "Como cuidar da saúde dos rins no dia a dia",
            "summary": "Descubra hábitos simples e eficazes para manter seus rins saudáveis e prevenir doenças renais.",
            "content": """
            <p>A saúde renal é fundamental para o bem-estar geral do corpo. Os rins desempenham um papel crucial na filtração de toxinas, regulação da pressão arterial e equilíbrio de eletrólitos.</p>
            <h3>Hidratação adequada</h3>
            <p>Beber água suficiente é o primeiro passo. A quantidade ideal varia conforme o peso, clima e atividade física, mas em média recomenda-se cerca de 2 litros por dia.</p>
            <h3>Alimentação balanceada</h3>
            <p>Reduza o consumo de sal e alimentos ultraprocessados. Prefira frutas, legumes e proteínas magras.</p>
            <h3>Exercícios regulares</h3>
            <p>A atividade física ajuda a controlar a pressão arterial e o peso, fatores de risco importantes para doença renal.</p>
            <blockquote>Este conteúdo é demonstrativo e não substitui uma avaliação médica individualizada.</blockquote>
            """,
            "status": "publicado"
        },
        {
            "title": "Hipertensão arterial e os rins: entenda a relação",
            "summary": "A pressão alta é uma das principais causas de doença renal crônica. Saiba como proteger seus rins.",
            "content": """
            <p>A hipertensão arterial e a doença renal têm uma relação de mão dupla: a pressão alta danifica os rins, e rins danificados pioram a pressão arterial.</p>
            <h3>Como a hipertensão afeta os rins?</h3>
            <p>Os vasos sanguíneos dos rins são delicados. A pressão elevada força esses vasos, causando espessamento e estreitamento, reduzindo a filtração.</p>
            <h3>Sinais de alerta</h3>
            <ul>
                <li>Inchaço nas pernas e pés</li>
                <li>Alterações na urina</li>
                <li>Fadiga persistente</li>
                <li>Dores de cabeça frequentes</li>
            </ul>
            <h3>Prevenção</h3>
            <p>Controle da pressão arterial, dieta com pouco sódio, exercícios e acompanhamento médico regular são essenciais.</p>
            <blockquote>Este conteúdo é demonstrativo e não substitui uma avaliação médica individualizada.</blockquote>
            """,
            "status": "publicado"
        },
        {
            "title": "A importância do acompanhamento da função renal",
            "summary": "Exames simples podem detectar precocemente alterações na função renal. Conheça os principais exames.",
            "content": """
            <p>O diagnóstico precoce de alterações renais permite intervenções que podem retardar ou prevenir a progressão da doença renal crônica.</p>
            <h3>Principais exames</h3>
            <ul>
                <li><strong>Creatinina sérica:</strong> avalia a filtração glomerular</li>
                <li><strong>Ureia:</strong> indica a capacidade de eliminação renal</li>
                <li><strong>Proteinúria:</strong> detecta perda de proteína na urina</li>
                <li><strong>Exame de urina (EAS):</strong> identifica sangue, células e outras alterações</li>
            </ul>
            <h3>Quem deve fazer acompanhamento?</h3>
            <p>Pessoas com diabetes, hipertensão, histórico familiar de doença renal, idosos e quem faz uso contínuo de medicamentos nefrotóxicos.</p>
            <blockquote>Este conteúdo é demonstrativo e não substitui uma avaliação médica individualizada.</blockquote>
            """,
            "status": "publicado"
        },
        {
            "title": "Prevenção da doença renal: o que você precisa saber",
            "summary": "Medidas preventivas simples podem reduzir significativamente o risco de desenvolver doença renal crônica.",
            "content": """
            <p>A doença renal crônica (DRC) afeta milhões de pessoas, muitas vezes sem sintomas nos estágios iniciais. A prevenção é a melhor estratégia.</p>
            <h3>Fatores de risco modificáveis</h3>
            <ul>
                <li>Diabetes mellitus mal controlado</li>
                <li>Hipertensão arterial</li>
                <li>Obesidade</li>
                <li>Tabagismo</li>
                <li>Uso abusivo de anti-inflamatórios</li>
            </ul>
            <h3>Check-up renal anual</h3>
            <p>Pacientes com fatores de risco devem realizar exames renais anuais. A detecção precoce muda o prognóstico.</p>
            <blockquote>Este conteúdo é demonstrativo e não substitui uma avaliação médica individualizada.</blockquote>
            """,
            "status": "rascunho"
        },
        {
            "title": "7 sinais que merecem atenção na saúde dos rins",
            "summary": "Nem toda doença renal causa sintomas. Veja alterações que merecem conversa com um profissional.",
            "content": "<p>Nem toda doença renal causa sintomas no início. Por isso, alterações em exames de sangue e urina podem ser importantes mesmo quando a pessoa se sente bem.</p><h3>O que observar</h3><ul><li>Inchaço persistente</li><li>Alterações na urina</li><li>Pressão alta ou difícil de controlar</li><li>Cansaço sem explicação</li><li>Creatinina ou TFG alteradas</li><li>Proteína ou sangue na urina</li><li>Histórico familiar de doença renal</li></ul><blockquote>Este conteúdo é educativo e não substitui uma avaliação individualizada.</blockquote>",
            "status": "publicado"
        },
        {
            "title": "Creatinina alta significa insuficiência renal?",
            "summary": "Entenda por que a creatinina precisa ser interpretada junto com a TFG e o contexto clínico.",
            "content": "<p>Não necessariamente. A creatinina deve ser interpretada considerando idade, sexo, massa muscular, hidratação, medicamentos, contexto clínico e estimativa da taxa de filtração glomerular.</p><h3>O que fazer?</h3><p>Compare com exames anteriores e converse com o médico responsável. Um resultado isolado não define sozinho um diagnóstico.</p><blockquote>Este conteúdo é educativo e não substitui uma avaliação individualizada.</blockquote>",
            "status": "publicado"
        },
        {
            "title": "Beber muita água protege os rins?",
            "summary": "A hidratação é importante, mas a quantidade ideal não é igual para todas as pessoas.",
            "content": "<p>A hidratação adequada é importante, mas não existe uma quantidade universal de água ideal para todas as pessoas. Necessidades variam conforme clima, atividade física, alimentação, idade e função dos rins.</p><h3>Individualize o cuidado</h3><p>Pessoas com doença renal, insuficiência cardíaca ou outras condições podem receber orientações específicas. Evite transformar uma recomendação geral em regra pessoal.</p><blockquote>Este conteúdo é educativo e não substitui uma avaliação individualizada.</blockquote>",
            "status": "publicado"
        },
        {
            "title": "Pressão alta pode causar doença renal?",
            "summary": "A hipertensão é um importante fator de risco para o desenvolvimento e a progressão da doença renal crônica.",
            "content": "<p>Sim. A hipertensão arterial pode danificar os vasos dos rins e acelerar a perda da função renal. Ao mesmo tempo, alterações renais podem dificultar o controle da pressão.</p><h3>Por que acompanhar?</h3><p>Medir a pressão, revisar o tratamento e acompanhar exames de função renal e urina são partes importantes da prevenção.</p><blockquote>Este conteúdo é educativo e não substitui uma avaliação individualizada.</blockquote>",
            "status": "publicado"
        }
    ]

    for data in demo_articles:
        if Article.query.filter_by(title=data["title"]).first():
            continue
        article = Article(
            title=data["title"],
            summary=data["summary"],
            content=data["content"],
            status=data["status"],
            author_id=admin.id
        )
        article.generate_slug()
        if data["status"] == "publicado":
            from datetime import datetime, timezone
            article.published_at = datetime.now(timezone.utc)
        db.session.add(article)

    db.session.commit()

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
