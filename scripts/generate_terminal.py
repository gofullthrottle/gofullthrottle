#!/usr/bin/env python3
"""
🖥️ Live Terminal SVG Generator
Generates an animated terminal SVG showing real GitHub activity.
"""

import os
import json
import requests
from datetime import datetime, timezone
from typing import List, Dict, Any
import html

# Configuration
GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME", "gofullthrottle")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

# Terminal styling
TERMINAL_CONFIG = {
    "width": 850,
    "height": 480,
    "bg_color": "#0d1117",
    "header_color": "#161b22",
    "text_color": "#c9d1d9",
    "prompt_color": "#58a6ff",
    "success_color": "#3fb950",
    "warning_color": "#d29922",
    "error_color": "#f85149",
    "accent_color": "#bc8cff",
    "comment_color": "#8b949e",
    "font_family": "JetBrains Mono, Fira Code, Monaco, Consolas, monospace",
    "font_size": 13,
    "line_height": 22,
}


def fetch_github_activity(username: str, token: str = "") -> List[Dict[str, Any]]:
    """Fetch recent GitHub activity for a user."""
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"

    events = []
    try:
        # Fetch recent events
        response = requests.get(
            f"https://api.github.com/users/{username}/events/public",
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            events = response.json()[:15]  # Get last 15 events
    except Exception as e:
        print(f"Error fetching events: {e}")

    return events


def fetch_recent_repos(username: str, token: str = "") -> List[Dict[str, Any]]:
    """Fetch recently updated repositories."""
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"

    repos = []
    try:
        response = requests.get(
            f"https://api.github.com/users/{username}/repos?sort=updated&per_page=5",
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            repos = response.json()
    except Exception as e:
        print(f"Error fetching repos: {e}")

    return repos


def format_event(event: Dict[str, Any]) -> tuple[str, str]:
    """Format a GitHub event into terminal output."""
    event_type = event.get("type", "")
    repo = event.get("repo", {}).get("name", "unknown").split("/")[-1]
    payload = event.get("payload", {})

    type_colors = {
        "PushEvent": "success",
        "CreateEvent": "accent",
        "PullRequestEvent": "warning",
        "IssuesEvent": "error",
        "WatchEvent": "accent",
        "ForkEvent": "success",
        "DeleteEvent": "error",
    }

    color = type_colors.get(event_type, "text")

    if event_type == "PushEvent":
        commits = payload.get("commits", [])
        if commits:
            msg = commits[0].get("message", "").split("\n")[0][:50]
            return f"git commit -m \"{msg}\"", color
        return f"git push origin {repo}", color

    elif event_type == "CreateEvent":
        ref_type = payload.get("ref_type", "repository")
        ref = payload.get("ref", "")
        if ref_type == "repository":
            return f"git init {repo}", color
        return f"git checkout -b {ref}", color

    elif event_type == "PullRequestEvent":
        action = payload.get("action", "opened")
        pr = payload.get("pull_request", {})
        title = pr.get("title", "")[:40]
        return f"gh pr {action}: \"{title}\"", color

    elif event_type == "IssuesEvent":
        action = payload.get("action", "opened")
        issue = payload.get("issue", {})
        title = issue.get("title", "")[:40]
        return f"gh issue {action}: \"{title}\"", color

    elif event_type == "WatchEvent":
        return f"gh repo star {repo}", color

    elif event_type == "ForkEvent":
        return f"gh repo fork {repo}", color

    return f"# Activity in {repo}", "comment"


def get_color(color_name: str) -> str:
    """Get color value from config."""
    color_map = {
        "text": TERMINAL_CONFIG["text_color"],
        "success": TERMINAL_CONFIG["success_color"],
        "warning": TERMINAL_CONFIG["warning_color"],
        "error": TERMINAL_CONFIG["error_color"],
        "accent": TERMINAL_CONFIG["accent_color"],
        "comment": TERMINAL_CONFIG["comment_color"],
        "prompt": TERMINAL_CONFIG["prompt_color"],
    }
    return color_map.get(color_name, TERMINAL_CONFIG["text_color"])


def generate_terminal_svg(username: str, events: List[Dict], repos: List[Dict]) -> str:
    """Generate the animated terminal SVG."""
    cfg = TERMINAL_CONFIG

    # Build terminal lines
    lines = []

    # Header
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines.append(("comment", f"# 🖥️  Live Terminal — Last updated: {now}"))
    lines.append(("comment", f"# 🔗  github.com/{username}"))
    lines.append(("text", ""))

    # Current project section
    lines.append(("prompt", "$ cat ~/.current_project"))
    if repos:
        top_repo = repos[0]
        lines.append(("accent", f"📦 {top_repo['name']}"))
        if top_repo.get('description'):
            desc = top_repo['description'][:60]
            lines.append(("text", f"   {desc}"))
        lang = top_repo.get('language', 'Unknown')
        stars = top_repo.get('stargazers_count', 0)
        lines.append(("comment", f"   ⭐ {stars} | 🔧 {lang}"))
    lines.append(("text", ""))

    # Recent activity section
    lines.append(("prompt", "$ git log --oneline --graph -n 8"))

    activity_count = 0
    seen_commands = set()
    for event in events:
        if activity_count >= 8:
            break
        cmd, color = format_event(event)
        if cmd not in seen_commands:
            seen_commands.add(cmd)
            prefix = "│ ●" if activity_count < 7 else "└ ○"
            lines.append((color, f"{prefix} {cmd}"))
            activity_count += 1

    lines.append(("text", ""))

    # Status section
    lines.append(("prompt", "$ echo $STATUS"))
    lines.append(("success", "🟢 Available for collaboration"))
    lines.append(("text", ""))
    lines.append(("prompt", "$ _"))

    # Calculate SVG dimensions
    num_lines = len(lines)
    content_height = num_lines * cfg["line_height"] + 80
    total_height = max(cfg["height"], content_height)

    # Generate SVG
    svg_lines = []
    svg_lines.append(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{cfg["width"]}" height="{total_height}" viewBox="0 0 {cfg["width"]} {total_height}">
  <defs>
    <style>
      @keyframes blink {{
        0%, 50% {{ opacity: 1; }}
        51%, 100% {{ opacity: 0; }}
      }}
      @keyframes typing {{
        from {{ width: 0; }}
        to {{ width: 100%; }}
      }}
      @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(-5px); }}
        to {{ opacity: 1; transform: translateY(0); }}
      }}
      .cursor {{
        animation: blink 1s infinite;
      }}
      .terminal-text {{
        font-family: {cfg["font_family"]};
        font-size: {cfg["font_size"]}px;
      }}
      .line {{
        animation: fadeIn 0.3s ease-out forwards;
        opacity: 0;
      }}
    </style>
  </defs>

  <!-- Terminal Window -->
  <rect width="{cfg["width"]}" height="{total_height}" rx="10" fill="{cfg["bg_color"]}"/>

  <!-- Terminal Header -->
  <rect width="{cfg["width"]}" height="36" rx="10" fill="{cfg["header_color"]}"/>
  <rect y="26" width="{cfg["width"]}" height="10" fill="{cfg["header_color"]}"/>

  <!-- Window Controls -->
  <circle cx="20" cy="18" r="6" fill="#f85149"/>
  <circle cx="40" cy="18" r="6" fill="#d29922"/>
  <circle cx="60" cy="18" r="6" fill="#3fb950"/>

  <!-- Terminal Title -->
  <text x="{cfg["width"]//2}" y="22" fill="{cfg["comment_color"]}" font-family="{cfg["font_family"]}" font-size="12" text-anchor="middle">
    {username}@github — zsh — {cfg["width"]}×{total_height}
  </text>

  <!-- Terminal Content -->
  <g transform="translate(20, 55)">''')

    # Add each line with staggered animation
    y_pos = 0
    for idx, (color_name, text) in enumerate(lines):
        color = get_color(color_name)
        escaped_text = html.escape(text)
        delay = idx * 0.08

        # Handle cursor on last line
        if text.endswith("$ _"):
            escaped_text = escaped_text[:-1]
            svg_lines.append(f'''    <g class="line" style="animation-delay: {delay}s">
      <text x="0" y="{y_pos}" fill="{color}" class="terminal-text">{escaped_text}</text>
      <rect x="{len(text) * 7.8}" y="{y_pos - 12}" width="10" height="16" fill="{cfg["prompt_color"]}" class="cursor"/>
    </g>''')
        else:
            svg_lines.append(f'''    <g class="line" style="animation-delay: {delay}s">
      <text x="0" y="{y_pos}" fill="{color}" class="terminal-text">{escaped_text}</text>
    </g>''')

        y_pos += cfg["line_height"]

    svg_lines.append('''  </g>
</svg>''')

    return "\n".join(svg_lines)


def main():
    """Main function to generate the terminal SVG."""
    print(f"🖥️  Generating terminal for {GITHUB_USERNAME}...")

    # Fetch data
    events = fetch_github_activity(GITHUB_USERNAME, GITHUB_TOKEN)
    repos = fetch_recent_repos(GITHUB_USERNAME, GITHUB_TOKEN)

    print(f"📊 Fetched {len(events)} events and {len(repos)} repos")

    # Generate SVG
    svg_content = generate_terminal_svg(GITHUB_USERNAME, events, repos)

    # Write output
    output_dir = os.environ.get("OUTPUT_DIR", "assets")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "terminal.svg")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"✅ Generated {output_path}")

    # Also generate a dark mode variant
    dark_path = os.path.join(output_dir, "terminal-dark.svg")
    with open(dark_path, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"✅ Generated {dark_path}")


if __name__ == "__main__":
    main()
