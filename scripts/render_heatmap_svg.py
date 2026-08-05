#!/usr/bin/env python3
import json
from datetime import datetime, timedelta

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
BOX_SIZE, BOX_GAP = 14, 3
WEEKS, DAYS = 53, 7
MARGIN_LEFT, MARGIN_TOP, MARGIN_RIGHT, MARGIN_BOTTOM = 30, 40, 30, 80
SVG_W = MARGIN_LEFT + WEEKS * (BOX_SIZE + BOX_GAP) + MARGIN_RIGHT
SVG_H = MARGIN_TOP + DAYS * (BOX_SIZE + BOX_GAP) + MARGIN_BOTTOM
BG, FG = "#0d1117", "#8b949e"

def main():
    with open("data/contributions.json") as f:
        data = json.load(f)

    days = data["days"]
    target = WEEKS * DAYS
    if len(days) > target:
        days = days[-target:]
    elif len(days) < target:
        first = datetime.strptime(days[0]["date"], "%Y-%m-%d").date()
        pad = target - len(days)
        padded = [{"date": (first - timedelta(days=pad-i)).isoformat(), "count": 0, "level": 0} for i in range(pad)]
        days = padded + days

    lines = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_W}" height="{SVG_H}" viewBox="0 0 {SVG_W} {SVG_H}" style="background:{BG}">']
    lines.append('<defs><style>.label{font-family:monospace;font-size:12px;fill:'+FG+';}.stat{font-family:monospace;font-size:13px;fill:'+FG+';}</style></defs>')

    month_names = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    last_m = -1
    for wi in range(WEEKS):
        di = wi * DAYS
        if di < len(days):
            d = datetime.strptime(days[di]["date"], "%Y-%m-%d").date()
            if d.month != last_m and d.day <= 7:
                x = MARGIN_LEFT + wi * (BOX_SIZE + BOX_GAP)
                lines.append(f'<text x="{x}" y="{MARGIN_TOP-10}" class="label">{month_names[d.month-1]}</text>')
                last_m = d.month

    for i, lbl in enumerate(["Mon","Wed","Fri"]):
        y = MARGIN_TOP + (i*2+1)*(BOX_SIZE+BOX_GAP)+10
        lines.append(f'<text x="5" y="{y}" class="label">{lbl}</text>')

    for wi in range(WEEKS):
        for dow in range(DAYS):
            idx = wi * DAYS + dow
            if idx >= len(days):
                continue
            d = days[idx]
            color = PALETTE[min(d["level"], len(PALETTE)-1)]
            x = MARGIN_LEFT + wi * (BOX_SIZE + BOX_GAP)
            y = MARGIN_TOP + dow * (BOX_SIZE + BOX_GAP)
            delay = (wi + dow) * 0.015
            lines.append(f'<rect x="{x}" y="{y}" width="{BOX_SIZE}" height="{BOX_SIZE}" rx="3" ry="3" fill="{color}"><animate attributeName="opacity" from="0" to="1" begin="{delay:.3f}s" dur="0.3s" fill="freeze" /><animateTransform attributeName="transform" type="translate" from="0 -8" to="0 0" begin="{delay:.3f}s" dur="0.3s" fill="freeze" additive="sum" /></rect>')

    ly = SVG_H - 50
    lx = MARGIN_LEFT
    lines.append(f'<text x="{lx}" y="{ly}" class="label">Less</text>')
    for i, c in enumerate(PALETTE):
        lines.append(f'<rect x="{lx+40+i*(BOX_SIZE+BOX_GAP)}" y="{ly-10}" width="{BOX_SIZE}" height="{BOX_SIZE}" rx="3" ry="3" fill="{c}" />')
    lines.append(f'<text x="{lx+40+len(PALETTE)*(BOX_SIZE+BOX_GAP)+5}" y="{ly}" class="label">More</text>')

    stats = f'{data["total"]:,} contributions in the last year · Current streak: {data["current_streak"]}d · Longest: {data["longest_streak"]}d'
    lines.append(f'<text x="{MARGIN_LEFT}" y="{SVG_H-20}" class="stat">{stats}</text>')
    lines.append('</svg>')

    with open("contrib-heatmap.svg", "w") as f:
        f.write("\n".join(lines))
    print("Saved contrib-heatmap.svg")

if __name__ == "__main__":
    main()
