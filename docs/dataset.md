# Datasets produced by pytmdb

This repo harvests the public TMDB catalog through the `/discover/movie` and `/discover/tv` endpoints. It produces two JSONL datasets: one for films and one for TV series. Each row is a single title with normalized genre names, vote statistics, and a short overview.

## Dataset format

Rows are written as JSON objects, one per line.

### `tmdb_movies`

One row per film.

| Field | Type | Description |
| --- | --- | --- |
| `tmdb_id` | integer | TMDB movie identifier. |
| `title` | string / null | English title. |
| `original_title` | string / null | Original release title. |
| `original_language` | string / null | ISO language code. |
| `release_date` | string / null | ISO-8601 date (`YYYY-MM-DD`). |
| `genres` | list of strings | Genre names mapped from TMDB genre IDs. |
| `vote_average` | float / null | Average user rating. |
| `vote_count` | integer / null | Number of user ratings. |
| `popularity` | float / null | TMDB popularity score. |
| `adult` | boolean | Adult content flag. |
| `overview` | string / null | Plot summary, truncated to 500 characters. |
| `poster_path` | string / null | TMDB poster path segment. |
| `entity_type` | string | Always `film`. |

### `tmdb_tv`

One row per TV series.

| Field | Type | Description |
| --- | --- | --- |
| `tmdb_id` | integer | TMDB series identifier. |
| `name` | string / null | English series name. |
| `original_name` | string / null | Original series name. |
| `original_language` | string / null | ISO language code. |
| `first_air_date` | string / null | ISO-8601 date (`YYYY-MM-DD`). |
| `origin_country` | list of strings | ISO country codes. |
| `genres` | list of strings | Genre names mapped from TMDB genre IDs. |
| `vote_average` | float / null | Average user rating. |
| `vote_count` | integer / null | Number of user ratings. |
| `popularity` | float / null | TMDB popularity score. |
| `overview` | string / null | Series summary, truncated to 500 characters. |
| `poster_path` | string / null | TMDB poster path segment. |
| `entity_type` | string | Always `tv_series`. |

## How to generate

Install the package with the optional HuggingFace publisher support:

```bash
pip install "pytmdb[hf]"
```

Set a TMDB API key and run the harvester:

```bash
TMDB_API_KEY=xxx pytmdb-harvest tmdb_movies --output ~/.cache/metadatarr/scrapers/
TMDB_API_KEY=xxx pytmdb-harvest tmdb_tv --output ~/.cache/metadatarr/scrapers/
```

The harvest is resumable. Stopping and rerunning the command continues from the last checkpoint kept in the output directory.

You can also run a source directly in Python:

```python
from pytmdb.harvest.tmdb_movies import TMDBMoviesSource

src = TMDBMoviesSource()
rows, cursor = src.fetch({"year": 1888, "page": 1})
```

## Worth publishing on Hugging Face?

Yes. The TMDB catalog is a large, language-diverse source of film and TV metadata. A published snapshot is useful for retrieval, recommendation, and entity-linking benchmarks. You must follow TMDB attribution requirements and include the TMDB logo and a link to themoviedb.org in the dataset card.

## ML tasks served

- Metadata enrichment for titles that lack structured tags.
- Genre and language classification.
- Cross-catalog entity linking through `tmdb_id`.
- Retrieval and RAG corpora for entertainment queries.
- Popularity and rating regression tasks.
