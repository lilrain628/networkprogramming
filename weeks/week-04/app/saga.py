
# Реализуйте здесь простую машину состояний (State Machine).
# Функция должна принимать текущее состояние и событие,
# и возвращать следующее состояние.

from typing import Dict, Tuple


TRANSITIONS: Dict[Tuple[str, str], str] = {
    ("NEW", "PAY_OK"): "PAID",
    ("NEW", "PAY_FAIL"): "CANCELLED",
    ("PAID", "FULFILL_OK"): "DONE",
    ("PAID", "FULFILL_FAIL"): "CANCELLED",
}


def next_state(state: str, event: str) -> str:
    return TRANSITIONS.get((state, event), state)
