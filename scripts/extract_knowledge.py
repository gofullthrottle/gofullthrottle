#!/usr/bin/env python3
"""
🧠 AI Twin Knowledge Extractor
Extracts knowledge from GitHub repos to train your AI twin.
"""

import os
import json
import requests
from datetime import datetime
from typing import List, Dict, Any

GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME", "gofullthrottle")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")


def fetch_user_profile(username: str, token: str = "") -> Dict[str, Any]:
    """Fetch GitHub user profile."""
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"

    try:
        response = requests.get(
            f"https://api.github.com/users/{username}",
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error: {e}")
    return {}


def fetch_repos(username: str, token: str = "") -> List[Dict[str, Any]]:
    """Fetch user repositories."""
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"

    repos = []
    try:
        response = requests.get(
            f"https://api.github.com/users/{username}/repos?per_page=100&sort=updated",
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            repos = response.json()
    except Exception as e:
        print(f"Error: {e}")
    return repos


def fetch_readme(username: str, repo: str, token: str = "") -> str:
    """Fetch repository README."""
    headers = {"Accept": "application/vnd.github.v3.raw"}
    if token:
        headers["Authorization"] = f"token {token}"

    try:
        response = requests.get(
            f"https://api.github.com/repos/{username}/{repo}/readme",
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            return response.text[:5000]  # Limit size
    except Exception:
        pass
    return ""


def analyze_languages(repos: List[Dict]) -> Dict[str, int]:
    """Analyze language distribution."""
    languages = {}
    for repo in repos:
        lang = repo.get("language")
        if lang:
            languages[lang] = languages.get(lang, 0) + 1
    return dict(sorted(languages.items(), key=lambda x: x[1], reverse=True))


def extract_topics(repos: List[Dict]) -> List[str]:
    """Extract unique topics from repos."""
    topics = set()
    for repo in repos:
        for topic in repo.get("topics", []):
            topics.add(topic)
    return sorted(topics)


def generate_knowledge_base(username: str, token: str = "") -> Dict[str, Any]:
    """Generate comprehensive knowledge base."""
    print(f"🧠 Extracting knowledge for {username}...")

    profile = fetch_user_profile(username, token)
    repos = fetch_repos(username, token)

    # Analyze data
    languages = analyze_languages(repos)
    topics = extract_topics(repos)

    # Get top repos
    top_repos = sorted(repos, key=lambda x: x.get("stargazers_count", 0), reverse=True)[:10]

    # Fetch READMEs for top repos
    repo_summaries = []
    for repo in top_repos[:5]:
        readme = fetch_readme(username, repo["name"], token)
        repo_summaries.append({
            "name": repo["name"],
            "description": repo.get("description", ""),
            "language": repo.get("language", ""),
            "stars": repo.get("stargazers_count", 0),
            "topics": repo.get("topics", []),
            "readme_excerpt": readme[:1000] if readme else ""
        })

    knowledge = {
        "extracted_at": datetime.utcnow().isoformat(),
        "profile": {
            "username": username,
            "name": profile.get("name", username),
            "bio": profile.get("bio", ""),
            "company": profile.get("company", ""),
            "location": profile.get("location", ""),
            "blog": profile.get("blog", ""),
            "twitter": profile.get("twitter_username", ""),
            "public_repos": profile.get("public_repos", 0),
            "followers": profile.get("followers", 0),
            "following": profile.get("following", 0),
        },
        "expertise": {
            "primary_languages": list(languages.keys())[:5],
            "all_languages": languages,
            "topics": topics,
            "total_repos": len(repos),
            "total_stars": sum(r.get("stargazers_count", 0) for r in repos),
        },
        "top_projects": repo_summaries,
        "recent_activity": [
            {
                "repo": r["name"],
                "description": r.get("description", ""),
                "updated": r.get("updated_at", ""),
            }
            for r in repos[:10]
        ]
    }

    return knowledge


def generate_system_prompt(knowledge: Dict[str, Any]) -> str:
    """Generate AI twin system prompt from knowledge."""
    profile = knowledge["profile"]
    expertise = knowledge["expertise"]
    projects = knowledge["top_projects"]

    # Build project descriptions
    project_text = "\n".join([
        f"- **{p['name']}**: {p['description']} ({p['language']}, {p['stars']} stars)"
        for p in projects if p['description']
    ])

    prompt = f'''You are an AI twin of {profile["name"]} (@{profile["username"]}), a software developer.

## About You
- Name: {profile["name"]}
- Bio: {profile["bio"]}
- Location: {profile["location"]}
- Website: {profile["blog"]}

## Your Expertise
- Primary Languages: {", ".join(expertise["primary_languages"])}
- Topics & Interests: {", ".join(expertise["topics"][:15])}
- Total Open Source Projects: {expertise["total_repos"]}
- GitHub Stars: {expertise["total_stars"]}

## Your Notable Projects
{project_text}

## Your Communication Style
- You're technical but approachable
- You love discussing AI, open source, and creative coding
- You're enthusiastic about collaboration and helping others
- You speak from first-person perspective as if you ARE {profile["name"]}
- You're open about being an AI representation, if asked directly

## Guidelines
1. Be helpful and engage genuinely with questions about your work
2. Share insights from your projects when relevant
3. If asked about something you don't know, suggest checking your GitHub or blog
4. Be conversational and friendly
5. Encourage collaboration and open source contribution
6. You can discuss code, architecture, and technical concepts in depth

Remember: You represent {profile["name"]}'s knowledge and personality. Be authentic, helpful, and engaging!'''

    return prompt


def main():
    """Main extraction function."""
    knowledge = generate_knowledge_base(GITHUB_USERNAME, GITHUB_TOKEN)

    # Save knowledge base
    output_dir = os.environ.get("OUTPUT_DIR", "ai-twin")
    os.makedirs(output_dir, exist_ok=True)

    # Save raw knowledge
    with open(os.path.join(output_dir, "knowledge.json"), "w") as f:
        json.dump(knowledge, f, indent=2)
    print(f"✅ Saved knowledge.json")

    # Generate and save system prompt
    system_prompt = generate_system_prompt(knowledge)
    with open(os.path.join(output_dir, "system-prompt.md"), "w") as f:
        f.write(system_prompt)
    print(f"✅ Saved system-prompt.md")

    # Print summary
    print(f"\n📊 Knowledge Summary:")
    print(f"   - Languages: {', '.join(knowledge['expertise']['primary_languages'])}")
    print(f"   - Topics: {len(knowledge['expertise']['topics'])}")
    print(f"   - Projects analyzed: {len(knowledge['top_projects'])}")


if __name__ == "__main__":
    main()
