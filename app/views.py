
from flask import Blueprint, render_template, request, redirect, url_for, send_file
from flask_login import login_required
import os

from app.extensions import db
from app.models import Post, Attachment, ShowcaseState
from app.storage import save_file, delete_file
from app.utils import get_free_space_gb

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
@login_required
def dashboard():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    free_space_gb = get_free_space_gb(".")
    return render_template("dashboard.html", posts=posts, free_space_gb=free_space_gb)

@main_bp.route("/posts/create", methods=["POST"])
@login_required
def create_post():
    body_text = request.form.get("body_text", "").strip()
    file = request.files.get("file")

    post = Post(
        body_text=body_text if body_text else None,
        direction="outgoing",
        kind="post",
    )

    db.session.add(post)
    db.session.flush()  # чтобы получить post.id

    if file and file.filename:
        file_data = save_file(file)

        attachment = Attachment(
            post_id=post.id,
            original_name=file_data["original_name"],
            stored_name=file_data["stored_name"],
            relative_path=file_data["relative_path"],
            size_bytes=file_data["size_bytes"],
            mime_type=file_data["mime_type"],
        )

        db.session.add(attachment)

    db.session.commit()

    return redirect(url_for("main.dashboard"))

@main_bp.route("/posts/<int:post_id>/publish", methods=["POST"])
@login_required
def publish_post(post_id):
    post = Post.query.get_or_404(post_id)

    state = ShowcaseState.query.first()

    if not state:
        state = ShowcaseState(id=1)
        db.session.add(state)

    state.mode = "post"
    state.active_post_id = post.id

    db.session.commit()

    return redirect(url_for("main.dashboard"))




@main_bp.route("/showcase/clear", methods=["POST"])
@login_required
def clear_showcase():
    state = ShowcaseState.query.first()

    if not state:
        state = ShowcaseState(id=1)
        db.session.add(state)

    state.mode = "empty"
    state.active_post_id = None

    db.session.commit()

    return redirect(url_for("main.dashboard"))


@main_bp.route("/files/<int:attachment_id>/download")
@login_required
def download_file(attachment_id):
    attachment = Attachment.query.get_or_404(attachment_id)

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    absolute_path = os.path.join(base_dir, attachment.relative_path)

    if not os.path.exists(absolute_path):
        return {"error": "file not found"}, 404

    return send_file(
        absolute_path,
        as_attachment=True,
        download_name=attachment.original_name
    )

    return send_file(path, as_attachment=True, download_name=attachment.original_name)

@main_bp.route("/posts/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    state = ShowcaseState.query.first()
    if state and state.active_post_id == post.id:
        state.mode = "empty"
        state.active_post_id = None

    for attachment in post.attachments:
        delete_file(attachment.relative_path)

    db.session.delete(post)
    db.session.commit()

    return redirect(url_for("main.dashboard"))

@main_bp.route("/showcase/request/start", methods=["POST"])
@login_required
def start_request_mode():
    state = ShowcaseState.query.first()

    if not state:
        state = ShowcaseState(id=1)
        db.session.add(state)

    state.mode = "request"
    state.active_post_id = None

    db.session.commit()

    return redirect(url_for("main.dashboard"))