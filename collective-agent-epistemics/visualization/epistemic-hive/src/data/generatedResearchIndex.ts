// Generated from committed scientific artifacts.
// Visualization-only projection.
// Do not edit manually.
export const generatedResearchIndex = {
  "schemaVersion": "0.1",
  "authority": "derived visualization metadata; not scientific authority",
  "researchQuestion": "As inference depth and inter-agent recursion increase without new independent evidence, what happens to epistemic lineage, calibration, confidence, and convergence?",
  "sources": {
    "exp001Worlds": {
      "path": "experiments/EXP_001/synthetic_worlds.json",
      "sha256": "17ef3ff3196968b559817d92a8194149da82c8793a9577ffe3fc813d820bb8c2"
    },
    "pilot002": {
      "path": "experiments/EXP_002/audits/pilots/EXP_002_PILOT_002_AUDIT_v0.1.json",
      "sha256": "0c3b89501bbe53a914bcc9d60b6eaa49e5e5b35287d55366ded649f80a03a873"
    },
    "gate2a": {
      "path": "experiments/EXP_002/audits/synthesis/EXP_002_SAME_WORLD_SYNTHESIS_v0.1.json",
      "sha256": "f809cd0d7b39228b50806607d3d21facbdc26e2709410c59fbdcffcf3cb15ce6"
    },
    "gate2b": {
      "path": "experiments/EXP_002/audits/gate_2b/synthesis/EXP_002_GATE_2B_SYNTHESIS_v0.1.json",
      "sha256": "8a6635d5e4473be2fc2b149a6d9619448d1e22081ca7d6787d286c58e608aeb4"
    }
  },
  "experiments": {
    "exp001": {
      "id": "EXP-001",
      "evidenceClass": "synthetic",
      "realModelEvidence": false,
      "worldCount": 4,
      "worlds": [
        {
          "id": "W1_single_root",
          "truth": "A",
          "description": "Only Agent A receives one external evidence root supporting A.",
          "evidenceRoots": {
            "A": [
              {
                "evidence_id": "E1",
                "supports_state": "A",
                "reliability": 0.7,
                "source": "sensor_1"
              }
            ],
            "B": [],
            "C": []
          }
        },
        {
          "id": "W2_two_independent_roots",
          "truth": "A",
          "description": "Agents A and B each receive independent evidence supporting A.",
          "evidenceRoots": {
            "A": [
              {
                "evidence_id": "E1",
                "supports_state": "A",
                "reliability": 0.7,
                "source": "sensor_1"
              }
            ],
            "B": [
              {
                "evidence_id": "E2",
                "supports_state": "A",
                "reliability": 0.65,
                "source": "sensor_2"
              }
            ],
            "C": []
          }
        },
        {
          "id": "W3_conflicting_roots",
          "truth": "A",
          "description": "Independent evidence conflicts: A receives pro-A evidence and B pro-B evidence.",
          "evidenceRoots": {
            "A": [
              {
                "evidence_id": "E1",
                "supports_state": "A",
                "reliability": 0.72,
                "source": "sensor_1"
              }
            ],
            "B": [
              {
                "evidence_id": "E2",
                "supports_state": "B",
                "reliability": 0.62,
                "source": "sensor_2"
              }
            ],
            "C": []
          }
        },
        {
          "id": "W4_misleading_single_root",
          "truth": "B",
          "description": "A single observed signal supports A, but ground truth is B. Tests confidently-wrong amplification.",
          "evidenceRoots": {
            "A": [
              {
                "evidence_id": "E1",
                "supports_state": "A",
                "reliability": 0.7,
                "source": "sensor_1"
              }
            ],
            "B": [],
            "C": []
          }
        }
      ]
    },
    "exp002": {
      "id": "EXP-002",
      "evidenceClass": "real-model exploratory and formal archived runs",
      "pilot002": {
        "experiment": "EXP-002",
        "runClass": "pilot_real_model",
        "model": "gpt-5.6-sol",
        "reasoningEffort": "medium",
        "seed": 42,
        "world": "EXP_002_W01",
        "rounds": 4,
        "executionPolicy": "paired",
        "eventCounts": {
          "actual_model_call_count": 25,
          "expected_model_call_count": 25,
          "shared_seed_calls": 1,
          "free_post_seed_calls": 12,
          "lineage_post_seed_calls": 12,
          "macro_independent_calls": 0,
          "reused_response_count": 4,
          "macro_reused_ids": [
            "M01",
            "M02",
            "M03",
            "M04"
          ],
          "input_tokens_actual": 4450,
          "output_tokens_actual": 2821,
          "total_tokens_actual": 7271
        },
        "finalAnswers": {
          "free": "A",
          "lineage": "A",
          "macro": "A"
        },
        "archivePath": "experiments/EXP_002/results/archive/pilots/pilot_002_seed42_r4/",
        "formalDenominator": false
      },
      "gate2a": {
        "world": "EXP_002_W01",
        "formalRuns": 15,
        "replicationSets": {
          "replication_set_001": 5,
          "replication_set_002": 10
        },
        "sharedConfiguration": {
          "model": "gpt-5.6-sol",
          "reasoning_effort": "medium",
          "world": "EXP_002_W01",
          "seed": 42,
          "sensor_reliability": 0.7,
          "truth": "A",
          "observed_state": "A",
          "execution_policy": "paired",
          "rounds": 4,
          "protocol": "EXP-002 v0.1"
        },
        "mechanicalResults": {
          "lineage_discount_runs": 12,
          "lineage_discount_run_denominator": 15,
          "free_drift_runs": 0,
          "free_drift_denominator": 15,
          "lineage_discount_events": 17,
          "actors": {
            "A": 0,
            "B": 7,
            "C": 10
          },
          "confidence_inflation_events": 0,
          "answer_flips": 0,
          "free_dependency_recognition_runs": 15,
          "macro_stopped_after_one_cycle_runs": 15
        },
        "interpretation": {
          "same_world_stochastic_reproducibility": true,
          "generalization": false,
          "causality": false,
          "recursion_alone": false,
          "emerging_question": "Does explicit representation of evidence dependency change evidence valuation as inferential distance grows, and is periodic direct evidence access responsible for the observed source/non-source difference?"
        }
      },
      "gate2b": {
        "status": "CLOSED_UNDER_FROZEN_V0_1_DESIGN",
        "question": "Do the architecture-dependent epistemic behaviors observed under W01 survive when the external world/evidence realization changes while the frozen EXP-002 communication protocol remains otherwise controlled?",
        "evidenceLayers": {
          "w01": {
            "formal_runs": 15,
            "role": "same-world same-model same-protocol stochastic reproducibility",
            "in_generalization_denominator": false
          },
          "generalization": {
            "worlds": 12,
            "role": "prospectively unfiltered multi-world/evidence-realization component"
          },
          "stress": {
            "worlds": 8,
            "role": "prospectively stratified conditional robustness component",
            "cells": {
              "A/A": 2,
              "B/B": 2,
              "A/B": 2,
              "B/A": 2
            }
          }
        },
        "generalization": {
          "n": 12,
          "aligned": 5,
          "misleading": 7,
          "accuracy_free": "5/12",
          "accuracy_lineage": "5/12",
          "final_answer_agreement_free_lineage": "12/12",
          "interpretation": "Mixed/conditional: transient differences occur in some worlds and one final FREE confidence/Brier divergence is recorded, while many worlds have equal final outcomes."
        },
        "stress": {
          "n": 8,
          "cells": {
            "A/A": 2,
            "B/B": 2,
            "A/B": 2,
            "B/A": 2
          },
          "final_architecture_equality_within_worlds": "8/8",
          "transient_trajectory_differences": "present in some B/B and B/A worlds",
          "interpretation": "Cell-conditional final equality with conditional transient trajectory variation."
        },
        "historicalHypothesisStatus": "ACTIVE / FALSIFIABLE / NOT ESTABLISHED",
        "nullAssessment": "NOT REJECTED BY THIS DESIGN / REMAINS VIABLE; Gate 2B lacks a clean non-interaction control separating individual-model stochastic behavior from interaction-induced degradation.",
        "gateAnswer": "W01-like architecture-dependent behavior survives only conditionally and stochastically in primary trajectories when world/evidence realization changes; no uniform persistent final-state architecture effect is established.",
        "notEstablished": [
          "Causality",
          "Population prevalence",
          "Global superiority of FREE, LINEAGE, or MACRO",
          "Lineage loss",
          "Evidence double counting",
          "Source correctness from dependency metadata",
          "Historical hypothesis confirmation"
        ],
        "sourceArtifacts": {
          "w01": "experiments/EXP_002/audits/synthesis/EXP_002_SAME_WORLD_SYNTHESIS_v0.1.*",
          "generalization": "experiments/EXP_002/audits/gate_2b/generalization_set_001/EXP_002_GATE_2B_GENERALIZATION_SET_001_PRIMARY_OUTCOME_AUDIT_v0.1.*",
          "stress": "experiments/EXP_002/audits/gate_2b/stress_set_001/EXP_002_GATE_2B_STRESS_SET_001_PRIMARY_OUTCOME_AUDIT_v0.1.*",
          "corpus": "experiments/EXP_002/audits/gate_2b/corpus/EXP_002_GATE_2B_CORPUS_AUDIT_v0.1.*"
        }
      }
    }
  },
  "consistency": {
    "pilot002InFormalDenominator": false,
    "gate2aFormalRuns": 15,
    "gate2bGeneralizationWorlds": 12,
    "gate2bStressWorlds": 8,
    "pooledDenominator": null
  }
} as const;
