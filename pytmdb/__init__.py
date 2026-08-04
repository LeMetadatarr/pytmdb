"""pytmdb — TMDB movie/TV catalog bulk harvesters, grouped on harvestkit.

Importing this package imports :mod:`pytmdb.harvest`, which in turn
imports every scraper module so it registers itself with
:mod:`harvestkit.engine` (``@register``).
"""
from pytmdb.version import __version__

import pytmdb.harvest  # noqa: F401  (import for @register side effects)

from pytmdb.client import TMDBClient
from pytmdb.models import TMDBMovie

__all__ = ["__version__", "TMDBClient", "TMDBMovie"]
