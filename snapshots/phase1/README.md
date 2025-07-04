# Phase 1 Pipeline Snapshot

This folder contains a reproducible snapshot of the PriceIQ pipeline as of PHASE 1.

## Contents

- `final_config.yaml`: The exact working configuration used by the orchestrator for this run.
- `final_input.json`: The input JSON used for the pipeline run (country: US, query: "iPhone 16 Pro, 128GB").
- `final_output.json`: The output product list returned by the pipeline for the above input.
- `final_logs.txt`: Full logs of the pipeline run, including step-by-step details and output.

## How to Re-run This Snapshot

To reproduce this run:

1. Ensure your working directory is the project root.
2. Run:
   ```bash
   python3 main.py --query "iPhone 16 Pro, 128GB" --country "US"
   ```
   Or, using the input file:
   ```bash
   python3 main.py --input snapshots/phase1/final_input.json
   ```

## When Was This Captured?

- Date: <!-- Fill in date/time here -->
- Codebase: Phase 1, with all modules in mock mode, and US/IN/UK/DE support

## What Config Was Used?

- See `final_config.yaml` for the full configuration, including all mock data, country/site support, and module toggles.

---

This snapshot is intended for reproducibility, debugging, and documentation of the pipeline's behavior at this stage. 