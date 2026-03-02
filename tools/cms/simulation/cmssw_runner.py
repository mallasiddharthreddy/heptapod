"""
CMS Software (CMSSW) cmsRun execution tool.
Source: https://github.com/cms-sw/cmssw
"""

import json, os
from typing import Dict, List, Optional
from orchestral.tools.base.tool import BaseTool
from orchestral.tools.base.field_utils import RuntimeField, StateField


class CMSSWTool(BaseTool):
    """Execute a CMSSW Python config file with cmsRun. Handles input file injection,
    event count, and thread count via command-line overrides. Used for NanoAOD
    production, re-reconstruction, or running CMS analyzer modules."""

    config_path: str = RuntimeField(description="CMSSW cmsConfig.py path (relative to base_directory).")
    input_files: List[str] = RuntimeField(description="Input ROOT file paths or xrootd URLs.")
    output_dir: str = RuntimeField(description="Output directory for cmsRun products.")
    n_events: Optional[int] = RuntimeField(default=-1, description="Events to process (-1 = all).")
    n_threads: Optional[int] = RuntimeField(default=1, description="CMSSW threads (1-8).")

    base_directory: str = StateField(description="Sandbox root directory.")
    cms_software_path: str = StateField(default="", description="CMSSW release path; empty = use PATH.")

    def _run(self) -> str:
        # TODO: build cmsRun command, subprocess.run, parse stdout for event count
        return json.dumps({"status": "ok", "n_events": self.n_events,
                           "output_dir": self.output_dir, "note": "stub - cmsRun pending"})
