"""
# __init__.py is a part of the HEPTAPOD package.
# Copyright (C) 2025 HEPTAPOD authors (see AUTHORS for details).
# HEPTAPOD is licensed under the GNU GPL v3 or later, see LICENSE for details.

CMS detector analysis tools for HEPTAPOD.

Extends HEPTAPOD from BSM Monte Carlo workflows to full CMS detector
analyses, bridging CMS-native data formats (NanoAOD) through object
reconstruction corrections (JEC, b-tagging, tau ID) to statistical
interpretation (HiggsAnalysis-CombinedLimit).

Tool groups:
    data_access:  NanoAOD reading, CMS DAS queries, Open Data access
    objects:      Jet corrections, b-tagging, tau/lepton ID, pileup
    analysis:     Event selection, histogramming, combine, datacards
    simulation:   cmsRun execution, HTCondor batch submission
    plotting:     CMS-style plots, Brazil-band limit plots

Source repositories:
    cms-sw          https://github.com/cms-sw
    cms-jet         https://github.com/cms-jet
    cms-btv-pog     https://github.com/cms-btv-pog
    cms-analysis    https://github.com/cms-analysis
    cms-opendata    https://github.com/cms-opendata-analyses
    cms-tau-pog     https://github.com/cms-tau-pog
    FNALLPC         https://github.com/FNALLPC
"""

from tools.cms.data_access import (
    UprootNanoAODTool,
    DASQueryTool,
    CMSOpenDataTool,
)
from tools.cms.objects import (
    CMSJetCorrectionTool,
    CMSBTagTool,
    CMSTauIDTool,
    CMSLeptonIDTool,
    CMSPileupTool,
)
from tools.cms.analysis import (
    CMSEventSelectionTool,
    CMSHistogramTool,
    DataCardTool,
    CMSCombineTool,
)
from tools.cms.simulation import (
    CMSSWTool,
    HTCondorTool,
)
from tools.cms.plotting import (
    CMSPlotTool,
    LimitPlotTool,
)

__all__ = [
    # data_access
    "UprootNanoAODTool",
    "DASQueryTool",
    "CMSOpenDataTool",
    # objects
    "CMSJetCorrectionTool",
    "CMSBTagTool",
    "CMSTauIDTool",
    "CMSLeptonIDTool",
    "CMSPileupTool",
    # analysis
    "CMSEventSelectionTool",
    "CMSHistogramTool",
    "DataCardTool",
    "CMSCombineTool",
    # simulation
    "CMSSWTool",
    "HTCondorTool",
    # plotting
    "CMSPlotTool",
    "LimitPlotTool",
]
