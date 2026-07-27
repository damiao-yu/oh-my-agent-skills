---
name: anysearch
description: Search the live web and specialized sources through the AnySearch API. Use for current facts, technical documentation, academic papers, finance, legal, security, travel, social-media, or other domain-specific searches that need source URLs and fresh content.
---

# AnySearch

Use the bundled dependency-free Python CLI to retrieve current, source-backed information. Prefer specific queries and preserve source URLs in the final response.

## Setup

AnySearch permits anonymous requests with a lower quota. For authenticated use, set `ANYSEARCH_API_KEY` in the environment. Never print, persist, or expose the key.

```bash
export ANYSEARCH_API_KEY="..."
```

## Search

Run:

```bash
python3 {baseDir}/scripts/anysearch.py search "Go 1.26 release notes" --max-results 5
```

Use `--tag` and `--params` when the domain is known:

```bash
python3 {baseDir}/scripts/anysearch.py search "Go 1.26 release notes" \
  --tag code.doc --params '{"library":"golang"}' --max-results 5
```

Use `--zone cn --language zh-CN` for China-focused Chinese results. Run `python3 {baseDir}/scripts/anysearch.py search --help` for all options.

## Research workflow

1. Decompose broad questions into focused searches.
2. Use a capability tag only when its required parameters are known; otherwise let AnySearch route automatically.
3. Inspect titles, snippets, content, and URLs. Do not treat snippets as complete evidence.
4. Cross-check consequential claims with multiple independent sources.
5. Cite the original result URLs, not the API endpoint.
6. Report gaps or conflicting evidence explicitly.

Read [references/api.md](references/api.md) when selecting request parameters or diagnosing API errors.

