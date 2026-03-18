"""
# deploy.py is a part of the HEPTAPOD package.
# Copyright (C) 2025 HEPTAPOD authors (see AUTHORS for details).
# HEPTAPOD is licensed under the GNU GPL v3 or later, see LICENSE for details.
"""

import json
from typing import Optional

from orchestral.tools.base.tool import BaseTool
from orchestral.tools.base.field_utils import RuntimeField, StateField

SCHEMA_VERSION = "evtjsonl-1.0"


class DQMModelRegistryTool(BaseTool):
    """
    Register a trained DQM model into the local model registry, versioning it with
    metadata and making it discoverable by inference tools via registry lookup.

    The registry is a simple JSON index at <base_directory>/dqm_model_registry.json.
    Each entry records the model path, type, subsystem, ME name, training date,
    performance metrics, and recommended anomaly threshold. Inference tools can query
    this registry to find the latest model for a given subsystem without hardcoding paths.

    Inputs (runtime):
      - model_path: relative path to the model file to register (.pt or .joblib)
      - model_type: 'autoencoder' or 'classifier'
      - subsystem: CMS subsystem this model covers, e.g. 'Pixel'
      - me_name: MonitorElement name this model covers
      - performance_metrics: JSON string of key metrics, e.g. '{"val_loss": 0.003}'
      - recommended_threshold: optional anomaly threshold from DQMThresholdTunerTool
      - notes: optional free-text notes about this model version

    State:
      - base_directory: sandbox root for all file operations

    Output (JSON):
      {
        "status": "ok",
        "registry_entry_id": "<str>",
        "registry_path": "<str>",
        "n_models_in_registry": <int>
      }
    """

    # Runtime fields
    model_path: str = RuntimeField(description="Relative path to model file (.pt or .joblib)")
    model_type: str = RuntimeField(description="Model type: 'autoencoder' or 'classifier'")
    subsystem: str = RuntimeField(description="CMS subsystem this model covers, e.g. 'Pixel'")
    me_name: str = RuntimeField(default="all", description="MonitorElement name this model covers")
    performance_metrics: str = RuntimeField(
        default="{}",
        description="JSON string of key performance metrics, e.g. '{\"val_loss\": 0.003}'"
    )
    recommended_threshold: Optional[float] = RuntimeField(
        default=None,
        description="Optional anomaly score threshold from DQMThresholdTunerTool"
    )
    notes: Optional[str] = RuntimeField(default=None, description="Optional notes about this model version")

    # State fields
    base_directory: str = StateField(description="Base sandbox root for all file operations")

    def _run(self) -> str:
        # TODO: load or initialize dqm_model_registry.json, append new entry with
        # model metadata and timestamp, write updated registry back to disk.
        raise NotImplementedError


class DQMLiveMonitorTool(BaseTool):
    """
    Poll a CMSSW harvesting output directory for new DQMIO ROOT files and score
    histograms in near-real-time during an active CMS data-taking run.

    CMSSW DQM harvesting writes histogram ROOT files as lumisections complete.
    This tool watches that directory, runs DQMIOReaderTool and DQMAnomalyScoreTool
    on each new file, and appends results to a running anomaly log. Designed to
    run alongside the harvesting workflow for online monitoring.

    Inputs (runtime):
      - harvest_dir: relative path to CMSSW harvesting output directory to watch
      - model_path: relative path to trained autoencoder .pt checkpoint
      - output_log: relative path for the running anomaly log JSONL
      - subsystem: subsystem to monitor, e.g. 'Pixel' or 'all'
      - threshold: anomaly score threshold for flagging
      - poll_interval_seconds: seconds between directory polls (default: 10)
      - max_lumisections: maximum lumi-sections to process before stopping (default: 100)
      - timeout_seconds: maximum total wall time (default: 3600)

    State:
      - base_directory: sandbox root for all file operations

    Output (JSON):
      {
        "status": "ok" | "timeout",
        "n_lumisections_processed": <int>,
        "n_anomalies_flagged": <int>,
        "output_log": "<str>"
      }
    """

    # Runtime fields
    harvest_dir: str = RuntimeField(description="Relative path to CMSSW harvesting output directory")
    model_path: str = RuntimeField(description="Relative path to trained autoencoder .pt checkpoint")
    output_log: str = RuntimeField(description="Relative path for the running anomaly log JSONL")
    subsystem: str = RuntimeField(default="all", description="CMS subsystem to monitor")
    threshold: float = RuntimeField(default=0.01, description="Anomaly score threshold (default: 0.01)")
    poll_interval_seconds: int = RuntimeField(default=10, description="Seconds between polls (default: 10)")
    max_lumisections: int = RuntimeField(default=100, description="Max lumi-sections to process (default: 100)")
    timeout_seconds: int = RuntimeField(default=3600, description="Max wall time in seconds (default: 3600)")

    # State fields
    base_directory: str = StateField(description="Base sandbox root for all file operations")

    def _run(self) -> str:
        # TODO: poll harvest_dir for new .root files, for each new file call
        # DQMIOReaderTool then DQMAnomalyScoreTool inline, append flagged MEs to
        # output_log, respect poll_interval_seconds and timeout_seconds limits.
        raise NotImplementedError


class DQMAlertGeneratorTool(BaseTool):
    """
    Read a DQM anomaly score log and generate a structured alert report summarizing
    which runs, subsystems, and MonitorElements were flagged as anomalous.

    Aggregates flagged records from DQMAnomalyScoreTool or DQMLiveMonitorTool output,
    groups by subsystem and ME name, ranks by anomaly score, and outputs both a JSON
    summary and an optional plain-text shift-crew report. This is the final deliverable
    in the DQM pipeline — the document a shift physicist receives.

    Inputs (runtime):
      - score_jsonl: relative path to anomaly score JSONL from DQMAnomalyScoreTool
      - output_report: relative path for the JSON alert report
      - text_report: optional relative path for a plain-text shift-crew report
      - top_n: number of top anomalous MEs to include in the summary (default: 20)
      - min_score: minimum anomaly score to include in the report (default: 0.0)

    State:
      - base_directory: sandbox root for all file operations

    Output (JSON):
      {
        "status": "ok",
        "run": <int>,
        "n_total_mes": <int>,
        "n_flagged": <int>,
        "top_anomalies": [{"me_name": "<str>", "subsystem": "<str>", "anomaly_score": <float>}, ...],
        "by_subsystem": {"<subsystem>": {"n_flagged": <int>, "max_score": <float>}}
      }
    """

    # Runtime fields
    score_jsonl: str = RuntimeField(
        description="Relative path to anomaly score JSONL from DQMAnomalyScoreTool"
    )
    output_report: str = RuntimeField(description="Relative path for the JSON alert report")
    text_report: Optional[str] = RuntimeField(
        default=None,
        description="Optional relative path for a plain-text shift-crew summary report"
    )
    top_n: int = RuntimeField(default=20, description="Number of top anomalous MEs to include (default: 20)")
    min_score: float = RuntimeField(default=0.0, description="Minimum anomaly score to include (default: 0.0)")

    # State fields
    base_directory: str = StateField(description="Base sandbox root for all file operations")

    def _run(self) -> str:
        # TODO: read score JSONL, group flagged records by subsystem and ME name,
        # sort by anomaly score descending, build top_n list, write JSON report
        # and optional plain-text shift-crew summary to output paths.
        raise NotImplementedError
