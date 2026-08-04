"""Row-schema equivalence tests for the 2 TMDB scrapers.

Relocated verbatim (assertions untouched) from metadatarr's
test_scrapers_batch1.py, keeping only the tests for scrapers that live in
this package, re-pointed at pytmdb.harvest.*. These lock the exact flat-row
shape each scraper emits (the contract the LeData datasets depend on)
against a realistic upstream sample, so a future engine change can't
silently alter the output schema.
"""
from __future__ import annotations

from harvestkit.engine import all_sources

from pytmdb.harvest.tmdb_movies import TMDBMoviesSource
from pytmdb.harvest.tmdb_tv import TMDBTVSource


def test_tmdb_movies_map_row_schema():
    src = TMDBMoviesSource()
    m = {
        "id": 603,
        "title": "The Matrix",
        "original_title": "The Matrix",
        "original_language": "en",
        "release_date": "1999-03-31",
        "genre_ids": [28, 878],
        "vote_average": 8.2,
        "vote_count": 24000,
        "popularity": 88.1,
        "adult": False,
        "overview": "x" * 600,
        "poster_path": "/poster.jpg",
    }
    row = src.map_row(m)
    assert row["tmdb_id"] == 603
    assert row["genres"] == ["Action", "Science Fiction"]
    assert len(row["overview"]) == 500
    assert row["entity_type"] == "film"
    assert set(row) == {
        "tmdb_id", "title", "original_title", "original_language",
        "release_date", "genres", "vote_average", "vote_count", "popularity",
        "adult", "overview", "poster_path", "entity_type",
    }


def test_tmdb_movies_map_row_drops_records_without_id():
    assert TMDBMoviesSource().map_row({"id": None, "title": "x"}) is None


def test_tmdb_movies_fetch_advances_page_then_year():
    src = TMDBMoviesSource()
    calls = []

    def fake_get_json(url, params):
        calls.append(dict(params))
        year = params["primary_release_year"]
        page = params["page"]
        if year == 1888 and page == 1:
            return {"total_pages": 2, "results": [{"id": 1, "title": "a"}]}
        if year == 1888 and page == 2:
            return {"total_pages": 2, "results": [{"id": 2, "title": "b"}]}
        return {"total_pages": 1, "results": []}

    src.get_json = fake_get_json
    rows, cursor = src.fetch({"year": 1888, "page": 1})
    assert len(rows) == 1
    assert cursor == {"year": 1888, "page": 2}

    rows, cursor = src.fetch(cursor)
    assert len(rows) == 1
    assert cursor == {"year": 1889, "page": 1}


def test_tmdb_tv_map_row_schema():
    src = TMDBTVSource()
    s = {
        "id": 1399,
        "name": "Game of Thrones",
        "original_name": "Game of Thrones",
        "original_language": "en",
        "first_air_date": "2011-04-17",
        "origin_country": ["US"],
        "genre_ids": [10765],
        "vote_average": 8.4,
        "vote_count": 21000,
        "popularity": 400.1,
        "overview": "y" * 600,
        "poster_path": "/poster2.jpg",
    }
    row = src.map_row(s)
    assert row["tmdb_id"] == 1399
    assert row["genres"] == ["Sci-Fi & Fantasy"]
    assert len(row["overview"]) == 500
    assert row["entity_type"] == "tv_series"
    assert set(row) == {
        "tmdb_id", "name", "original_name", "original_language",
        "first_air_date", "origin_country", "genres", "vote_average",
        "vote_count", "popularity", "overview", "poster_path", "entity_type",
    }


def test_pytmdb_scrapers_are_registered():
    reg = all_sources()
    assert reg.get("tmdb_movies") is TMDBMoviesSource
    assert reg.get("tmdb_tv") is TMDBTVSource
