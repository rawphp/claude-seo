# Architecture

## Overview

An agent-based SEO analysis system. Clone the repo, point any LLM at `agents/orchestrator.md`, and run audits from the project directory. All outputs are saved locally under `projects/`.

## Directory Structure

```
claude-seo/
├── agents/                   # Agent definitions
│   ├── orchestrator.md       # Project manager — intake, coordination, synthesis
│   ├── seo-technical.md      # Technical SEO specialist
│   ├── seo-content.md        # Content quality reviewer
│   ├── seo-schema.md         # Schema markup expert
│   ├── seo-sitemap.md        # Sitemap architect
│   ├── seo-performance.md    # Performance analyzer
│   └── seo-visual.md         # Visual/screenshot analyzer
│
├── skills/                   # Sub-skill definitions (used for individual commands)
│   ├── seo-page/
│   ├── seo-technical/
│   ├── seo-content/
│   ├── seo-schema/
│   ├── seo-images/
│   ├── seo-sitemap/
│   ├── seo-geo/
│   ├── seo-plan/
│   │   └── assets/           # Industry templates (saas, local, ecommerce, etc.)
│   ├── seo-programmatic/
│   ├── seo-competitor-pages/
│   └── seo-hreflang/
│
├── seo/                      # Main entry point
│   ├── SKILL.md              # Routing logic and orchestration overview
│   └── references/           # On-demand reference files
│       ├── cwv-thresholds.md
│       ├── schema-types.md
│       ├── eeat-framework.md
│       └── quality-gates.md
│
├── scripts/                  # Python utility scripts
│   ├── fetch_page.py
│   ├── parse_html.py
│   ├── capture_screenshot.py
│   ├── analyze_visual.py
│   └── image_audit.py
│
├── schema/
│   └── templates.json        # JSON-LD templates for 20+ schema types
│
├── pdf/
│   └── google-seo-reference.md
│
└── projects/                 # Audit history (created at runtime)
    ├── .current-project      # Active project slug
    └── {domain-slug}/
        ├── project.md        # Persists across runs — audit history table
        ├── .current-run      # Active run name
        └── run-001/
            ├── intake-brief.md
            ├── progress.md
            ├── technical-audit.md
            ├── visual-audit.md
            ├── content-analysis.md
            ├── schema-report.md
            ├── sitemap-analysis.md
            ├── performance-report.md
            ├── final-report.md
            └── screenshots/
```

## Orchestration Flow

### Full Audit

```
User: "audit https://example.com"
    │
    ▼
┌──────────────────┐
│  orchestrator.md │  ← Intake, project/run creation
└────────┬─────────┘
         │  Creates projects/{slug}/run-{NNN}/
         │  Spawns all 6 agents in parallel
         │
    ┌────┴────┬────────┬────────┬────────┬────────┐
    ▼         ▼        ▼        ▼        ▼        ▼
 technical  content  schema  sitemap  perf    visual
  agent     agent    agent   agent   agent   agent
    │         │        │        │        │        │
    └─────────┴────────┴────────┴────────┴────────┘
                            │
                            ▼ Each writes to projects/{slug}/{run}/
                     ┌──────────────┐
                     │ orchestrator │  ← Synthesises all 6 reports
                     │  synthesis   │    Computes health score
                     └──────┬───────┘    Compares vs prev run
                            │
                            ▼
                  projects/{slug}/{run}/final-report.md
```

### Project Versioning

Each domain is a project. Each audit of that domain creates a new numbered run:

```
projects/example-com/
  project.md          ← audit history table (all runs)
  run-001/            ← first audit
  run-002/            ← second audit (includes score delta vs run-001)
  run-003/            ← third audit
```

### Individual Commands

Individual sub-skill commands (e.g. `/seo page`, `/seo schema`) route directly to the relevant skill without creating a project folder.

## Component Types

### Agents (`agents/`)
Markdown files with YAML frontmatter. The orchestrator coordinates them; each agent writes its output to the active project run folder.

### Skills (`skills/`)
Markdown instruction files for individual analysis commands. Used standalone — no project folder required.

### Reference Files (`seo/references/`)
Static data loaded on-demand to avoid bloating the main skill context. Never loaded at startup.

## Design Principles

1. **Project persistence** — every full audit is saved to `projects/` with full run history
2. **Versioned runs** — re-audit the same domain to track progress over time
3. **Parallel execution** — all 6 agents run simultaneously; orchestrator synthesises after all complete
4. **Progressive disclosure** — main skill is concise; details in sub-skills and reference files
5. **Quality gates** — built-in thresholds prevent bad recommendations (thin content, deprecated schema, location page limits)
6. **LLM-agnostic** — plain markdown files, no provider-specific dependencies

## Extension Points

### Adding a New Sub-Skill
1. Create `skills/seo-newskill/SKILL.md`
2. Write skill instructions
3. Add to sub-skills list in `seo/SKILL.md`

### Adding a New Subagent
1. Create `agents/seo-newagent.md`
2. Add output destination block pointing to `projects/{slug}/{run}/`
3. Add to orchestrator's parallel execution step
