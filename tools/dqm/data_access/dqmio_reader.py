"""
# dqmio_reader.py is a part of the HEPTAPOD package.
# Copyright (C) 2025 HEPTAPOD authors (see AUTHORS for details).
# HEPTAPOD is licensed under the GNU GPL v3 or later, see LICENSE for details.
"""

import json
from typing import Optional

from orchestral.tools.base.tool import BaseTool
from orchestral.tools.base.field_utils import RuntimeField, StateField

SCHEMA_VERSION = "evtjsonl-1.0"


class DQMIOReaderTool(BaseTool):
    """
    Read CMS DQM histograms from a DQMIO ROOT file and write them to evtjsonl-1.0 format.

    DQMIO ROOT files contain per-run and per-lumi MonitorElement histograms for every
    CMS detector subsystem. This tool reads those histograms using uproot, extracts bin
    counts and edges, and writes one JSON line per MonitorElement to a JSONL output file
    compatible with all downstream HEPTAPOD analysis tools.

    Inputs (runtime):
      - dqmio_path: path (relative to base_directory) to a DQMIO ROOT file (.root)
      - output_path: relative path for the output JSONL file
      - subsystem: CMS subsystem filter, e.g. 'Pixel', 'CSC', 'ECAL', 'all'
      - run_number: integer run number to extract
      - lumi_section: lumi section to extract; 0 means run-level MEs only
      - me_pattern: optional glob pattern to filter MonitorElement names

    State:
      - base_directory: sandbox root for all file operations

    Output (JSON per line, evtjsonl-1.0):
      {
        "schema": "evtjsonl-1.0",
        "run": <int>,
        "lumi": <int>,
        "subsystem": "<str>",
        "me_name": "<str>",
        "me_type": "TH1F" | "TH2F" | "TProfile" | "scalar",
        "data": {
          "bin_edges_x": [...],
          "bin_edges_y": [...],
          "counts": [...],
          "entries": <int>
        }
      }
    """

    # Runtime fields
    dqmio_path: str = RuntimeField(
        description="Relative path to DQMIO ROOT file, e.g. 'data/DQM_V0001_R000370293.root'"
    )
    output_path: str = RuntimeField(
        description="Relative path for output JSONL file, e.g. 'data/run370293_dqm.jsonl'"
    )
    subsystem: str = RuntimeField(
        default="all",
        description="CMS subsystem to extract: 'Pixel', 'CSC', 'ECAL', 'HCAL', 'Muon', 'all'"
    )
    run_number: int = RuntimeField(
        description="CMS run number to extract from the DQMIO file, e.g. 370293"
    )
    lumi_section: int = RuntimeField(
        default=0,
        description="Lumi section to extract; 0 means run-level MonitorElements only"
    )
    me_pattern: Optional[str] = RuntimeField(
        default=None,
        description="Optional glob pattern for MonitorElement names"
    )

    # State fields
    base_directory: str = StateField(
        description="Base sandbox root for all file operations"
    )

    def _run(self) -> str:
        # TODO: implement DQMIO ROOT reading via uproot, extract histogram bin counts
        # and edges per MonitorElement, write one evtjsonl-1.0 line per ME.
        raise NotImplementedError


class RunRegistryQueryTool(BaseTool):
    """
    Query the CMS Run Registry to retrieve run metadata and data certification flags.

    The CMS Run Registry is the authoritative database for run quality flags. Each run
    has per-subsystem certification: GOOD, BAD, NOTSET, or EXCLUDED. This tool queries
    the Run Registry REST API and returns structured metadata including lumi delivered,
    recorded, and per-subsystem DQM flags.

    Use this tool before training to identify GOOD runs (training reference) and BAD
    runs (validation/threshold tuning examples).

    Inputs (runtime):
      - run_min: first run number in range, e.g. 368000
      - run_max: last run number in range, e.g. 370000
      - dataset: CMS dataset name, e.g. '/StreamExpress/Run2023D-Express-v1/DQMIO'
      - subsystems: comma-separated subsystem names, e.g. 'Pixel,CSC,ECAL'
      - output_path: relative path to write the output JSONL

    State:
      - base_directory: sandbox root for all file operations

    Output (JSON per line):
      {
        "run": <int>,
        "fill": <int>,
        "lumi_delivered_pb": <float>,
        "lumi_recorded_pb": <float>,
        "certification": {
          "Pixel": "GOOD" | "BAD" | "NOTSET",
          ...
        }
      }
    """

    # Runtime fields
    run_min: int = RuntimeField(description="First run number of query range, e.g. 368000")
    run_max: int = RuntimeField(description="Last run number of query range, e.g. 370000")
    dataset: str = RuntimeField(
        default="/StreamExpress/Run2023D-Express-v1/DQMIO",
        description="CMS dataset string for the Run Registry query"
    )
    subsystems: str = RuntimeField(
        default="Pixel,CSC,ECAL,HCAL,Muon",
        description="Comma-separated subsystem names to include in the output"
    )
    output_path: str = RuntimeField(
        description="Relative path to write the output JSONL"
    )

    # State fields
    base_directory: str = StateField(description="Base sandbox root for all file operations")

    def _run(self) -> str:
        # TODO: implement Run Registry REST API query, parse per-subsystem
        # certification flags, write per-run records to JSONL output.
        raise NotImplementedError


class OMSQueryTool(BaseTool):
    """
    Query the CMS Online Monitoring System (OMS) API for run and lumisection metadata.

    OMS is the primary source for online detector conditions: luminosity, pileup,
    trigger rates, beam energy, and run duration. This tool queries the OMS REST API
    and returns structured per-run or per-lumi metadata that can be joined with DQMIO
    histogram data to condition DQM anomaly models on detector operating state.

    Inputs (runtime):
      - query_type: 'runs' or 'lumisections'
      - run_number: run number for lumisections query
      - run_min: lower bound for runs query
      - run_max: upper bound for runs query
      - fields: comma-separated OMS field names to retrieve
      - output_path: relative path to write output JSONL

    State:
      - base_directory: sandbox root for all file operations

    Output (JSON per line):
      {
        "run": <int>,
        "lumi": <int>,
        "b_field_T": <float>,
        "pileup": <float>,
        "lumi_inst_hz_ub": <float>,
        "cms_active": <bool>
      }
    """

    # Runtime fields
    query_type: str = RuntimeField(
        default="runs",
        description="Query type: 'runs' for per-run metadata, 'lumisections' for per-lumi data"
    )
    run_number: Optional[int] = RuntimeField(
        default=None,
        description="Run number for lumisections query, e.g. 370293"
    )
    run_min: Optional[int] = RuntimeField(
        default=None,
        description="Lower run bound for runs query"
    )
    run_max: Optional[int] = RuntimeField(
        default=None,
        description="Upper run bound for runs query"
    )
    fields: str = RuntimeField(
        default="run_number,b_field,fill_number,pileup,init_lumi,recorded_lumi",
        description="Comma-separated OMS field names to retrieve"
    )
    output_path: str = RuntimeField(
        description="Relative path to write output JSONL"
    )

    # State fields
    base_directory: str = StateField(description="Base sandbox root for all file operations")

    def _run(self) -> str:
        # TODO: implement OMS API v3 query, paginate results, write per-record
        # JSONL output with requested field subset.
        raise NotImplementedError
