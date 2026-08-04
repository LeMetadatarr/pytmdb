# pytmdb

2 TMDB (The Movie Database) catalog bulk harvesters grouped onto the
[harvestkit](https://github.com/LeMetadatarr/harvestkit) resumable-harvest
engine. Extracted from [metadatarr](https://github.com/TigreGotico/metadatarr)'s
scraper collection into its own standalone package.

NOTE: a real-time query client for this source will be extracted from metadatarr's
resolver into this package as a follow-up (the "full extraction" step); this package
currently ships the bulk harvester only.

## Sources

| Scraper | Registry name | Source |
| --- | --- | --- |
| `tmdb_movies` | `tmdb_movies` | TMDB `/discover/movie`, paginated year-by-year (requires `TMDB_API_KEY`) |
| `tmdb_tv` | `tmdb_tv` | TMDB `/discover/tv`, paginated year-by-year (requires `TMDB_API_KEY`) |

## Install

```bash
pip install pytmdb
# or, for the HuggingFace publisher (via harvestkit):
pip install "pytmdb[hf]"
# or, for Cloudflare-guarded sources:
pip install "pytmdb[stealth]"
```

## Usage

```bash
# list every registered scraper
pytmdb-harvest --list

# harvest one source (resumable — safe to Ctrl-C and rerun)
TMDB_API_KEY=xxx pytmdb-harvest tmdb_movies --output ~/.cache/metadatarr/scrapers/
```

Every scraper is a `harvestkit.engine.Source` subclass: checkpoint/dedup/
pagination/throttle are handled by the shared engine, each module only
answers `initial_cursor()` and `fetch(cursor)`. See
[harvestkit](https://github.com/LeMetadatarr/harvestkit) for the full engine
API.

## License

Apache-2.0
