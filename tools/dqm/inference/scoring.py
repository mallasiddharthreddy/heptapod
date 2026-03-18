"""
# scoring.py is a part of the HEPTAPOD package.
# Copyright (C) 2025 HEPTAPOD authors (see AUTHORS for details).
# HEPTAPOD is licensed under the GNU GPL v3 or later, see LICENSE for details.
"""

import json
from typing import Optional

from orchestral.tools.base.tool import BaseTool
from orchestral.tools.base.field_utils import RuntimeField, StateField

SCHEMA_VERSION = "evtjsonl-1.0"


class DQMAnomalyScoreTool(BaseTool):
    """
    Score new DQM run histograms with a trained autoencoder and compute
    per-MonitorElement reconstruction error as an anomaly score.

    Loads a trained autoencoder checkpoint (from DQMAutoencoderTrainTool), runs
    inference on a new run's histogram JSONL, and writes per-ME anomaly scores
    (mean squared reconstruction error) to an output JSONL. High reconstruction
    error indicates the histogram deviates significantly from the reference
    distribution the autoencoder was trained on.

    Inputs (runtime):
      - input_jsonl: relative path to JSONL of new-run histograms from DQMIOReaderTool
      - model_path: relative path to trained autoencoder .pt checkpoint
      - output_jsonl: relative path for output anomaly score JSONL
      - threshold: optional float; MEs with score above this are flagged as anomalous

    State:
      - base_directory: sandbox root for all file operations

    Output (JSON per line):
      {
        "schema": "evtjsonl-1.0",
        "run": <int>,
        "me_name": "<str>",
        "anomaly_score": <float>,
        "flagged": <bool>,
        "threshold_used": <float> | null
      }
    """

    # Runtime fields
    input_jsonl: str = RuntimeField(
        description="Relative path to JSONL of new-run histograms from DQMIOReaderTool"
    )
    model_path: str = RuntimeField(
        description="Relative path to trained autoencoder .pt checkpoint from DQMAutoencoderTrainTool"
    )
    output_jsonl: str = RuntimeField(
        description="Relative path for output anomaly score JSONL"
    )
    threshold: Optional[float] = RuntimeField(
        default=None,
        description="Anomaly score threshold; MEs with score above this are flagged anomalous"
    )

    # State fields
    base_directory: str = StateField(description="Base sandbox root for all file operations")

    def _run(self) -> str:
        # TODO: load autoencoder checkpoint, normalize histogram bin counts to match
        # training input_dim, run forward pass, compute MSE reconstruction error per ME,
        # compare against threshold if provided, write scored records to output JSONL.
        raise NotImplementedError


class DQMRunClassifierTool(BaseTool):
    """
    Classify a new CMS run as GOOD or BAD using a trained binary classifier
    (from DQMClassifierTrainTool) applied to per-histogram summary statistics.

    Loads a trained XGBoost classifier, extracts summary features from a new run's
    JSONL, predicts the good/bad label, and reports the prediction probability and
    top contributing features. Faster than the autoencoder and interpretable.

    Inputs (runtime):
      - input_jsonl: relative path to JSONL of new-run histograms
      - model_path: relative path to trained classifier .joblib file
      - output_path: relative path for output classification result JSON

    State:
      - base_directory: sandbox root for all file operations

    Output (JSON):
      {
        "status": "ok",
        "run": <int>,
        "prediction": "GOOD" | "BAD",
        "probability_bad": <float>,
        "top_features": {"<feature_name>": <float>, ...},
        "n_histograms_scored": <int>
      }
    """

    # Runtime fields
    input_jsonl: str = RuntimeField(
        description="Relative path to JSONL of new-run histograms from DQMIOReaderTool"
    )
    model_path: str = RuntimeField(
        description="Relative path to trained classifier .joblib from DQMClassifierTrainTool"
    )
    output_path: str = RuntimeField(
        description="Relative path for the output classification result JSON"
    )

    # State fields
    base_directory: str = StateField(description="Base sandbox root for all file operations")

    def _run(self) -> str:
        # TODO: load joblib classifier, extract per-histogram summary statistics,
        # aggregate across all MEs with median, predict class probabilities,
        # write prediction + feature importances to output JSON.
        raise NotImplementedError


class DQMThresholdTunerTool(BaseTool):
    """
    Tune the anomaly score threshold for DQMAnomalyScoreTool on a validation
    set of known-good and known-bad runs to maximize F1 or recall at a target precision.

    Sweeps candidate threshold values and computes precision, recall, F1, and false
    positive rate at each point. Outputs the recommended threshold and full
    precision-recall curve.

    Inputs (runtime):
      - good_scores_jsonl: relative path to anomaly score JSONL for GOOD runs
      - bad_scores_jsonl: relative path to anomaly score JSONL for BAD runs
      - output_path: relative path for the threshold report JSON
      - optimize_for: 'f1' or 'recall_at_precision' (default: 'f1')
      - min_precision: minimum required precision for 'recall_at_precision' (default: 0.9)
      - n_threshold_steps: number of threshold candidates (default: 100)

    State:
      - base_directory: sandbox root for all file operations

    Output (JSON):
      {
        "status": "ok",
        "recommended_threshold": <float>,
        "at_threshold": {"precision": <float>, "recall": <float>, "f1": <float>},
        "n_good_runs": <int>,
        "n_bad_runs": <int>,
        "pr_curve": [{"threshold": <float>, "precision": <float>, ...}, ...]
      }
    """

    # Runtime fields
    good_scores_jsonl: str = RuntimeField(
        description="Relative path to anomaly score JSONL for certified GOOD runs"
    )
    bad_scores_jsonl: str = RuntimeField(
        description="Relative path to anomaly score JSONL for certified BAD runs"
    )
    output_path: str = RuntimeField(description="Relative path for output threshold report JSON")
    optimize_for: str = RuntimeField(
        default="f1",
        description="Optimization target: 'f1' or 'recall_at_precision'"
    )
    min_precision: float = RuntimeField(
        default=0.9,
        description="Minimum precision required when optimize_for='recall_at_precision'"
    )
    n_threshold_steps: int = RuntimeField(
        default=100,
        description="Number of threshold candidates to evaluate (default: 100)"
    )

    # State fields
    base_directory: str = StateField(description="Base sandbox root for all file operations")

    def _run(self) -> str:
        # TODO: load good and bad anomaly score JSONLs, sweep thresholds from
        # min to max score in n_threshold_steps steps, compute precision/recall/F1/FPR
        # at each point, select threshold per optimize_for criterion, write report.
        raise NotImplementedError
