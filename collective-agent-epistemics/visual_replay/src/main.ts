import "./styles/tokens.css";
import "./styles/base.css";

import { sampleReplay } from "./data/sampleReplay";
import { wireTimeline } from "./replay/timeline";
import { createLandingView } from "./views/landingView";

const root = document.querySelector<HTMLElement>("#app");

if (!root) {
  throw new Error("Missing #app root");
}

root.innerHTML = createLandingView(sampleReplay);
wireTimeline(root, sampleReplay);