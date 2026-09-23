import type { ReplaySnapshot } from "../types/replay";

const activeClass = "active";

export const wireTimeline = (root: HTMLElement, snapshot: ReplaySnapshot): void => {
  const tickButtons = Array.from(root.querySelectorAll<HTMLButtonElement>(".tick"));
  const readout = root.querySelector<HTMLSpanElement>("#time-readout");
  if (tickButtons.length === 0 || !readout) {
    return;
  }

  const updateStep = (step: number): void => {
    const point = snapshot.timeline.find((item) => item.step === step);
    if (!point) {
      return;
    }
    for (const btn of tickButtons) {
      btn.classList.toggle(activeClass, Number(btn.dataset.step) === step);
    }
    readout.textContent = point.aggregateSignal.toFixed(2);
  };

  for (const btn of tickButtons) {
    btn.addEventListener("click", () => {
      const step = Number(btn.dataset.step);
      updateStep(step);
    });
  }

  updateStep(snapshot.timeline[0]?.step ?? 0);
};