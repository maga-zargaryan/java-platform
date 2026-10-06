"""Drawing kit for the Java Platform diagrams: layered bands, cards with AWS-style icons, arrows.

Every function returns an SVG fragment string. Colours come from a theme so each
diagram renders in a light and a dark variant.
"""
from html import escape

FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"

# AWS architecture-icon category colours.
CAT = {
    "storage": "#3F8624",
    "security": "#DD344C",
    "network": "#8C4FFF",
    "compute": "#ED7100",
    "database": "#4D4AD9",
    "mgmt": "#E7157B",
    "github": "#24292F",
    "neutral": "#5A6B86",
}

THEMES = {
    "light": {
        "canvas": "#FFFFFF", "card": "#FFFFFF", "card_line": "#E2E8F0", "fg": "#0F172A", "muted": "#526075",
        "bands": {
            "blue": ("#3B82F6", "#EFF6FF", "#0B3D91"),
            "green": ("#22A35A", "#ECFAF1", "#0E5A2E"),
            "orange": ("#F08C24", "#FFF6EC", "#8A4A06"),
            "purple": ("#7C4DDB", "#F5F0FE", "#3E1F8A"),
            "gray": ("#64748B", "#F5F7FA", "#1F2937"),
            "red": ("#DD344C", "#FEF1F2", "#8A1C2B"),
        },
    },
    "dark": {
        "canvas": "#0D1117", "card": "#161B22", "card_line": "#30363D", "fg": "#E6EDF3", "muted": "#9AA7B4",
        "bands": {
            "blue": ("#4A90F5", "#0E1D33", "#A9CBFF"),
            "green": ("#2FB867", "#0C2116", "#94E5B5"),
            "orange": ("#F39A3C", "#26180A", "#FFC891"),
            "purple": ("#9670F0", "#1B1430", "#CDB8FF"),
            "gray": ("#7D8B9E", "#141A22", "#D7DEE7"),
            "red": ("#F0566B", "#2A1116", "#FFB3BD"),
        },
    },
}

# 24x24 white line glyphs drawn inside the coloured icon square.
GLYPHS = {
    "bucket": '<path d="M4 6h16l-2 14H6z"/><ellipse cx="12" cy="6" rx="8" ry="2.5"/>',
    "lock": '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
    "git": '<circle cx="7" cy="5" r="2"/><circle cx="7" cy="19" r="2"/><circle cx="17" cy="9" r="2"/><path d="M7 7v10M17 11c0 4-4 4-8 6"/>',
    "helmet": '<path d="M4 16a8 8 0 0 1 16 0"/><path d="M2.5 16.5h19"/><path d="M12 8v4"/><path d="M8.5 9.5l1 3M15.5 9.5l-1 3"/>',
    "shield": '<path d="M12 3l7 3v6c0 4-3 7-7 9-4-2-7-5-7-9V6z"/><path d="M9 12l2 2 4-4"/>',
    "cloud": '<path d="M7 18h10a4 4 0 0 0 0-8 5 5 0 0 0-9.6-1A4.5 4.5 0 0 0 7 18z"/>',
    "arch": '<path d="M5 20V11a7 7 0 0 1 14 0v9"/><path d="M9 20v-8a3 3 0 0 1 6 0v8"/>',
    "list": '<rect x="4" y="4" width="16" height="16" rx="2"/><path d="M9 9h7M9 13h7M9 17h5"/><path d="M6.5 9h0M6.5 13h0M6.5 17h0" stroke-width="2.6"/>',
    "endpoint": '<circle cx="12" cy="12" r="8"/><path d="M8 10.5h8l-2.5-2.5M16 13.5H8l2.5 2.5"/>',
    "key": '<circle cx="8" cy="12" r="4"/><path d="M12 12h9M17 12v3M20 12v2"/>',
    "cert": '<rect x="3.5" y="4" width="17" height="12" rx="1.5"/><path d="M7 8h6M7 11h4"/><circle cx="16" cy="14" r="3"/><path d="M14.5 16.5l-1 4.5 2.5-1.2 2.5 1.2-1-4.5"/>',
    "r53": '<path d="M12 3l8 4v5c0 5-3.5 8-8 9-4.5-1-8-4-8-9V7z"/><text x="12" y="15.5" font-size="7.5" font-weight="700" text-anchor="middle" fill="#fff" stroke="none" font-family="Arial">53</text>',
    "alb": '<circle cx="12" cy="5" r="2.4"/><circle cx="5" cy="19" r="2.4"/><circle cx="12" cy="19" r="2.4"/><circle cx="19" cy="19" r="2.4"/><path d="M12 7.4v9.2M11 7l-5 9.8M13 7l5 9.8"/>',
    "ec2": '<rect x="6" y="6" width="12" height="12" rx="1.5"/><path d="M9 6V3M12 6V3M15 6V3M9 21v-3M12 21v-3M15 21v-3M6 9H3M6 12H3M6 15H3M21 9h-3M21 12h-3M21 15h-3"/>',
    "asg": '<rect x="3" y="9" width="11" height="11" rx="1.5"/><rect x="10" y="4" width="11" height="11" rx="1.5"/>',
    "db": '<ellipse cx="12" cy="5.5" rx="7" ry="2.5"/><path d="M5 5.5v13c0 1.4 3.1 2.5 7 2.5s7-1.1 7-2.5v-13"/><path d="M5 12c0 1.4 3.1 2.5 7 2.5s7-1.1 7-2.5"/>',
    "folder": '<path d="M3.5 7h6l2 2h9v10h-17z"/>',
    "layers": '<path d="M12 4l8.5 4-8.5 4-8.5-4z"/><path d="M3.5 12l8.5 4 8.5-4"/><path d="M3.5 16l8.5 4 8.5-4"/>',
    "ami": '<rect x="3.5" y="5" width="17" height="14" rx="2"/><path d="M8 9v6M12 9v6M16 9v6"/>',
    "gear": '<circle cx="12" cy="12" r="3"/><path d="M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M5.6 18.4l2.1-2.1M16.3 7.7l2.1-2.1"/><circle cx="12" cy="12" r="6.2"/>',
    "watch": '<circle cx="10" cy="10" r="6.5"/><path d="M14.8 14.8L20 20"/><path d="M5.5 10.5h1.8l1.3-2.8 1.6 4.6 1.4-2.6h1.9"/>',
    "vault": '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="2.5"/><path d="M12 3.5v4M12 16.5v4M3.5 12h4M16.5 12h4"/>',
    "wall": '<rect x="3.5" y="5" width="17" height="14" rx="1"/><path d="M3.5 9.7h17M3.5 14.3h17M9 5v4.7M15 5v4.7M12 9.7v4.6M7 14.3V19M17 14.3V19"/>',
    "trail": '<path d="M4 19l4-8 4 4 4-9 4 5"/><circle cx="4" cy="19" r="1.2"/><circle cx="20" cy="11" r="1.2"/>',
    "mail": '<rect x="3.5" y="6" width="17" height="12" rx="1.5"/><path d="M3.5 7l8.5 6.5L20.5 7"/>',
    "play": '<circle cx="12" cy="12" r="8.5"/><path d="M10 8.5l5.5 3.5-5.5 3.5z"/>',
    "check": '<circle cx="12" cy="12" r="8.5"/><path d="M8 12.2l2.8 2.8L16.2 9.5"/>',
    "doc": '<path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4"/><path d="M9.5 12.5L8 14l1.5 1.5M14.5 12.5L16 14l-1.5 1.5"/>',
    "user": '<circle cx="12" cy="8" r="3.5"/><path d="M5 20a7 7 0 0 1 14 0"/>',
    "token": '<rect x="3.5" y="6" width="17" height="12" rx="2"/><circle cx="8.5" cy="12" r="2"/><path d="M12.5 10.5h5M12.5 13.5h3.5"/>',
    "sts": '<circle cx="12" cy="12" r="8.5"/><path d="M8 12h8M13 9l3 3-3 3"/>',
    "branch": '<path d="M5 4v16"/><path d="M5 9h6a4 4 0 0 1 4 4v7"/><circle cx="5" cy="4" r="1.2"/><circle cx="15" cy="20" r="1.2"/>',
    "approve": '<circle cx="9" cy="8" r="3.2"/><path d="M3 19a6 6 0 0 1 11.5-2.5"/><path d="M14.5 17l2.2 2.2 4-4.4"/>',
    "var": '<path d="M8 4c-2 0-3 1-3 3v2.5c0 1.2-.8 2-2 2.5 1.2.5 2 1.3 2 2.5V17c0 2 1 3 3 3M16 4c2 0 3 1 3 3v2.5c0 1.2.8 2 2 2.5-1.2.5-2 1.3-2 2.5V17c0 2-1 3-3 3"/>',
    "dollar": '<circle cx="12" cy="12" r="8.5"/><path d="M14.8 9.2c-.6-1-1.6-1.4-2.8-1.4-1.6 0-2.8.8-2.8 2.1 0 2.9 5.8 1.6 5.8 4.4 0 1.3-1.2 2.1-3 2.1-1.3 0-2.4-.5-3-1.5M12 6v1.8M12 16.4V18"/>',
    "search": '<circle cx="10.5" cy="10.5" r="6"/><path d="M15 15l5 5"/>',
    "flow": '<path d="M3 8c3-3 6 3 9 0s6 3 9 0M3 13c3-3 6 3 9 0s6 3 9 0M3 18c3-3 6 3 9 0s6 3 9 0"/>',
    "box": '<path d="M12 3l8 4.5v9L12 21l-8-4.5v-9z"/><path d="M4 7.5l8 4.5 8-4.5M12 12v9"/>',
    "terraform": '<path d="M5 4l6 3.5v7L5 11zM12.5 7.5l6-3.5v7l-6 3.5zM12.5 15.5l6-3.5v7l-6 3.5z"/>',
}


def t(x, y, s, size, color, weight="400", anchor="start", family=FONT):
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" '
            f'fill="{color}" text-anchor="{anchor}">{escape(s)}</text>')


def icon(x, y, glyph, cat, size=40, outline=False):
    c = CAT[cat]
    scale = size / 40
    if outline:  # line icon without a coloured tile (role helmets, like the reference style)
        return (f'<g transform="translate({x + 8 * scale},{y + 8 * scale}) scale({scale})" fill="none" stroke="{c}" '
                f'stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">{GLYPHS[glyph]}</g>')
    return (f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="{8 * scale}" fill="{c}"/>'
            f'<g transform="translate({x + 8 * scale},{y + 8 * scale}) scale({scale})" fill="none" stroke="#FFFFFF" '
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{GLYPHS[glyph]}</g>')


class Canvas:
    def __init__(self, theme, width, height, label):
        self.th = THEMES[theme]
        self.w, self.h, self.label = width, height, label
        self.parts = []
        self.markers = {}

    def add(self, s):
        self.parts.append(s)

    def _marker(self, color):
        mid = "m" + color.lstrip("#")
        self.markers[mid] = color
        return f"url(#{mid})"

    # ---- building blocks -------------------------------------------------
    def band(self, x, y, w, h, tone, title, subtitle=None, title_size=24):
        line, fill, tcol = self.th["bands"][tone]
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="{line}" stroke-width="1.6"/>')
        self.add(t(x + 24, y + 38, title, title_size, tcol, "700"))
        if subtitle:
            self.add(t(x + 24, y + 64, subtitle, 15, tcol))

    def panel(self, x, y, w, h, tone=None, title=None, dashed=False, title_center=False, glyph=None, cat=None):
        if tone:
            line, fill, tcol = self.th["bands"][tone]
        else:
            line, fill, tcol = self.th["card_line"], self.th["card"], self.th["fg"]
        dash = ' stroke-dasharray="6 5"' if dashed else ""
        bg = self.th["card"] if not dashed else fill
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{bg}" stroke="{line}" stroke-width="1.3"{dash}/>')
        if title:
            tx = x + w / 2 if title_center else x + (52 if glyph else 16)
            if glyph:
                self.add(icon(x + 12, y + 10, glyph, cat, 30))
            self.add(t(tx, y + 30, title, 15, tcol, "700", "middle" if title_center else "start"))

    def card(self, x, y, w, glyph, cat, title, sub=None, boxed=True, h=64):
        if boxed:
            self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{self.th["card"]}" '
                     f'stroke="{self.th["card_line"]}" stroke-width="1.2"/>')
        iy = y + (h - 40) / 2
        self.add(icon(x + 12, iy, glyph, cat))
        ty = y + h / 2 + (-3 if sub else 5)
        self.add(t(x + 64, ty, title, 15, self.th["fg"], "600"))
        if sub:
            self.add(t(x + 64, ty + 19, sub, 12.5, self.th["muted"]))

    def small(self, x, y, w, glyph, cat, title, sub=None, tone=None):
        """Compact card (subnet / AZ style) with a tinted fill."""
        line, fill, tcol = self.th["bands"][tone] if tone else (self.th["card_line"], self.th["card"], self.th["fg"])
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="52" rx="8" fill="{self.th["card"]}" stroke="{line}" stroke-opacity="0.55" stroke-width="1.1"/>')
        self.add(icon(x + 10, y + 12, glyph, "neutral" if not tone else cat, 28, outline=True))
        self.add(t(x + 46, y + (24 if sub else 31), title, 13.5, self.th["fg"], "600"))
        if sub:
            self.add(t(x + 46, y + 41, sub, 11.5, self.th["muted"]))

    def role(self, x, y, w, label1, label2=None):
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="96" rx="10" fill="{self.th["card"]}" stroke="{self.th["card_line"]}" stroke-width="1.2"/>')
        self.add(icon(x + w / 2 - 28, y + 2, "helmet", "security", 56, outline=True))
        self.add(t(x + w / 2, y + 66, label1, 13.5, self.th["fg"], "600", "middle"))
        if label2:
            self.add(t(x + w / 2, y + 83, label2, 13.5, self.th["fg"], "600", "middle"))

    def arrow(self, pts, tone="gray", label=None, lx=None, ly=None, anchor="middle", dashed=False, width=2):
        color = self.th["bands"][tone][0]
        p = " ".join(f"{a},{b}" for a, b in pts)
        dash = ' stroke-dasharray="6 5"' if dashed else ""
        self.add(f'<polyline points="{p}" fill="none" stroke="{color}" stroke-width="{width}"{dash} '
                 f'stroke-linecap="round" stroke-linejoin="round" marker-end="{self._marker(color)}"/>')
        if label:
            if lx is None:
                (x1, y1), (x2, y2) = pts[-2], pts[-1]
                lx, ly = (x1 + x2) / 2 + 10, (y1 + y2) / 2 + 4
            self.add(t(lx, ly, label, 12.5, self.th["bands"][tone][2], "600", anchor))

    def text(self, x, y, s, size=13, muted=True, weight="400", anchor="start"):
        self.add(t(x, y, s, size, self.th["muted"] if muted else self.th["fg"], weight, anchor))

    def render(self):
        defs = "".join(
            f'<marker id="{mid}" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" markerHeight="7" '
            f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>'
            for mid, c in self.markers.items())
        return (f'<?xml version="1.0" encoding="UTF-8"?>\n'
                f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}" '
                f'role="img" aria-label="{escape(self.label)}"><title>{escape(self.label)}</title>'
                f'<defs>{defs}</defs><rect width="{self.w}" height="{self.h}" rx="16" fill="{self.th["canvas"]}"/>'
                + "\n".join(self.parts) + "</svg>\n")
