"""
dqm_anomaly_demo.py — End-to-end DQM anomaly detection demo for HEPTAPOD.

This demo drives an agent through a complete CMS Data Quality Monitoring
anomaly detection workflow on CMS Run 3 open data, from raw DQMIO ROOT files
through a trained autoencoder to a structured alert report for the shift crew.

The 7-phase pipeline demonstrates that the DQM tool group integrates cleanly
with existing HEPTAPOD tools and that the full workflow runs from natural
language instructions to a publication-quality alert report.

Usage:
    python examples/dqm_workflows/dqm_anomaly_demo.py

Pipeline phases:
    Phase 1 — Query Run Registry to identify GOOD (reference) and BAD runs
    Phase 2 — Fetch DQMIO histogram data for reference runs with DQMIOReaderTool
    Phase 3 — Extract statistical features with DQMFeatureExtractorTool
    Phase 4 — Train autoencoder on reference histograms with DQMAutoencoderTrainTool
    Phase 5 — Tune anomaly threshold with DQMThresholdTunerTool
    Phase 6 — Score a new run and generate anomaly report with DQMAnomalyScoreTool
    Phase 7 — Generate shift-crew alert report with DQMAlertGeneratorTool
"""

# TODO: implement full agent demo during GSoC coding period.
# The skeleton below shows the intended tool call sequence.

DEMO_PIPELINE = [
    {
        "phase": 1,
        "tool": "RunRegistryQueryTool",
        "description": "Query CMS Run Registry for runs 370000-370500 in StreamExpress dataset",
        "inputs": {
            "run_min": 370000,
            "run_max": 370500,
            "dataset": "/StreamExpress/Run2023D-Express-v1/DQMIO",
            "subsystems": "Pixel,CSC,ECAL",
            "output_path": "data/run_registry_370000_370500.jsonl",
        },
    },
    {
        "phase": 2,
        "tool": "DQMIOReaderTool",
        "description": "Read Pixel histograms from a certified GOOD run DQMIO file",
        "inputs": {
            "dqmio_path": "data/DQM_V0001_R000370293.root",
            "output_path": "data/run370293_pixel.jsonl",
            "subsystem": "Pixel",
            "run_number": 370293,
            "lumi_section": 0,
        },
    },
    {
        "phase": 3,
        "tool": "DQMFeatureExtractorTool",
        "description": "Extract chi2 and KL divergence features vs reference histogram",
        "inputs": {
            "input_jsonl": "data/run370293_pixel.jsonl",
            "reference_jsonl": "data/run370100_pixel_reference.jsonl",
            "output_jsonl": "data/run370293_pixel_features.jsonl",
            "subsystem": "Pixel",
        },
    },
    {
        "phase": 4,
        "tool": "DQMAutoencoderTrainTool",
        "description": "Train convolutional autoencoder on Pixel reference histograms",
        "inputs": {
            "train_jsonl": "data/good_runs_pixel.jsonl",
            "output_dir": "models/",
            "subsystem": "Pixel",
            "me_name": "all",
            "latent_dim": 16,
            "epochs": 50,
        },
    },
    {
        "phase": 5,
        "tool": "DQMThresholdTunerTool",
        "description": "Tune anomaly threshold on validation good/bad run scores",
        "inputs": {
            "good_scores_jsonl": "data/val_good_scores.jsonl",
            "bad_scores_jsonl": "data/val_bad_scores.jsonl",
            "output_path": "data/threshold_report.json",
            "optimize_for": "f1",
        },
    },
    {
        "phase": 6,
        "tool": "DQMAnomalyScoreTool",
        "description": "Score a new run with the trained autoencoder",
        "inputs": {
            "input_jsonl": "data/run370450_pixel.jsonl",
            "model_path": "models/autoencoder_Pixel_all.pt",
            "output_jsonl": "data/run370450_scores.jsonl",
            "threshold": 0.008,
        },
    },
    {
        "phase": 7,
        "tool": "DQMAlertGeneratorTool",
        "description": "Generate structured shift-crew alert report",
        "inputs": {
            "score_jsonl": "data/run370450_scores.jsonl",
            "output_report": "data/run370450_alert.json",
            "text_report": "data/run370450_alert.txt",
            "top_n": 20,
        },
    },
]

if __name__ == "__main__":
    print("DQM anomaly detection demo pipeline:")
    for step in DEMO_PIPELINE:
        print(f"  Phase {step['phase']}: {step['tool']} — {step['description']}")
    print("\nFull implementation to be completed during GSoC 2026 coding period.")
