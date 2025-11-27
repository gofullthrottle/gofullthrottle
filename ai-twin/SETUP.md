# 🤖 AI Twin Setup Guide

Your personal AI clone that visitors can chat with! This guide covers multiple deployment options from simple to advanced.

## Quick Start

### Step 1: Generate Your Knowledge Base

Run the extraction script to pull your GitHub data:

```bash
export GITHUB_USERNAME=gofullthrottle
export GITHUB_TOKEN=your_token_here  # Optional, for higher rate limits
python scripts/extract_knowledge.py
```

This creates:
- `ai-twin/knowledge.json` - Raw data about your projects & activity
- `ai-twin/system-prompt.md` - Ready-to-use system prompt for your AI twin

### Step 2: Choose Your Platform

---

## Option A: Poe (Easiest - Free)

1. Go to [poe.com/create_bot](https://poe.com/create_bot)
2. Name your bot (e.g., "gofullthrottle-twin")
3. Paste your `system-prompt.md` content into the system prompt
4. Select a base model (Claude or GPT-4 recommended)
5. Make it public
6. Share the link on your profile!

**Embed in README:**
```markdown
[![Chat with my AI Twin](https://img.shields.io/badge/Chat-AI_Twin-purple?style=for-the-badge)](https://poe.com/your-bot-name)
```

---

## Option B: Character.ai (Free, Popular)

1. Go to [character.ai](https://character.ai)
2. Create a new character
3. Use knowledge.json to fill in personality details
4. Set greeting message
5. Make public and share

---

## Option C: HuggingFace Spaces (Free, Customizable)

Create a Gradio app for full control:

1. Create a new Space at [huggingface.co/spaces](https://huggingface.co/spaces)
2. Use the `chat-widget/app.py` template (included below)
3. Add your API key as a secret
4. Deploy!

---

## Option D: Custom Website (Most Control)

Use the included `chat-widget.html` as a starting point:

1. Host on GitHub Pages, Vercel, or Netlify
2. Connect to OpenAI, Anthropic, or other API
3. Full customization of UI and behavior

---

## Option E: Chatbase / CustomGPT (Paid, Professional)

For a more polished solution:

1. **Chatbase** ([chatbase.co](https://chatbase.co))
   - Upload your knowledge.json
   - Add your blog/website URLs
   - Embed widget on your site

2. **CustomGPT** ([customgpt.ai](https://customgpt.ai))
   - Train on your GitHub repos
   - Professional embed options

---

## Enhancing Your AI Twin

### Add More Knowledge Sources

Edit `knowledge.json` to include:

```json
{
  "additional_context": {
    "blog_posts": ["url1", "url2"],
    "talks": ["conference talk 1", "workshop 2"],
    "publications": ["paper 1"],
    "interests": ["topic 1", "topic 2"],
    "fun_facts": ["fact 1", "fact 2"]
  }
}
```

### Personality Tweaks

Add to your system prompt:

```
## Personality Traits
- Enthusiastic about [specific topics]
- Tends to use [specific phrases or expressions]
- Humor style: [dry/playful/technical]
- Responds to greetings with [specific greeting]
```

### Conversation Starters

Suggest these to visitors:
- "What are you currently working on?"
- "Tell me about your favorite project"
- "What's your tech stack?"
- "How did you get into programming?"
- "What advice do you have for new developers?"

---

## Keeping It Updated

Add to `.github/workflows/`:

```yaml
name: Update AI Twin Knowledge

on:
  schedule:
    - cron: "0 0 * * 0"  # Weekly
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install requests
      - run: python scripts/extract_knowledge.py
        env:
          GITHUB_USERNAME: ${{ github.repository_owner }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      - uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: "🧠 Update AI twin knowledge"
```

---

## Privacy Considerations

- Only public GitHub data is extracted
- Review `knowledge.json` before deploying
- Remove any sensitive information
- Consider what you want your AI twin to discuss

---

## Need Help?

- Open an issue on this repo
- Check the examples in `ai-twin/examples/`
- Join discussions in the community
