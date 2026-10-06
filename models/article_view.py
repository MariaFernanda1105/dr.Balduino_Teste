"""Modelo de visualização de artigo — sem dados pessoais."""
from datetime import datetime, timezone
from models import db


class ArticleView(db.Model):
    __tablename__ = "article_views"
    
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey("articles.id"), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    
    article = db.relationship("Article", back_populates="views")
    
    def __repr__(self):
        return f"<ArticleView article={self.article_id}>"