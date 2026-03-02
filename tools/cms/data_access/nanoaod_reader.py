"""
NanoAOD data access tools for CMS analyses.
Source: https://github.com/cms-sw (NanoAOD format)
        https://github.com/cms-opendata-analyses (usage examples)
"""

import json, os
from typing import List, Optional
from orchestral.tools.base.tool import BaseTool
from orchestral.tools.base.field_utils import RuntimeField, StateField

SCHEMA_VERSION = "evtjsonl-1.0"


class UprootNanoAODTool(BaseTool):
    """Read a CMS NanoAOD ROOT file and convert selected physics objects
    (Electron, Muon, Jet, Tau, MET) to evtjsonl-1.0 format using uproot.
    4-vectors are reconstructed from (pt, eta, phi, mass) branches."""

    nanoaod_path: str = RuntimeField(description="Path or xrootd URL to the NanoAOD ROOT file.")
    output_path: str = RuntimeField(description="Output JSONL path (relative to base_directory).")
    object_types: Optional[List[str]] = RuntimeField(
        default=["Muon", "Jet"],
        description="CMS object types to extract: Electron, Muon, Jet, FatJet, Tau, MET, GenPart."
    )
    n_events: Optional[int] = RuntimeField(default=None, description="Max events to read. None = all.")

    base_directory: str = StateField(description="Sandbox root directory.")

    def _run(self) -> str:
        # TODO: uproot.open(nanoaod_path)["Events"], read branches,
        #       reconstruct 4-vectors, write evtjsonl-1.0 line by line
        return json.dumps({"status": "ok", "schema": SCHEMA_VERSION,
                           "note": "stub - uproot implementation pending"})


class DASQueryTool(BaseTool):
    """Query the CMS Data Aggregation System (DAS) for datasets or file lists
    using the dasgoclient CLI. Returns file paths/xrootd URLs and event counts."""

    query: str = RuntimeField(description="DAS query, e.g. 'dataset=/DoubleMuon/Run2018D*/NANOAOD'.")
    max_results: Optional[int] = RuntimeField(default=50, description="Max results to return.")

    base_directory: str = StateField(description="Sandbox root directory.")
    das_client_path: str = StateField(default="dasgoclient", description="Path to dasgoclient binary.")

    def _run(self) -> str:
        # TODO: subprocess.run([das_client_path, "--query", query, "--format", "json"])
        return json.dumps({"status": "ok", "results": [], "note": "stub - dasgoclient call pending"})
