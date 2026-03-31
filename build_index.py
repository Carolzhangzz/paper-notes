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
        
        # Find all ## and ### headings
        all_headings = list(re.finditer(r'^(#{2,3}) (.+)$', body, re.M))

        if not all_headings:
            title_match = re.search(r'^# (.+)$', body, re.M)
            title = title_match.group(1) if title_match else date
            papers.append({
                'date': date,
                'title': title,
                'category': classify(title, body[:800]),
                'file': f'posts/{name}',
            })
            continue

        for i, match in enumerate(all_headings):
            level = match.group(1)  # ## or ###
            title = match.group(2).strip()

            # Skip non-paper headings
            skip_patterns = ['cross-cutting', 'theme', 'summary', 'paper notes',
                             'build-on', 'trend signal', 'multi-perspective',
                             'core problem', 'key contribution', 'method', 'results']
            if any(p in title.lower() for p in skip_patterns):
                continue

            # Get content snippet for this section
            start = match.end()
            end = all_headings[i+1].start() if i+1 < len(all_headings) else len(body)
            snippet = body[start:start+800]

            # Detect if this is a paper entry (has Authors/Venue or Core Problem)
            is_paper = bool(re.search(r'Authors|Venue|Core Problem|Key Contribution|arXiv|CHI|ICML|EMNLP|NeurIPS|Science\b', snippet))

            # ## heading that contains ### sub-papers: skip the container
            if level == '##':
                # Check if ### children have paper TITLES (not just section headings)
                has_sub_papers = False
                for j in range(i+1, len(all_headings)):
                    if all_headings[j].group(1) == '##':
                        break
                    if all_headings[j].group(1) == '###':
                        sub_title = all_headings[j].group(2).strip().lower()
                        # Section headings like "Core Problem", "Method" are NOT sub-papers
                        section_names = ['core problem', 'key contribution', 'method', 'results',
                                        'multi-perspective', 'build-on', 'trend signal',
                                        'cross-cutting']
                        if any(sub_title.startswith(s) for s in section_names):
                            continue
                        # This ### has a real paper title — check if it has Authors/Venue
                        sub_start = all_headings[j].end()
                        sub_end = all_headings[j+1].start() if j+1 < len(all_headings) else len(body)
                        sub_snippet = body[sub_start:sub_start+500]
                        if re.search(r'Authors.*Venue|Venue.*Authors', sub_snippet):
                            has_sub_papers = True
                            break
                if has_sub_papers:
                    continue  # skip container, extract sub-papers below

            # ### headings: only include if they look like paper entries (not section headings)
            if level == '###':
                section_names = ['core problem', 'key contribution', 'method', 'results',
                                'multi-perspective', 'build-on', 'trend signal',
                                'cross-cutting']
                if any(title.lower().startswith(s) for s in section_names):
                    continue
                if not is_paper:
                    continue

            # Clean title
            clean_title = re.sub(r'^\d+(\.\d+)?\s*\.?\s*', '', title).strip()

            anchor = slugify(title)

            # Extract paper links (arXiv, ACL, Science, etc.)
            link_match = re.search(r'\*\*Links?\*\*:?\s*(.+)', snippet)
            links = []
            if link_match:
                for lm in re.finditer(r'\[([^\]]+)\]\(([^)]+)\)', link_match.group(1)):
                    links.append({'label': lm.group(1), 'url': lm.group(2)})
            # Also try to find arXiv URL in the section
            if not links:
                arxiv_match = re.search(r'https://arxiv\.org/abs/[\d.]+', snippet)
                if arxiv_match:
                    links.append({'label': 'arXiv', 'url': arxiv_match.group(0)})

            entry = {
                'date': date,
                'title': clean_title,
                'category': classify(clean_title, snippet),
                'file': f'posts/{name}',
                'anchor': anchor,
            }
            if links:
                entry['links'] = links
            papers.append(entry)
    
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
