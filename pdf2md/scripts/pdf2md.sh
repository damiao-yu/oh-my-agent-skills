#!/usr/bin/env bash

set -euo pipefail

usage() {
  cat <<'EOF'
Usage: pdf2md.sh INPUT_PDF [TARGET_DIR] [MINERU_OPTIONS...]

Converts one PDF with MinerU's local pipeline backend. TARGET_DIR defaults to
./<pdf-basename>. Supported extra options include -m, -l, -s, and -e.

Environment:
  PDF2MD_MINERU_BIN       MinerU executable (default: $HOME/tools/.venv/bin/mineru)
  MINERU_TOOLS_CONFIG_JSON
                          MinerU config (default: $HOME/mineru.json)
EOF
}

if [[ $# -lt 1 ]] || [[ ${1:-} == "-h" ]] || [[ ${1:-} == "--help" ]]; then
  usage
  [[ $# -ge 1 ]] && exit 0
  exit 2
fi

input=$1
shift

if [[ ! -f "$input" ]]; then
  printf 'pdf2md: input file not found: %s\n' "$input" >&2
  exit 1
fi

input_dir=$(cd "$(dirname "$input")" && pwd -P)
input="$input_dir/$(basename "$input")"
stem=$(basename "${input%.*}")

if [[ $# -gt 0 && $1 != -* ]]; then
  target=$1
  shift
else
  target="$PWD/$stem"
fi

if [[ $target != /* ]]; then
  target="$PWD/$target"
fi

mineru_bin=${PDF2MD_MINERU_BIN:-$HOME/tools/.venv/bin/mineru}
if [[ ! -x "$mineru_bin" ]]; then
  if resolved_bin=$(command -v "$mineru_bin" 2>/dev/null); then
    mineru_bin=$resolved_bin
  else
    printf 'pdf2md: MinerU executable not found: %s\n' "$mineru_bin" >&2
    printf 'Set PDF2MD_MINERU_BIN to the MinerU executable.\n' >&2
    exit 1
  fi
fi

mineru_config=${MINERU_TOOLS_CONFIG_JSON:-$HOME/mineru.json}
if [[ ! -f "$mineru_config" ]]; then
  printf 'pdf2md: MinerU config not found: %s\n' "$mineru_config" >&2
  printf 'Set MINERU_TOOLS_CONFIG_JSON to the MinerU config file.\n' >&2
  exit 1
fi

work_dir=$(mktemp -d "${TMPDIR:-/tmp}/pdf2md.XXXXXX")
cleanup() {
  rm -rf "$work_dir"
}
trap cleanup EXIT

# MinerU 3.x starts a temporary localhost API. Proxy variables can make httpx
# require an unavailable SOCKS transport or proxy localhost, so disable them
# for this fully local pipeline invocation.
env \
  -u all_proxy -u http_proxy -u https_proxy \
  -u ALL_PROXY -u HTTP_PROXY -u HTTPS_PROXY \
  TMPDIR="$work_dir" \
  MINERU_TOOLS_CONFIG_JSON="$mineru_config" \
  "$mineru_bin" -p "$input" -o "$work_dir" -b pipeline "$@"

source_dir=$(find "$work_dir" -mindepth 2 -maxdepth 2 -type d -name auto -print -quit)
if [[ -z "$source_dir" ]]; then
  printf 'pdf2md: MinerU auto output directory was not found under %s\n' "$work_dir" >&2
  exit 1
fi

markdown_file=$(find "$source_dir" -maxdepth 1 -type f -name '*.md' -print -quit)
if [[ -z "$markdown_file" ]]; then
  printf 'pdf2md: MinerU produced no Markdown file under %s\n' "$source_dir" >&2
  exit 1
fi

mkdir -p "$target"
cp "$markdown_file" "$target/"
if [[ -d "$source_dir/images" ]]; then
  mkdir -p "$target/images"
  cp -R "$source_dir/images/." "$target/images/"
fi

printf 'Markdown: %s/%s\n' "$target" "$(basename "$markdown_file")"
if [[ -d "$source_dir/images" ]]; then
  printf 'Images:   %s/images\n' "$target"
fi
