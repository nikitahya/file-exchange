from flask import Blueprint, render_template, abort, current_app, request, send_file, redirect, url_for
import os

from app.extensions import db
from app.models import ShowcaseState, Post, Attachment
from app.storage import save_files


showcase_bp = Blueprint("showcase", __name__)


@showcase_bp.route("/showcase/<token>")
def showcase(token):
    state = ShowcaseState.query.first()

    if not state or token != state.token:
        abort(404)

    if state.mode == "empty":
        return render_template("showcase_empty.html")

    if state.mode == "request":
        return render_template("showcase_request.html", token=token)

    if state.mode == "post" and state.active_post_id:
        post = Post.query.get(state.active_post_id)
        if not post:
            return render_template("showcase_empty.html")
        return render_template("showcase.html", post=post, token=token)

    return render_template("showcase_empty.html")


@showcase_bp.route("/showcase/<token>/reply", methods=["POST"])
def showcase_reply(token):
    state = ShowcaseState.query.first()

    if not state or token != state.token:
        abort(404)

    if state.mode != "request":
        return {"error": "request mode is not active"}, 400

    body_text = request.form.get("body_text", "").strip()
    files = request.files.getlist("files")

    incoming_post = Post(
        body_text=body_text if body_text else None,
        direction="incoming",
        kind="response",
    )

    db.session.add(incoming_post)
    db.session.flush()

    valid_files = [file for file in files if file and file.filename]

    if valid_files:
        try:
            files_data = save_files(valid_files)
        except ValueError as e:
            return str(e), 400

        for file_data in files_data:
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

    return redirect(url_for("showcase.showcase", token=token))


@showcase_bp.route("/showcase/files/<int:attachment_id>/download/<token>")
def showcase_download_file(attachment_id, token):
    state = ShowcaseState.query.first()

    if not state or token != state.token:
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