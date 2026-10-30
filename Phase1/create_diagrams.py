import json
import math
from pathlib import Path
from html import escape

OUT = Path("results")
OUT.mkdir(exist_ok=True)

def svg_start(title, width=900, height=600):
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="{width/2}" y="35" font-family="Arial" font-size="22" font-weight="bold" text-anchor="middle">{escape(title)}</text>',
        '<text x="20" y="580" font-family="Arial" font-size="12" fill="#555">Development diagram — processor configuration pending organizer approval where applicable</text>'
    ]

def save_graph():
    data = json.loads(Path("results/o1_reproducible_graph.json").read_text(encoding="utf-8-sig"))
    nodes, edges = data["nodes"], data["edges"]
    width, height = 900, 600
    cx, cy, radius = 450, 300, 190
    positions = {
        n: (cx + radius * math.cos(2*math.pi*i/len(nodes)-math.pi/2),
            cy + radius * math.sin(2*math.pi*i/len(nodes)-math.pi/2))
        for i, n in enumerate(nodes)
    }
    s = svg_start("Weighted Max-Cut graph — non-official example", width, height)
    for e in edges:
        x1,y1 = positions[e["u"]]
        x2,y2 = positions[e["v"]]
        s.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#777" stroke-width="2"/>')
        mx,my=(x1+x2)/2,(y1+y2)/2
        s.append(f'<rect x="{mx-13}" y="{my-12}" width="26" height="22" rx="5" fill="white" stroke="#ddd"/>')
        s.append(f'<text x="{mx}" y="{my+4}" text-anchor="middle" font-family="Arial" font-size="14" font-weight="bold">{e["weight"]}</text>')
    for n,(x,y) in positions.items():
        s.append(f'<circle cx="{x}" cy="{y}" r="24" fill="#e8f1ff" stroke="#2459a9" stroke-width="2"/>')
        s.append(f'<text x="{x}" y="{y+6}" text-anchor="middle" font-family="Arial" font-size="17" font-weight="bold">{n}</text>')
    s.append("</svg>")
    Path(OUT/"weighted_maxcut_graph.svg").write_text("\n".join(s), encoding="utf-8")

def save_processor(filename, outname, title, n, layout):
    data = json.loads(Path(filename).read_text(encoding="utf-8-sig"))
    undirected = sorted({tuple(sorted(edge)) for edge in data["coupling_map"]})
    width, height = 900, 600
    s = svg_start(title, width, height)
    positions = layout
    for a,b in undirected:
        x1,y1=positions[a]; x2,y2=positions[b]
        s.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#777" stroke-width="3"/>')
    for q in range(n):
        x,y=positions[q]
        s.append(f'<circle cx="{x}" cy="{y}" r="22" fill="#e7f6e9" stroke="#287a3b" stroke-width="2"/>')
        s.append(f'<text x="{x}" y="{y+6}" text-anchor="middle" font-family="Arial" font-size="16" font-weight="bold">{q}</text>')
    s.append(f'<text x="450" y="75" text-anchor="middle" font-family="Arial" font-size="14" fill="#555">{n} qubits | {len(undirected)} unique undirected connections</text>')
    s.append("</svg>")
    Path(OUT/outname).write_text("\n".join(s), encoding="utf-8")

save_graph()

layout_a = {
    0:(180,300), 1:(360,300), 2:(540,180),
    3:(540,420), 4:(720,420)
}
save_processor("processors/processor_A.json", "processor_A_coupling.svg",
               "Processor A coupling map — PDF-derived, pending approval", 5, layout_a)

layout_b = {
    0:(130,150), 1:(300,150), 2:(470,150), 3:(640,150), 4:(780,280),
    5:(640,410), 6:(430,330), 7:(280,470), 8:(130,330)
}
save_processor("processors/processor_B.json", "processor_B_coupling.svg",
               "Processor B coupling map — PDF-derived, pending approval", 9, layout_b)

print("Created diagrams:")
for name in ["weighted_maxcut_graph.svg", "processor_A_coupling.svg", "processor_B_coupling.svg"]:
    p = OUT/name
    print(f"{p} — {p.stat().st_size} bytes")
