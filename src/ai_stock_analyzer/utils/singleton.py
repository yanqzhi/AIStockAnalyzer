"""Reusable singleton implementation."""

from typing import ClassVar


class Singleton(type):
    """Metaclass that creates one shared instance per class."""

    _instances: ClassVar[dict[type[object], object]] = {}

    def __call__(cls, *args: object, **kwargs: object) -> object:
        """Return a shared instance for the class.

        Args:
            *args: Positional arguments for first instance creation.
            **kwargs: Keyword arguments for first instance creation.

        Returns:
            The shared class instance.
        """
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)

        return cls._instances[cls]
