"""
CMS HiggsAnalysis-CombinedLimit datacard creator.
Source: https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit
"""

import json, os
from typing import Dict, List, Optional
from orchestral.tools.base.tool import BaseTool
from orchestral.tools.base.field_utils import RuntimeField, StateField


class DataCardTool(BaseTool):
    """Write a CMS combine datacard encoding observed yields, signal and background
    expectations, and systematic uncertainties (lnN, shape, gmN) for one or more
    analysis channels. Output is a plain-text .txt file ready for CMSCombineTool."""

    output_path: str = RuntimeField(description="Output datacard .txt file path.")
    channels: List[str] = RuntimeField(description="Channel names, e.g. ['SR_ee', 'SR_mumu'].")
    signal_name: str = RuntimeField(description="Signal process name, e.g. 'LQ_1000'.")
    observed_yields: Dict = RuntimeField(description="Observed counts per channel: {'SR_ee': 42}.")
    signal_yields: Dict = RuntimeField(description="Expected signal yields per channel: {'SR_ee': 3.2}.")
    background_yields: Dict = RuntimeField(
        description="Background yields: {'SR_ee': {'DY': 35.1, 'ttbar': 4.2}}."
    )
    systematics: Optional[List[Dict]] = RuntimeField(
        default=None,
        description="Systematics: [{'name': 'lumi', 'type': 'lnN', 'value': {'LQ_1000': 1.025}}]."
    )

    base_directory: str = StateField(description="Sandbox root directory.")

    def _run(self) -> str:
        # TODO: format and write combine datacard text file (imax/jmax/kmax header,
        #       bin/observation/process/rate blocks, systematic rows)
        return json.dumps({"status": "ok", "datacard_path": self.output_path,
                           "n_channels": len(self.channels), "note": "stub - datacard writer pending"})
