"""
CMS event selection tool: HLT triggers and object quality cuts.
Source: https://github.com/cms-sw (HLT config, MET filter flags in NanoAOD)
"""

import json, os
from typing import Dict, List, Optional
from orchestral.tools.base.tool import BaseTool
from orchestral.tools.base.field_utils import RuntimeField, StateField

SCHEMA_VERSION = "evtjsonl-1.0"


class CMSEventSelectionTool(BaseTool):
    """Apply CMS event selection in order: MET filters, HLT trigger requirement,
    primary vertex, lepton quality cuts, and jet multiplicity cuts.
    Returns filtered events JSONL and a cutflow table showing efficiency per stage."""

    events_jsonl: str = RuntimeField(description="Input events JSONL.")
    output_path: str = RuntimeField(description="Output selected events JSONL.")
    trigger_paths: Optional[List[str]] = RuntimeField(
        default=None,
        description="HLT trigger paths; at least one must fire, e.g. ['HLT_IsoMu24']."
    )
    lepton_selection: Optional[Dict] = RuntimeField(
        default=None,
        description="Lepton cuts: {'min_pt': 26, 'max_eta': 2.4, 'id': 'tight', 'max_iso': 0.15}."
    )
    jet_selection: Optional[Dict] = RuntimeField(
        default=None,
        description="Jet cuts: {'min_pt': 30, 'max_eta': 4.7, 'min_jets': 2}."
    )
    apply_met_filters: Optional[bool] = RuntimeField(default=True, description="Apply CMS MET cleaning filters.")

    base_directory: str = StateField(description="Sandbox root directory.")

    def _run(self) -> str:
        # TODO: iterate events JSONL, check HLT flags, apply object cuts, write passing events
        return json.dumps({"status": "ok", "n_events_in": 0, "n_events_out": 0,
                           "cutflow": {}, "note": "stub - event selection pending"})
