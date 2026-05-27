#!/usr/bin/env python3
"""
LocalAI Lab — Deploy Script
Builds and deploys the static site to GitHub Pages.
Run with: python3 scripts/deploy.py

Prerequisites:
  gh auth login     # GitHub CLI authentication
"""
import subprocess
import sys
import os
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
DOCS_DIR = REPO_ROOT / "docs"
SITE_DIR = REPO_ROOT / "_site"

def run(cmd, cwd=None):
    print(f"$ {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd or REPO_ROOT, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ERROR: {result.stderr}")
        sys.exit(1)
    return result.stdout.strip()

def check_gh_auth():
    """Check GitHub CLI is authenticated."""
    status = run("gh auth status 2>&1")
    if "You are not logged" in status:
        print("❌ GitHub CLI not authenticated.")
        print()
        print("To deploy, run:")
        print("  gh auth login")
        print()
        print("Then run this script again.")
        sys.exit(1)
    print("✓ GitHub CLI authenticated")

def build_site():
    """The site is static HTML — just copy docs/ to _site/."""
    print(f"\n📦 Building site...")
    if SITE_DIR.exists():
        run(f"rm -rf {SITE_DIR}")
    run(f"cp -r {DOCS_DIR} {SITE_DIR}")
    print(f"✓ Site built at {SITE_DIR}")

def deploy_gh_pages():
    """Deploy to GitHub Pages via gh-pages branch."""
    print(f"\n🚀 Deploying to GitHub Pages...")
    
    # Check for git repo
    if not (REPO_ROOT / ".git").exists():
        print("❌ No git repository found. Set up a repo first:")
        print()
        print("  cd /home/kevyn/projects/localai-lab")
        print("  git init")
        print("  git add .")
        print('  git commit -m "Initial commit"')
        print("  gh repo create localai-lab --public --push")
        print()
        print("Then run this script again.")
        sys.exit(1)
    
    # Check if remote exists
    remotes = run("git remote -v")
    if not remotes:
        print("❌ No git remote configured.")
        print("Run: gh repo create localai-lab --public --push")
        sys.exit(1)
    
    # Deploy using gh
    run(f"gh deploy {DOCS_DIR} --from-file")
    print("✓ Deployed to GitHub Pages!")
    print()
    print("🌐 Your site will be live at:")
    print("   https://<username>.github.io/localai-lab/")
    print()
    print("   ⚡ Configure a custom domain in repo Settings > Pages.")

def preview_local():
    """Start a local HTTP server for preview."""
    port = 8080
    print(f"\n🔍 Starting local preview at http://localhost:{port}")
    print("   Press Ctrl+C to stop.")
    os.chdir(DOCS_DIR)
    run(f"python3 -m http.server {port}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="LocalAI Lab deployment tools")
    parser.add_argument("action", nargs="?", default="preview",
                        choices=["preview", "deploy", "build"],
                        help="Action to perform")
    args = parser.parse_args()
    
    if args.action == "preview":
        preview_local()
    elif args.action == "build":
        build_site()
    elif args.action == "deploy":
        check_gh_auth()
        build_site()
        deploy_gh_pages()
