from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from boto3 import client as boto3_client
from typing import Optional
from smtplib import SMTP_SSL
from os import environ, path
from loguru import logger


ses = boto3_client("ses", region_name=environ.get("AWS_REGION", "sa-east-1"))
FROM_EMAIL = environ.get("FROM_EMAIL", "")
EMAIL_PASSWORD = environ.get("EMAIL_PASSWORD", "")
TO_EMAIL_DEFAULT = environ.get("TO_EMAIL", "")
NORMAL_EMAILS = list(environ.get("NORMAL_EMAILS", [])) + [FROM_EMAIL, TO_EMAIL_DEFAULT]


def send_email(
    msg_body: MIMEText,
    assunto: str,
    destination: str = TO_EMAIL_DEFAULT,
    attachment_path: Optional[str] = None,
    logging: bool = True,
):
    try:
        return _send(
            assunto,
            destination,
            msg_body,
            attachment_path=attachment_path,
            logging=logging,
        )
    except Exception as e:
        if logging:
            logger.exception("Erro ao enviar e-mail")
        else:
            print(f"Erro ao enviar e-mail: {e}")


def _attach_file(msg: MIMEMultipart, attachment_path: str) -> None:
    if not path.isfile(attachment_path):
        raise FileNotFoundError(f"Attachment file not found: {attachment_path}")

    with open(attachment_path, "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f'attachment; filename="{path.basename(attachment_path)}"',
        )
        msg.attach(part)


def _send(
    assunto: str,
    destination: str,
    msg_body: MIMEText,
    attachment_path: Optional[str] = None,
    logging: bool = True,
):
    msg = MIMEMultipart()
    msg["Subject"] = assunto
    msg["From"] = FROM_EMAIL
    msg["To"] = destination
    msg.attach(msg_body)

    if attachment_path:
        _attach_file(msg, attachment_path)

    if destination not in NORMAL_EMAILS:
        response = _send_aws(destination, msg)
    else:
        response = _send_smtp_email(destination, msg)

    if logging:
        logger.info("Email enviado com sucesso")
    else:
        print("Email enviado com sucesso")

    return response


def _send_aws(destination: str, msg: MIMEMultipart):
    return ses.send_raw_email(
        Source=FROM_EMAIL,
        Destinations=[destination],
        RawMessage={"Data": msg.as_string()},
    )


def _send_smtp_email(destination: str, msg: MIMEMultipart):
    with SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(FROM_EMAIL, EMAIL_PASSWORD)
        server.sendmail(FROM_EMAIL, destination, msg.as_string())
    return f"Email enviado com sucesso para {destination} via SMTP"


def get_formatted_msg(template: str, variables: dict) -> MIMEText:
    template_path = f"{path.dirname(__file__)}/templates/{template}.html"
    with open(template_path, "r", encoding="utf-8") as file:
        html = file.read()

    for key, value in variables.items():
        html = html.replace(f"{{{key}}}", str(value))

    return MIMEText(html, "html")
