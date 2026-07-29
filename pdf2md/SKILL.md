---
name: pdf2md
description: Convert PDF files to clean Markdown with the local MinerU pipeline. Use when the user wants PDF-to-Markdown conversion, PDF text/table/formula/image extraction, document parsing, pdf2md, or MinerU.
license: MIT
compatibility: Requires Bash and a local MinerU 3.x installation with pipeline models. Defaults target $HOME/tools/.venv/bin/mineru and $HOME/mineru.json.
---

# PDF2MD — PDF to Markdown via MinerU

Convert one PDF to Markdown with the local MinerU pipeline backend. The result contains the generated Markdown and its referenced images; MinerU's JSON and diagnostic PDF intermediates are discarded.

## Local defaults

| Item | Default |
| --- | --- |
| MinerU executable | `$HOME/tools/.venv/bin/mineru` |
| MinerU config | `$HOME/mineru.json` |
| Configured pipeline models on this machine | `$HOME/models/PDF-Extract-Kit-1.0` |

Override non-default installations with `PDF2MD_MINERU_BIN` and `MINERU_TOOLS_CONFIG_JSON`. Do not install packages or download models unless the user explicitly approves it.

## Workflow

1. Resolve the input PDF to an absolute path and confirm that it exists.
2. Ask for the target directory if the destination matters. If none is given, use `./<pdf-basename>/` under the current working directory.
3. Resolve `scripts/pdf2md.sh` relative to this `SKILL.md`, then run:

```bash
bash "<skill-dir>/scripts/pdf2md.sh" "<pdf-path>" "<target-dir>"
```

The helper script invokes the venv's MinerU executable directly, uses `-b pipeline`, creates a collision-safe temporary directory, copies only Markdown and images, and removes temporary files on exit. It also unsets proxy variables for MinerU's temporary localhost API; this avoids routing local requests through a SOCKS proxy.

4. Verify that the reported Markdown file exists. If it references `images/...`, confirm the target's `images/` directory exists.
5. Report the final Markdown path and image directory to the user.

## Partial conversion and OCR options

Pass supported MinerU options after the target directory:

```bash
# Pages 0 through 4
bash "<skill-dir>/scripts/pdf2md.sh" "<pdf-path>" "<target-dir>" -s 0 -e 4
```

| Flag | Purpose |
| --- | --- |
| `-m auto` | Auto-detect text extraction versus OCR; this is the default |
| `-l ch` | OCR language; `ch` is the installed default and also handles Latin script. Use another language only if its model is installed |
| `-s N` / `-e N` | Start/end page, zero-indexed |

Do not override `-p`, `-o`, or `-b`; the helper owns the input, temporary output, and local pipeline backend.

## Failure handling

- If the executable or config is missing, explain which environment variable can override its path.
- If MinerU fails, preserve its error in the response; do not claim conversion succeeded.
- If no Markdown file appears, report the malformed output rather than copying MinerU intermediates.
- Markdown may contain HTML tables and LaTeX formulas, which render differently across Markdown viewers.
