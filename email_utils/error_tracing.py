from traceback import format_exc, extract_tb
from typing import Tuple


def extract_relevant_traceback(tb) -> str:
    if tb is None:
        return "No traceback available."
    relevant_tb = []
    stack_summary = extract_tb(tb)
    for frame in stack_summary:
        if "site-packages" not in frame.filename:  # Filtra dependências externas
            line = frame.line or ""  # Pode ser None
            relevant_tb.append(
                f'File "{frame.filename}", line {frame.lineno}, in {frame.name}\n  {line}'
            )
    return "\n".join(relevant_tb) if relevant_tb else "No relevant frames found."


def get_error_msg(tb) -> Tuple[str, str | None]:
    full_tb = format_exc()
    clean_tb = extract_relevant_traceback(tb)
    if (
        "requests.exceptions.HTTPError: 401 Client Error: Unauthorized for url"
        in full_tb
    ):
        return clean_tb, None

    return clean_tb, full_tb
