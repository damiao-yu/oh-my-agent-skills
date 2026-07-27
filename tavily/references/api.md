# Tavily API notes

Official documentation:

- Search: https://docs.tavily.com/documentation/api-reference/endpoint/search
- Extract: https://docs.tavily.com/documentation/api-reference/endpoint/extract

## Search

- Endpoint: `POST https://api.tavily.com/search`
- Authentication: `Authorization: Bearer $TAVILY_API_KEY`
- `topic`: `general` or `news`
- `search_depth`: `basic` or `advanced`; advanced retrieval can consume more credits.
- `time_range`: `day`, `week`, `month`, or `year`
- Use `include_domains` and `exclude_domains` to control source scope.
- Use `include_answer` for Tavily synthesis and `include_raw_content` only when full page content is required.

## Extract

- Endpoint: `POST https://api.tavily.com/extract`
- Accepts one URL or a list of up to 20 URLs.
- `extract_depth`: `basic` or `advanced`
- `format`: `markdown` or `text`
- Use `query` to return chunks relevant to a specific question.

On errors, preserve the HTTP status and response body. Retry rate limits and transient server failures with backoff; do not blindly retry invalid requests or authentication failures.

