export type AgentId = "A" | "B" | "C";

export interface AgentTrajectory {
  id: AgentId;
  confidence: number[];
}

export interface ReplayPoint {
  step: number;
  evidenceNode: string;
  aggregateSignal: number;
}

export interface ReplaySnapshot {
  experimentId: string;
  rootNode: string;
  observedAgents: number;
  depthMode: string;
  trajectories: AgentTrajectory[];
  timeline: ReplayPoint[];
  caveat: string;
}