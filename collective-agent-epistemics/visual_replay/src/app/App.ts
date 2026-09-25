import { generatedReplay } from "../data/generatedReplay";

type View = "intro" | "origin" | "research" | "replay" | "hive";
type Condition = "free" | "lineage" | "macro";
type Agent = "A" | "B" | "C";

interface AppState {
  view: View;
  condition: Condition;
  eventIndex: number;
  worldId: string;
  playing: boolean;
  detailOpen: boolean;
  reducedMotion: boolean;
}

const anchorWorldId = "G2B_GEN001_seed_1114638083";
const chapters: Array<{ view: View; label: string }> = [
  { view: "intro", label: "Experiment" },
  { view: "origin", label: "Origin / W01" },
  { view: "replay", label: "World replay" },
  { view: "hive", label: "View hive" },
  { view: "research", label: "Research" }
];

const initialState: AppState = {
  view: "intro", condition: "free", eventIndex: 0, worldId: anchorWorldId,
  playing: false, detailOpen: false,
  reducedMotion: window.matchMedia("(prefers-reduced-motion: reduce)").matches
};

const getWorld = (state: AppState) => generatedReplay.worlds.find((world) => world.id === state.worldId) ?? generatedReplay.worlds[0];
const getEvents = (state: AppState) => getWorld(state).conditions[state.condition];
const getEvent = (state: AppState) => getEvents(state)[Math.min(state.eventIndex, getEvents(state).length - 1)];
const conditionLabel = (condition: Condition) => condition.toUpperCase();
const cellLabel = (world: typeof generatedReplay.worlds[number]) => `${world.truth}/${world.observed}`;

const firstDifferenceIndex = (state: AppState): number => {
  if (state.condition === "macro") return 0;
  const world = getWorld(state);
  const current = world.conditions[state.condition];
  const comparison = world.conditions[state.condition === "free" ? "lineage" : "free"];
  const differingIndexes = current.flatMap((event, eventIndex) => {
    const other = comparison[eventIndex];
    return Boolean(other) && (event.answer !== other.answer || event.confidence !== other.confidence || event.pA !== other.pA) ? [eventIndex] : [];
  });
  if (differingIndexes.length === 0) return 0;
  const finalIndex = Math.min(current.length, comparison.length) - 1;
  return differingIndexes.includes(finalIndex) ? finalIndex : differingIndexes[0];
};

const edgeFor = (sender: string, receiver: string): string => {
  if (sender === "A" && receiver === "B") return "M 798 167 L 529 422";
  if (sender === "B" && receiver === "C") return "M 529 422 L 1024 452";
  if (sender === "C" && receiver === "A") return "M 1024 452 L 798 167";
  return "M 798 167 L 798 167";
};

const renderBee = (agent: Agent, active: boolean, receiver: boolean): string => `
  <div class="facet-bee facet-bee-${agent.toLowerCase()} ${active ? "event-sender" : ""} ${receiver ? "event-receiver" : ""}" aria-label="Agent ${agent}">
    <span class="bee-halo"></span><span class="bee-wing wing-left"></span><span class="bee-wing wing-right"></span><span class="bee-shell"></span><img class="bee-art" src="/assets/bee-agent.webp" alt="" onerror="this.style.display='none'"><b>${agent}</b>
  </div>`;

const renderStage = (state: AppState): string => {
  const world = getWorld(state);
  const event = getEvent(state);
  const misleading = world.truth !== world.observed;
  const path = edgeFor(event.sender, event.receiver);
  const showWorld = state.view === "replay" || state.view === "hive";
  const replayMotion = showWorld && state.playing && !state.reducedMotion;
  const sourcePulse = (event.id === "M01" || event.sameRootRegrounding) && showWorld;
  const misleadingVisible = misleading && state.view === "replay";
  const stageTitle = event.id === "M01" ? "One observation enters the loop." : event.id === "M13" ? `Final answer ${event.answer}. World truth ${world.truth}.` : event.sameRootRegrounding ? "A sees the same E1 again." : `${event.sender} passes the report to ${event.receiver}.`;
  return `<section class="eh-stage ${misleadingVisible ? "is-misleading" : ""} ${showWorld ? "is-replay" : ""}" aria-label="Archived world replay">
    <div class="stage-art"><img src="/assets/lab-stage.webp" alt="" class="lab-stage-art" onerror="this.style.display='none'"></div><div class="stage-grid"></div>
    <div class="stage-label"><span>EXP-002 / ${world.setLabel.toUpperCase()}</span><b>${world.id}</b><em>${event.id}</em></div>${showWorld ? `<div class="stage-center-label"><p>${event.id === "M01" ? "E1 / ONE EXTERNAL OBSERVATION" : event.sameRootRegrounding ? "E1 REOBSERVED / SAME ROOT" : `MESSAGE ${event.id} / ${event.sender} → ${event.receiver}`}</p><h2>${stageTitle}</h2></div>` : ""}
    <div class="truth-label ${state.view === "replay" && state.eventIndex >= 12 ? "revealed" : ""}">WORLD TRUTH <strong>${world.truth}</strong></div>
    <div class="evidence-root"><span>E1</span><small>ONE INDEPENDENT ROOT</small></div>
    <div class="observation-badge">OBSERVED BY A <strong>${world.observed}</strong><small>REPORTED RELIABILITY ${world.sensorReliability.toFixed(2)}</small></div>
    <svg class="hive-edges" viewBox="0 0 1536 864" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><path class="edge evidence-edge ${misleading ? "misleading-edge" : ""} ${sourcePulse ? "source-lit" : ""}" d="M 769 363 L 798 167"></path><path class="edge edge-ab" d="M 798 167 L 529 422"></path><path class="edge edge-bc" d="M 529 422 L 1024 452"></path><path class="edge edge-ca" d="M 1024 452 L 798 167"></path><path class="event-edge ${misleading ? "misleading-edge" : ""} ${replayMotion ? "edge-moving" : ""}" d="${showWorld ? path : "M 798 167 L 529 422"}"></path>${state.condition === "lineage" ? `<path class="lineage-edge" d="${path}"></path>` : ""}${replayMotion ? `<path class="message-pulse pulse-active" d="M -11 -5 L 4 -5 L 12 0 L 4 5 L -11 5 Z"><animateMotion dur="1.45s" repeatCount="1" path="${path}" begin="${sourcePulse ? "0.45s" : "0s"}"></animateMotion></path>` : ""}${sourcePulse && replayMotion ? `<path class="evidence-pulse pulse-active" d="M -7 0 L 0 -6 L 7 0 L 0 6 Z"><animateMotion dur=".55s" repeatCount="1" path="M 769 363 L 798 167" begin="0s"></animateMotion></path>` : ""}</svg>
    ${renderBee("A", event.sender === "A", event.receiver === "A")}${renderBee("B", event.sender === "B", event.receiver === "B")}${renderBee("C", event.sender === "C", event.receiver === "C")}
    <div class="capsule ${replayMotion ? "capsule-moving" : ""}">${event.sender} → ${event.receiver}</div>
    <div class="stage-readout"><span>ROOTS <b>${event.roots.length}</b></span><span>DEPTH <b>${event.depth}</b></span><span>CONF <b>${event.confidence.toFixed(2)}</b></span></div>
  </section>`;
};

const renderComparison = (state: AppState): string => {
  if (state.condition === "macro") return "";
  const world = getWorld(state);
  const event = getEvent(state);
  const otherCondition: Condition = state.condition === "free" ? "lineage" : "free";
  const other = world.conditions[otherCondition][Math.min(state.eventIndex, world.conditions[otherCondition].length - 1)];
  const differs = event.answer !== other.answer || event.confidence !== other.confidence || event.pA !== other.pA;
  if (!differs) return "";
  return `<aside class="recorded-difference"><strong>RECORDED DIFFERENCE ${event.id}</strong><span>${conditionLabel(state.condition)} ${event.confidence.toFixed(2)} confidence · ${conditionLabel(otherCondition)} ${other.confidence.toFixed(2)} confidence</span><small>Same world and event. This is an observed value difference, not a proven mechanism.</small></aside>`;
};

const renderTransport = (state: AppState): string => {
  const events = getEvents(state);
  const event = getEvent(state);
  const atEnd = state.eventIndex >= events.length - 1;
  return `<footer class="replay-footer"><div class="transport"><button data-action="previous" aria-label="Previous event">‹</button><button data-action="toggle-play" class="play-control" aria-label="${state.playing ? "Pause" : "Play"}">${state.playing ? "Ⅱ" : "▶"}</button><button data-action="next" aria-label="Next event" ${atEnd ? "disabled" : ""}>›</button><span>${event.id} / ${events.length} · ${conditionLabel(state.condition)}</span></div><div class="timeline"><p>REPLAY TIMELINE <b>${event.id}</b></p><div>${events.map((item, index) => `<button data-action="event" data-index="${index}" class="timeline-dot ${index === state.eventIndex ? "active" : ""}" aria-label="${item.id}"></button>`).join("")}</div></div><div class="replay-note">ARCHIVED EVENTS · INTERPOLATED VISUAL PATH<br><b>SIMULATION OFF</b></div></footer>`;
};

const renderIntro = (state: AppState): string => `<main class="story-screen intro-screen"><div class="story-copy"><p class="kicker">EXP-002 / THE RESEARCH QUESTION</p><h1>ONE OBSERVATION.<br><span class="eh-accent">MANY INFERENCES.</span></h1><p>What happens when agents keep passing around information that began with a single observation?</p><p>Three model agents exchanged messages in a loop. We tracked their answers, confidence and evidence lineage through repeated runs of one world, then across new worlds.</p><div class="intro-actions"><button class="primary-action" data-action="view" data-view="origin">ENTER EXPERIMENT <span>→</span></button><button class="text-action" data-action="view" data-view="research">READ THE RESEARCH QUESTION</button></div><div class="intro-stats"><b>01</b> EXTERNAL ROOT <b>03</b> AGENTS <b>15</b> SAME-WORLD RUNS <b>12 + 08</b> NEW WORLDS</div></div>${renderStage(state)}</main>`;
const renderOrigin = (state: AppState): string => `<main class="story-screen origin-screen"><div class="story-copy"><p class="kicker">02 / ORIGIN · W01</p><h1>First, the <span class="eh-accent">same world.</span></h1><p>One observation reached Agent A. Messages then moved A → B → C → A. The team repeated this exact world and protocol fifteen times before opening the wider world replay.</p><div class="fact-line"><b>15</b><span>formal runs of one world</span><b>1</b><span>independent root</span></div><button class="primary-action" data-action="view" data-view="replay">ENTER WORLD REPLAY <span>→</span></button></div><div class="origin-graphic" aria-label="Agent bee and W01 repeated fifteen times"><div class="origin-agent"><img src="/assets/bee-agent.webp" alt=""><b>A</b><small>AGENT</small></div><div class="origin-replicas">${Array.from({ length: 15 }, () => "<i></i>").join("")}</div><div class="origin-hex"><strong>W01</strong><small>SAME WORLD ×15</small></div></div>${renderStage(state)}</main>`;
const renderResearch = (state: AppState): string => `<main class="research-record"><p class="kicker">RESEARCH / THE SCIENTIFIC RECORD</p><h1>What was actually tested?</h1><p class="research-lede">As inference depth and inter-agent recursion increase without new independent evidence, what happens to lineage, calibration, confidence and convergence?</p><p class="research-lede">EXP-002 examined this under a frozen protocol, first in one world and then across different truth/observation realizations.</p><div class="research-grid"><article><h2>Same world · W01</h2><p>15 formal repetitions of one world. The repeated-run evidence does not count as 15 worlds in Gate 2B.</p></article><article><h2>Generalization · 12</h2><p>One misleading B/A world showed a final FREE confidence/Brier difference. FREE and LINEAGE final answers still agreed in all 12.</p></article><article><h2>Stress · 8</h2><p>Final primary outcomes matched within each world; some paths differed temporarily. The two sets have different selection schemes.</p></article></div><p class="research-limit">Neither causal interaction-induced degradation, evidence double counting nor lineage loss was established. The historical null remains viable.</p><button class="primary-action" data-action="view" data-view="replay">SEE THE RECORDED PATH <span>→</span></button></main>`;

const renderReplay = (state: AppState): string => {
  const world = getWorld(state);
  const event = getEvent(state);
  return `<main class="replay-screen"><aside class="replay-control-panel"><p class="kicker">ACT 02 / EMPIRICAL REPLAY</p><h2>WORLD <span>REPLAY</span></h2><p class="control-world-id">${world.id}</p><div class="control-tags"><span>● ARCHIVED EVENTS</span><span>● SIMULATION OFF</span></div><div class="control-modes" role="group" aria-label="Replay condition">${(["free", "lineage", "macro"] as Condition[]).map((condition) => `<button data-action="condition" data-condition="${condition}" class="${state.condition === condition ? "active" : ""}">${conditionLabel(condition)}</button>`).join("")}</div><div class="control-trace"><p>RECORDED CONFIDENCE <span>FREE / LINEAGE</span></p><div><i style="width:${Math.round(event.confidence * 100)}%"></i></div><small>Values update only at archived event boundaries.</small></div><p class="control-note">${state.condition === "macro" && event.id === "M04" ? "MACRO stops at M04: no new independent roots." : world.truth !== world.observed ? `MISLEADING E1 · OBSERVED ${world.observed} · WORLD TRUTH ${world.truth}` : "One source enters the system; each message derives from it."}</p></aside>${renderStage(state)}<section class="replay-caption"><p>ARCHIVED WORLD REPLAY · ${world.id} · ${event.id}</p><h1>${event.sender} sent a recorded message to ${event.receiver}.</h1><p>${state.eventIndex >= 12 && world.truth !== world.observed ? "The observed answer is incorrect against the revealed world truth. This does not establish that conversation caused the error." : "The event order, endpoints, root count, and values come from the archived record."}</p><div class="replay-actions"><button data-action="message">VIEW ORIGINAL MESSAGE</button><button data-action="difference" ${state.condition === "macro" ? "hidden" : ""}>INSPECT RECORDED DIFFERENCE</button></div></section><aside class="replay-right-hud"><div class="hud-panel"><p class="hud-title">WORLD METRICS <span>ARCHIVED EVENT</span></p><div class="hud-rows"><span>TRUTH <b>${world.truth}</b></span><span>OBSERVED <b>${world.observed}</b></span><span>ANSWER <b>${event.answer}</b></span><span>CONFIDENCE <b>${event.confidence.toFixed(2)}</b></span><span>P(A) <b>${event.pA.toFixed(2)}</b></span><span>BRIER <b>${event.brierScore.toFixed(4)}</b></span><span>DEPTH <b>${event.depth}</b></span><span>ROOTS <b>${event.roots.length}</b></span></div></div><div class="hud-panel message-hud"><p class="hud-title">TRANSMITTED MESSAGE <span>VERBATIM</span></p><p class="hud-route"><b>${event.sender}</b> → <b>${event.receiver}</b></p><blockquote>${event.message}</blockquote><small>Agent wording is archived; the cyan capsule is a message, not a new observation.</small></div></aside>${renderComparison(state)}${state.detailOpen ? `<aside class="message-drawer"><button data-action="close-detail" aria-label="Close message">×</button><p>MESSAGE LITERAL FROM ${event.sender} · ${event.id}</p><blockquote>${event.message}</blockquote><small>${world.archivePath}</small></aside>` : ""}</main>${renderTransport(state)}`;
};

const renderHive = (state: AppState): string => `<main class="hive-screen"><header><p class="kicker">05 / VIEW HIVE</p><h1>Different worlds. Separate records.</h1><p>Only the selected cell plays its own archive. No message travels between worlds.</p></header><div class="hive-groups">${["generalization", "stress"].map((set) => `<section><h2>${set === "generalization" ? "GENERALIZATION · 12 WORLDS" : "STRESS · 8 WORLDS"}</h2><div class="world-cells">${generatedReplay.worlds.filter((world) => world.set === set).map((world) => `<button data-action="select-world" data-world="${world.id}" class="world-cell ${world.id === state.worldId ? "selected" : ""}"><span class="mini-cell">E1</span><b>${cellLabel(world)}</b><small>${world.id.replace("G2B_", "")}</small></button>`).join("")}</div></section>`).join("")}</div><aside class="selected-readout"><p>SELECTED WORLD</p><strong>${worldLabel(getWorld(state))}</strong><span>FREE / LINEAGE / MACRO remain inside this world.</span><button data-action="open-selected">OPEN SELECTED REPLAY ↗</button></aside></main>`;

const worldLabel = (world: typeof generatedReplay.worlds[number]) => `${world.id} · TRUTH ${world.truth} / OBSERVED ${world.observed}`;
const decorateHiveCells = (root: HTMLElement): void => {
  for (const cell of root.querySelectorAll<HTMLElement>(".mini-cell")) {
    cell.innerHTML = `<svg viewBox="0 0 64 48" aria-hidden="true"><path class="mini-edge" d="M32 25 L32 5"></path><path class="mini-edge" d="M32 5 L10 39"></path><path class="mini-edge" d="M10 39 L54 39"></path><path class="mini-edge" d="M54 39 L32 5"></path><circle class="mini-root" cx="32" cy="25" r="4"></circle><circle cx="32" cy="5" r="3"></circle><circle cx="10" cy="39" r="3"></circle><circle cx="54" cy="39" r="3"></circle><circle class="mini-pulse" cx="32" cy="5" r="2.5"></circle></svg>`;
    const world = generatedReplay.worlds.find((item) => item.id === cell.closest<HTMLElement>("[data-world]")?.dataset.world);
    cell.closest<HTMLElement>("[data-world]")?.classList.toggle("misleading", world?.alignment === "misleading");
    cell.closest<HTMLElement>("[data-world]")?.classList.toggle("different", world?.finalDifference === true);
  }
};

const updateHiveSelection = (root: HTMLElement, worldId: string): void => {
  root.querySelectorAll<HTMLElement>(".world-cell").forEach((cell) => {
    cell.classList.toggle("selected", cell.dataset.world === worldId);
  });
  const world = generatedReplay.worlds.find((item) => item.id === worldId);
  const selected = root.querySelector<HTMLElement>(".selected-readout strong");
  if (world && selected) selected.textContent = worldLabel(world);
};
const render = (state: AppState): string => `<div class="eh-app ${state.reducedMotion ? "reduced-motion" : ""}"><header class="eh-topbar"><div class="eh-brand"><span>◈</span> EPISTEMIC HIVE</div><nav aria-label="Primary navigation">${chapters.map((chapter) => `<button data-action="view" data-view="${chapter.view}" class="${state.view === chapter.view ? "active" : ""}">${chapter.label}</button>`).join("")}</nav><button class="motion-button" data-action="motion">${state.reducedMotion ? "REDUCED MOTION" : "MOTION ACTIVE"}</button></header>${state.view === "intro" ? renderIntro(state) : state.view === "origin" ? renderOrigin(state) : state.view === "research" ? renderResearch(state) : state.view === "replay" ? renderReplay(state) : renderHive(state)}${state.view !== "replay" ? `<footer class="bottom-line"><span>EXP-002 / EPISTEMIC HIVE</span><b>ONE ROOT · INCREASING DEPTH · OBSERVED TRAJECTORIES</b><span>Agent state ≠ transmitted message ≠ network evidence state</span></footer>` : ""}</div>`;

export const mountApp = (root: HTMLElement): void => {
  let state = { ...initialState };
  const rerender = () => { root.innerHTML = render(state); decorateHiveCells(root); };
  root.addEventListener("click", (input) => {
    const button = (input.target as HTMLElement).closest<HTMLButtonElement>("button[data-action]");
    if (!button) return;
    const action = button.dataset.action;
    const events = getEvents(state);
    if (action === "view") state = { ...state, view: button.dataset.view as View, playing: false, detailOpen: false };
    if (action === "previous") state = { ...state, eventIndex: Math.max(0, state.eventIndex - 1), playing: false };
    if (action === "next") state = { ...state, eventIndex: Math.min(events.length - 1, state.eventIndex + 1), playing: false };
    if (action === "event") state = { ...state, eventIndex: Number(button.dataset.index ?? 0), playing: false };
    if (action === "toggle-play") state = { ...state, playing: !state.playing };
    if (action === "condition") {
      const condition = button.dataset.condition as Condition;
      state = { ...state, condition, eventIndex: Math.min(state.eventIndex, getWorld(state).conditions[condition].length - 1), playing: false };
    }
    if (action === "message") state = { ...state, detailOpen: true };
    if (action === "close-detail") state = { ...state, detailOpen: false };
    if (action === "difference") state = { ...state, eventIndex: firstDifferenceIndex(state), playing: false };
    if (action === "select-world") {
      const worldId = button.dataset.world ?? anchorWorldId;
      state = { ...state, worldId, eventIndex: 0, playing: false };
      if (state.view === "hive") {
        updateHiveSelection(root, worldId);
        return;
      }
    }
    if (action === "open-selected") state = { ...state, view: "replay", eventIndex: 0, playing: false };
    if (action === "motion") state = { ...state, reducedMotion: !state.reducedMotion, playing: false };
    rerender();
  });
  window.setInterval(() => {
    if (state.view === "replay" && state.playing && !state.reducedMotion) {
      const events = getEvents(state);
      if (state.eventIndex < events.length - 1) state = { ...state, eventIndex: state.eventIndex + 1 };
      else state = { ...state, playing: false };
      rerender();
    }
  }, 2400);
  rerender();
};
