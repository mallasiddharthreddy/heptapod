"""
CMS histogram filling tool.
Source: https://github.com/FNALLPC (coffea-casa examples)
"""

import json, os
from typing import Dict, List, Optional
from orchestral.tools.base.tool import BaseTool
from orchestral.tools.base.field_utils import RuntimeField, StateField

SCHEMA_VERSION = "evtjsonl-1.0"


class CMSHistogramTool(BaseTool):
    """Fill 1D analysis histograms from evtjsonl-1.0 events for a set of
    standard observables (dimuon_mass, HT, MET, n_jets, leading_lepton_pt, etc.).
    Supports per-event weights and outputs a JSON histogram file."""

    events_jsonl: str = RuntimeField(description="Input events JSONL.")
    output_path: str = RuntimeField(description="Output histogram JSON or ROOT file.")
    observables: List[str] = RuntimeField(
        description="Observables to fill: dimuon_mass, HT, MET, n_jets, n_bjets, leading_lepton_pt, etc."
    )
    bins: Optional[Dict] = RuntimeField(
        default=None,
        description="Binning per observable: {'dimuon_mass': [60, 120, 60]}. Defaults used if not set."
    )
    weight_branch: Optional[str] = RuntimeField(default="pu_weight", description="Event weight branch name.")

    base_directory: str = StateField(description="Sandbox root directory.")

    def _run(self) -> str:
        # TODO: read events line by line, compute observable per event, np.histogram, write JSON
        return json.dumps({"status": "ok", "observables": self.observables,
                           "histograms": {}, "note": "stub - histogram filling pending"})
