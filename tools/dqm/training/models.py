"""
# models.py is a part of the HEPTAPOD package.
# Copyright (C) 2025 HEPTAPOD authors (see AUTHORS for details).
# HEPTAPOD is licensed under the GNU GPL v3 or later, see LICENSE for details.
"""

import json
from typing import Optional

from orchestral.tools.base.tool import BaseTool
from orchestral.tools.base.field_utils import RuntimeField, StateField

SCHEMA_VERSION = "evtjsonl-1.0"


class DQMAutoencoderTrainTool(BaseTool):
    """
    Train a fully-connected autoencoder on reference (good-run) DQM histograms
    for unsupervised anomaly detection in CMS Data Quality Monitoring.

    Autoencoders are the standard approach for CMS DQM anomaly detection (CMS-DP-2020-020)
    because they require only good-run reference data. The model learns to compress and
    reconstruct healthy detector histograms. Anomalous histograms produce high reconstruction
    error at inference time, flagging bad detector channels without labeled bad-run examples.

    Inputs (runtime):
      - train_jsonl: relative path to JSONL with good-run histogram data from DQMIOReaderTool
      - output_dir: relative directory where model weights and training manifest will be saved
      - subsystem: subsystem to train on, e.g. 'Pixel' or 'all'
      - me_name: specific MonitorElement name to train on; 'all' trains one model per unique ME
      - latent_dim: bottleneck dimension of the autoencoder (default: 16)
      - epochs: number of training epochs (default: 50)
      - batch_size: mini-batch size (default: 64)
      - learning_rate: Adam optimizer learning rate (default: 1e-3)
      - val_fraction: fraction of data held out for validation (default: 0.1)

    State:
      - base_directory: sandbox root for all file operations

    Output (JSON):
      {
        "status": "ok",
        "model_path": "<relative path to saved .pt weights>",
        "manifest_path": "<relative path to training manifest JSON>",
        "n_train_samples": <int>,
        "n_val_samples": <int>,
        "final_train_loss": <float>,
        "final_val_loss": <float>
      }
    """

    # Runtime fields
    train_jsonl: str = RuntimeField(
        description="Relative path to JSONL with good-run histogram data from DQMIOReaderTool"
    )
    output_dir: str = RuntimeField(
        description="Relative output directory for model weights and manifest"
    )
    subsystem: str = RuntimeField(
        default="all",
        description="CMS subsystem to train on, e.g. 'Pixel', 'CSC', or 'all'"
    )
    me_name: str = RuntimeField(
        default="all",
        description="MonitorElement name to train on; 'all' trains one model per unique ME"
    )
    latent_dim: int = RuntimeField(
        default=16,
        description="Bottleneck dimension of the autoencoder (default: 16)"
    )
    epochs: int = RuntimeField(default=50, description="Number of training epochs (default: 50)")
    batch_size: int = RuntimeField(default=64, description="Mini-batch size (default: 64)")
    learning_rate: float = RuntimeField(default=1e-3, description="Adam learning rate (default: 0.001)")
    val_fraction: float = RuntimeField(default=0.1, description="Validation fraction (default: 0.1)")

    # State fields
    base_directory: str = StateField(description="Base sandbox root for all file operations")

    def _run(self) -> str:
        # TODO: load histogram JSONL, pad/normalize bin counts to fixed-length vectors,
        # define encoder-decoder architecture with PyTorch nn.Sequential,
        # train with Adam + MSELoss, save .pt checkpoint and manifest JSON.
        raise NotImplementedError


class DQMClassifierTrainTool(BaseTool):
    """
    Train a binary good/bad run classifier on labeled DQM histogram data.

    Unlike the autoencoder (unsupervised), this tool requires labeled training data:
    a JSONL of good-run histograms and a JSONL of bad-run histograms. It trains an
    XGBoost classifier on per-histogram summary statistics (mean, std, skewness,
    kurtosis, chi2 vs reference) to distinguish good from anomalous detector states.

    Inputs (runtime):
      - good_jsonl: relative path to JSONL of certified GOOD run histograms
      - bad_jsonl: relative path to JSONL of certified BAD run histograms
      - output_dir: relative directory for saved model and manifest
      - subsystem: subsystem filter, e.g. 'Pixel' or 'all'
      - me_name: MonitorElement name filter
      - n_estimators: number of XGBoost trees (default: 100)
      - max_depth: maximum tree depth (default: 4)
      - val_fraction: fraction held out for validation (default: 0.2)

    State:
      - base_directory: sandbox root for all file operations

    Output (JSON):
      {
        "status": "ok",
        "model_path": "<relative path>",
        "val_accuracy": <float>,
        "val_auc": <float>,
        "n_good_samples": <int>,
        "n_bad_samples": <int>,
        "feature_importances": {"<feature_name>": <float>, ...}
      }
    """

    # Runtime fields
    good_jsonl: str = RuntimeField(description="Relative path to JSONL of certified GOOD run histograms")
    bad_jsonl: str = RuntimeField(description="Relative path to JSONL of certified BAD run histograms")
    output_dir: str = RuntimeField(description="Relative output directory for model and manifest")
    subsystem: str = RuntimeField(default="all", description="CMS subsystem filter")
    me_name: str = RuntimeField(default="all", description="MonitorElement name filter")
    n_estimators: int = RuntimeField(default=100, description="Number of XGBoost trees (default: 100)")
    max_depth: int = RuntimeField(default=4, description="Maximum tree depth (default: 4)")
    val_fraction: float = RuntimeField(default=0.2, description="Validation fraction (default: 0.2)")

    # State fields
    base_directory: str = StateField(description="Base sandbox root for all file operations")

    def _run(self) -> str:
        # TODO: extract summary statistics (mean, std, skewness, kurtosis, nonzero_frac)
        # from each histogram record, train XGBoost binary classifier, evaluate on
        # validation split, save .joblib checkpoint and manifest with feature importances.
        raise NotImplementedError


class DQMFeatureExtractorTool(BaseTool):
    """
    Extract a fixed-length feature vector from DQM histograms for use in downstream
    ML models or dimensionality reduction and visualization.

    Reads histogram JSONL data from DQMIOReaderTool, computes per-histogram statistical
    features (mean, std, entropy, chi2 vs reference, KL divergence vs reference,
    overflow fraction), and writes one feature-vector record per MonitorElement.
    Output is directly consumable by DQMAutoencoderTrainTool and DQMClassifierTrainTool
    as a pre-processed representation, or by external UMAP/t-SNE visualization tools.

    Inputs (runtime):
      - input_jsonl: relative path to JSONL from DQMIOReaderTool
      - reference_jsonl: optional relative path to reference run JSONL for chi2 and KL divergence
      - output_jsonl: relative path for output feature-vector JSONL
      - subsystem: subsystem filter
      - me_pattern: optional glob pattern to filter MonitorElement names

    State:
      - base_directory: sandbox root for all file operations

    Output (JSON per line):
      {
        "schema": "evtjsonl-1.0",
        "run": <int>,
        "me_name": "<str>",
        "features": {
          "mean": <float>, "std": <float>, "entropy": <float>,
          "overflow_frac": <float>,
          "chi2_vs_ref": <float>,   # if reference_jsonl provided
          "kl_div_vs_ref": <float>  # if reference_jsonl provided
        }
      }
    """

    # Runtime fields
    input_jsonl: str = RuntimeField(description="Relative path to JSONL from DQMIOReaderTool")
    reference_jsonl: Optional[str] = RuntimeField(
        default=None,
        description="Optional relative path to reference run JSONL for chi2 and KL divergence features"
    )
    output_jsonl: str = RuntimeField(description="Relative path for output feature-vector JSONL")
    subsystem: str = RuntimeField(default="all", description="CMS subsystem filter")
    me_pattern: Optional[str] = RuntimeField(
        default=None,
        description="Optional glob pattern for MonitorElement names"
    )

    # State fields
    base_directory: str = StateField(description="Base sandbox root for all file operations")

    def _run(self) -> str:
        # TODO: compute mean, std, entropy, overflow_frac per histogram;
        # if reference_jsonl provided, compute chi2 and KL divergence vs reference;
        # write one feature record per ME to output JSONL.
        raise NotImplementedError
