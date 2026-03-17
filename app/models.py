
from datetime import datetime

from app.extensions import db

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    body_text = db.Column(db.Text, nullable=True)

    direction = db.Column(db.String(20), nullable=False, default="outgoing")
    kind = db.Column(db.String(20), nullable=False, default="post")

    is_deleted = db.Column(db.Boolean, nullable=False, default=False)

    parent_post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=True)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    attachments = db.relationship(
        "Attachment",
        backref="post",
        lazy=True,
        cascade="all, delete-orphan"
    )

class Attachment(db.Model):
    __tablename__ = "attachments"

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)

    original_name = db.Column(db.String(255), nullable=False)
    stored_name = db.Column(db.String(255), nullable=False)
    relative_path = db.Column(db.String(500), nullable=False)

    size_bytes = db.Column(db.Integer, nullable=False, default=0)
    mime_type = db.Column(db.String(255), nullable=True)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class ShowcaseState(db.Model):
    __tablename__ = "showcase_state"

    id = db.Column(db.Integer, primary_key=True, default=1)

    mode = db.Column(db.String(20), nullable=False, default="empty")
    active_post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=True)
    token = db.Column(db.String(255), nullable=False, unique=True)

    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)