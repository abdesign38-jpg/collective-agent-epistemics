import "./styles/tokens.css";
import "./styles/base.css";
import "./styles/narrative.css";

import { mountApp } from "./app/App";

const root = document.querySelector<HTMLElement>("#app");

if (!root) {
  throw new Error("Missing #app root");
}

mountApp(root);