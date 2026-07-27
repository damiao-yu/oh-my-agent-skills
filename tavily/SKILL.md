---
name: tavily
description: Search the live web and extract page content through the Tavily API. Use for current research, news discovery, fact checking, source collection, domain-filtered searches, or retrieving clean content from known URLs for an AI agent.
---

# Tavily

Use the bundled dependency-free Python CLI for web search and content extraction. Preserve original URLs and distinguish retrieved evidence from inference.

## Setup

Set `TAVILY_API_KEY` in the environment. Never print, persist, or expose the key.

```bash
export TAVILY_API_KEY="tvly-..."
```

## Search

Run a basic search first:

```bash
python3 {baseDir}/scripts/tavily.py search "latest database release notes" --max-results 5
```

Useful refinements:

```bash
python3 {baseDir}/scripts/tavily.py search "AI regulation" \
  --topic news --time-range week --include-answer --max-results 8

python3 {baseDir}/scripts/tavily.py search "Python asyncio documentation" \
  --include-domain docs.python.org --depth advanced
```

Keep `--depth basic` unless advanced retrieval is worth the additional credits. Use `--include-raw-content` only when result snippets are insufficient.

## Extract known pages

```bash
python3 {baseDir}/scripts/tavily.py extract https://example.com/page \
  --format markdown
```

Pass up to 20 URLs. Add `--query` when only content relevant to a question is needed.

## Research workflow

1. Decompose broad questions into focused searches.
2. Apply topic, time, country, and domain filters only when they improve precision.
3. Extract promising pages when search content is too shallow.
4. Cross-check consequential claims with multiple independent sources.
5. Cite original page URLs rather than Tavily's API endpoint.
6. State uncertainty, missing coverage, or source disagreement.

Read [references/api.md](references/api.md) for parameter guidance and error handling.

