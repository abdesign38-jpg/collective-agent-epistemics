import "./styles/tokens.css";
import "./styles/base.css";
import "./styles/narrative.css";
import "./styles/v04-controls.css";
import "./styles/preview-composition.css";
import "./styles/preview-copy.css";
import "./styles/replay-hud.css";
import "./styles/replay-clearance.css";
import "./styles/preview-state.css";
import "./styles/hive-preview.css";
import "./styles/hive-fidelity.css";
import "./styles/hive-colors.css";
import "./styles/hive-text.css";
import "./styles/selected-cell-layer.css";
import "./styles/animation-fidelity.css";
import "./styles/difference-placement.css";
import "./styles/pulse-lifecycle.css";
import "./styles/section-actions.css";
import "./styles/origin-graphic.css";
import "./styles/origin-agent.css";
import "./styles/origin-bee-fidelity.css";
import "./styles/origin-alignment.css";
import "./styles/research-record.css";
import "./styles/replay-control-panel.css";
import "./styles/replay-grid.css";
import "./styles/stage-center-label.css";
import "./styles/replay-caption-reference.css";
import "./styles/replay-difference-offset.css";
import "./styles/pages-assets.css";

import { mountApp } from "./app/App";

const root = document.querySelector<HTMLElement>("#app");

if (!root) {
  throw new Error("Missing #app root");
}

mountApp(root);