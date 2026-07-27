# oh-my-agent-skills

A personal collection of portable AI-agent skills. Each skill is a top-level directory containing a `SKILL.md`, so it can be discovered by pi, Codex, Claude Code, and other Agent Skills-compatible tools.

Repository: [damiao-yu/oh-my-agent-skills](https://github.com/damiao-yu/oh-my-agent-skills)

## Skills

| Skill | Description |
| --- | --- |
| [anysearch](anysearch/) | Live web and specialized-source search through AnySearch |
| [tavily](tavily/) | Live web search and page extraction through Tavily |

## Installation

Clone this repository into a supported skills directory, or symlink individual skill folders when the agent only scans one directory level.

```bash
# pi
git clone https://github.com/damiao-yu/oh-my-agent-skills.git ~/.pi/agent/skills/oh-my-agent-skills

# Codex
git clone https://github.com/damiao-yu/oh-my-agent-skills.git ~/.codex/skills/oh-my-agent-skills
```

Provider credentials are read from environment variables. See each skill's `SKILL.md` for setup and usage.
