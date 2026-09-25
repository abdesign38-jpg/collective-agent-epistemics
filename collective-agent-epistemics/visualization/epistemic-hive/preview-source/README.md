# Epistemic Hive v0.4 Preview Source

This directory is reserved for the supplied v0.4 design package.

The production interface uses the repository-backed EXP-002 snapshot and does not load the package fixture as scientific data. The preview source expects these package assets:

- `assets/bee-agent.webp`
- `assets/lab-stage.webp`
- `fragment.template.html`
- `fixture.json`

The two artwork files are referenced by the application at `/assets/bee-agent.webp` and `/assets/lab-stage.webp`. They must be copied into `visualization/epistemic-hive/public/assets/` for the supplied artwork to render. The attachment viewer exposes the files, but this container does not expose their binary bytes as writable filesystem paths.
