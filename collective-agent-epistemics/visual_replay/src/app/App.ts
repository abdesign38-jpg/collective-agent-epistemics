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

const renderLanding = (): string => `
  <div class="page-shell">
    <header class="topbar glass">
      <div class="brand" aria-label="Epistemic Hive home">
        <div class="brand-mark">◈</div>
        <span>EPISTEMIC HIVE</span>
      </div>

      <nav class="main-nav" aria-label="Main navigation">
        <button type="button" class="nav-link">Research</button>
        <button type="button" class="nav-link active">Visual Replay</button>
        <button type="button" class="nav-link">Data</button>
        <button type="button" class="nav-link">Methods</button>
      </nav>

      <div class="user-widget" aria-label="Researcher profile">
        <div class="user-icon">L</div>
        <div class="user-meta">
          <span class="user-label">Researcher</span>
          <span class="user-tag">LAB-7</span>
        </div>
      </div>
    </header>

    <main class="dashboard-grid">
      <section class="hero glass">
        <p class="eyebrow">01 Research Visualization Platform</p>
        <h1>Epistemic <span>Hive</span></h1>
        <p class="subtitle">EXP-002 Visual Replay</p>
        <p class="descriptor">One root · Increasing depth · Observed trajectories</p>
        <p class="caveat">Agent state ≠ transmitted message ≠ network evidence state</p>

        <div class="toggle-row" role="group" aria-label="Replay mode">
          <button type="button" class="chip chip-active">Empirical Replay</button>
          <button type="button" class="chip">Simulation Off</button>
        </div>

        <button type="button" class="cta">Enter Experiment</button>
      </section>

      <section class="network-panel glass" aria-hidden="true">
        <div class="mini-card mini-card-left">
          <h3>Evidence Flow</h3>
          <div class="mini-graph"></div>
        </div>

        <div class="mini-card mini-card-right">
          <h3>Agent Trajectories</h3>
          <div class="mini-graph mini-graph-small"></div>
        </div>

        <div class="mini-card mini-card-bottom">
          <h3>Network Topology</h3>
          <div class="mini-graph mini-graph-hex"></div>
        </div>

        <div class="node node-root"><span>E1</span></div>
        <div class="node node-a"><span>A</span></div>
        <div class="node node-b"><span>B</span></div>
        <div class="node node-c"><span>C</span></div>
        <svg class="network-lines" viewBox="0 0 100 100" preserveAspectRatio="none">
          <line x1="50" y1="52" x2="18" y2="24" />
          <line x1="50" y1="52" x2="18" y2="82" />
          <line x1="50" y1="52" x2="82" y2="78" />
        </svg>
      </section>

      <section class="metrics glass">
        <article>
          <h2>EXP-002</h2>
          <p>Visual replay</p>
        </article>
        <article>
          <h2>1</h2>
          <p>Root</p>
          <small>Evidence node</small>
        </article>
        <article>
          <h2>3</h2>
          <p>Agents</p>
          <small>Observed</small>
        </article>
        <article>
          <h2>∞</h2>
          <p>Depth</p>
          <small>Exploration</small>
        </article>
        <div class="metrics-visual">
          <div class="metric-line"></div>
        </div>
      </section>
    </main>
  </div>
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
  return renderLanding();
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
