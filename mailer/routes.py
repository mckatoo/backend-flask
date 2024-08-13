from flask import Blueprint, jsonify, request
from configurations.mail_config import send_mail
from middlewares.verify_token import verify_token_middleware
from database.models.messages import Messages

mailer_routes = Blueprint("mailer", __name__)


def valid_email_error(error: str):
    mail_args = ["from", "to", "message"]
    return any(word in error for word in mail_args)


@mailer_routes.route("", methods=["POST"])
@verify_token_middleware
def send_email():
    try:
        sender: str = request.json["from"]
        recipients: str = request.json["to"]
        message: str = request.json["message"]
        subject: str = "Email send from ikatoo."

        message_config = dict(
            sender=sender,
            recipients=recipients,
            message=message,
            subject=subject,
        )

        send_mail(*message_config)
        message = Messages.create(**message_config)

        return jsonify({"id": message.id}), 201
    except Exception as e:
        if valid_email_error(str(e)):
            return jsonify({"error": "Bad Request"}), 400
        raise e
