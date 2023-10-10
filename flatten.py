"""Helper module for a simple speckle object tree flattening."""

from collections.abc import Iterable

from specklepy.objects import Base


def flatten_base(base: Base) -> Iterable[Base]:
    """Take a base and flatten it to an iterable of bases."""
    if hasattr(base, "elements"):
        for element in base["elements"]:
            yield from flatten_base(element)
    yield base
