"""Configurações da aplicação."""
import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-change-in-production"
    database_url = os.environ.get("DATABASE_URL")
    if database_url and database_url.startswith("sqlite:///") and not database_url.startswith("sqlite:////"):
        database_url = "sqlite:///" + os.path.join(basedir, database_url[10:])
    SQLALCHEMY_DATABASE_URI = database_url or \
        "sqlite:///" + os.path.join(basedir, "instance", "database.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Uploads
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2MB
    UPLOAD_FOLDER = os.path.join(basedir, "static", "uploads")
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
    
    # Contato e informações institucionais
    WHATSAPP_NUMBER = os.environ.get("WHATSAPP_NUMBER") or "5563984668607"
    APPOINTMENT_URL = os.environ.get("APPOINTMENT_URL") or "https://www.doctoralia.com.br/balduino-andrade/nefrologista/palmas2"
    # URL pública do site (sem barra final), usada em canonical, sitemap e JSON-LD
    SITE_URL = (os.environ.get("SITE_URL") or "").rstrip("/")
    CLINIC_NAME = os.environ.get("CLINIC_NAME") or "DaVita Tratamento Renal"
    CLINIC_SUBTITLE = os.environ.get("CLINIC_SUBTITLE") or "Consultório e tratamento renal em Palmas"
    CLINIC_ADDRESS = os.environ.get("CLINIC_ADDRESS") or "Av. Teotônio Segurado, Quadra 201 Sul, Cj 1 Lt 5"
    CLINIC_CITY = os.environ.get("CLINIC_CITY") or "DaVita Tratamento Renal · Palmas, Tocantins"
    CLINIC_HOURS = os.environ.get("CLINIC_HOURS") or "Atendimento sob agendamento"
    CLINIC_PHONE = os.environ.get("CLINIC_PHONE") or "(63) 3216-2659"
    CLINIC_EMAIL = os.environ.get("CLINIC_EMAIL") or ""
    CLINIC_INSTAGRAM = os.environ.get("CLINIC_INSTAGRAM") or "https://www.instagram.com/balduino.nefrologista/"
    CLINIC_MAP_URL = os.environ.get("CLINIC_MAP_URL") or "https://maps.app.goo.gl/gnWA3uu4U8aExbdz8"
    DOCTOR_CRM = os.environ.get("DOCTOR_CRM") or ""
    DOCTOR_RQE = os.environ.get("DOCTOR_RQE") or ""
    DOCTOR_TRAINING = os.environ.get("DOCTOR_TRAINING") or "Formação e registros profissionais em atualização"
