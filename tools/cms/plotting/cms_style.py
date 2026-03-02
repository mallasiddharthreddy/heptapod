"""
CMS publication-style matplotlib plots (mplhep) and Brazil-band limit plots.
Source: https://github.com/scikit-hep/mplhep
"""

import json, os
from typing import Dict, List, Optional
from orchestral.tools.base.tool import BaseTool
from orchestral.tools.base.field_utils import RuntimeField, StateField


class CMSPlotTool(BaseTool):
    """Generate a CMS publication-style figure using mplhep.style.CMS.
    Supports 1D histograms and data/MC stacked plots with the standard
    CMS lumi label (e.g. '59.7 fb⁻¹ (13 TeV)') and Preliminary tag."""

    histogram_path: str = RuntimeField(description="Input histogram JSON path (from CMSHistogramTool).")
    output_path: str = RuntimeField(description="Output figure path (.pdf or .png).")
    observable: str = RuntimeField(description="Observable key to plot, e.g. 'dimuon_mass'.")
    x_label: str = RuntimeField(description="X-axis label, e.g. 'm(μμ) [GeV]'.")
    lumi: Optional[float] = RuntimeField(default=59.7, description="Luminosity in fb⁻¹.")
    cms_label: Optional[str] = RuntimeField(
        default="Preliminary",
        description="CMS label: 'Preliminary', 'Private Work', or '' (published)."
    )
    log_y: Optional[bool] = RuntimeField(default=False, description="Log scale on y-axis.")

    base_directory: str = StateField(description="Sandbox root directory.")

    def _run(self) -> str:
        # TODO: load histogram JSON, mplhep.style.use("CMS"), histplot, cms.label, savefig
        return json.dumps({"status": "ok", "output_path": self.output_path,
                           "note": "stub - mplhep CMS plot pending"})


class LimitPlotTool(BaseTool):
    """Generate a CMS Brazil-band exclusion limit plot from a JSON array of
    per-mass-point limit values (obs, exp, ±1σ, ±2σ). Optionally overlays
    the theory cross section curve to show the mass exclusion point."""

    limits_json: str = RuntimeField(
        description="JSON array of limit dicts: [{'mass':500,'obs':0.83,'exp':1.02,'m2s':...}]."
    )
    output_path: str = RuntimeField(description="Output figure path (.pdf or .png).")
    x_label: str = RuntimeField(description="X-axis label, e.g. 'm(LQ) [GeV]'.")
    lumi: Optional[float] = RuntimeField(default=59.7, description="Luminosity in fb⁻¹.")
    cms_label: Optional[str] = RuntimeField(default="Preliminary", description="CMS label string.")
    theory_curve: Optional[str] = RuntimeField(
        default=None, description="Optional JSON path with theory cross sections per mass point."
    )
    log_y: Optional[bool] = RuntimeField(default=True, description="Log scale on y-axis.")

    base_directory: str = StateField(description="Sandbox root directory.")

    def _run(self) -> str:
        # TODO: load limits JSON, mplhep Brazil-band plot (fill_between ±2s yellow, ±1s green)
        return json.dumps({"status": "ok", "output_path": self.output_path,
                           "note": "stub - Brazil-band plot pending"})
