from typing import Protocol


class Service(Protocol):
    """Protocol for domain services.

    Domain service logic should remain independent of transport concerns.
    """
