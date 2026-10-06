# Diagram generator

The architecture diagrams in all Java Platform repositories are generated, not drawn by hand.

| File | Purpose |
|---|---|
| `kit.py` | Drawing kit: themes (light/dark), layer bands, cards, AWS-style icons, arrows |
| `diagrams.py` | One function per diagram |
| `build.py` | Renders every diagram as `<name>.light.svg` and `<name>.dark.svg` |

```bash
python3 tools/diagrams/build.py            # writes docs/diagrams/
python3 tools/diagrams/build.py /some/dir  # or anywhere else
```

Requires only Python 3. READMEs embed both variants with `<picture>`, so GitHub shows the one
matching the reader's theme. After changing a diagram, copy the affected SVGs into the
repositories that use them.
