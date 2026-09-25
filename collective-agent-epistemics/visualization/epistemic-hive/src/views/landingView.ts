import type { ReplaySnapshot } from "../types/replay";

const trajectoryClass = (idx: number): string => {
  if (idx === 0) {
    return "trajectory trajectory-a";
  }
  if (idx === 1) {
    return "trajectory trajectory-b";
  }
  return "trajectory trajectory-c";
};

const renderTrajectoryRows = (snapshot: ReplaySnapshot): string =>
  snapshot.trajectories
    .map(
      (line, idx) => `
        <div class="trajectory-row">
          <span class="agent-label">${line.id}</span>
          <svg viewBox="0 0 100 20" class="${trajectoryClass(idx)}" preserveAspectRatio="none" aria-hidden="true">
            <path d="${line.confidence
              .map((value, point) => `${point === 0 ? "M" : "L"}${point * 20} ${20 - value * 20}`)
              .join(" ")}" />
          </svg>
        </div>`
    )
    .join("\n");

const renderTimelineTicks = (snapshot: ReplaySnapshot): string =>
  snapshot.timeline
    .map(
      (point, idx) => `
        <button class="tick ${idx === snapshot.timeline.length - 1 ? "active" : ""}" type="button" data-step="${point.step}">
          <span class="sr-only">Step ${point.step}</span>
        </button>`
    )
    .join("\n");

export const createLandingView = (snapshot: ReplaySnapshot): string => `
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
        <p class="caveat">${snapshot.caveat}</p>

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

        <div class="node node-root">
          <span>${snapshot.rootNode}</span>
        </div>
        <div class="node node-a"><span>A</span></div>
        <div class="node node-b"><span>B</span></div>
        <div class="node node-c"><span>C</span></div>
        <svg class="network-lines" viewBox="0 0 100 100" preserveAspectRatio="none">
          <line x1="50" y1="52" x2="22" y2="24" />
          <line x1="50" y1="52" x2="20" y2="82" />
          <line x1="50" y1="52" x2="80" y2="76" />
        </svg>
      </section>

      <section class="metrics glass">
        <article>
          <h2>${snapshot.experimentId}</h2>
          <p>Visual replay</p>
        </article>
        <article>
          <h2>1</h2>
          <p>Root node</p>
        </article>
        <article>
          <h2>${snapshot.observedAgents}</h2>
          <p>Agents observed</p>
        </article>
        <article>
          <h2>&infin;</h2>
          <p>${snapshot.depthMode}</p>
        </article>
      </section>

      <section class="trajectory-panel glass">
        <header>
          <h2>Agent trajectories</h2>
        </header>
        <div class="trajectory-grid">${renderTrajectoryRows(snapshot)}</div>
      </section>

      <section class="timeline glass" aria-label="Replay timeline controls">
        <header>
          <h2>Replay timeline</h2>
          <p class="time-readout">t = <span id="time-readout">0.00</span></p>
        </header>
        <div class="timeline-track">${renderTimelineTicks(snapshot)}</div>
      </section>
    </main>
  </div>
`;