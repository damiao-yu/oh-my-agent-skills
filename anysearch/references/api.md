# AnySearch API notes

Official documentation: https://www.anysearch.com/docs

- Endpoint: `POST https://api.anysearch.com/v1/search`
- Authentication: optional `Authorization: Bearer $ANYSEARCH_API_KEY`
- Required field: `query`
- Common optional fields: `max_results` (1–20), `tag`, `zone` (`cn` or `intl`), `language`, `params`, and `format`
- Successful responses contain `data.results`; each result may include `title`, `url`, `snippet`, and `content`.
- Anonymous access is rate-limited. An invalid supplied key fails rather than falling back to anonymous access.

Use an exponential backoff for `429` and transient `5xx` responses. Do not retry malformed requests, authentication failures, or exhausted quotas without changing the request or credentials. Preserve `request_id` when reporting errors.

Capability tags can require fields inside `params`. Consult the live documentation before using an unfamiliar tag because the tag catalog can change.

