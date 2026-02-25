from flask import Blueprint, render_template, request
from app.utils.image_handler import process_image
from app.utils.celebrity_detector import CelebrityDetector
from app.utils.qa_engine import QAEngine
import base64
import logging

logger = logging.getLogger(__name__)

main = Blueprint("main", __name__)

celebrity_detector = CelebrityDetector()
qa_engine = QAEngine()


@main.route("/", methods=["GET", "POST"])
def index():
    player_info = ""
    result_img_data = ""
    answer = ""
    error = ""

    if request.method == "POST":

        # ── Image Upload ──────────────────────────────────────────────
        if "image" in request.files:
            image_file = request.files["image"]

            if image_file:
                try:
                    img_bytes, face_box = process_image(image_file)

                    if face_box is None:
                        error = "No face detected in the image. Please try a clearer photo."
                    else:
                        result, name = celebrity_detector.identify(img_bytes)

                        if result is None:
                            error = "Celebrity detection failed. Please check your API key or try again."
                        else:
                            player_info = result
                            result_img_data = base64.b64encode(img_bytes).decode()

                except Exception as e:
                    logger.error(f"Image processing error: {e}")
                    error = "Failed to process the image. Please try a different photo."

        # ── Q&A ───────────────────────────────────────────────────────
        elif "question" in request.form:
            try:
                user_question = request.form.get("question", "").strip()
                player_name = request.form.get("player_name", "")
                player_info = request.form.get("player_info", "")
                result_img_data = request.form.get("result_img_data", "")

                if user_question and player_name:
                    answer = qa_engine.ask_about_celebrity(player_name, user_question)
                else:
                    error = "Please provide a valid question."

            except Exception as e:
                logger.error(f"Q&A processing error: {e}")
                error = "Something went wrong while processing your question. Please try again."

    return render_template(
        "index.html",
        player_info=player_info,
        result_img_data=result_img_data,
        answer=answer,
        error=error
    )
