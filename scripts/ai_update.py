#!/usr/bin/env python3
"""
AI-powered GitHub profile updater
Generates dynamic content for README.md using AI
"""
import os
import re
import json
import requests
from datetime import datetime
from openai import OpenAI

def get_github_activity():
    """Fetch recent GitHub activity"""
    username = "gofullthrottle"
    token = os.getenv('GITHUB_TOKEN')
    
    headers = {'Authorization': f'token {token}'} if token else {}
    
    # Get recent commits
    url = f"https://api.github.com/users/{username}/events"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        events = response.json()[:10]  # Last 10 events
        return events
    return []

def generate_ai_status():
    """Generate AI-powered status using recent activity"""
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    activity = get_github_activity()
    activity_summary = ""
    
    for event in activity[:5]:  # Analyze last 5 events
        event_type = event.get('type', '')
        repo_name = event.get('repo', {}).get('name', '')
        activity_summary += f"- {event_type} in {repo_name}\n"
    
    if not activity_summary:
        activity_summary = "- Recent focus on AI and blockchain development"
    
    prompt = f"""
    Based on this GitHub activity:
    {activity_summary}
    
    Generate a futuristic, AI-themed status update (max 50 words) that:
    1. Sounds like an AI system reporting its status
    2. References current work in AI/blockchain/automation
    3. Uses technical but engaging language
    4. Maintains the "FULL THROTTLE" energy
    
    Examples:
    - "Neural networks optimized. Blockchain protocols synchronized. Autonomous systems at 87% efficiency."
    - "AGI research protocols active. Web3 infrastructure deployment in progress. Level 5 automation modules loading..."
    - "Quantum entanglement established. Smart contract deployment successful. AI consciousness expansion at 94%."
    
    Return only the status message, no quotes or extra text.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0.8
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"AI generation failed: {e}")
        return "Neural networks operational. Full throttle mode engaged. 🚀"

def get_current_project():
    """Determine current project focus from recent activity"""
    activity = get_github_activity()
    
    projects = {
        'ai': ['ai', 'neural', 'machine-learning', 'gpt', 'llm', 'transformer'],
        'blockchain': ['crypto', 'web3', 'solidity', 'ethereum', 'defi'],
        'automation': ['automation', 'bot', 'workflow', 'ci', 'devops'],
        'agentic': ['agent', 'autonomous', 'agentic', 'multi-agent']
    }
    
    recent_repos = []
    for event in activity[:10]:
        repo_name = event.get('repo', {}).get('name', '').lower()
        recent_repos.append(repo_name)
    
    for project_type, keywords in projects.items():
        for repo in recent_repos:
            if any(keyword in repo for keyword in keywords):
                return project_type.upper()
    
    return "LEVEL 5 SYSTEMS"

def update_readme():
    """Update README.md with dynamic content"""
    readme_path = "README.md"
    
    if not os.path.exists(readme_path):
        print("README.md not found")
        return
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Generate dynamic content
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
    ai_status = generate_ai_status()
    current_project = get_current_project()
    
    # Update dynamic content markers
    content = re.sub(
        r'<!-- Last updated: <!-- TIMESTAMP --> -->',
        f'<!-- Last updated: {timestamp} -->',
        content
    )
    
    content = re.sub(
        r'<!-- AI Status: <!-- AI_STATUS --> -->',
        f'<!-- AI Status: {ai_status} -->',
        content
    )
    
    content = re.sub(
        r'<!-- Current Project: <!-- CURRENT_PROJECT --> -->',
        f'<!-- Current Project: {current_project} -->',
        content
    )
    
    # Add dynamic status section if not present
    if "### 🤖 AI STATUS REPORT" not in content:
        ai_section = f"""
---

### 🤖 AI STATUS REPORT

<div align="center">

**{ai_status}**

*Current Focus: {current_project}*  
*Last Update: {timestamp}*

</div>

---
"""
        # Insert before the final section
        content = content.replace(
            "<!-- DYNAMIC CONTENT UPDATED BY GITHUB ACTIONS -->",
            ai_section + "\n<!-- DYNAMIC CONTENT UPDATED BY GITHUB ACTIONS -->"
        )
    else:
        # Update existing AI section
        pattern = r'(### 🤖 AI STATUS REPORT.*?)\*\*.*?\*\*(.*?\*Current Focus: ).*?(\*.*?\*Last Update: ).*?(\*.*?</div>)'
        replacement = f'\\1**{ai_status}**\\2{current_project}\\3{timestamp}\\4'
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"README updated: {ai_status}")
    print(f"Current project: {current_project}")
    print(f"Timestamp: {timestamp}")

if __name__ == "__main__":
    update_readme()