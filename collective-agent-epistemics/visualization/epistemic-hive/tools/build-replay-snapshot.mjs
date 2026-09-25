import { createHash } from "node:crypto";
import { existsSync } from "node:fs";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import { dirname, join, relative, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";

const appRoot = dirname(dirname(fileURLToPath(import.meta.url)));
const projectRoot = resolve(appRoot, "..", "..");
const experimentRoot = join(projectRoot, "experiments", "EXP_002");

const assertProjectRoot = () => {
  const requiredPaths = [
    join(projectRoot, "experiments"),
    join(projectRoot, "research"),
    join(projectRoot, "src"),
    join(projectRoot, "tests"),
    join(projectRoot, "schemas")
  ];

  for (const required of requiredPaths) {
    if (!existsSync(required)) {
      throw new Error(`Invalid project root: expected ${required} to exist, resolved to ${projectRoot}.`);
    }
  }
};

assertProjectRoot();
const manifestPath = join(experimentRoot, "GATE_2B_WORLD_MANIFEST_v0.1.json");
const auditPaths = {
  generalization: join(experimentRoot, "audits", "gate_2b", "generalization_set_001", "EXP_002_GATE_2B_GENERALIZATION_SET_001_PRIMARY_OUTCOME_AUDIT_v0.1.json"),
  stress: join(experimentRoot, "audits", "gate_2b", "stress_set_001", "EXP_002_GATE_2B_STRESS_SET_001_PRIMARY_OUTCOME_AUDIT_v0.1.json")
};
const outputPath = join(appRoot, "src", "data", "generatedReplay.ts");

const sha256 = (value) => createHash("sha256").update(value).digest("hex");

const readJsonLines = async (path) => {
  const source = await readFile(path, "utf8");
  return {
    source,
    records: source.trim().split("\n").filter(Boolean).map((line) => JSON.parse(line))
  };
};

const projectEvent = (event) => ({
  id: event.visible_message_id,
  condition: event.condition,
  sender: event.sender,
  receiver: event.receiver,
  message: event.agent_message.content,
  answer: event.model_output.answer,
  confidence: event.metrics.confidence,
  pA: event.metrics.p_a,
  brierScore: event.metrics.brier_score,
  roots: event.actual_lineage.actual_roots,
  derivedFrom: event.actual_lineage.derived_from,
  depth: event.actual_lineage.inference_depth,
  newExternalEvidence: event.actual_lineage.new_external_evidence,
  responseReused: event.response_reused
});

const hasSameRootRegrounding = (event) => event.sender === "A"
  && event.actual_lineage.actual_roots?.length === 1
  && event.actual_lineage.actual_roots[0] === "E1"
  && event.actual_lineage.new_external_evidence === false
  && event.model_visible_input.includes("Direct observation:");

const setDefinitions = [
  { key: "generalization_set_001", id: "generalization", label: "Generalization" },
  { key: "stress_set_001", id: "stress", label: "Stress" }
];

if (!existsSync(manifestPath)) {
  throw new Error(`Manifest not found at expected project path: ${manifestPath}`);
}

for (const [set, path] of Object.entries(auditPaths)) {
  if (!existsSync(path)) {
    throw new Error(`Audit file not found for ${set}: ${path}`);
  }
}

const manifestSource = await readFile(manifestPath, "utf8");
const manifest = JSON.parse(manifestSource);
const audits = {};
for (const [set, path] of Object.entries(auditPaths)) {
  audits[set] = JSON.parse(await readFile(path, "utf8"));
}
const worlds = [];

for (const definition of setDefinitions) {
  for (const world of manifest[definition.key].worlds) {
    const auditRecord = audits[definition.id].world_records.find((record) => record.canonical_world_id === world.canonical_world_id);
    if (!auditRecord) throw new Error(`Missing audit record for ${world.canonical_world_id}.`);
    const attempt = auditRecord.authoritative_attempt;
    const archiveRelativePath = join(
      auditRecord.archive_path,
      "events.jsonl"
    );
    const { source, records } = await readJsonLines(join(projectRoot, archiveRelativePath));
    const conditions = Object.fromEntries(
      ["free", "lineage", "macro"].map((condition) => [
        condition,
        records.filter((event) => event.condition === condition).map((event) => ({
          ...projectEvent(event),
          sameRootRegrounding: hasSameRootRegrounding(event)
        }))
      ])
    );

    if (conditions.free.length !== 13 || conditions.lineage.length !== 13 || conditions.macro.length !== 4) {
      throw new Error(`Unexpected condition counts for ${world.canonical_world_id}.`);
    }
    const pairedDifferences = conditions.free.map((event, index) => {
      const other = conditions.lineage[index];
      return event.answer !== other.answer || event.confidence !== other.confidence || event.pA !== other.pA;
    });

    worlds.push({
      id: world.canonical_world_id,
      set: definition.id,
      setLabel: definition.label,
      truth: world.truth,
      observed: world.observed_state,
      alignment: world.evidence_alignment,
      sensorReliability: world.sensor_reliability,
      evidenceRoot: world.evidence_root,
      finalDifference: pairedDifferences.at(-1) ?? false,
      trajectoryDifference: pairedDifferences.some(Boolean),
      archivePath: auditRecord.archive_path,
      attempt,
      auditPath: relative(projectRoot, auditPaths[definition.id]).split(sep).join("/"),
      sourceHash: sha256(source),
      conditions
    });
  }
}

if (worlds.length !== 20) {
  throw new Error(`Expected 20 valid Gate 2B worlds, received ${worlds.length}.`);
}

const snapshot = {
  manifestHash: sha256(manifestSource),
  sourceManifest: "experiments/EXP_002/GATE_2B_WORLD_MANIFEST_v0.1.json",
  totals: { generalization: 12, stress: 8, events: 600, validProviderCalls: 500, reusedResponses: 80 },
  worlds
};

await mkdir(dirname(outputPath), { recursive: true });
await writeFile(
  outputPath,
  `// Generated by tools/build-replay-snapshot.mjs. Do not edit manually.\nexport const generatedReplay = ${JSON.stringify(snapshot, null, 2)} as const;\n`,
  "utf8"
);

console.log(`Generated ${outputPath} from ${worlds.length} valid Gate 2B worlds.`);