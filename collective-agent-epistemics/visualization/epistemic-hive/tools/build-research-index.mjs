import { createHash } from "node:crypto";
import { existsSync } from "node:fs";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import { dirname, join, relative, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";

const appRoot = dirname(dirname(fileURLToPath(import.meta.url)));
const projectRoot = resolve(appRoot, "..", "..");
const outputPath = join(appRoot, "src", "data", "generatedResearchIndex.ts");
const sourcePaths = {
  exp001Worlds: "experiments/EXP_001/synthetic_worlds.json",
  pilot002: "experiments/EXP_002/audits/pilots/EXP_002_PILOT_002_AUDIT_v0.1.json",
  gate2a: "experiments/EXP_002/audits/synthesis/EXP_002_SAME_WORLD_SYNTHESIS_v0.1.json",
  gate2b: "experiments/EXP_002/audits/gate_2b/synthesis/EXP_002_GATE_2B_SYNTHESIS_v0.1.json"
};
const protectedProjectPaths = ["experiments", "research", "src", "tests", "schemas"];

const fail = (message) => {
  throw new Error(`Research index generation failed: ${message}`);
};

const assertProjectRoot = () => {
  for (const directory of protectedProjectPaths) {
    const path = join(projectRoot, directory);
    if (!existsSync(path)) fail(`invalid project root; expected ${path} to exist.`);
  }
};

const sha256 = (source) => createHash("sha256").update(source).digest("hex");
const readSource = async (relativePath) => {
  const absolutePath = join(projectRoot, relativePath);
  if (!existsSync(absolutePath)) fail(`required source artifact is missing: ${relativePath}`);
  const source = await readFile(absolutePath, "utf8");
  return { absolutePath, source, value: JSON.parse(source) };
};
const sourceRecord = (relativePath, source) => ({ path: relativePath, sha256: sha256(source) });
const repoRelative = (absolutePath) => relative(projectRoot, absolutePath).split(sep).join("/");
const requireEqual = (actual, expected, label) => {
  if (actual !== expected) fail(`${label}: expected ${expected}, received ${actual}.`);
};

assertProjectRoot();
const loaded = {};
for (const [key, relativePath] of Object.entries(sourcePaths)) loaded[key] = await readSource(relativePath);

const exp001Worlds = loaded.exp001Worlds.value;
const pilot = loaded.pilot002.value;
const gate2a = loaded.gate2a.value;
const gate2b = loaded.gate2b.value;

requireEqual(exp001Worlds.length, 4, "EXP-001 world count");
requireEqual(gate2a.sets.replication_set_001 + gate2a.sets.replication_set_002, gate2a.formal_runs, "Gate 2A denominator");
requireEqual(gate2a.pilot_002_in_formal_denominator, false, "Pilot 002 formal denominator exclusion");
requireEqual(pilot.run_identity.world, gate2a.shared_configuration.world, "Pilot 002 / Gate 2A world identity");
requireEqual(pilot.run_identity.world, "EXP_002_W01", "Pilot 002 world");
requireEqual(gate2b.evidence_layers.w01.formal_runs, gate2a.formal_runs, "Gate 2B W01 formal run count");
requireEqual(gate2b.generalization_summary.n, gate2b.evidence_layers.generalization.worlds, "Gate 2B generalization count");
requireEqual(gate2b.stress_summary.n, gate2b.evidence_layers.stress.worlds, "Gate 2B stress count");
requireEqual(gate2a.formal_runs, 15, "Gate 2A formal runs");
requireEqual(gate2a.sets.replication_set_001, 5, "Gate 2A replication set 001");
requireEqual(gate2a.sets.replication_set_002, 10, "Gate 2A replication set 002");
requireEqual(gate2b.generalization_summary.n, 12, "Gate 2B generalization worlds");
requireEqual(gate2b.stress_summary.n, 8, "Gate 2B stress worlds");

const index = {
  schemaVersion: "0.1",
  authority: "derived visualization metadata; not scientific authority",
  researchQuestion: "As inference depth and inter-agent recursion increase without new independent evidence, what happens to epistemic lineage, calibration, confidence, and convergence?",
  sources: Object.fromEntries(Object.entries(loaded).map(([key, item]) => [key, sourceRecord(sourcePaths[key], item.source)])),
  experiments: {
    exp001: {
      id: "EXP-001",
      evidenceClass: "synthetic",
      realModelEvidence: false,
      worldCount: exp001Worlds.length,
      worlds: exp001Worlds.map((world) => ({
        id: world.world_id,
        truth: world.truth,
        description: world.description,
        evidenceRoots: world.agents
      }))
    },
    exp002: {
      id: "EXP-002",
      evidenceClass: "real-model exploratory and formal archived runs",
      pilot002: {
        experiment: pilot.run_identity.experiment,
        runClass: pilot.run_identity.run_class,
        model: pilot.run_identity.requested_model,
        reasoningEffort: pilot.run_identity.reasoning_effort,
        seed: pilot.run_identity.seed,
        world: pilot.run_identity.world,
        rounds: pilot.run_identity.rounds,
        executionPolicy: pilot.run_identity.execution_policy,
        eventCounts: pilot.call_accounting,
        finalAnswers: pilot.run_identity.final_answers,
        archivePath: pilot.preservation.path,
        formalDenominator: gate2a.pilot_002_in_formal_denominator
      },
      gate2a: {
        world: gate2a.shared_configuration.world,
        formalRuns: gate2a.formal_runs,
        replicationSets: gate2a.sets,
        sharedConfiguration: gate2a.shared_configuration,
        mechanicalResults: gate2a.mechanical_results,
        interpretation: gate2a.interpretation
      },
      gate2b: {
        status: gate2b.status,
        question: gate2b.gate_2b_question,
        evidenceLayers: gate2b.evidence_layers,
        generalization: gate2b.generalization_summary,
        stress: gate2b.stress_summary,
        historicalHypothesisStatus: gate2b.historical_hypothesis_status,
        nullAssessment: gate2b.null_hypothesis_assessment,
        gateAnswer: gate2b.gate_2b_answer,
        notEstablished: gate2b.not_established,
        sourceArtifacts: gate2b.source_artifacts
      }
    }
  },
  consistency: {
    pilot002InFormalDenominator: gate2a.pilot_002_in_formal_denominator,
    gate2aFormalRuns: gate2a.formal_runs,
    gate2bGeneralizationWorlds: gate2b.generalization_summary.n,
    gate2bStressWorlds: gate2b.stress_summary.n,
    pooledDenominator: null
  }
};

await mkdir(dirname(outputPath), { recursive: true });
await writeFile(
  outputPath,
  `// Generated from committed scientific artifacts.\n// Visualization-only projection.\n// Do not edit manually.\nexport const generatedResearchIndex = ${JSON.stringify(index, null, 2)} as const;\n`,
  "utf8"
);

console.log(`Generated ${repoRelative(outputPath)} from ${Object.keys(sourcePaths).length} authoritative artifacts.`);
