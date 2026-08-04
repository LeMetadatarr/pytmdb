"""Pydantic models returned by :class:`pytmdb.client.TMDBClient`.

Mirrors the fields metadatarr's TMDB resolver provider read off
``/search/movie`` results — kept intentionally small (this is a search-result
shape, not the full ``/movie/{id}`` detail response).
"""
from typing import Optional
from pydantic import BaseModel, ConfigDict


class TMDBMovie(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: int
    title: Optional[str] = None
    original_title: Optional[str] = None
    overview: Optional[str] = None
    release_date: Optional[str] = None
    popularity: Optional[float] = None
    vote_average: Optional[float] = None
    vote_count: Optional[int] = None
    poster_path: Optional[str] = None
    backdrop_path: Optional[str] = None
    original_language: Optional[str] = None
    adult: Optional[bool] = None

    @property
    def year(self) -> Optional[int]:
        if self.release_date and len(self.release_date) >= 4:
            try:
                return int(self.release_date[:4])
            except ValueError:
                return None
        return None
