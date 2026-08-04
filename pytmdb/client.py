from typing import List, Optional, Tuple

from .version import __version__
from .transport import make_cf_session

# Canonical user-agent string for this client. Keeping this in one place
# means a version bump doesn't need to touch the client constructor.
_USER_AGENT = f"pytmdb/{__version__}"

from .models import TMDBMovie


class TMDBClient:
    """Client for the TMDB (The Movie Database) search API
    (https://developer.themoviedb.org/reference/search-movie).

    Requires a ``TMDB_API_KEY`` — pass one explicitly or set the
    ``TMDB_API_KEY`` environment variable. Uses the same anti-bot transport
    (:func:`pytmdb.transport.make_cf_session`) as metadatarr's resolver
    provider this was extracted from.
    """

    BASE = "https://api.themoviedb.org/3"

    def __init__(self, api_key: Optional[str] = None, user_agent: str = _USER_AGENT):
        import os

        self.api_key = api_key or os.environ.get("TMDB_API_KEY", "")
        self._session = make_cf_session()
        try:
            self._session.headers["User-Agent"] = user_agent
        except Exception:
            pass

    def is_available(self) -> bool:
        return bool(self.api_key)

    def _get(self, path: str, **params) -> Optional[dict]:
        if not self.api_key:
            return None
        params["api_key"] = self.api_key
        try:
            r = self._session.get(f"{self.BASE}{path}", params=params, timeout=20)
            r.raise_for_status()
            return r.json()
        except Exception:
            return None

    # ------------------------------------------------------------------
    # Movie search
    # ------------------------------------------------------------------

    def search_movie(self, query: str, page: int = 1) -> List[TMDBMovie]:
        """Raw ``/search/movie`` results, in TMDB's own relevance order."""
        data = self._get("/search/movie", query=query, page=page)
        if not data:
            return []
        results = data.get("results") or []
        out = []
        for r in results:
            try:
                out.append(TMDBMovie.model_validate(r))
            except Exception:
                continue
        return out

    def best_match(self, title: str, year: Optional[int] = None) -> Optional[Tuple[TMDBMovie, float]]:
        """Search *title* and return the ``(movie, confidence)`` pair TMDB
        best agrees with, using the same title/year heuristic metadatarr's
        resolver provider used:

        - exact (case-insensitive) title match + year within 1 → 0.95
        - exact title match, no/mismatched year → 0.85
        - substring match either direction → 0.60
        - otherwise → 0.35 (first result, as a low-confidence fallback)
        """
        results = self.search_movie(title)
        if not results:
            return None

        query = title.lower()
        best: Optional[TMDBMovie] = None
        best_confidence = -1.0

        for movie in results:
            candidate_title = (movie.title or "").lower()
            result_year = movie.year

            if candidate_title == query:
                if year and result_year and abs(year - result_year) <= 1:
                    confidence = 0.95
                else:
                    confidence = 0.85
            elif query in candidate_title or candidate_title in query:
                confidence = 0.60
            else:
                confidence = 0.35

            if confidence > best_confidence:
                best_confidence = confidence
                best = movie

        if best is None:
            best = results[0]
            best_confidence = 0.35

        return best, best_confidence
