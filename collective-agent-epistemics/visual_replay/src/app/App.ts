import { sampleReplay } from "../data/sampleReplay";

interface WorldCard {
  id: string;
  tag: string;
  note: string;
}

const GENERALIZATION: WorldCard[] = [
  { id: "G01", tag: "A/B", note: "Misleading trajectory varies" },
  { id: "G02", tag: "B/B", note: "Aligned same recorded P(A)" },
  { id: "G03", tag: "A/B", note: "Misleading same recorded P(A)" },
  { id: "G04", tag: "B/B", note: "Aligned trajectory varies" },
  { id: "G05", tag: "B/B", note: "Aligned trajectory varies" },
  { id: "G06", tag: "B/A", note: "Misleading same recorded P(A)" },
  { id: "G07", tag: "A/A", note: "Aligned same recorded P(A)" },
  { id: "G08", tag: "B/A", note: "Misleading same recorded P(A)" },
  { id: "G09", tag: "A/A", note: "Aligned trajectory varies" },
  { id: "G10", tag: "B/A", note: "Misleading trajectory varies" },
  { id: "G11", tag: "B/A", note: "Misleading trajectory varies" },
  { id: "G12", tag: "A/B", note: "Misleading same recorded P(A)" }
];

const STRESS: WorldCard[] = [
  { id: "S01", tag: "B/B", note: "Aligned trajectory varies" },
  { id: "S02", tag: "B/B", note: "Aligned trajectory varies" },
  { id: "S03", tag: "B/A", note: "Misleading same recorded P(A)" },
  { id: "S04", tag: "A/B", note: "Misleading same recorded P(A)" },
  { id: "S05", tag: "B/A", note: "Misleading trajectory varies" },
  { id: "S06", tag: "A/A", note: "Aligned trajectory varies" },
  { id: "S07", tag: "A/A", note: "Aligned same recorded P(A)" },
  { id: "S08", tag: "A/B", note: "Misleading same recorded P(A)" }
];

const condCopy: Record<string, string> = {
  free: "Natural-language handoff without visible structured lineage.",
  lineage: "Lineage labels are carried with message transmission metadata.",
  macro: "MACRO can stop when a full cycle adds no independent evidence."
};

const stageLabel = [
  "01 / Origin",
  "02 / W01 x 15",
  "03 / Hive x 20",
  "04 / Replay"
];

const trajectoryRows = `
  <tr><td>M06</td><td>Agent C</td><td>0.30</td><td>0.37</td></tr>
  <tr><td>M08</td><td>Agent B</td><td>0.30</td><td>0.32</td></tr>
  <tr><td>M11</td><td>Agent B</td><td>0.30</td><td>0.38</td></tr>
  <tr><td>M12</td><td>Agent C</td><td>0.30</td><td>0.44</td></tr>
`;

const navTemplate = (active: number): string => `
  <header class="eh-top">
    <div class="eh-brand"><span class="hex">⬡</span><span>Epistemic <strong>Hive</strong></span></div>
    <nav class="eh-progress" aria-label="Stage navigation">
      ${stageLabel
        .map(
          (label, idx) => `<button class="eh-step ${active === idx ? "active" : ""}" data-action="go-stage" data-stage="${idx}">${label}</button>`
        )
        .join("")}
    </nav>
    <p class="eh-version">EXP-002 · v0.1</p>
  </header>
`;

const worldCardTemplate = (w: WorldCard): string => `
  <button class="world-card" data-action="open-world" data-world="${w.id}">
    <span class="world-hex">${w.id}</span>
    <span class="world-tag">${w.tag}</span>
    <span class="world-note">${w.note}</span>
  </button>
`;

const renderOrigin = (): string => `
  <section class="screen split-screen">
    <article class="copy-panel">
      <p class="kicker">01 / The source</p>
      <h1>One root.<br/><span>Before the network.</span></h1>
      <p class="lede">A single external observation, E1, exists before any agent speaks. It is the independent evidence basis for this world.</p>
      <p class="micro">Agent state  ·  transmitted message  ·  network evidence</p>
      <div class="chip-row"><span class="chip active">Empirical replay</span><span class="chip">Simulation off</span></div>
      <button class="hero-btn" data-action="go-stage" data-stage="3">Reveal agent A</button>
      <footer class="panel-foot">Roots 01 · Depth 00</footer>
    </article>
    <article class="viz-panel">
      <p class="viz-label">Evidence basis · one independent root</p>
      <div class="node-space root-only">
        <div class="n n-root"><span>E1</span></div>
      </div>
    </article>
  </section>
`;

const renderW01 = (): string => `
  <section class="screen">
    <article class="title-block">
      <p class="kicker">02 / Gate 2A · same-world stochastic replication</p>
      <h1>One world.<br/><span>Fifteen times.</span></h1>
      <p class="lede">Same E1, truth, topology, model, protocol and seed. Fifteen formal runs of W01, not fifteen different worlds.</p>
    </article>
    <div class="w01-grid-wrap">
      <div class="w01-grid">
        ${Array.from({ length: 15 }, (_, i) => `<div class="rep-card"><span class="world-hex">W01</span><small>REP ${String(i + 1).padStart(2, "0")}</small></div>`).join("")}
      </div>
      <aside class="archive-box">
        <p class="archive-kicker">What the archive records</p>
        <h2>12<span>/15</span></h2>
        <p>LINEAGE runs with transient numerical confidence discounting</p>
        <ul>
          <li>FREE numerical drift <strong>8/15</strong></li>
          <li>Confidence inflation events <strong>0</strong></li>
          <li>Answer flips <strong>0</strong></li>
          <li>MACRO stopped after one cycle <strong>15/15</strong></li>
        </ul>
      </aside>
    </div>
    <div class="bridge">
      <p class="kicker">One context world</p>
      <h3>Does this behavior survive when the world changes?</h3>
      <button class="hero-btn" data-action="go-stage" data-stage="2">Expand to 20 worlds</button>
    </div>
  </section>
`;

const renderHive = (): string => `
  <section class="screen">
    <article class="title-block compact">
      <p class="kicker">03 / Gate 2B · frozen v0.1 protocol</p>
      <h1>A hive of<br/><span>different worlds.</span></h1>
      <p class="lede">Each hexagon is a distinct truth and observation realization. Select one to inspect its archived messages.</p>
    </article>
    <section class="world-set">
      <header><h2>Generalization <small>12 / 12</small></h2><p>Unfiltered evidence realizations</p></header>
      <div class="world-grid">${GENERALIZATION.map(worldCardTemplate).join("")}</div>
    </section>
    <section class="world-set">
      <header><h2>Stress <small>8 / 8</small></h2><p>Two worlds per truth / observation cell</p></header>
      <div class="world-grid">${STRESS.map(worldCardTemplate).join("")}</div>
    </section>
    <p class="obs-banner"><strong>Observed across sets:</strong> one root persists while inference depth grows. Trajectories sometimes differ; a uniform final architectural advantage was not established.</p>
  </section>
`;

const timelineTicks = () =>
  sampleReplay.timeline
    .map((point, idx) => `<button class="dot ${idx === 0 ? "active" : ""}" data-action="step" data-step="${idx}">M${String(point.step + 1).padStart(2, "0")}</button>`)
    .join("");

const renderReplay = (world: string, condition: string): string => `
  <section class="screen replay-screen">
    <article class="replay-head">
      <div>
        <p class="kicker">04 / Archived world replay · Generalization / ${world}</p>
        <h1>Inside world <span>${world}</span></h1>
        <p class="micro">Truth A · Observed E1 B · Misleading · Seed 874625177</p>
      </div>
      <div class="chip-row"><span class="chip active">Empirical replay</span><span class="chip">Simulation off</span></div>
    </article>

    <div class="condition-row">
      <button class="cond ${condition === "free" ? "active" : ""}" data-action="cond" data-cond="free">Free</button>
      <button class="cond ${condition === "lineage" ? "active" : ""}" data-action="cond" data-cond="lineage">Lineage</button>
      <button class="cond ${condition === "macro" ? "active" : ""}" data-action="cond" data-cond="macro">Macro</button>
      <p>${condCopy[condition]}</p>
    </div>

    <div class="replay-grid">
      <section class="card network-card">
        <p class="micro">Network / E1 · A · B · C</p>
        <div class="node-space">
          <div class="n n-a"><span>A</span></div>
          <div class="n n-b"><span>B</span></div>
          <div class="n n-c"><span>C</span></div>
          <div class="n n-root"><span>E1</span></div>
          <svg viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">
            <line x1="50" y1="54" x2="50" y2="23" />
            <line x1="50" y1="54" x2="22" y2="66" />
            <line x1="50" y1="54" x2="78" y2="66" />
          </svg>
        </div>
        <footer class="panel-foot">Roots 01 · Depth 00</footer>
      </section>

      <section class="card event-card">
        <h3>Event state / <span id="event-id">M01</span></h3>
        <div class="kv"><span>Reported answer</span><strong>B</strong></div>
        <div class="grid2"><div><span>Confidence</span><strong id="event-confidence">0.70</strong></div><div><span>P(A)</span><strong id="event-p">0.30</strong></div></div>
        <div class="grid2"><div><span>Brier</span><strong>0.4900</strong></div><div><span>Accuracy</span><strong>0</strong></div></div>
        <div class="grid2"><div><span>Inference depth</span><strong id="event-depth">0</strong></div><div><span>Independent roots</span><strong>1</strong></div></div>
      </section>

      <section class="card message-card">
        <h3>Transmitted message / A → B</h3>
        <p>Sensor 1 directly observed B with reported reliability 0.70; no other evidence was provided.</p>
        <small>Cycle 0 · recorded response reused</small>
      </section>

      <section class="card observation-card">
        <h3>World-level observation</h3>
        <strong>Trajectories differ</strong>
        <p>FREE and LINEAGE share final primary values in this world. Trajectory difference marks an observation, not an identified failure mechanism.</p>
      </section>

      <section class="card timeline-card">
        <h3>Empirical event timeline</h3>
        <p><strong id="event-id-secondary">M01</strong> / M13</p>
        <div class="dots">${timelineTicks()}</div>
      </section>

      <section class="card chart-card">
        <h3>Recorded trajectories</h3>
        <p>P(A) across messages</p>
        <svg viewBox="0 0 100 30" preserveAspectRatio="none" class="traj">
          <path d="M0 14 L11 14 L22 14 L33 14 L44 14 L55 14 L66 14 L77 14 L88 14 L100 14" class="line-free"/>
          <path d="M0 14 L11 14 L22 14 L33 14 L44 14 L55 13 L66 13 L77 13 L88 12 L100 11" class="line-lineage"/>
        </svg>
      </section>

      <section class="card table-card">
        <h3>Where to inspect / FREE ↔ LINEAGE</h3>
        <p>Agent-level trajectory differences</p>
        <table>
          <thead><tr><th>Event</th><th>Sender</th><th>P(A) free</th><th>P(A) lineage</th></tr></thead>
          <tbody>${trajectoryRows}</tbody>
        </table>
      </section>
    </div>
  </section>
`;

interface AppState {
  stage: number;
  world: string;
  condition: "free" | "lineage" | "macro";
  step: number;
}

const initialState: AppState = {
  stage: 0,
  world: "G01",
  condition: "free",
  step: 0
};

const render = (state: AppState): string => {
  const screen =
    state.stage === 0
      ? renderOrigin()
      : state.stage === 1
        ? renderW01()
        : state.stage === 2
          ? renderHive()
          : renderReplay(state.world, state.condition);

  return `<div class="eh-shell">${navTemplate(state.stage)}${screen}<footer class="eh-foot">Collective Agent Epistemics / Observer layer <span>Scientific checkpoint 80d6db0</span></footer></div>`;
};

const wireTimeline = (root: HTMLElement, step: number): void => {
  const point = sampleReplay.timeline[step] ?? sampleReplay.timeline[0];
  const eventId = `M${String((point?.step ?? 0) + 1).padStart(2, "0")}`;
  const confidence = (0.7 - step * 0.03).toFixed(2);
  const pa = Math.min(0.3 + step * 0.02, 0.44).toFixed(2);
  const depth = Math.min(step, 4);

  const idA = root.querySelector<HTMLElement>("#event-id");
  const idB = root.querySelector<HTMLElement>("#event-id-secondary");
  const c = root.querySelector<HTMLElement>("#event-confidence");
  const p = root.querySelector<HTMLElement>("#event-p");
  const d = root.querySelector<HTMLElement>("#event-depth");

  if (idA) idA.textContent = eventId;
  if (idB) idB.textContent = eventId;
  if (c) c.textContent = confidence;
  if (p) p.textContent = pa;
  if (d) d.textContent = String(depth);

  for (const dot of root.querySelectorAll<HTMLButtonElement>(".dot")) {
    dot.classList.toggle("active", Number(dot.dataset.step) === step);
  }
};

export const mountApp = (root: HTMLElement): void => {
  let state = { ...initialState };

  const rerender = (): void => {
    root.innerHTML = render(state);
    if (state.stage === 3) {
      wireTimeline(root, state.step);
    }
  };

  root.addEventListener("click", (evt) => {
    const target = evt.target as HTMLElement;
    const button = target.closest<HTMLButtonElement>("button[data-action]");
    if (!button) {
      return;
    }

    const action = button.dataset.action;
    if (action === "go-stage") {
      state = { ...state, stage: Number(button.dataset.stage), step: 0 };
      rerender();
      return;
    }

    if (action === "open-world") {
      state = { ...state, world: button.dataset.world ?? "G01", stage: 3, step: 0 };
      rerender();
      return;
    }

    if (action === "cond") {
      state = { ...state, condition: (button.dataset.cond as AppState["condition"]) ?? "free" };
      rerender();
      return;
    }

    if (action === "step") {
      state = { ...state, step: Number(button.dataset.step ?? 0) };
      wireTimeline(root, state.step);
    }
  });

  rerender();
};
