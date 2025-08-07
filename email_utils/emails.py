from .email_utils import get_formatted_msg, send_email
from .payload_template import get_payload_template
from .error_tracing import get_error_msg
from typing import Optional
from os import environ
from dotenv import load_dotenv

load_dotenv(override=True)

IN_PROD = (
    environ.get("IN_PROD", "false").lower() == "true"
    or environ.get("IN_PRODUCTION", "false").lower() == "true"
)


def send_success_email() -> None:
    msg = get_formatted_msg("success", {})
    send_email(msg, "ZIA Backend em Execução")


def send_error_log_email(tb=None, payload: Optional[dict] = None) -> str:
    clean_tb, full_tb = get_error_msg(tb)
    if not full_tb:
        return clean_tb

    payload_msg = get_payload_template(payload) if payload else ""
    variables = {"payload": payload_msg}
    if lambda_name := environ.get("AWS_LAMBDA_FUNCTION_NAME"):
        variables["lambda_name"] = lambda_name
        title = f"Erro no Lambda: {lambda_name}"
        template = "lambda_error"

    else:
        title = "Erro no Backend"
        template = "backend_error"
        # variables |= {"clean_tb": clean_tb, "full_tb": full_tb}

    msg = get_formatted_msg(template, variables)
    if not IN_PROD:
        title = f"TEST SERVER - {title}"

    send_email(msg, title, logging=False)
    return clean_tb


def send_new_user_email(
    destination: str, nome: str, username: str, password: str
) -> None:

    variables = {"nome": nome, "username": username, "password": password}
    msg = get_formatted_msg("primeiro_login", variables)
    send_email(msg, "Credenciais para 1º Login no sistema ZIA", destination)


def send_recuperacao_email(destination: str, user: str, senha: str) -> None:
    variables = {"user": user, "senha": senha}
    msg = get_formatted_msg("recuperacao", variables)
    send_email(msg, "Envio de senha temporária", destination)


def send_novo_cliente_email(
    nome_empresa: str, email: str, nome: str, username: str
) -> None:

    variables = {
        "nome_empresa": nome_empresa,
        "email": email,
        "nome": nome,
        "username": username,
    }
    msg = get_formatted_msg("novo_cliente", variables)
    send_email(msg, "Novo cliente cadastrado")


def send_faq_email(phone_id: str, faq: str) -> None:
    variables = {"db_name": phone_id}
    msg = get_formatted_msg("faq", variables)
    send_email(msg, f"FAQ - {phone_id}", attachment_path=faq)


def send_cancelamento_email(empresa_name: str, motivo: str) -> None:
    variables = {"empresa_name": empresa_name, "motivo": motivo}
    msg = get_formatted_msg("cancelamento", variables)
    send_email(msg, f"Cancelamento - {empresa_name}")


def send_appointment_email(
    servico_agendado: str,
    nome_cliente: str,
    numero_cliente: str,
    nome_funcionario: str,
    data_hora_inicio: str,
    email: str,
) -> None:
    variables = {
        "servico_agendado": servico_agendado,
        "nome_cliente": nome_cliente,
        "numero_cliente": numero_cliente,
        "nome_funcionario": nome_funcionario,
        "data_hora_inicio": data_hora_inicio,
    }
    msg = get_formatted_msg("novo_agendamento", variables)
    send_email(msg, "Novo Agendamento", destination=email)
