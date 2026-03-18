# DQM Anomaly Detection — 7-Phase Todo Pipeline

This todo list drives a HEPTAPOD agent through a complete CMS Data Quality
Monitoring anomaly detection workflow. Each phase maps to one or more tools
in the `tools/dqm/` group and produces a concrete artifact that the next
phase consumes.

---

## Phase 1 — Run Registry Query

Use `RunRegistryQueryTool` to query the CMS Run Registry for runs 370000
through 370500 in the `/StreamExpress/Run2023D-Express-v1/DQMIO` dataset.
Include subsystems: Pixel, CSC, ECAL.
Save output to `data/run_registry_370000_370500.jsonl`.
Identify which runs are certified GOOD (for training reference) and which
are certified BAD (for validation and threshold tuning).

---

## Phase 2 — DQMIO Data Ingestion

Use `DQMIOReaderTool` on at least 5 certified GOOD runs to read Pixel
subsystem histograms. For each run, write the MonitorElement histogram data
to `data/good_runs_pixel.jsonl`. Use `run_number` matching each GOOD run
identified in Phase 1. Set `lumi_section=0` for run-level MEs only.

Also read at least 2 certified BAD runs to `data/bad_runs_pixel.jsonl`
for use in threshold tuning in Phase 5.

---

## Phase 3 — Feature Extraction

Use `DQMFeatureExtractorTool` on the good-run JSONL from Phase 2.
Use the earliest GOOD run as the reference histogram for chi2 and KL
divergence features. Write output to `data/good_runs_pixel_features.jsonl`.
Repeat for bad runs, writing to `data/bad_runs_pixel_features.jsonl`.

---

## Phase 4 — Autoencoder Training

Use `DQMAutoencoderTrainTool` with:
- `train_jsonl` = `data/good_runs_pixel.jsonl`
- `output_dir` = `models/`
- `subsystem` = `Pixel`
- `me_name` = `all`
- `latent_dim` = 16
- `epochs` = 50
- `val_fraction` = 0.1

Confirm that `final_val_loss` is lower than `final_train_loss` (no overfitting).
Register the trained model with `DQMModelRegistryTool`.

---

## Phase 5 — Score Validation Runs and Tune Threshold

Run `DQMAnomalyScoreTool` on the good-run JSONL and the bad-run JSONL
separately (without a threshold) to produce:
- `data/val_good_scores.jsonl`
- `data/val_bad_scores.jsonl`

Then use `DQMThresholdTunerTool` with `optimize_for=f1` to find the optimal
anomaly threshold. Save the threshold report to `data/threshold_report.json`.
Record the `recommended_threshold` for use in Phase 6.

---

## Phase 6 — Score a New Run

Use `DQMIOReaderTool` to read Pixel histograms for a run NOT seen during
training (e.g. run 370450). Write to `data/run370450_pixel.jsonl`.

Use `DQMAnomalyScoreTool` with:
- `model_path` = the autoencoder .pt from Phase 4
- `threshold` = the `recommended_threshold` from Phase 5
- `output_jsonl` = `data/run370450_scores.jsonl`

Confirm the output contains `flagged: true` entries if the run was BAD,
or all `flagged: false` if the run was GOOD.

---

## Phase 7 — Generate Alert Report

Use `DQMAlertGeneratorTool` on the score JSONL from Phase 6:
- `output_report` = `data/run370450_alert.json`
- `text_report` = `data/run370450_alert.txt`
- `top_n` = 20

Read the text report and confirm it lists the top anomalous MonitorElements
with subsystem labels, anomaly scores, and a by-subsystem summary.
This is the deliverable that a shift-crew physicist would receive.
