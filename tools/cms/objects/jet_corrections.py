"""
CMS Jet Energy Corrections (JEC) and Resolution (JER) tool.
Source: https://github.com/cms-jet (JECDatabase, correctionlib)
"""

import json, os
from typing import List, Optional
from orchestral.tools.base.tool import BaseTool
from orchestral.tools.base.field_utils import RuntimeField, StateField

SCHEMA_VERSION = "evtjsonl-1.0"


class CMSJetCorrectionTool(BaseTool):
    """Apply factorised CMS jet energy corrections (L1FastJet, L2Relative, L3Absolute,
    L2L3Residual) and optional JER smearing to a jets JSONL file using correctionlib.
    Outputs corrected 4-vectors plus raw_pt and jec_factor per jet."""

    jets_jsonl: str = RuntimeField(description="Input jets JSONL path.")
    output_path: str = RuntimeField(description="Output corrected jets JSONL path.")
    era: str = RuntimeField(description="Correction era, e.g. 'Summer19UL18_V5_MC' or 'Run2018D_V19_DATA'.")
    correction_levels: Optional[List[str]] = RuntimeField(
        default=["L1FastJet", "L2Relative", "L3Absolute"],
        description="Correction levels to apply. Add 'L2L3Residual' for data."
    )
    apply_jer: Optional[bool] = RuntimeField(default=False, description="Apply JER smearing (MC only).")

    base_directory: str = StateField(description="Sandbox root directory.")
    correctionlib_path: str = StateField(default="", description="Path to correctionlib JSON files.")

    def _run(self) -> str:
        # TODO: correctionlib.CorrectionSet.from_file(era_json)
        #       apply L1, L2, L3 scale factors to each jet's 4-vector
        return json.dumps({"status": "ok", "schema": SCHEMA_VERSION,
                           "era": self.era, "note": "stub - correctionlib JEC pending"})
