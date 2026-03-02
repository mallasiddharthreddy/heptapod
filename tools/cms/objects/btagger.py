"""
CMS DeepJet b-tagging tool.
Source: https://github.com/cms-btv-pog
"""

import json, os
from typing import Optional
from orchestral.tools.base.tool import BaseTool
from orchestral.tools.base.field_utils import RuntimeField, StateField

SCHEMA_VERSION = "evtjsonl-1.0"


class CMSBTagTool(BaseTool):
    """Apply CMS DeepJet b-tagging: flag jets passing a chosen working point
    (Loose/Medium/Tight) and optionally apply per-jet scale factors from the
    cms-btv-pog correctionlib JSON files."""

    jets_jsonl: str = RuntimeField(description="Input jets JSONL (must contain btagDeepFlavB branch).")
    output_path: str = RuntimeField(description="Output jets JSONL with b-tag flags added.")
    era: str = RuntimeField(description="Era for scale factors, e.g. '2018'.")
    working_point: Optional[str] = RuntimeField(default="M", description="'L', 'M', or 'T'.")
    apply_sf: Optional[bool] = RuntimeField(default=True, description="Apply b-tag scale factors (MC only).")

    base_directory: str = StateField(description="Sandbox root directory.")
    correctionlib_path: str = StateField(default="", description="Path to btv-pog correctionlib files.")

    def _run(self) -> str:
        if self.working_point not in ("L", "M", "T"):
            return self.format_error(error="Invalid WP", reason="working_point must be L, M, or T.")
        # TODO: load WP threshold from correctionlib, flag jets, compute btag_sf weights
        return json.dumps({"status": "ok", "schema": SCHEMA_VERSION,
                           "working_point": self.working_point, "note": "stub - DeepJet pending"})
