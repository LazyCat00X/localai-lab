# LocalAI Lab

**Practical guides for self-hosted AI.** Every guide includes real terminal output, not theory.

## What

A static content site covering Ollama, vLLM, llama.cpp, ComfyUI, RAG pipelines, Open WebUI, and related tools. New guides published every 2 days via automated pipeline.

## Stack

- **Static HTML/CSS** — no build tools, no frameworks, no JS overhead
- **Automated Content Pipeline** — Hermes Agent cron job produces new guides every 2 days
- **Hosting** — designed for GitHub Pages (deploy via `python3 scripts/deploy.py deploy`)

## Quick Start (Preview Locally)

```bash
python3 scripts/deploy.py preview
# → http://localhost:8080
```

## Deployment

```bash
# 1. Set up GitHub
gh auth login
git init && git add . && git commit -m "Initial commit"
gh repo create localai-lab --public --push

# 2. Deploy
python3 scripts/deploy.py deploy
```

## Content Pipeline

A cron job runs every 2 days that:
1. Researches trending topics in self-hosted AI
2. Writes comprehensive guides with real terminal output
3. Updates the site index
4. Outputs a summary

See `scripts/content_pipeline.py` (or the skill `localai-lab-content-pipeline`).

## Monetization

- **Affiliate links** — DigitalOcean, Vultr, RunPod, Vast.ai
- **Newsletter** — Email list for future monetization
- **Future** — Digital products (config templates, one-click deploy scripts)

## Structure

```
docs/
├── index.html              # Landing page
├── assets/style.css        # Theme
├── guides/                 # All guides
│   ├── index.json          # Auto-loaded by landing page
│   ├── ollama-complete-guide/
│   ├── local-llm-linux/
│   ├── vllm-setup-guide/
│   └── ...
├── tools/                  # Tools directory
└── newsletter/             # Subscription page
scripts/
├── deploy.py               # Build and deploy
└── content_pipeline.py     # Automation (via cron)
```

## License

Content is CC BY 4.0. Code is MIT.
