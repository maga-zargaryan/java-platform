"""Render every diagram as <name>.light.svg and <name>.dark.svg.

Usage: python3 build.py [output_dir]   (default: ../../docs/diagrams)
"""
import os
import sys

from diagrams import ALL

out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "..", "docs", "diagrams")
os.makedirs(out, exist_ok=True)
for name, draw in ALL.items():
    for theme in ("light", "dark"):
        with open(os.path.join(out, f"{name}.{theme}.svg"), "w") as f:
            f.write(draw(theme))
print(f"wrote {len(ALL) * 2} files to {os.path.abspath(out)}")
