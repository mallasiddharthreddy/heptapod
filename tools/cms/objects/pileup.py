"""
CMS pileup reweighting tool.
Source: https://github.com/cms-sw (LumiDB pileup profiles)
"""

import json, os
from typing import Optional
from orchestral.tools.base.tool import BaseTool
from orchestral.tools.base.field_utils import RuntimeField, StateField

SCHEMA_VERSION = "evtjsonl-1.0"


class CMSPileupTool(BaseTool):
    """Compute per-event pileup reweighting weights for MC events by comparing
    the simulated nPU distribution to the data pileup profile for a given era.
    Adds a 'pu_weight' field to each event header in the output JSONL."""

    events_jsonl: str = RuntimeField(description="Input events JSONL (must contain nPU or nPUTrue).")
    output_path: str = RuntimeField(description="Output events JSONL with pu_weight added.")
    era: str = RuntimeField(description="Data era for the pileup profile, e.g. '2018'.")
    variation: Optional[str] = RuntimeField(
        default="nominal",
        description="Weight variation: 'nominal', 'up', or 'down'."
    )

    base_directory: str = StateField(description="Sandbox root directory.")
    correctionlib_path: str = StateField(default="", description="Path to pileup correctionlib JSON files.")

    def _run(self) -> str:
        if self.variation not in ("nominal", "up", "down"):
            return self.format_error(error="Invalid variation",
                                     reason="variation must be nominal, up, or down.")
        # TODO: correctionlib pileup weight lookup by nPU, write pu_weight to event headers
        return json.dumps({"status": "ok", "era": self.era,
                           "variation": self.variation, "note": "stub - pileup reweighting pending"})
