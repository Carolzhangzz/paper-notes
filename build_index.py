#!/usr/bin/env python3
"""Build posts/index.json with per-paper entries and auto-categorization."""
import os, json, re, glob

# Category rules: keyword -> category
# Order matters: first match wins
CATEGORY_RULES = [
    # HCI first — catches interaction/alignment/sycophancy papers
    (['hci', 'human-computer', 'human-ai interaction', 'interaction design', 'user study',
      'creativity', 'creative', 'sensemaking', 'sense-making', 'steering', 'alignment reading',
      'friction', 'constitutional', 'policy design', 'interpretability', 'prompt chain',
      'library context', 'non-ai expert', 'dreamsheet', 'patchview', 'agentbuilder'], 'HCI/Creativity'),
    # Safety — sycophancy, bias, toxicity, collectives
    (['sycophant', 'prosocial', 'safety', 'bias', 'fairness', 'toxic', 'moderation',
      'self-regulation', 'ai collective', 'feature steering', 'mitigat'], 'AI Safety'),
    # World models
    (['world model', 'world-model', 'worldmodel', 'kinema', 'dreamer', 'imagination',
      'dynamics model', 'dream to chat'], 'World Models'),
    # Embodied
    (['embodied', 'robotics', 'robot', 'manipulation', 'navigation', 'locomotion',
      'autonomous driving'], 'Embodied AI'),
    # Multimodal
    (['multimodal', 'vision-language', 'vlm', 'vqa', 'visual question', 'image-text',
      'video understanding', 'videoitg'], 'Multimodal/VLM'),
    # AI for Science
    (['drug', 'protein', 'molecular', 'climate', 'material science', 'interdisciplinary',
      'scientific research'], 'AI for Science'),
    # LLM/Foundation
    (['llm', 'language model', 'transformer', 'foundation model', 'pretraining',
      'fine-tuning', 'rlhf', 'reinforcement learning', 'dialogue', 'reward shaping'], 'LLM/Foundation'),
    # Survey
    (['survey', 'overview', 'reading list'], 'Survey'),
]

def classify(title, content_snippet):
    """Auto-classify a paper based on title + first ~500 chars of content."""
    text = (title + ' ' + content_snippet).lower()
    for keywords, category in CATEGORY_RULES:
        if any(kw in text for kw in keywords):
            return category
    return 'LLM/Foundation'  # default

def slugify(text):
    """Convert heading to anchor slug matching marked.js default."""
    text = re.sub(r'[^\w\s-]', '', text.lower().strip())
    return re.sub(r'\s+', '-', text)

def build_index():
    papers = []
    
    for filepath in sorted(glob.glob('posts/*.md'), reverse=True):
        name = os.path.basename(filepath)
        date = name.replace('.md', '')
        
        with open(filepath) as f:
            content = f.read()
        
        # Remove frontmatter
        body = re.sub(r'^---\s*\n.*?\n---\s*', '', content, flags=re.S)
        
        # Find all ## headings (individual papers)
        headings = list(re.finditer(r'^## (.+)$', body, re.M))
        
        if not headings:
            # No sub-papers, treat whole file as one entry
            title_match = re.search(r'^# (.+)$', body, re.M)
            title = title_match.group(1) if title_match else date
            papers.append({
                'date': date,
                'title': title,
                'category': classify(title, body[:800]),
                'file': f'posts/{name}',
            })
            continue
        
        for i, match in enumerate(headings):
            title = match.group(1).strip()
            
            # Skip non-paper headings (like "Cross-Cutting Themes")
            skip_patterns = ['cross-cutting', 'theme', 'summary', 'paper notes']
            if any(p in title.lower() for p in skip_patterns):
                continue
            
            # Get content snippet for this section
            start = match.end()
            end = headings[i+1].start() if i+1 < len(headings) else len(body)
            snippet = body[start:start+800]
            
            # Clean title: remove numbering like "1. " or "1.1 " or "1.9 "
            clean_title = re.sub(r'^\d+(\.\d+)?\s*\.?\s*', '', title).strip()
            
            anchor = slugify(title)
            
            papers.append({
                'date': date,
                'title': clean_title,
                'category': classify(clean_title, snippet),
                'file': f'posts/{name}',
                'anchor': anchor,
            })
    
    with open('posts/index.json', 'w') as f:
        json.dump(papers, f, indent=2, ensure_ascii=False)
    
    # Print summary
    cats = {}
    for p in papers:
        cats[p['category']] = cats.get(p['category'], 0) + 1
    print(f"Total: {len(papers)} papers")
    for cat, count in sorted(cats.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")

if __name__ == '__main__':
    build_index()
