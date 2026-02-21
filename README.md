<!-- Updated: 2026-02-21 -->

# Claude SEO

Agent-based SEO analysis system. Audits websites across technical SEO, content quality (E-E-A-T), schema markup, performance, images, sitemaps, and AI search optimization (GEO). Saves all outputs locally with versioned run history per project.

Works with any LLM provider — Claude, GPT-4, Gemini, or any agent runner that can read markdown and use tools.

## Quick Start

```bash
git clone https://github.com/AgriciDaniel/claude-seo.git
cd claude-seo
pip install -r requirements.txt
playwright install chromium  # optional, for screenshots
```

Then open the repo in your LLM of choice and run an audit:

```
Audit https://example.com
```

The orchestrator handles the rest — intake, parallel agent execution, synthesis, and saving everything to `projects/`.

## How It Works

Point your LLM at `agents/orchestrator.md` to start a full audit:

1. **Intake** — asks for URL, goal, priority pages; creates `projects/{slug}/run-001/`
2. **Parallel analysis** — 6 specialist agents run simultaneously
3. **Synthesis** — orchestrator combines all reports into `final-report.md` with health score
4. **History** — re-audit the same domain to get score deltas and track progress over time

```
projects/
  example-com/
    project.md        ← audit history across all runs
    run-001/          ← first audit
    run-002/          ← second audit (shows what improved/regressed)
```

## Analysis Coverage

| Agent | What it covers |
|-------|---------------|
| `seo-technical` | Crawlability, indexability, security, URL structure, mobile, Core Web Vitals, JS rendering |
| `seo-content` | E-E-A-T signals, word count, readability, AI citation readiness, thin content |
| `seo-schema` | JSON-LD detection/validation, deprecated type enforcement, generation |
| `seo-sitemap` | XML validation, coverage gaps, location page quality gates |
| `seo-performance` | LCP, INP, CLS — current 2026 thresholds |
| `seo-visual` | Desktop + mobile screenshots, above-fold analysis, layout issues |

## Individual Commands (Claude Code)

For targeted analysis without creating a project:

| Command | Description |
|---------|-------------|
| `/seo page <url>` | Deep single-page analysis |
| `/seo technical <url>` | Technical SEO audit (8 categories) |
| `/seo content <url>` | E-E-A-T and content quality |
| `/seo schema <url>` | Schema detection, validation, generation |
| `/seo images <url>` | Image optimization analysis |
| `/seo sitemap <url>` | Sitemap validation and generation |
| `/seo geo <url>` | AI Overviews / Generative Engine Optimization |
| `/seo plan <type>` | Strategic SEO planning (saas, local, ecommerce, publisher, agency) |
| `/seo programmatic <url>` | Programmatic SEO analysis |
| `/seo competitor-pages <url>` | Competitor comparison page generation |
| `/seo hreflang <url>` | Hreflang/i18n SEO audit |

## Features

### Core Web Vitals (2026)
- **LCP** < 2.5s — Largest Contentful Paint
- **INP** < 200ms — Interaction to Next Paint (replaced FID March 2024)
- **CLS** < 0.1 — Cumulative Layout Shift

### E-E-A-T (Dec 2025 QRG)
Now applies to all competitive queries (not just YMYL):
- Experience, Expertise, Authoritativeness, Trustworthiness

### Schema Enforcement
- Deprecated: HowTo (Sept 2023), SpecialAnnouncement (July 2025)
- Restricted: FAQ — government and healthcare only (Aug 2023)
- 20+ ready-to-use JSON-LD templates in `schema/templates.json`

### AI Search Optimization (GEO)
- Google AI Overviews, ChatGPT, Perplexity optimization
- AI crawler access (GPTBot, ClaudeBot, PerplexityBot)
- llms.txt compliance, passage-level citability scoring

### Quality Gates
- Warning at 30+ location pages (enforce 60%+ unique content)
- Hard stop at 50+ location pages
- Programmatic SEO: warning at 100+ pages, hard stop at 500+

## Requirements

- Python 3.8+
- `pip install -r requirements.txt`
- Playwright (optional, for screenshots): `playwright install chromium`

## MCP Integrations

Integrates with MCP servers for live data — Ahrefs (`@ahrefs/mcp`), Semrush, Google Search Console, PageSpeed Insights, DataForSEO. See [MCP Integration Guide](docs/MCP-INTEGRATION.md).

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Commands Reference](docs/COMMANDS.md)
- [MCP Integration](docs/MCP-INTEGRATION.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)

## License

MIT — see [LICENSE](LICENSE)
