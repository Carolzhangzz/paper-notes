# Paper Notes: Dual-View with Category System

## Overview

Add a Topics view alongside the existing Timeline view, enabling per-paper category browsing. Each paper gets a predefined category label; the Topics view groups papers by category across all dates.

## Data Structure

### index.json (per-paper granularity)

Each paper is a separate entry:

```json
{
  "date": "2026-03-30",
  "title": "Short descriptive title",
  "category": "HCI/Creativity",
  "file": "posts/2026-03-30.md",
  "anchor": "2-computational-scaffolding-of-composition-value-and-color-for-disciplined-drawing"
}
```

- `anchor`: derived from the `## N. Title` heading in the markdown, used for deep-linking to a specific paper within a day's notes
- `category`: one of the predefined categories (see below)
- Multiple entries can share the same `file` (same day, different papers)

### Predefined Categories (8)

| Category | Scope |
|----------|-------|
| World Models | world models, video prediction, latent dynamics |
| Embodied AI | robotics, simulation, embodied agents |
| HCI/Creativity | interaction design, creativity tools, art, education |
| AI Safety | adversarial ML, alignment, image protection, security |
| Multimodal/VLM | vision-language models, visual reasoning |
| AI for Science | scientific discovery, automated research, AI4Science |
| LLM/Foundation | language models, training, scaling |
| Survey | review papers, surveys, meta-analyses |

New categories can be added by simply writing a new category string in index.json; the frontend renders any category it encounters without code changes.

## Frontend Design

### Tab Bar

Two tabs below the header: **Timeline** | **Topics**. Active tab highlighted. Default: Timeline.

### Timeline View

- Lists all papers in reverse chronological order (newest first)
- Each card shows: title, date, category badge
- Click navigates to the markdown file and scrolls to the paper's anchor

### Topics View

- Groups all papers under their category heading
- Each category section lists papers with title + date
- Empty categories are hidden
- Papers within a category sorted by date descending
- Click navigates to the markdown file and scrolls to the paper's anchor

### Paper Detail View

- Loads the full markdown file
- Scrolls to the anchor position for the clicked paper
- Back button returns to the previous view (Timeline or Topics), preserving the active tab

## Files Changed

1. **`index.html`** — Rewrite JS (tab switching, per-paper rendering, anchor navigation), add CSS for tabs and category badges
2. **`posts/index.json`** — Convert from per-day to per-paper structure, backfill all existing papers with categories
3. **Markdown files** — No changes needed

## Maintenance

When writing paper notes, update `posts/index.json` with one entry per paper analyzed. No build step required.
