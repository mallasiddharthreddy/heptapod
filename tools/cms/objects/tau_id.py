"""
CMS DeepTau tau identification tool.
Source: https://github.com/cms-tau-pog
"""

import json, os
from typing import Optional
from orchestral.tools.base.tool import BaseTool
from orchestral.tools.base.field_utils import RuntimeField, StateField

SCHEMA_VERSION = "evtjsonl-1.0"


class CMSTauIDTool(BaseTool):
    """Apply CMS DeepTau v2p5 identification to hadronic tau candidates.
    Flags taus passing VSjet, VSe, and VSmu working points and applies
    tau ID scale factors from the cms-tau-pog correctionlib JSON files."""

    taus_jsonl: str = RuntimeField(description="Input tau JSONL (from UprootNanoAODTool Tau objects).")
    output_path: str = RuntimeField(description="Output JSONL with DeepTau flags added.")
    era: str = RuntimeField(description="Era tag, e.g. '2018' or '2022postEE'.")
    vs_jet_wp: Optional[str] = RuntimeField(default="Medium", description="VSjet WP (VVVLoose to VVTight).")
    vs_ele_wp: Optional[str] = RuntimeField(default="Tight", description="VSe WP.")
    vs_mu_wp: Optional[str] = RuntimeField(default="Loose", description="VSmu WP.")
    apply_sf: Optional[bool] = RuntimeField(default=True, description="Apply tau ID scale factors (MC only).")

    base_directory: str = StateField(description="Sandbox root directory.")
    correctionlib_path: str = StateField(default="", description="Path to tau POG correctionlib files.")

    def _run(self) -> str:
        # TODO: correctionlib tau ID WP thresholds + scale factor lookup per decay mode
        return json.dumps({"status": "ok", "schema": SCHEMA_VERSION,
                           "vs_jet_wp": self.vs_jet_wp, "note": "stub - DeepTau pending"})
