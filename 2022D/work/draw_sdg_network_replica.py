from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Inches, Pt


OUT_DIR = Path(__file__).resolve().parent / "sdg_network_replica"
OUT_DIR.mkdir(parents=True, exist_ok=True)


SDGS = {
    1: ("No Poverty", "#e5243b", "people"),
    2: ("Zero Hunger", "#dda63a", "bowl"),
    3: ("Good Health and Well-being", "#4c9f38", "health"),
    4: ("Quality Education", "#c5192d", "book"),
    5: ("Gender Equity", "#ff3a21", "gender"),
    6: ("Clean Water and Sanitation", "#26bde2", "water"),
    7: ("Affordable and Clean Energy", "#fcc30b", "sun"),
    8: ("Decent Work and Economic Growth", "#a21942", "chart"),
    9: ("Industry,Innovation and Infrastructure", "#fd6925", "blocks"),
    10: ("Reduced Inequality", "#dd1367", "eq"),
    11: ("Sustainable Cities and Production", "#fd9d24", "city"),
    12: ("Responsible Consumption and Production", "#bf8b2e", "loop"),
    13: ("Climate Action", "#3f7e44", "earth"),
    14: ("Life below Water", "#0a97d9", "fish"),
    15: ("Life on Land", "#56c02b", "tree"),
    16: ("Peace and Justice Strong Institutions", "#00689d", "peace"),
    17: ("Partnerships to achieve the Goal", "#19486f", "network"),
}


# Hand-tuned layout to mimic the paper screenshot. Coordinates are in [0, 1].
POS = {
    17: (0.52, 0.52),
    3: (0.54, 0.77),
    16: (0.78, 0.72),
    5: (0.86, 0.60),
    10: (0.86, 0.42),
    8: (0.76, 0.28),
    1: (0.56, 0.18),
    4: (0.63, 0.36),
    2: (0.72, 0.55),
    9: (0.43, 0.10),
    11: (0.42, 0.30),
    12: (0.31, 0.24),
    7: (0.20, 0.36),
    6: (0.34, 0.50),
    13: (0.28, 0.68),
    14: (0.17, 0.62),
    15: (0.38, 0.76),
}

NODE_R = {
    17: 0.066,
    6: 0.055,
    3: 0.061,
    1: 0.057,
    4: 0.053,
    2: 0.049,
    8: 0.043,
    5: 0.046,
    13: 0.046,
    12: 0.038,
    7: 0.040,
    11: 0.039,
    9: 0.036,
    10: 0.034,
    14: 0.030,
    15: 0.030,
    16: 0.036,
}


def edge_weight(i: int, j: int) -> float:
    """Deterministic pseudo-weight for visual replication when no model matrix exists."""
    base = ((i * 37 + j * 19 + i * j * 7) % 100) / 100
    return 0.25 + 0.75 * base


def all_edges() -> list[tuple[int, int, float, bool]]:
    edges: list[tuple[int, int, float, bool]] = []
    for i in range(1, 18):
        for j in range(i + 1, 18):
            w = edge_weight(i, j)
            highlighted = i == 17 or j == 17
            edges.append((i, j, w, highlighted))
    return edges


def label_for(n: int) -> str:
    return f"SDG{n}: {SDGS[n][0]}"


def draw_matplotlib(path_base: Path) -> None:
    fig, ax = plt.subplots(figsize=(12.5, 7.6))
    ax.set_xlim(0.02, 0.98)
    ax.set_ylim(-0.08, 0.90)
    ax.set_aspect("equal")
    ax.axis("off")

    for i, j, w, highlighted in all_edges():
        x1, y1 = POS[i]
        x2, y2 = POS[j]
        if highlighted:
            color = "#1f3f78"
            alpha = 0.34 + 0.25 * w
            lw = 1.8 + 4.6 * w
        else:
            color = "#c9d9df"
            alpha = 0.22 + 0.22 * w
            lw = 1.2 + 3.4 * w
        ax.plot([x1, x2], [y1, y2], color=color, alpha=alpha, lw=lw, solid_capstyle="round", zorder=1)

    for n, (x, y) in POS.items():
        radius = NODE_R[n]
        ax.add_patch(Circle((x, y), radius, facecolor=SDGS[n][1], edgecolor="white", linewidth=2.2, zorder=3))
        ax.text(x, y + radius * 0.12, str(n), color="white", ha="center", va="center",
                fontsize=21 if n == 17 else 14.5, fontweight="bold", zorder=4)
        ax.text(x, y - radius * 0.42, SDGS[n][2], color="white", ha="center", va="center",
                fontsize=5.7 if n != 17 else 6.4, fontweight="bold", zorder=4)

    label_offsets = {
        17: (0, -0.075), 3: (0, -0.075), 16: (0, -0.062), 5: (0, -0.065),
        10: (0.015, -0.047), 8: (0, -0.055), 1: (0, -0.065), 4: (0, -0.060),
        2: (0, -0.056), 9: (0, -0.055), 11: (0, -0.052), 12: (0, -0.052),
        7: (0, -0.052), 6: (0, -0.062), 13: (0, -0.057), 14: (0, -0.042),
        15: (0, -0.042),
    }
    for n, (x, y) in POS.items():
        dx, dy = label_offsets[n]
        ax.text(x + dx, y + dy, label_for(n), color="#333333", ha="center", va="top",
                fontsize=5.6 if n != 17 else 6.0, fontweight="bold", zorder=5)

    fig.text(0.5, 0.055, "Figure 7: SDG Network (with Edge of SDG 17 Highlighted)",
             ha="center", va="center", fontsize=15.5, fontfamily="serif")
    fig.subplots_adjust(left=0.02, right=0.98, top=0.97, bottom=0.12)
    fig.savefig(path_base.with_suffix(".png"), dpi=300)
    fig.savefig(path_base.with_suffix(".pdf"))
    plt.close(fig)


def svg_text(x: float, y: float, text: str, size: int, color: str, weight: str = "normal",
             anchor: str = "middle") -> str:
    text = text.replace("&", "&amp;")
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" '
        f'font-family="Arial, Helvetica, sans-serif" font-size="{size}" '
        f'font-weight="{weight}" fill="{color}">{text}</text>'
    )


def write_svg(path: Path) -> None:
    width, height = 1400, 900
    margin_x, margin_y = 80, 80

    def sx(x: float) -> float:
        return margin_x + x * (width - 2 * margin_x)

    def sy(y: float) -> float:
        return margin_y + (0.88 - y) / 0.86 * (height - 2 * margin_y - 90)

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<g id="edges">',
    ]
    for i, j, w, highlighted in all_edges():
        x1, y1 = sx(POS[i][0]), sy(POS[i][1])
        x2, y2 = sx(POS[j][0]), sy(POS[j][1])
        color = "#1f3f78" if highlighted else "#c9d9df"
        opacity = 0.34 + 0.25 * w if highlighted else 0.22 + 0.22 * w
        lw = 2.5 + 8.5 * w if highlighted else 1.8 + 5.6 * w
        lines.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{color}" stroke-opacity="{opacity:.3f}" stroke-width="{lw:.2f}" stroke-linecap="round"/>'
        )
    lines.append("</g>")

    lines.append('<g id="nodes">')
    for n, (x, y) in POS.items():
        cx, cy = sx(x), sy(y)
        r = NODE_R[n] * 720
        lines.append(f'<g id="SDG{n}">')
        lines.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{SDGS[n][1]}" stroke="white" stroke-width="4"/>')
        lines.append(svg_text(cx, cy + r * 0.12, str(n), 30 if n == 17 else 22, "white", "700"))
        lines.append(svg_text(cx, cy + r * 0.52, SDGS[n][2], 10 if n != 17 else 11, "white", "700"))
        lines.append("</g>")
    lines.append("</g>")

    label_offsets = {
        17: (0, 58), 3: (0, 62), 16: (0, 54), 5: (0, 58), 10: (20, 44),
        8: (0, 50), 1: (0, 58), 4: (0, 54), 2: (0, 52), 9: (0, 48),
        11: (0, 48), 12: (0, 48), 7: (0, 48), 6: (0, 56), 13: (0, 54),
        14: (0, 40), 15: (0, 40),
    }
    lines.append('<g id="labels">')
    for n, (x, y) in POS.items():
        cx, cy = sx(x), sy(y)
        dx, dy = label_offsets[n]
        lines.append(svg_text(cx + dx, cy + dy, label_for(n), 12 if n != 17 else 13, "#333333", "700"))
    lines.append("</g>")
    lines.append(svg_text(width / 2, height - 35, "Figure 7: SDG Network (with Edge of SDG 17 Highlighted)", 28, "#111111", "normal"))
    lines.append("</svg>")
    path.write_text("\n".join(lines), encoding="utf-8")


def add_ppt_text(slide, x, y, w, h, text, size, color, bold=False):
    box = slide.shapes.add_textbox(x, y, w, h)
    tf = box.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = RGBColor(*color)
    p.alignment = 1
    return box


def write_pptx(path: Path) -> None:
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    def sx(x: float) -> float:
        return Inches(0.75 + x * 11.9)

    def sy(y: float) -> float:
        return Inches(0.42 + (0.88 - y) / 0.86 * 5.55)

    def rgb(hex_color: str) -> RGBColor:
        h = hex_color.lstrip("#")
        return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

    for i, j, w, highlighted in all_edges():
        line = slide.shapes.add_connector(1, sx(POS[i][0]), sy(POS[i][1]), sx(POS[j][0]), sy(POS[j][1]))
        line.line.color.rgb = rgb("#1f3f78" if highlighted else "#c9d9df")
        line.line.width = Pt(1.5 + 5.0 * w if highlighted else 1.0 + 3.0 * w)
        line.line.transparency = 45 if highlighted else 62

    for n, (x, y) in POS.items():
        r = NODE_R[n] * 4.7
        left = sx(x) - Inches(r / 2)
        top = sy(y) - Inches(r / 2)
        diameter = Inches(r)
        node = slide.shapes.add_shape(MSO_SHAPE.OVAL, left, top, diameter, diameter)
        node.fill.solid()
        node.fill.fore_color.rgb = rgb(SDGS[n][1])
        node.line.color.rgb = RGBColor(255, 255, 255)
        node.line.width = Pt(1.5)

        add_ppt_text(slide, left, top + diameter * 0.23, diameter, diameter * 0.34,
                     str(n), 20 if n == 17 else 15, (255, 255, 255), True)
        add_ppt_text(slide, left, top + diameter * 0.54, diameter, diameter * 0.22,
                     SDGS[n][2], 5.5 if n != 17 else 6.0, (255, 255, 255), True)

    for n, (x, y) in POS.items():
        text_w = Inches(2.15)
        add_ppt_text(slide, sx(x) - text_w / 2, sy(y) + Inches(NODE_R[n] * 2.5), text_w, Inches(0.25),
                     label_for(n), 6.8 if n != 17 else 7.1, (45, 45, 45), True)

    add_ppt_text(slide, Inches(2.4), Inches(6.93), Inches(8.6), Inches(0.38),
                 "Figure 7: SDG Network (with Edge of SDG 17 Highlighted)", 18, (20, 20, 20), False)
    prs.save(path)


def write_evidence(path: Path) -> None:
    rows = [{
        "figure_id": "fig_sdg_network_replica",
        "problem_id": "ICM2022D",
        "claim_id": "mechanism_sdg_interdependency",
        "paper_role": "mechanism",
        "figure_path": str((OUT_DIR / "sdg_network_replica.svg").resolve()),
        "figure_type": "network diagram",
        "plot_family": "network",
        "plot_type": "weighted node-link graph",
        "why_this_plot": "Replicates the SDG interdependency mechanism and highlights SDG17 connections.",
        "scenario": "demonstration layout; replace edge weights with model matrix for final paper use",
        "metric": "edge weight",
        "unit": "dimensionless",
        "source_table": "synthetic deterministic weights in script",
        "source_script": str(Path(__file__).resolve()),
        "run_id": "local_replicate_001",
        "baseline_or_threshold": "SDG17 edges highlighted",
        "uncertainty_or_error": "not applicable",
        "constraint_status": "visual replica, not final computed result",
        "caption": "SDG network under illustrative interdependency weights: thicker and darker links highlight SDG17 partnerships.",
        "post_figure_conclusion": "Figure 7 decomposes SDG interdependency into a weighted network and emphasizes SDG17 as the partnership hub.",
        "validation_status": "generated",
        "risk_note": "Current weights are illustrative; paper-ready use requires replacing them with the model-derived matrix.",
        "data_source": "replica from supplied screenshot",
        "notes": "SVG and PPTX are editable; PNG/PDF are export versions.",
    }]
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    base = OUT_DIR / "sdg_network_replica"
    draw_matplotlib(base)
    write_svg(base.with_suffix(".svg"))
    write_pptx(base.with_suffix(".pptx"))
    write_evidence(OUT_DIR / "figure_evidence.csv")
    print(f"Generated files in: {OUT_DIR}")
    for p in sorted(OUT_DIR.iterdir()):
        print(p.name)


if __name__ == "__main__":
    main()
