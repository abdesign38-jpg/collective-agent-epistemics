import math

EPS = 1e-9

def clamp(p: float) -> float:
    return min(max(p, EPS), 1.0 - EPS)

def logit(p: float) -> float:
    p = clamp(p)
    return math.log(p / (1.0 - p))

def logistic(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))

def signed_weight(supports_state: str, reliability: float) -> float:
    w = logit(reliability)
    return w if supports_state == "A" else -w

def confidence_for_a(weights: list[float]) -> float:
    return logistic(sum(weights))

def brier(p_a: float, truth: str) -> float:
    y = 1.0 if truth == "A" else 0.0
    return (p_a - y) ** 2
