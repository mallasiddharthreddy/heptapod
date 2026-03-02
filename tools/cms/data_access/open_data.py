"""
CMS Open Data portal access tool.
Source: https://github.com/cms-opendata-analyses
        https://opendata.cern.ch/api
"""

import json, os
from typing import Optional
from orchestral.tools.base.tool import BaseTool
from orchestral.tools.base.field_utils import RuntimeField, StateField


class CMSOpenDataTool(BaseTool):
    """Search the CERN Open Data portal for public CMS datasets (Run 1 and Run 2),
    retrieve file lists, or download NanoAOD ROOT files without CERN credentials.
    Actions: 'search', 'files', 'download'."""

    action: str = RuntimeField(description="Action: 'search', 'files', or 'download'.")
    query: Optional[str] = RuntimeField(default=None, description="Search string, e.g. 'DoubleMuon 2018 NanoAOD'.")
    dataset_id: Optional[str] = RuntimeField(default=None, description="CERN Open Data record ID.")
    output_dir: Optional[str] = RuntimeField(default=None, description="Download target directory.")

    base_directory: str = StateField(description="Sandbox root directory.")

    def _run(self) -> str:
        if self.action not in ("search", "files", "download"):
            return self.format_error(error="Invalid Action",
                                     reason=f"action must be search, files, or download.")
        # TODO: requests.get("https://opendata.cern.ch/api/records", params={...})
        return json.dumps({"status": "ok", "action": self.action, "results": [],
                           "note": "stub - CERN Open Data API call pending"})
