"""Rotas públicas do site e biblioteca de conteúdos clínicos."""
from datetime import datetime, timezone
from flask import Blueprint, render_template, abort, make_response, request, url_for, current_app
from models.article import Article
from models.article_view import ArticleView
from models import db
from utils.exams_content import EXAMS

public_bp = Blueprint("public", __name__)


def section(title, body):
    return {"title": title, "body": body}


TOPICS = {
    "quando-procurar": {
        "eyebrow": "Orientação ao paciente", "title": "Quando procurar um nefrologista?",
        "lead": "Algumas alterações podem permanecer silenciosas durante muito tempo. A avaliação nefrológica ajuda a investigar riscos e a definir os próximos passos.",
        "highlight": "Exames alterados nem sempre significam uma doença grave — mas merecem ser compreendidos no contexto de cada pessoa.",
        "icon": "bi-person-check",
        "sections": [section("Situações que merecem avaliação", "<ul><li>Creatinina sérica elevada ou em elevação</li><li>Taxa de filtração glomerular (TFG) reduzida</li><li>Proteinúria ou albuminúria</li><li>Hematúria ou alterações persistentes no exame de urina</li><li>Hipertensão arterial de difícil controle</li><li>Cálculos renais recorrentes</li><li>Infecções urinárias recorrentes em situações selecionadas</li><li>Alterações de eletrólitos</li><li>Diabetes, doença cardiovascular ou histórico familiar de doença renal</li></ul>"), section("Por que avaliar cedo?", "A função renal e o risco cardiovascular estão relacionados. Uma avaliação individualizada pode esclarecer a causa de uma alteração, orientar exames e ajudar a prevenir progressão ou complicações.")]
    },
    "doenca-renal-cronica": {
        "eyebrow": "Doença renal", "title": "Doença renal crônica: muitas vezes, silenciosa",
        "lead": "A doença renal crônica pode evoluir durante anos sem provocar sintomas evidentes. Identificar cedo permite investigar a causa e controlar fatores de progressão.",
        "highlight": "Nem toda alteração da creatinina significa doença renal crônica — e nem toda doença renal apresenta creatinina elevada no início.", "icon": "bi-heart-pulse",
        "sections": [section("O que precisa ser investigado", "A avaliação considera a função renal, a presença de albumina ou proteína na urina, a pressão arterial, o histórico clínico, os medicamentos e exames de imagem quando indicados."), section("Cuidar além do número", "O acompanhamento busca reduzir riscos cardiovasculares, preservar a função renal e orientar decisões sobre alimentação, pressão, diabetes e medicamentos. O estágio e a causa da doença fazem diferença no plano de cuidado.")]
    },
    "hipertensao-e-rins": {
        "eyebrow": "Pressão arterial", "title": "Sua pressão está difícil de controlar? Os rins podem estar envolvidos.",
        "lead": "Os rins participam diretamente da regulação da pressão arterial. Ao mesmo tempo, a hipertensão pode causar ou acelerar a perda da função renal.", "highlight": "Pressão alta e doença renal podem se influenciar mutuamente — por isso, o cuidado precisa olhar para as duas condições.", "icon": "bi-activity",
        "sections": [section("Quando investigar", "Quando a pressão permanece elevada apesar do tratamento, quando são necessários vários medicamentos ou quando aparecem alterações nos exames, uma investigação especializada pode ser necessária."), section("O que a consulta organiza", "A avaliação revisa medidas de pressão, adesão e horários dos medicamentos, função renal, eletrólitos, hábitos e possíveis causas secundárias, sempre de acordo com a história clínica.")]
    },
    "diabetes-e-rins": {
        "eyebrow": "Diabetes", "title": "Diabetes: proteja seus rins antes que apareçam sintomas",
        "lead": "O diabetes mellitus é uma das principais causas de doença renal crônica. A avaliação periódica ajuda a identificar alterações precocemente.", "highlight": "A albuminúria pode sinalizar risco renal mesmo quando a pessoa ainda se sente bem.", "icon": "bi-droplet-half",
        "sections": [section("O que acompanhar", "Além da glicemia, a avaliação costuma considerar creatinina, taxa de filtração glomerular e albuminúria, junto com pressão arterial, peso e outros fatores de risco."), section("Prevenção personalizada", "O objetivo é construir estratégias realistas para reduzir o risco de progressão, em parceria com as equipes que já acompanham o diabetes e outras condições de saúde.")]
    },
    "glomerulopatias": {
        "eyebrow": "Atuação especializada", "title": "Glomerulopatias",
        "lead": "As glomerulopatias são doenças que acometem os glomérulos, estruturas responsáveis por parte fundamental da filtração dos rins.", "highlight": "Proteína na urina não é um diagnóstico. É um sinal que precisa ser investigado.", "icon": "bi-filter-circle",
        "sections": [section("Como podem aparecer", "Podem se manifestar por proteinúria, albuminúria, hematúria, edema, hipertensão arterial ou redução da função renal. Em muitos casos, os sinais são percebidos primeiro em exames."), section("Investigação", "O diagnóstico pode exigir exames laboratoriais especializados e, em situações selecionadas, biópsia renal. A indicação depende do conjunto de achados e da avaliação médica.")]
    },
    "calculo-renal": {
        "eyebrow": "Cálculo renal", "title": "Investigar a causa é tão importante quanto tratar a crise",
        "lead": "Pessoas que apresentam cálculos renais recorrentes podem se beneficiar de uma investigação metabólica para identificar fatores associados à formação das pedras.", "highlight": "Depois de uma crise, entender por que o cálculo se formou pode ajudar a reduzir novas ocorrências.", "icon": "bi-gem",
        "sections": [section("Investigação metabólica", "Conforme o caso, podem ser avaliados histórico alimentar, hidratação, composição do cálculo, exames de sangue e urina e outros fatores que participam da formação de cristais."), section("Prevenção individualizada", "Hidratação, consumo de sal, alimentação e outras medidas devem ser orientados de acordo com o tipo de cálculo, a função renal e as condições de saúde da pessoa.")]
    },
    "medicamentos-e-rins": {
        "eyebrow": "Segurança medicamentosa", "title": "Seus medicamentos são seguros para os rins?",
        "lead": "Alguns medicamentos precisam ter sua dose ajustada de acordo com a função renal. Outros podem aumentar o risco de lesão renal em determinadas situações.", "highlight": "Não suspenda medicamentos por conta própria. A revisão deve ser feita com orientação profissional.", "icon": "bi-capsule",
        "sections": [section("O que pode ser revisado", "A consulta pode organizar nomes, doses, horários, suplementos e medicamentos de uso eventual, além de avaliar função renal, hidratação e combinações que merecem atenção."), section("Anti-inflamatórios e outros riscos", "Medicamentos como diclofenaco, nimesulida e ibuprofeno podem oferecer riscos em determinados contextos, especialmente em pessoas idosas, desidratadas ou com doença renal. A decisão é individual.")]
    },
    "hemodialise": {
        "eyebrow": "Terapia renal substitutiva", "title": "Quando os rins deixam de funcionar adequadamente",
        "lead": "A terapia renal substitutiva pode ser necessária quando a função dos rins se torna insuficiente para manter o equilíbrio de líquidos, eletrólitos e substâncias produzidas pelo metabolismo.", "highlight": "A indicação de diálise considera o quadro clínico completo, e não apenas um determinado valor de creatinina.", "icon": "bi-hospital",
        "sections": [section("O que é hemodiálise", "A hemodiálise utiliza uma máquina e um filtro para ajudar a remover substâncias e excesso de líquido do sangue quando os rins não conseguem cumprir adequadamente essa função."), section("Decisões compartilhadas", "O acompanhamento envolve sintomas, exames, estado nutricional, acesso vascular, rotina e preferências. Hemodiálise, diálise peritoneal e transplante fazem parte de uma conversa individualizada quando indicados.")]
    },
    "prevencao": {
        "eyebrow": "Prevenção", "title": "Você conhece o risco dos seus rins?",
        "lead": "Diabetes, hipertensão arterial, obesidade, doença cardiovascular, histórico familiar e uso de determinados medicamentos podem aumentar o risco de doença renal.", "highlight": "Prevenir não significa fazer todos os exames — significa identificar o que faz sentido para o seu risco.", "icon": "bi-shield-plus",
        "sections": [section("Fatores que merecem atenção", "Pressão alta, glicemia alterada, excesso de peso, tabagismo, sedentarismo, histórico familiar e episódios de lesão renal podem mudar a necessidade de acompanhamento."), section("Hábitos que protegem", "Alimentação equilibrada, atividade física, controle da pressão e do diabetes, evitar tabaco e uso sem orientação de medicamentos são atitudes importantes. A quantidade ideal de água varia conforme cada pessoa.")]
    },
    "nefrologista-ou-urologista": {
        "eyebrow": "Entenda a diferença", "title": "Nefrologista ou urologista: quem devo procurar?",
        "lead": "As duas especialidades cuidam do sistema urinário, mas atuam com focos diferentes e muitas vezes trabalham em conjunto.", "highlight": "Em algumas situações, o acompanhamento conjunto é o mais adequado.", "icon": "bi-people",
        "sections": [section("Nefrologista", "É o médico especializado no diagnóstico e tratamento clínico das doenças dos rins e de alterações relacionadas à função renal, como doença renal crônica, glomerulopatias, hipertensão relacionada aos rins e distúrbios de eletrólitos."), section("Urologista", "Atua principalmente nas doenças cirúrgicas e anatômicas do aparelho urinário e do sistema reprodutor masculino, incluindo situações que podem exigir procedimentos."), section("E quando há dúvida?", "Uma avaliação inicial pode ajudar a organizar os sintomas e exames e indicar qual especialista — ou quais equipes — devem participar do cuidado.")]
    },
    "consulta-nefrologica": {
        "eyebrow": "Como funciona", "title": "Como funciona a consulta nefrológica",
        "lead": "Mais importante do que interpretar um exame isoladamente é compreender o paciente por trás dele.", "highlight": "A consulta é um espaço para organizar informações, esclarecer dúvidas e construir prioridades.", "icon": "bi-clipboard2-pulse",
        "sections": [section("As seis etapas do cuidado", "<ol><li>Avaliação clínica e escuta da história</li><li>Análise dos exames disponíveis</li><li>Identificação dos fatores de risco cardiovascular e renal</li><li>Investigação diagnóstica quando necessária</li><li>Definição do tratamento e das orientações</li><li>Acompanhamento da evolução e reavaliação</li></ol>"), section("Como se preparar", "Leve exames anteriores e recentes, lista de medicamentos e suplementos, informações sobre pressão arterial e suas principais dúvidas. Não é necessário esperar ter todos os exames para buscar orientação.")]
    },
}

CITY_TAG = "Nefrologista em Palmas – TO"

TOPIC_SEO_TITLES = {
    "quando-procurar": "Quando procurar um nefrologista em Palmas – TO",
    "doenca-renal-cronica": "Doença renal crônica: avaliação e acompanhamento | Palmas – TO",
    "hipertensao-e-rins": "Hipertensão e rins: avaliação com nefrologista em Palmas – TO",
    "diabetes-e-rins": "Diabetes e rins: prevenção com nefrologista em Palmas – TO",
    "glomerulopatias": "Glomerulopatias: investigação com nefrologista em Palmas – TO",
    "calculo-renal": "Cálculo renal: investigação e prevenção em Palmas – TO",
    "medicamentos-e-rins": "Medicamentos e rins: revisão com nefrologista em Palmas – TO",
    "hemodialise": "Hemodiálise e terapia renal substitutiva | Palmas – TO",
    "prevencao": "Prevenção da doença renal | Nefrologista em Palmas – TO",
    "nefrologista-ou-urologista": "Nefrologista ou urologista: qual procurar? | Palmas – TO",
    "consulta-nefrologica": "Como funciona a consulta com o nefrologista | Palmas – TO",
}


def seo_description(text, suffix=" " + CITY_TAG + ".", limit=158):
    """Meta description com até ~158 caracteres, cortada em palavra inteira e terminando com a cidade."""
    room = limit - len(suffix)
    if len(text) > room:
        text = text[:room].rsplit(" ", 1)[0].rstrip(" ,;:.") + "…"
    return text + suffix


def topic_canonical_path(slug):
    return "/quando-procurar" if slug == "quando-procurar" else "/nefrologia/" + slug


def render_topic(topic, slug, **extra):
    topic = dict(topic)
    topic.setdefault("seo_title", topic["title"] + " | " + CITY_TAG)
    topic.setdefault("seo_description", seo_description(topic["lead"]))
    return render_template("topic.html", topic=topic, slug=slug, **extra)


FAQS = [
    ("Quando devo procurar um nefrologista?", "Quando houver alteração persistente na creatinina, TFG reduzida, proteína ou sangue na urina, pressão difícil de controlar, diabetes, cálculos recorrentes ou histórico familiar."),
    ("Creatinina alta é sempre doença renal?", "Não. A creatinina depende de vários fatores e deve ser interpretada com a TFG, o histórico e outros exames."),
    ("Quem tem diabetes precisa consultar um nefrologista?", "Nem sempre de forma imediata, mas o diabetes exige acompanhamento periódico da função renal e da albuminúria. Alterações ou maior risco podem indicar avaliação especializada."),
    ("Pedra nos rins é tratada pelo nefrologista?", "O nefrologista investiga fatores metabólicos e prevenção de recorrência. O urologista participa quando há necessidade de procedimento ou abordagem cirúrgica."),
    ("Qual a diferença entre nefrologista e urologista?", "O nefrologista trata clinicamente a função e as doenças dos rins. O urologista atua principalmente em condições anatômicas e cirúrgicas do aparelho urinário."),
    ("Tenho proteína na urina. É grave?", "A proteinúria é um sinal que precisa ser confirmado e quantificado. A importância depende da quantidade, persistência e contexto."),
    ("Posso tomar anti-inflamatório tendo doença renal?", "Não use sem orientação. Alguns anti-inflamatórios podem aumentar o risco de lesão renal em determinadas situações."),
    ("É possível prevenir a progressão da doença renal crônica?", "Em muitos casos é possível reduzir riscos com diagnóstico da causa, controle da pressão e diabetes, revisão de medicamentos e acompanhamento contínuo."),
]


@public_bp.route("/")
def index():
    articles = Article.query.filter_by(status="publicado").order_by(Article.published_at.desc()).limit(3).all()
    return render_template("index.html", articles=articles)


@public_bp.route("/sobre")
def sobre():
    return render_template("sobre.html")


@public_bp.route("/especialidades")
def especialidades():
    return render_template("especialidades.html", topics=TOPICS)


@public_bp.route("/quando-procurar")
def quando_procurar():
    return render_topic(dict(TOPICS["quando-procurar"], seo_title=TOPIC_SEO_TITLES["quando-procurar"]), "quando-procurar", canonical_path="/quando-procurar")


@public_bp.route("/nefrologia/<slug>")
def tema(slug):
    topic = TOPICS.get(slug)
    if not topic:
        abort(404)
    return render_topic(dict(topic, seo_title=TOPIC_SEO_TITLES.get(slug)) if slug in TOPIC_SEO_TITLES else topic, slug, canonical_path=topic_canonical_path(slug))


@public_bp.route("/doenca-renal-cronica")
@public_bp.route("/hipertensao-e-rins")
@public_bp.route("/diabetes-e-rins")
@public_bp.route("/glomerulopatias")
@public_bp.route("/calculo-renal")
@public_bp.route("/medicamentos-e-rins")
@public_bp.route("/hemodialise")
@public_bp.route("/prevencao")
@public_bp.route("/nefrologista-ou-urologista")
@public_bp.route("/consulta-nefrologica")
def tema_alias():
    slug = request.path.strip("/")
    topic = dict(TOPICS[slug], seo_title=TOPIC_SEO_TITLES[slug])
    # Mesma página existe em /nefrologia/<slug>; o canonical aponta para a versão principal
    return render_topic(topic, slug, canonical_path=topic_canonical_path(slug))


@public_bp.route("/exames")
def exames():
    return render_template("exames.html", exams=EXAMS)


@public_bp.route("/exames/<slug>")
def exame_detalhe(slug):
    data = EXAMS.get(slug)
    if not data:
        abort(404)
    sections = [section(item["title"], item["body"]) for item in data["sections"]]
    related = "".join(
        '<li><a href="{}">{}</a></li>'.format(url_for("public.exame_detalhe", slug=r), EXAMS[r]["title"])
        for r in data.get("related", []) if r in EXAMS
    )
    if related:
        sections.append(section("Exames relacionados", "<ul>" + related + "</ul>"))
    sections.append(section("Converse com um especialista", "<p>Se o exame estiver alterado, leve o resultado e exames anteriores para que a evolução possa ser compreendida com segurança. Não suspenda medicamentos nem mude a rotina por conta própria com base em um único resultado.</p>"))
    topic = {
        "eyebrow": "Exames dos rins", "title": data["title"], "lead": data["lead"],
        "highlight": "O resultado de um exame precisa ser interpretado junto com a história clínica e os demais achados.",
        "icon": "bi-file-earmark-medical", "sections": sections,
        "seo_title": data["title"] + " | Palmas – TO",
        "seo_description": seo_description(data["lead"]),
    }
    return render_topic(topic, slug, back_url="exames", back_label="Exames dos rins", canonical_path="/exames/" + slug)


@public_bp.route("/perguntas-frequentes")
def faq():
    return render_template("faq.html", faqs=FAQS)


@public_bp.route("/artigos")
def artigos():
    articles = Article.query.filter_by(status="publicado").order_by(Article.published_at.desc()).all()
    return render_template("artigos.html", articles=articles)


@public_bp.route("/artigos/<slug>")
def artigo_detalhes(slug):
    article = Article.query.filter_by(slug=slug, status="publicado").first_or_404()
    view = ArticleView(article_id=article.id)
    db.session.add(view)
    db.session.commit()
    return render_template("artigo_detalhes.html", article=article)


@public_bp.route("/contato")
def contato():
    return render_template("contato.html")


@public_bp.route("/politica-de-privacidade")
def politica_privacidade():
    return render_template("politica_privacidade.html")


def _site_url():
    return (current_app.config.get("SITE_URL") or request.url_root).rstrip("/")


@public_bp.route("/sitemap.xml")
def sitemap():
    base = _site_url()
    paths = ["/", "/sobre", "/especialidades", "/quando-procurar"]
    paths += ["/nefrologia/" + slug for slug in TOPICS if slug != "quando-procurar"]
    paths += ["/exames"] + ["/exames/" + slug for slug in EXAMS]
    paths += ["/perguntas-frequentes", "/artigos", "/contato", "/politica-de-privacidade"]
    pages = [{"loc": base + path, "lastmod": None} for path in paths]
    articles = Article.query.filter_by(status="publicado").order_by(Article.published_at.desc()).all()
    for a in articles:
        when = a.updated_at or a.published_at
        pages.append({"loc": base + url_for("public.artigo_detalhes", slug=a.slug), "lastmod": when.strftime("%Y-%m-%d") if when else None})
    response = make_response(render_template("sitemap.xml", pages=pages))
    response.headers["Content-Type"] = "application/xml; charset=utf-8"
    return response


@public_bp.route("/robots.txt")
def robots():
    response = make_response(render_template("robots.txt", site_url=_site_url()))
    response.headers["Content-Type"] = "text/plain; charset=utf-8"
    return response
