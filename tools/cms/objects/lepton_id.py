"""
CMS electron and muon identification tool.
Source: https://github.com/cms-sw (EgammaAnalysis, MuonPOG)
"""

import json, os
from typing import Optional
from orchestral.tools.base.tool import BaseTool
from orchestral.tools.base.field_utils import RuntimeField, StateField

SCHEMA_VERSION = "evtjsonl-1.0"


class CMSLeptonIDTool(BaseTool):
    """Apply CMS POG lepton ID and isolation to electrons or muons.
    Supports cut-based and MVA-based IDs for electrons (EGamma POG)
    and Loose/Medium/Tight/HighPt IDs for muons (Muon POG).
    Returns filtered JSONL with per-lepton ID flags and scale factors."""

    leptons_jsonl: str = RuntimeField(description="Input lepton JSONL path.")
    output_path: str = RuntimeField(description="Output JSONL with ID flags and SFs.")
    lepton_type: str = RuntimeField(description="'Electron' or 'Muon'.")
    id_wp: str = RuntimeField(description="ID working point, e.g. 'Tight' or 'mvaFall17V2Iso_WP80'.")
    iso_cut: Optional[float] = RuntimeField(default=0.15, description="Max pfRelIso (None = no cut).")
    era: str = RuntimeField(description="Era for scale factors, e.g. '2018'.")

    base_directory: str = StateField(description="Sandbox root directory.")
    correctionlib_path: str = StateField(default="", description="Path to EGamma/muon POG correctionlib files.")

    def _run(self) -> str:
        if self.lepton_type not in ("Electron", "Muon"):
            return self.format_error(error="Invalid lepton_type",
                                     reason="Must be 'Electron' or 'Muon'.")
        # TODO: apply id_wp flag + iso_cut filter + correctionlib SF lookup
        return json.dumps({"status": "ok", "lepton_type": self.lepton_type,
                           "note": "stub - lepton ID pending"})
