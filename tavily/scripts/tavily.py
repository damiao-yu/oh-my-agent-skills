#!/usr/bin/env python3
"""Minimal Tavily Search and Extract CLI with no third-party dependencies."""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

API_BASE = "https://api.tavily.com"


def request(endpoint, payload, api_key):
    if not api_key:
        raise RuntimeError("TAVILY_API_KEY is not set")
    req = urllib.request.Request(
        f"{API_BASE}/{endpoint}",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "oh-my-agent-skills/tavily",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Tavily HTTP {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Tavily request failed: {exc.reason}") from exc


def add_key_argument(parser):
    parser.add_argument("--api-key", help="Override TAVILY_API_KEY")


def build_parser():
    parser = argparse.ArgumentParser(description="Search or extract content with Tavily")
    commands = parser.add_subparsers(dest="command", required=True)

    search = commands.add_parser("search", help="Search the web")
    search.add_argument("query")
    search.add_argument("--depth", choices=("basic", "advanced"), default="basic")
    search.add_argument("--topic", choices=("general", "news"), default="general")
    search.add_argument("--max-results", type=int, default=5, choices=range(1, 21), metavar="1..20")
    search.add_argument("--time-range", choices=("day", "week", "month", "year"))
    search.add_argument("--start-date", help="Date in YYYY-MM-DD format")
    search.add_argument("--end-date", help="Date in YYYY-MM-DD format")
    search.add_argument("--country")
    search.add_argument("--include-domain", action="append", default=[])
    search.add_argument("--exclude-domain", action="append", default=[])
    search.add_argument("--include-answer", action="store_true")
    search.add_argument("--include-raw-content", action="store_true")
    search.add_argument("--safe-search", action="store_true")
    add_key_argument(search)

    extract = commands.add_parser("extract", help="Extract clean content from URLs")
    extract.add_argument("urls", nargs="+")
    extract.add_argument("--query")
    extract.add_argument("--depth", choices=("basic", "advanced"), default="basic")
    extract.add_argument("--format", choices=("markdown", "text"), default="markdown")
    add_key_argument(extract)
    return parser


def main():
    args = build_parser().parse_args()
    api_key = args.api_key or os.environ.get("TAVILY_API_KEY")
    if args.command == "search":
        payload = {
            "query": args.query,
            "search_depth": args.depth,
            "topic": args.topic,
            "max_results": args.max_results,
            "include_answer": args.include_answer,
            "include_raw_content": args.include_raw_content,
            "include_domains": args.include_domain,
            "exclude_domains": args.exclude_domain,
            "safe_search": args.safe_search,
        }
        for key in ("time_range", "start_date", "end_date", "country"):
            value = getattr(args, key)
            if value:
                payload[key] = value
        endpoint = "search"
    else:
        if len(args.urls) > 20:
            print("error: Tavily Extract accepts at most 20 URLs", file=sys.stderr)
            return 2
        payload = {"urls": args.urls, "extract_depth": args.depth, "format": args.format}
        if args.query:
            payload["query"] = args.query
        endpoint = "extract"

    try:
        result = request(endpoint, payload, api_key)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
