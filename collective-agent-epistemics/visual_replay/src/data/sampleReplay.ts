import type { ReplaySnapshot } from "../types/replay";

export const sampleReplay: ReplaySnapshot = {
  experimentId: "EXP-002",
  rootNode: "E1",
  observedAgents: 3,
  depthMode: "Increasing depth",
  caveat:
    "Agent epistemic state is distinct from transmitted message and network evidence state.",
  trajectories: [
    { id: "A", confidence: [0.42, 0.49, 0.56, 0.58, 0.61, 0.63] },
    { id: "B", confidence: [0.38, 0.44, 0.51, 0.53, 0.55, 0.57] },
    { id: "C", confidence: [0.35, 0.4, 0.46, 0.47, 0.49, 0.51] }
  ],
  timeline: [
    { step: 0, evidenceNode: "E1", aggregateSignal: 0.38 },
    { step: 1, evidenceNode: "E1", aggregateSignal: 0.45 },
    { step: 2, evidenceNode: "E1", aggregateSignal: 0.51 },
    { step: 3, evidenceNode: "E1", aggregateSignal: 0.53 },
    { step: 4, evidenceNode: "E1", aggregateSignal: 0.55 },
    { step: 5, evidenceNode: "E1", aggregateSignal: 0.57 }
  ]
};