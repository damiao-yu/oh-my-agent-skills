#!/usr/bin/env python3
"""Minimal AnySearch REST API CLI with no third-party dependencies."""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

API_URL = "https://api.anysearch.com/v1/search"


def request(payload, api_key):
    headers = {"Content-Type": "application/json", "User-Agent": "oh-my-agent-skills/anysearch"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=45) as response:
            body = response.read().decode("utf-8")
            try:
                return json.loads(body)
            except json.JSONDecodeError:
                return body
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"AnySearch HTTP {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"AnySearch request failed: {exc.reason}") from exc


def main():
    parser = argparse.ArgumentParser(description="Query the AnySearch API")
    subparsers = parser.add_subparsers(dest="command", required=True)
    search = subparsers.add_parser("search", help="Search live and specialized sources")
    search.add_argument("query")
    search.add_argument("--max-results", type=int, default=10, choices=range(1, 21), metavar="1..20")
    search.add_argument("--tag")
    search.add_argument("--zone", choices=("cn", "intl"))
    search.add_argument("--language")
    search.add_argument("--params", default="{}", help="JSON object with tag-specific parameters")
    search.add_argument("--format", choices=("json", "markdown"), default="json")
    search.add_argument("--api-key", help="Override ANYSEARCH_API_KEY")
    args = parser.parse_args()

    try:
        params = json.loads(args.params)
        if not isinstance(params, dict):
            raise ValueError("--params must decode to a JSON object")
        payload = {"query": args.query, "max_results": args.max_results, "format": args.format}
        for key in ("tag", "zone", "language"):
            value = getattr(args, key)
            if value:
                payload[key] = value
        if params:
            payload["params"] = params
        result = request(payload, args.api_key or os.environ.get("ANYSEARCH_API_KEY"))
        if isinstance(result, str):
            print(result)
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))
    except (ValueError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
