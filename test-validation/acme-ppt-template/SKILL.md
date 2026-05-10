---
name: acme-ppt-template
description: ACME Corp. PowerPoint template for creating branded investment analysis presentations. Use when creating ACME Corp.-branded pitch decks, board materials, investment reports, or client presentations.
---

# ACME Corp. PPT Template

Template: `assets/template.pptx` (13.33" x 7.50", 11 layouts)

## Creating Presentations

```python
from pptx import Presentation

prs = Presentation("path/to/skill/assets/template.pptx")

# DELETE all existing slides first
while len(prs.slides) > 0:
    rId = prs.slides._sldIdLst[0].rId
    prs.part.drop_rel(rId)
    del prs.slides._sldIdLst[0]

# Add slides from layouts
slide = prs.slides.add_slide(prs.slide_layouts[LAYOUT_IDX])
```

## Key Layouts

| Index | Name | Use For |
|-------|------|---------|
| 0 | Title Slide | Cover/title slide, company name + presentation title |
| 1 | Title and Content | Main content slides with bullet points |
| 2 | Section Header | Section dividers with title and body text |
| 3 | Two Content | Two-column content layout |
| 4 | Comparison | Side-by-side comparison with headers |
| 5 | Title Only | Free-form content with title only |
| 6 | Blank | Fully blank canvas |
| 7 | Content with Caption | Content + caption text below |
| 8 | Picture with Caption | Image-centric slide with caption |
| 9 | Title and Vertical Text | Title with vertical text body |
| 10 | Vertical Title and Text | Vertical title + horizontal text |

## Placeholder Mapping

### Layout 0: Title Slide (Cover Page)
| idx | Type | Position | Use |
|-----|------|----------|-----|
| 0 | CENTER_TITLE (3) | x=0.75", y=2.33", w=8.50", h=1.61" | Company name |
| 1 | SUBTITLE (4) | x=1.50", y=4.25", w=7.00", h=1.92" | Presentation title / date |
| 10 | DATE (16) | x=0.50", y=6.95", w=2.33", h=0.40" | Date |
| 11 | FOOTER (15) | x=3.42", y=6.95", w=3.17", h=0.40" | Footer text |
| 12 | SLIDE_NUMBER (13) | x=7.17", y=6.95", w=2.33", h=0.40" | Slide number |

### Layout 1: Title and Content (Main Content)
| idx | Type | Position | Use |
|-----|------|----------|-----|
| 0 | TITLE (1) | x=0.50", y=0.30", w=9.00", h=1.25" | Slide title |
| 1 | OBJECT (7) | x=0.50", y=1.75", w=9.00", h=4.95" | Main content body (bullets, text) |
| 10 | DATE (16) | x=0.50", y=6.95", w=2.33", h=0.40" | Date |
| 11 | FOOTER (15) | x=3.42", y=6.95", w=3.17", h=0.40" | Footer text |
| 12 | SLIDE_NUMBER (13) | x=7.17", y=6.95", w=2.33", h=0.40" | Slide number |

### Layout 3: Two Content (Two-Column)
| idx | Type | Position | Use |
|-----|------|----------|-----|
| 0 | TITLE (1) | x=0.50", y=0.30", w=9.00", h=1.25" | Slide title |
| 1 | OBJECT (7) | x=0.50", y=1.75", w=4.42", h=4.95" | Left column content |
| 2 | OBJECT (7) | x=5.08", y=1.75", w=4.42", h=4.95" | Right column content |

### Layout 5: Title Only
| idx | Type | Position | Use |
|-----|------|----------|-----|
| 0 | TITLE (1) | x=0.50", y=0.30", w=9.00", h=1.25" | Slide title |
| (no content placeholder - free area from y=1.55" to y=6.95") |

### Layout 6: Blank
| idx | Type | Position | Use |
|-----|------|----------|-----|
| (no title/content placeholders - full canvas available) |

## Content Area Boundaries

```
Content Area (Layout 1 - Title and Content):
- Left margin: 0.50" (content starts here)
- Top: 1.75" (below title placeholder ending at y=1.55")
- Width: 9.00"
- Height: 4.95" (ends before footer at y=6.95")

For 2-column layouts (Layout 3):
- Left column: x=0.50", width=4.42"
- Right column: x=5.08", width=4.42"

For 4-quadrant layouts (Layout 4 - Comparison):
- Left column: x=0.50", width=4.42"
- Right column: x=5.08", width=4.42"
- Top row: y=2.38", height=4.32"
- Bottom row: (same as top, use vertical split within each column)
```

## Filling Content

**Do NOT add manual bullet characters** - slide master handles formatting.

```python
# Fill title
for shape in slide.shapes:
    if hasattr(shape, 'placeholder_format'):
        if shape.placeholder_format.type == 1:  # TITLE
            shape.text = "Slide Title"

# Fill content with hierarchy (level 0 = header, level 1 = bullet)
for shape in slide.shapes:
    if hasattr(shape, 'placeholder_format'):
        idx = shape.placeholder_format.idx
        if idx == 1:  # OBJECT placeholder in Layout 1
            tf = shape.text_frame
            for para in tf.paragraphs:
                para.clear()

            content = [
                ("Section Header", 0),
                ("First bullet point", 1),
                ("Second bullet point", 1),
            ]

            tf.paragraphs[0].text = content[0][0]
            tf.paragraphs[0].level = content[0][1]
            for text, level in content[1:]:
                p = tf.add_paragraph()
                p.text = text
                p.level = level
```

## Example: Cover Slide

```python
slide = prs.slides.add_slide(prs.slide_layouts[0])
for shape in slide.shapes:
    if hasattr(shape, 'placeholder_format'):
        idx = shape.placeholder_format.idx
        if idx == 0:  # CENTER_TITLE
            shape.text = "ACME Corp."
        elif idx == 1:  # SUBTITLE
            shape.text = "Investment Analysis Report | May 2026"
```

## Example: Content Slide (Company Overview)

```python
slide = prs.slides.add_slide(prs.slide_layouts[1])
for shape in slide.shapes:
    if hasattr(shape, 'placeholder_format'):
        ph_type = shape.placeholder_format.type
        idx = shape.placeholder_format.idx
        if ph_type == 1:
            shape.text = "Company Overview"
        elif idx == 1:  # OBJECT placeholder
            tf = shape.text_frame
            for para in tf.paragraphs:
                para.clear()
            content = [
                ("Company Profile", 0),
                ("ACME Corp. founded in 2010, focused on AI-driven fintech", 1),
                ("Headquartered in Shanghai, 2,000+ employees", 1),
                ("Key Financials", 0),
                ("2025 Revenue: RMB 5B (+40% YoY)", 1),
                ("Net margin: 22%", 1),
                ("Market cap: RMB 80B", 1),
            ]
            tf.paragraphs[0].text = content[0][0]
            tf.paragraphs[0].level = content[0][1]
            for text, level in content[1:]:
                p = tf.add_paragraph()
                p.text = text
                p.level = level
```

## Example: Valuation Summary Slide

```python
slide = prs.slides.add_slide(prs.slide_layouts[1])
for shape in slide.shapes:
    if hasattr(shape, 'placeholder_format'):
        ph_type = shape.placeholder_format.type
        idx = shape.placeholder_format.idx
        if ph_type == 1:
            shape.text = "Valuation Summary"
        elif idx == 1:  # OBJECT placeholder
            tf = shape.text_frame
            for para in tf.paragraphs:
                para.clear()
            content = [
                ("Valuation Methods", 0),
                ("DCF: RMB 120-150/share", 1),
                ("Comps: RMB 110-135/share", 1),
                ("P/E Multiple: RMB 130/share", 1),
                ("Recommendation", 0),
                ("Current price: RMB 95", 1),
                ("Target price: RMB 135 (42% upside)", 1),
                ("Rating: BUY", 1),
            ]
            tf.paragraphs[0].text = content[0][0]
            tf.paragraphs[0].level = content[0][1]
            for text, level in content[1:]:
                p = tf.add_paragraph()
                p.text = text
                p.level = level
```
