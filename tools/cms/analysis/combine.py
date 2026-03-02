"""
CMS HiggsAnalysis-CombinedLimit (combine) runner.
Source: https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit
"""

import json, os
from typing import Optional
from orchestral.tools.base.tool import BaseTool
from orchestral.tools.base.field_utils import RuntimeField, StateField


class CMSCombineTool(BaseTool):
    """Run the CMS combine tool on a datacard to compute statistical results.
    Supports AsymptoticLimits (fast CLs), HybridNew (toy CLs), FitDiagnostics
    (signal strength fit), and Significance. Returns limit values and band edges."""

    datacard_path: str = RuntimeField(description="Path to combine datacard .txt file.")
    output_dir: str = RuntimeField(description="Directory for combine output ROOT files and logs.")
    method: Optional[str] = RuntimeField(
        default="AsymptoticLimits",
        description="Method: AsymptoticLimits, HybridNew, FitDiagnostics, Significance."
    )
    mass: Optional[float] = RuntimeField(default=125.0, description="Signal mass hypothesis in GeV.")
    options: Optional[str] = RuntimeField(default="", description="Extra combine CLI flags.")

    base_directory: str = StateField(description="Sandbox root directory.")
    combine_path: str = StateField(default="combine", description="Path to combine executable.")

    _VALID = {"AsymptoticLimits", "HybridNew", "FitDiagnostics", "Significance", "MultiDimFit"}

    def _run(self) -> str:
        if self.method not in self._VALID:
            return self.format_error(error="Invalid Method",
                                     reason=f"method must be one of {self._VALID}.")
        # TODO: subprocess.run([combine_path, "-M", method, datacard_path, "-m", str(mass), ...])
        #       parse output ROOT TTree "limit" with uproot, return structured dict
        return json.dumps({"status": "ok", "method": self.method, "mass": self.mass,
                           "limit_expected": None, "limit_observed": None,
                           "note": "stub - combine subprocess pending"})
