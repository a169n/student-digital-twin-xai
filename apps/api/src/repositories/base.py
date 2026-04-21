from typing import Protocol


class Repository(Protocol):
    """Protocol for repository components.

    Concrete implementations can target PostgreSQL or other storage backends.
    """
