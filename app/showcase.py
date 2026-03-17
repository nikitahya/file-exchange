from flask import Blueprint, render_template, abort, current_app, request, send_file
import os

from app.extensions import db
from app.models import ShowcaseState, Post, Attachment
from app.storage import save_file

showcase_bp = Blueprint("showcase", __name__)

@showcase_bp.route("/showcase/<token>")
def showcase(token):
    expected_token = current_app.config["SHOWCASE_TOKEN"]

    if token != expected_token:
        abort(404)

    state = ShowcaseState.query.first()


    if not state or state.mode == "empty":
        return render_template("showcase_empty.html")

    if state.mode == "request":
        return render_template("showcase_request.html", token=token)

    if state.mode == "post" and state.active_post_id:
        post = Post.query.get(state.active_post_id)
        if not post:
            return {"status": "empty"}
        return render_template("showcase.html", post=post, token=token)

    return {"status": "empty"}

@showcase_bp.route("/showcase/<token>/reply", methods=["POST"])
def showcase_reply(token):
    expected_token = current_app.config["SHOWCASE_TOKEN"]

    if token != expected_token:
        abort(404)

    state = ShowcaseState.query.first()

    if not state or state.mode != "request":
        return {"error": "request mode is not active"}, 400

    body_text = request.form.get("body_text", "").strip()
    file = request.files.get("file")

    incoming_post = Post(
        body_text=body_text if body_text else None,
        direction="incoming",
        kind="response",
    )

    db.session.add(incoming_post)
    db.session.flush()

    if file and file.filename:
        file_data = save_file(file)

        attachment = Attachment(
            post_id=incoming_post.id,
            original_name=file_data["original_name"],
            stored_name=file_data["stored_name"],
            relative_path=file_data["relative_path"],
            size_bytes=file_data["size_bytes"],
            mime_type=file_data["mime_type"],
        )

        db.session.add(attachment)

    state.mode = "empty"
    state.active_post_id = None

    db.session.commit()

    return render_template("showcase_reply_done.html")

@showcase_bp.route("/showcase/files/<int:attachment_id>/download/<token>")
def showcase_download_file(attachment_id, token):
    expected_token = current_app.config["SHOWCASE_TOKEN"]

    if token != expected_token:
        abort(404)

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