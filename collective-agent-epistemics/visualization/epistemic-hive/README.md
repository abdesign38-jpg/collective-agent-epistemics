# Epistemic Hive Visual Replay Starter

This folder contains a standalone Vite + TypeScript starter for a visual replay interface aligned with EXP-002 framing.

## Run

```bash
npm install
npm run dev
```

## Build

```bash
npm run build
```

## Scope and guardrails

- This UI is a repository-backed visualization of committed EXP-002 evidence and derived replay state.
- It reads the frozen scientific manifest and audit artifacts without altering scientific runtime paths.
- It does not make model calls and does not write to the experimental evidence tree.
- Agent epistemic state, transmitted messages, and network evidence state remain distinct in copy and structure.
