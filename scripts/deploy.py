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
    """Enable GitHub Pages serving from /docs on main branch."""
    print(f"\n🚀 Enabling GitHub Pages from /docs...")
    
    if not (REPO_ROOT / ".git").exists():
        print("❌ No git repository. Run: gh repo create localai-lab --public --source=.")
        sys.exit(1)
    
    remotes = run("git remote -v")
    if not remotes:
        print("❌ No git remote. Run: gh repo create localai-lab --public --source=.")
        sys.exit(1)
    
    # Push latest to main
    run("git push origin main")
    
    # Enable GitHub Pages via API
    owner_repo = run("gh repo view --json owner,name -q '.owner.login + \"/\" + .name'")
    result = subprocess.run(
        f'gh api repos/{owner_repo}/pages -X POST --input - <<< \'{{"source":{{"branch":"main","path":"/docs"}}}}\'',
        shell=True, capture_output=True, text=True, timeout=30
    )
    if result.returncode == 0:
        print("✓ GitHub Pages enabled!")
    elif "already has a GitHub Pages site" in result.stderr:
        # Update existing config
        result = subprocess.run(
            f'gh api repos/{owner_repo}/pages -X PUT --input - <<< \'{{"source":{{"branch":"main","path":"/docs"}}}}\'',
            shell=True, capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            print("✓ GitHub Pages config updated!")
        else:
            print(f"⚠ Update failed: {result.stderr.strip()}")
            print("Manual: Settings > Pages > Source: Deploy from branch > main,/docs")
    else:
        print(f"⚠ API error: {result.stderr.strip()}")
        print("Manual fix: Settings > Pages > Source: Deploy from branch > main,/docs")
    
    url = f"https://{owner_repo.split('/')[0]}.github.io/localai-lab/"
    print(f"\n🌐 Live at: {url}")
    print("   (may take 1-2 minutes to deploy)")

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
