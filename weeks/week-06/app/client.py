# Реализуйте здесь клиент для GraphQL.

PROJECT_CODE = "notifications-s10"


def build_payload(query: str, variables: dict) -> dict:
    """
    Формирует словарь для отправки GraphQL запроса.

    :param query: Текст запроса (query или mutation).
    :param variables: Словарь с переменными.
    :return: Словарь с ключами "query" и "variables".
    """
    return {"query": query, "variables": variables}


def _handle_response(data: dict) -> None:
    if "errors" in data:
        print("errors:", data["errors"])
    if "data" in data:
        print("data:", data["data"])


if __name__ == "__main__":
    import os

    import requests

    from coursekit.variant import load_variant

    v = load_variant("06")
    g = v["graphql"]
    xf = v["extra_field"]["name"]
    url = os.getenv("GRAPHQL_URL", "http://127.0.0.1:8000/graphql")

    fields = f"id name {xf}"
    q_notifications = f"query {{ {g['query']} {{ {fields} }} }}"
    m_create = (
        f"mutation($input: {g['type']}Input!) "
        f"{{ {g['mutation']}(input: $input) {{ {fields} }} }}"
    )

    for label, payload in (
        (f"query {g['query']}", build_payload(q_notifications, {})),
        (
            f"mutation {g['mutation']}",
            build_payload(
                m_create,
                {"input": {"name": "from-client", xf: "email"}},
            ),
        ),
    ):
        print(f"\n--- {label} ---")
        r = requests.post(url, json=payload, timeout=10)
        print("HTTP", r.status_code)
        _handle_response(r.json())
