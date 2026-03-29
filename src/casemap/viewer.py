from __future__ import annotations

import json


def render_knowledge_map(graph_payload: dict) -> str:
    data = json.dumps(graph_payload, ensure_ascii=False)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Casemap Knowledge Map</title>
  <style>
    :root {{
      --bg: #f4efe3;
      --panel: #fffaf0;
      --ink: #1c1d21;
      --muted: #6d6658;
      --line: rgba(28, 29, 33, 0.18);
      --section: #205072;
      --concept: #f4b942;
      --statute: #d95d39;
      --case: #5f7c4f;
      --accent: #7c2d12;
    }}

    * {{
      box-sizing: border-box;
    }}

    body {{
      margin: 0;
      font-family: "Georgia", "Times New Roman", serif;
      color: var(--ink);
      background:
        radial-gradient(circle at top left, rgba(244, 185, 66, 0.22), transparent 32%),
        radial-gradient(circle at top right, rgba(32, 80, 114, 0.18), transparent 28%),
        linear-gradient(180deg, #f7f1e5 0%, var(--bg) 100%);
      min-height: 100vh;
    }}

    .shell {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) 360px;
      min-height: 100vh;
    }}

    .canvas-panel {{
      padding: 28px;
    }}

    .header {{
      display: flex;
      justify-content: space-between;
      gap: 16px;
      align-items: end;
      margin-bottom: 18px;
    }}

    h1 {{
      margin: 0;
      font-size: clamp(30px, 4vw, 44px);
      line-height: 0.95;
      letter-spacing: -0.03em;
    }}

    .subtitle {{
      max-width: 720px;
      color: var(--muted);
      font-size: 15px;
      line-height: 1.5;
    }}

    .search {{
      display: grid;
      gap: 8px;
      align-self: start;
    }}

    .search input {{
      width: min(320px, 100%);
      padding: 12px 14px;
      border: 1px solid rgba(28, 29, 33, 0.2);
      border-radius: 999px;
      background: rgba(255, 250, 240, 0.9);
      color: var(--ink);
      font-size: 14px;
    }}

    .legend {{
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
      color: var(--muted);
      font-size: 12px;
    }}

    .legend span {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }}

    .swatch {{
      width: 11px;
      height: 11px;
      border-radius: 999px;
      display: inline-block;
    }}

    .board {{
      background: rgba(255, 250, 240, 0.82);
      border: 1px solid rgba(28, 29, 33, 0.1);
      border-radius: 24px;
      box-shadow: 0 26px 80px rgba(28, 29, 33, 0.08);
      overflow: hidden;
      min-height: calc(100vh - 120px);
    }}

    svg {{
      width: 100%;
      height: calc(100vh - 120px);
      display: block;
    }}

    .side-panel {{
      border-left: 1px solid rgba(28, 29, 33, 0.08);
      background: linear-gradient(180deg, rgba(255, 250, 240, 0.92), rgba(244, 239, 227, 0.98));
      padding: 24px 22px;
      overflow-y: auto;
    }}

    .meta {{
      color: var(--muted);
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.12em;
      margin-bottom: 10px;
    }}

    .node-title {{
      margin: 0 0 10px;
      font-size: 28px;
      line-height: 1.05;
    }}

    .node-type {{
      display: inline-block;
      margin-bottom: 16px;
      padding: 6px 10px;
      border-radius: 999px;
      font-size: 12px;
      background: rgba(28, 29, 33, 0.06);
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }}

    .node-copy {{
      margin: 0 0 18px;
      color: var(--ink);
      line-height: 1.6;
    }}

    .list-block {{
      margin: 0 0 20px;
      padding: 0;
      list-style: none;
      display: grid;
      gap: 8px;
    }}

    .list-block li {{
      padding: 10px 12px;
      border: 1px solid rgba(28, 29, 33, 0.08);
      border-radius: 14px;
      background: rgba(255, 255, 255, 0.5);
      font-size: 14px;
      line-height: 1.45;
    }}

    .empty {{
      color: var(--muted);
      font-style: italic;
    }}

    .node {{
      cursor: pointer;
      transition: opacity 120ms ease;
    }}

    .node-label {{
      font-size: 11px;
      fill: var(--ink);
      pointer-events: none;
    }}

    .edge {{
      stroke: rgba(28, 29, 33, 0.14);
      stroke-width: 1.2;
    }}

    .faded {{
      opacity: 0.13;
    }}

    .active-node circle {{
      stroke: var(--accent);
      stroke-width: 4;
    }}

    .active-edge {{
      stroke: rgba(124, 45, 18, 0.72);
      stroke-width: 2.4;
    }}

    @media (max-width: 1024px) {{
      .shell {{
        grid-template-columns: 1fr;
      }}

      .side-panel {{
        border-left: 0;
        border-top: 1px solid rgba(28, 29, 33, 0.08);
      }}

      svg {{
        height: 70vh;
      }}
    }}
  </style>
</head>
<body>
  <div class="shell">
    <section class="canvas-panel">
      <div class="header">
        <div>
          <div class="meta">Casemap MVP GraphRAG</div>
          <h1>Contract Big Knowledge Map</h1>
          <p class="subtitle">Sections, concepts, statutes, and cases are clustered into a legal knowledge map. Select a node to inspect the summary, cited authorities, and graph neighbors.</p>
          <div class="legend">
            <span><i class="swatch" style="background: var(--section)"></i>Section</span>
            <span><i class="swatch" style="background: var(--concept)"></i>Concept</span>
            <span><i class="swatch" style="background: var(--statute)"></i>Statute</span>
            <span><i class="swatch" style="background: var(--case)"></i>Case</span>
          </div>
        </div>
        <label class="search">
          <span class="meta">Find a node</span>
          <input id="searchInput" type="search" placeholder="Search concepts, statutes, cases">
        </label>
      </div>
      <div class="board">
        <svg id="graph" viewBox="0 0 1280 920" preserveAspectRatio="xMidYMid meet"></svg>
      </div>
    </section>
    <aside class="side-panel">
      <div class="meta">Selection</div>
      <h2 class="node-title" id="nodeTitle">Overview</h2>
      <div class="node-type" id="nodeType">Graph</div>
      <p class="node-copy" id="nodeSummary">The graph groups the contract outline into numbered sections, concept nodes, and cited legal authorities. Search or click on a node to inspect its local neighborhood.</p>
      <div class="meta">Citations</div>
      <ul class="list-block" id="citationList"><li class="empty">No node selected.</li></ul>
      <div class="meta">Neighbors</div>
      <ul class="list-block" id="neighborList"><li class="empty">No node selected.</li></ul>
    </aside>
  </div>
  <script>
    const payload = {data};
    const nodes = payload.nodes.map((node) => ({{ ...node }}));
    const edges = payload.edges.map((edge, index) => ({{ ...edge, id: `edge-${{index}}` }}));
    const svg = document.getElementById("graph");
    const titleEl = document.getElementById("nodeTitle");
    const typeEl = document.getElementById("nodeType");
    const summaryEl = document.getElementById("nodeSummary");
    const citationList = document.getElementById("citationList");
    const neighborList = document.getElementById("neighborList");
    const searchInput = document.getElementById("searchInput");

    const colors = {{
      section: getComputedStyle(document.documentElement).getPropertyValue("--section").trim(),
      concept: getComputedStyle(document.documentElement).getPropertyValue("--concept").trim(),
      statute: getComputedStyle(document.documentElement).getPropertyValue("--statute").trim(),
      case: getComputedStyle(document.documentElement).getPropertyValue("--case").trim(),
    }};

    const index = new Map(nodes.map((node) => [node.id, node]));
    const neighbors = new Map(nodes.map((node) => [node.id, new Set()]));
    edges.forEach((edge) => {{
      neighbors.get(edge.source)?.add(edge.target);
      neighbors.get(edge.target)?.add(edge.source);
    }});

    function radiusFor(node) {{
      if (node.type === "section") return 18;
      if (node.type === "concept") return 10;
      return 9;
    }}

    function layout() {{
      const width = 1280;
      const height = 920;
      const centerX = width / 2;
      const centerY = height / 2;
      const sections = nodes.filter((node) => node.type === "section");
      const concepts = nodes.filter((node) => node.type === "concept");
      const authorities = nodes.filter((node) => node.type !== "section" && node.type !== "concept");

      sections.forEach((section, idx) => {{
        const angle = (Math.PI * 2 * idx) / Math.max(sections.length, 1) - Math.PI / 2;
        section.x = centerX + Math.cos(angle) * 240;
        section.y = centerY + Math.sin(angle) * 220;
      }});

      const groupedConcepts = new Map();
      concepts.forEach((concept) => {{
        const bucket = groupedConcepts.get(concept.section_id) || [];
        bucket.push(concept);
        groupedConcepts.set(concept.section_id, bucket);
      }});

      groupedConcepts.forEach((group, sectionId) => {{
        const parent = index.get(sectionId);
        if (!parent) return;
        group.forEach((concept, idx) => {{
          const angle = (Math.PI * 2 * idx) / Math.max(group.length, 1);
          const distance = 74 + (idx % 3) * 18;
          concept.x = parent.x + Math.cos(angle) * distance;
          concept.y = parent.y + Math.sin(angle) * distance;
        }});
      }});

      authorities.forEach((authority, idx) => {{
        const angle = (Math.PI * 2 * idx) / Math.max(authorities.length, 1) - Math.PI / 2;
        const ring = authority.type === "statute" ? 380 : 430;
        authority.x = centerX + Math.cos(angle) * ring;
        authority.y = centerY + Math.sin(angle) * (ring * 0.72);
      }});
    }}

    layout();

    const edgeLayer = document.createElementNS("http://www.w3.org/2000/svg", "g");
    const nodeLayer = document.createElementNS("http://www.w3.org/2000/svg", "g");
    svg.append(edgeLayer, nodeLayer);

    const edgeEls = new Map();
    edges.forEach((edge) => {{
      const source = index.get(edge.source);
      const target = index.get(edge.target);
      if (!source || !target) return;
      const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
      line.setAttribute("class", "edge");
      line.setAttribute("x1", source.x);
      line.setAttribute("y1", source.y);
      line.setAttribute("x2", target.x);
      line.setAttribute("y2", target.y);
      edgeLayer.appendChild(line);
      edgeEls.set(edge.id, line);
    }});

    const nodeEls = new Map();
    nodes.forEach((node) => {{
      const group = document.createElementNS("http://www.w3.org/2000/svg", "g");
      group.setAttribute("class", "node");
      group.dataset.id = node.id;

      const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
      circle.setAttribute("cx", node.x);
      circle.setAttribute("cy", node.y);
      circle.setAttribute("r", radiusFor(node));
      circle.setAttribute("fill", colors[node.type] || colors.concept);
      circle.setAttribute("fill-opacity", node.type === "section" ? "0.96" : "0.9");

      const label = document.createElementNS("http://www.w3.org/2000/svg", "text");
      label.setAttribute("class", "node-label");
      label.setAttribute("x", node.x + radiusFor(node) + 6);
      label.setAttribute("y", node.y + 4);
      label.textContent = node.label;

      group.append(circle, label);
      group.addEventListener("click", () => selectNode(node.id));
      nodeLayer.appendChild(group);
      nodeEls.set(node.id, group);
    }});

    function renderList(element, values) {{
      element.innerHTML = "";
      if (!values.length) {{
        const item = document.createElement("li");
        item.className = "empty";
        item.textContent = "None";
        element.appendChild(item);
        return;
      }}
      values.forEach((value) => {{
        const item = document.createElement("li");
        item.textContent = value;
        element.appendChild(item);
      }});
    }}

    function selectNode(nodeId) {{
      const node = index.get(nodeId);
      if (!node) return;
      const localNeighbors = [...(neighbors.get(nodeId) || [])].map((id) => index.get(id)).filter(Boolean);
      titleEl.textContent = node.label;
      typeEl.textContent = node.type;
      summaryEl.textContent = node.summary || "No summary available.";
      renderList(citationList, node.citations || []);
      renderList(
        neighborList,
        localNeighbors
          .sort((left, right) => left.label.localeCompare(right.label))
          .map((item) => `${{item.label}} (${{item.type}})`)
      );

      nodeEls.forEach((element, id) => {{
        const isNeighbor = id === nodeId || (neighbors.get(nodeId)?.has(id));
        element.classList.toggle("faded", !isNeighbor);
        element.classList.toggle("active-node", id === nodeId);
      }});

      edges.forEach((edge) => {{
        const active = edge.source === nodeId || edge.target === nodeId;
        const edgeEl = edgeEls.get(edge.id);
        if (!edgeEl) return;
        edgeEl.classList.toggle("faded", !active);
        edgeEl.classList.toggle("active-edge", active);
      }});
    }}

    function clearSelection() {{
      titleEl.textContent = "Overview";
      typeEl.textContent = "Graph";
      summaryEl.textContent = "The graph groups the contract outline into numbered sections, concept nodes, and cited legal authorities. Search or click on a node to inspect its local neighborhood.";
      citationList.innerHTML = '<li class="empty">No node selected.</li>';
      neighborList.innerHTML = '<li class="empty">No node selected.</li>';
      nodeEls.forEach((element) => {{
        element.classList.remove("faded", "active-node");
      }});
      edgeEls.forEach((element) => {{
        element.classList.remove("faded", "active-edge");
      }});
    }}

    function searchNode(value) {{
      const query = value.trim().toLowerCase();
      if (!query) {{
        clearSelection();
        return;
      }}
      const match = nodes.find((node) => {{
        const haystack = `${{node.label}} ${{node.summary || ""}} ${{(node.citations || []).join(" ")}}`.toLowerCase();
        return haystack.includes(query);
      }});
      if (match) {{
        selectNode(match.id);
      }}
    }}

    searchInput.addEventListener("input", (event) => searchNode(event.target.value));
    clearSelection();
  </script>
</body>
</html>
"""
