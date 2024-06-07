from dataclasses import dataclass


@dataclass
class ProblemDetails:
    type: str
    title: str
    status: int
    detail: str
    instance: str