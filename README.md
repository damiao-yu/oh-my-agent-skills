# oh-my-agent-skills

A personal collection of portable AI-agent skills. Each skill is a top-level directory containing a `SKILL.md`, so it can be discovered by pi, Codex, Claude Code, and other Agent Skills-compatible tools.

## Skills

| Skill | Description | Source | License |
| --- | --- | --- | --- |
| [anysearch](anysearch/) | Search the web, vertical domains, batches, and URL content with AnySearch | [anysearch-ai/anysearch-skill@caed9ea](https://github.com/anysearch-ai/anysearch-skill/tree/caed9eac2eb6e869b89faa2f3e92d8956b013b56) | [Apache-2.0](anysearch/LICENSE) |
| [grill-me](grill-me/) | Explicit user entry point for starting a grilling session | [mattpocock/skills](https://github.com/mattpocock/skills/blob/main/skills/productivity/grill-me/SKILL.md) | [MIT](grill-me/LICENSE) |
| [grilling](grilling/) | Reusable interview workflow for stress-testing a plan or decision | [mattpocock/skills](https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md) | [MIT](grilling/LICENSE) |
| [pdf2md](pdf2md/) | Convert PDFs to Markdown and images with a local MinerU pipeline | Local | [MIT](LICENSE) |
| [tavily-search](tavily-search/) | Search the web for current, LLM-optimized results | [tavily-ai/skills@ea5e820](https://github.com/tavily-ai/skills/tree/ea5e8201b0d3ed9c10b70b71187589bd761fe2d2/skills/tavily-search) | [MIT](tavily-search/LICENSE) |

Vendor skills are pinned snapshots of the linked upstream commits. Codex compatibility changes are limited to frontmatter, generated `agents/openai.yaml` metadata, and removal of Tavily Search links to omitted sibling skills. Upstream CI, security-policy, and test-plan maintenance files are omitted.

## Installation

Clone this repository into a supported skills directory, or symlink individual skill folders when the agent only scans one directory level.

```bash
# pi
git clone https://github.com/damiao-yu/oh-my-agent-skills.git ~/.pi/agent/skills/oh-my-agent-skills

# Codex
git clone https://github.com/damiao-yu/oh-my-agent-skills.git ~/.codex/skills/oh-my-agent-skills
```

See each skill's `SKILL.md` for its runtime requirements, credentials, setup, and usage.
