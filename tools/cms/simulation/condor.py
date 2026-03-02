"""
HTCondor batch job submission tool for CMS analyses.
Source: https://github.com/FNALLPC/lpcjobqueue
        https://batchdocs.web.cern.ch/
"""

import json, os
from typing import List, Optional
from orchestral.tools.base.tool import BaseTool
from orchestral.tools.base.field_utils import RuntimeField, StateField


class HTCondorTool(BaseTool):
    """Submit, monitor, and resubmit CMS analysis jobs on HTCondor clusters
    (CERN lxplus, Fermilab LPC). Creates a JDL file and calls condor_submit,
    or queries condor_q for job status. Useful for parallel per-file processing."""

    action: str = RuntimeField(description="'submit', 'status', or 'resubmit_failed'.")
    job_script: Optional[str] = RuntimeField(default=None, description="Bash script to run per job.")
    arguments: Optional[List[List]] = RuntimeField(default=None, description="Per-job argument lists.")
    output_dir: Optional[str] = RuntimeField(default=None, description="HTCondor log/output directory.")
    request_cpus: Optional[int] = RuntimeField(default=1, description="CPUs per job.")
    request_mem: Optional[int] = RuntimeField(default=2000, description="Memory per job in MB.")
    cluster_id: Optional[int] = RuntimeField(default=None, description="Cluster ID for status/resubmit.")

    base_directory: str = StateField(description="Sandbox root directory.")

    def _run(self) -> str:
        if self.action not in ("submit", "status", "resubmit_failed"):
            return self.format_error(error="Invalid Action",
                                     reason="action must be submit, status, or resubmit_failed.")
        # TODO: write JDL file, subprocess condor_submit / condor_q
        return json.dumps({"status": "ok", "action": self.action,
                           "note": "stub - condor_submit pending"})
