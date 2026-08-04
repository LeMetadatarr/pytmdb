"""Network-free smoke test for the real-time TMDB query client.

The client's ``_get`` is monkeypatched to return a captured sample
``/search/movie`` response, so parsing and the confidence heuristic are
exercised without ever touching the network.
"""
from __future__ import annotations

from pytmdb import TMDBClient, TMDBMovie

_SAMPLE_SEARCH = {
    "page": 1,
    "results": [
        {
            "id": 27205,
            "title": "Inception",
            "original_title": "Inception",
            "overview": "A thief who steals corporate secrets...",
            "release_date": "2010-07-15",
            "popularity": 123.4,
            "vote_average": 8.4,
            "vote_count": 34000,
            "poster_path": "/poster.jpg",
            "original_language": "en",
            "adult": False,
        },
        {
            "id": 99999,
            "title": "Inception: Behind the Scenes",
            "release_date": "2010-08-01",
        },
    ],
    "total_results": 2,
}


def _client_with_fake_get(payload):
    client = TMDBClient(api_key="fake-key")

    def _fake_get(path, **params):
        return payload

    client._get = _fake_get
    return client


def test_search_movie_parses_results():
    client = _client_with_fake_get(_SAMPLE_SEARCH)
    results = client.search_movie("Inception")
    assert len(results) == 2
    assert isinstance(results[0], TMDBMovie)
    assert results[0].id == 27205
    assert results[0].year == 2010


def test_best_match_prefers_exact_title_and_year():
    client = _client_with_fake_get(_SAMPLE_SEARCH)
    match = client.best_match("Inception", year=2010)
    assert match is not None
    movie, confidence = match
    assert movie.id == 27205
    assert confidence == 0.95


def test_is_available_reflects_api_key():
    client = TMDBClient(api_key="")
    assert client.is_available() is False
    client2 = TMDBClient(api_key="x")
    assert client2.is_available() is True


def test_get_returns_none_without_api_key():
    client = TMDBClient(api_key="")
    assert client._get("/search/movie", query="x") is None
