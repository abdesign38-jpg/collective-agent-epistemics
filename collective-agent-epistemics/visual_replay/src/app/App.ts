import { generatedReplay } from "../data/generatedReplay";

type View = "story" | "worlds" | "record";
type Condition = "free" | "lineage" | "macro";

interface AppState {
  view: View;
  chapter: number;
  condition: Condition;
  eventIndex: number;
  worldId: string;
  playing: boolean;
  detailOpen: boolean;
  reducedMotion: boolean;
}

const anchorWorldId = "G2B_GEN001_seed_1114638083";
const chapters = [
  "Entrar en la colmena", "La observación", "Conversación", "Recursión",
  "Dos maneras de transmitir", "Repetir el mismo mundo", "Abrir la colmena",
  "Error visible", "Contraste honesto", "Qué se sabe"
];
const captions = [
  "Tres agentes deben decidir entre A y B. Solo A recibe una observación externa.",
  "Una observación con fiabilidad reportada 0,70 inicia la historia.",
  "Cada abeja recibe el mensaje anterior y prepara el siguiente.",
  "Se repite la misma fuente; el número de pruebas independientes sigue siendo uno.",
  "Cambia cómo se comunica el origen. Comparamos caminos, sin proclamar un ganador.",
  "Quince ejecuciones de la misma configuración: no son quince mundos distintos.",
  "Ahora cambia qué era verdad y qué observó el sensor.",
  "Aquí la respuesta final fue equivocada. La diferencia de confianza apareció en este mundo, no en todos.",
  "El recorrido puede variar aunque el resultado final coincida.",
  "Una sola fuente circuló muchas veces. Queda por probar si la interacción causó una degradación adicional."
];
const chapterEvents = [0, 0, 1, 3, 3, 3, 0, 12, 8, 12];

const initialState: AppState = {
  view: "story", chapter: 0, condition: "free", eventIndex: 0,
  worldId: anchorWorldId, playing: false, detailOpen: false,
  reducedMotion: window.matchMedia("(prefers-reduced-motion: reduce)").matches
};

const getWorld = (state: AppState) => generatedReplay.worlds.find((world) => world.id === state.worldId) ?? generatedReplay.worlds[0];
const getEvents = (state: AppState) => getWorld(state).conditions[state.condition];
const conditionLabel = (condition: Condition) => condition === "free" ? "FREE" : condition === "lineage" ? "LINEAGE" : "MACRO";

const renderBee = (agent: "A" | "B" | "C", active: boolean, receiver: boolean): string => `
  <div class="story-bee bee-${agent.toLowerCase()} ${active ? "is-active" : ""} ${receiver ? "is-receiver" : ""}" aria-label="Agente ${agent}">
    <span class="story-wing left-wing"></span><span class="story-wing right-wing"></span><span class="story-body"></span><b>${agent}</b>
  </div>`;

const renderScene = (state: AppState): string => {
  const world = getWorld(state);
  const events = getEvents(state);
  const event = events[Math.min(state.eventIndex, events.length - 1)];
  return `
    <section class="story-scene" aria-label="Reproducción visual del mundo ${world.id}">
      <div class="scene-grid"></div>
      <div class="scene-meta"><span>Registro EXP-002</span><span>${world.id}</span><span>${event.id}</span></div>
      <div class="world-truth ${state.chapter >= 7 ? "shown" : ""}">Verdad del mundo <b>${world.truth}</b></div>
      <div class="source-card"><small>Observación de A</small><strong>${world.observed}</strong><span>Fiabilidad ${world.sensorReliability.toFixed(2)}</span></div>
      <div class="evidence-crystal ${event.id === "M01" ? "is-lit" : ""}"><span>E1</span><small>Fuente externa única</small></div>
      ${renderBee("A", event.sender === "A", event.receiver === "A")}
      ${renderBee("B", event.sender === "B", event.receiver === "B")}
      ${renderBee("C", event.sender === "C", event.receiver === "C")}
      <svg class="story-links" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true"><path class="link-base" d="M51 50 L25 74 L76 74 Z"></path><path class="link-pulse ${state.playing && !state.reducedMotion ? "is-moving" : ""}" d="M${event.sender === "A" ? "25 74 L76 74" : event.sender === "B" ? "76 74 L51 25" : "51 25 L25 74"}"></path></svg>
      <div class="event-pulse ${state.playing && !state.reducedMotion ? "is-moving" : ""}"><span>${event.sender} → ${event.receiver}</span></div>
      <div class="scene-status"><span>Raíces independientes</span><b>${event.roots.length}</b><span>Profundidad</span><b>${event.depth}</b></div>
    </section>`;
};

const renderTransport = (state: AppState): string => {
  const events = getEvents(state);
  const event = events[Math.min(state.eventIndex, events.length - 1)];
  return `<section class="transport" aria-label="Controles de reproducción"><div class="chapter-label"><span>Capítulo ${String(state.chapter).padStart(2, "0")}</span><strong>${chapters[state.chapter]}</strong></div><div class="transport-controls"><button class="icon-button" data-action="previous-chapter" aria-label="Capítulo anterior">«</button><button class="icon-button" data-action="previous" aria-label="Evento anterior">‹</button><button class="play-button" data-action="toggle-play">${state.playing ? "Pausar" : "Reproducir"}</button><button class="icon-button" data-action="next" aria-label="Evento siguiente">›</button><button class="icon-button" data-action="next-chapter" aria-label="Capítulo siguiente">»</button><span class="event-id">${event.id} · ${conditionLabel(state.condition)}</span></div><div class="event-track">${events.map((item, index) => `<button data-action="event" data-index="${index}" class="track-dot ${index === state.eventIndex ? "active" : ""}" aria-label="${item.id}"></button>`).join("")}</div></section>`;
};

const renderStory = (state: AppState): string => {
  const world = getWorld(state);
  const event = getEvents(state)[Math.min(state.eventIndex, getEvents(state).length - 1)];
  return `<main class="narrative-shell">${renderScene(state)}<section class="story-caption"><p>Grabación del experimento</p><h1>${captions[state.chapter]}</h1><p class="event-summary"><b>${event.sender} recibió y transmitió un mensaje a ${event.receiver}.</b> Esto es un evento archivado, no una simulación en vivo.</p></section><div class="story-actions"><button data-action="message">Ver mensaje original</button><button data-action="provenance">¿De dónde sale esta afirmación?</button></div><div class="condition-switch" role="group" aria-label="Condición del replay">${(["free", "lineage", "macro"] as Condition[]).map((condition) => `<button data-action="condition" data-condition="${condition}" class="${condition === state.condition ? "active" : ""}">${conditionLabel(condition)}</button>`).join("")}</div>${renderTransport(state)}${state.detailOpen ? `<aside class="detail-drawer"><button class="drawer-close" data-action="close-detail" aria-label="Cerrar detalle">×</button><p class="drawer-kicker">Mensaje literal del agente · ${event.id}</p><blockquote>${event.message}</blockquote><dl><div><dt>Emisor</dt><dd>${event.sender}</dd></div><div><dt>Receptor</dt><dd>${event.receiver}</dd></div><div><dt>Respuesta</dt><dd>${event.answer}</dd></div><div><dt>Confianza</dt><dd>${event.confidence.toFixed(2)}</dd></div></dl><p class="source-path">${world.archivePath}</p></aside>` : ""}</main>`;
};

const renderWorlds = (state: AppState): string => {
  const world = getWorld(state);
  return `<main class="world-explorer"><header><p class="eyebrow">Explorar mundos</p><h1>La colmena se abre.</h1><p>La comparación cambia de mundo: no transmite mensajes entre mundos.</p></header><div class="world-groups">${["generalization", "stress"].map((set) => `<section class="world-group"><h2>${set === "generalization" ? "Generalization · 12 mundos" : "Stress · 8 mundos"}</h2><div class="world-cells">${generatedReplay.worlds.filter((item) => item.set === set).map((item) => `<button class="world-cell ${item.id === world.id ? "selected" : ""}" data-action="world" data-world="${item.id}"><span>${item.truth}/${item.observed}</span><small>${item.id.replace("G2B_", "")}</small></button>`).join("")}</div></section>`).join("")}</div><aside class="selected-world"><p>${world.id}</p><strong>Verdad ${world.truth} · Observación ${world.observed}</strong><span>${world.alignment === "misleading" ? "Observación engañosa" : "Observación alineada"}</span><button data-action="watch-world">Reproducir este mundo</button></aside></main>`;
};

const renderRecord = (): string => `<main class="record-shell"><header><p class="eyebrow">Registro científico</p><h1>Fuentes, protocolo y límites</h1><p>Esta capa documenta el replay; no sustituye la escena narrada.</p></header><div class="record-grid"><section><h2>Gate 2B</h2><dl><div><dt>Mundos válidos</dt><dd>12 Generalization + 8 Stress</dd></div><div><dt>Eventos archivados</dt><dd>${generatedReplay.totals.events}</dd></div><div><dt>Llamadas válidas</dt><dd>${generatedReplay.totals.validProviderCalls}</dd></div><div><dt>Respuestas reutilizadas</dt><dd>${generatedReplay.totals.reusedResponses}</dd></div></dl></section><section><h2>Lectura responsable</h2><p>Una misma observación puede reaparecer en una conversación sin volverse una segunda prueba.</p><p>Las diferencias de trayectoria no establecen que conversar haya causado un daño adicional.</p><p>W01 representa 15 ejecuciones del mismo mundo, no 15 mundos Gate 2B.</p></section><section><h2>Provenencia</h2><p>${generatedReplay.sourceManifest}</p><p>Hash del manifest: ${generatedReplay.manifestHash}</p><p>Todos los datos de esta vista son artefactos de visualización generados desde registros archivados de solo lectura.</p></section></div></main>`;

const render = (state: AppState): string => `<div class="narrative-app ${state.reducedMotion ? "reduced-motion" : ""}"><header class="narrative-topbar"><div class="narrative-brand"><span>◈</span> EPISTEMIC HIVE</div><nav aria-label="Navegación principal"><button data-action="view" data-view="story" class="${state.view === "story" ? "active" : ""}">Ver la historia</button><button data-action="view" data-view="worlds" class="${state.view === "worlds" ? "active" : ""}">Explorar mundos</button><button data-action="view" data-view="record" class="${state.view === "record" ? "active" : ""}">Registro científico</button></nav><button class="motion-toggle" data-action="motion">${state.reducedMotion ? "Movimiento reducido" : "Movimiento activo"}</button></header>${state.view === "story" ? renderStory(state) : state.view === "worlds" ? renderWorlds(state) : renderRecord()}</div>`;

export const mountApp = (root: HTMLElement): void => {
  let state = { ...initialState };
  const rerender = (): void => { root.innerHTML = render(state); };
  root.addEventListener("click", (event) => {
    const button = (event.target as HTMLElement).closest<HTMLButtonElement>("button[data-action]");
    if (!button) return;
    const action = button.dataset.action;
    const events = getEvents(state);
    if (action === "view") state = { ...state, view: button.dataset.view as View, playing: false };
    if (action === "condition") state = { ...state, condition: button.dataset.condition as Condition, eventIndex: 0 };
    if (action === "event") state = { ...state, eventIndex: Number(button.dataset.index ?? 0), playing: false };
    if (action === "previous") state = { ...state, eventIndex: Math.max(0, state.eventIndex - 1), playing: false };
    if (action === "next") state = { ...state, eventIndex: Math.min(events.length - 1, state.eventIndex + 1), playing: false };
    if (action === "previous-chapter") {
      const chapter = Math.max(0, state.chapter - 1);
      state = { ...state, chapter, eventIndex: Math.min(chapterEvents[chapter], events.length - 1), playing: false };
    }
    if (action === "next-chapter") {
      const chapter = Math.min(chapters.length - 1, state.chapter + 1);
      state = { ...state, chapter, eventIndex: Math.min(chapterEvents[chapter], events.length - 1), playing: false };
    }
    if (action === "toggle-play") state = { ...state, playing: !state.playing };
    if (action === "message" || action === "provenance") state = { ...state, detailOpen: true };
    if (action === "close-detail") state = { ...state, detailOpen: false };
    if (action === "motion") state = { ...state, reducedMotion: !state.reducedMotion, playing: false };
    if (action === "world") state = { ...state, worldId: button.dataset.world ?? anchorWorldId };
    if (action === "watch-world") state = { ...state, view: "story", chapter: 6, eventIndex: 0 };
    rerender();
  });
  window.setInterval(() => {
    const events = getEvents(state);
    if (state.view === "story" && state.playing && !state.reducedMotion) {
      state = { ...state, eventIndex: state.eventIndex === events.length - 1 ? 0 : state.eventIndex + 1 };
      rerender();
    }
  }, 1800);
  rerender();
};
