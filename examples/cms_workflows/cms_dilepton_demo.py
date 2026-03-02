"""
# cms_dilepton_demo.py is a part of the HEPTAPOD package.
# Copyright (C) 2025 HEPTAPOD authors (see AUTHORS for details).
# HEPTAPOD is licensed under the GNU GPL v3 or later, see LICENSE for details.

CMS Dilepton Resonance Search — HEPTAPOD Demo
==============================================

This demo drives an LLM agent through a complete CMS dilepton analysis
entirely via natural language, from DAS dataset discovery through
statistical limit-setting to a Brazil-band exclusion plot.

Pipeline:
    DASQueryTool          → find DoubleMuon 2018 NanoAOD files
    UprootNanoAODTool     → read muons + jets → evtjsonl-1.0
    CMSPileupTool         → pileup reweighting (MC)
    CMSJetCorrectionTool  → JEC L1+L2+L3+L2L3Residual (data)
    CMSLeptonIDTool       → tight muon ID + isolation
    CMSEventSelectionTool → HLT_IsoMu24, object cuts
    GetHardestNTool       → select 2 hardest muons
    CalculateInvariantMassTool → dimuon mass spectrum
    CMSHistogramTool      → fill m(μμ) distribution
    DataCardTool          → create combine datacard
    CMSCombineTool        → 95% CLs AsymptoticLimits
    LimitPlotTool         → Brazil-band exclusion plot

Run:
    python examples/cms_workflows/cms_dilepton_demo.py

Then open http://localhost:8001 in your browser.
"""

import sys
from pathlib import Path

# ─── Path setup ─────────────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SHARED_DIR = REPO_ROOT / "examples" / "shared"
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(SHARED_DIR))

# ─── Orchestral AI framework ────────────────────────────────────────────────
from orchestral import Agent
from orchestral.tools import (
    RunCommandTool,
    WriteFileTool,
    ReadFileTool,
    RunPythonTool,
    FindFilesTool,
    WebSearchTool,
    TodoRead,
    TodoWrite,
)
from orchestral.tools.hooks import TruncateOutputHook

# ─── LLM backend (choose one) ───────────────────────────────────────────────
from orchestral.llm import Claude           # Anthropic Claude
# from orchestral.llm import GPT            # OpenAI GPT
# from orchestral.llm import Gemini         # Google Gemini
# from llm import get_ollama               # local Ollama

# ─── Existing HEPTAPOD analysis tools (unchanged) ───────────────────────────
from tools.analysis.kinematics import (
    CalculateInvariantMassTool,
    CalculateTransverseMomentumTool,
    CalculateDeltaRTool,
    ApplyCutsTool,
    GetHardestNTool,
    FilterByPDGIDTool,
    SortByPtTool,
    FilterByDeltaRTool,
)
from tools.analysis.reconstruction import ResonanceReconstructionTool
from tools.analysis.conversions import LHEToJSONLTool, EventJSONLToNumpyTool

# ─── NEW: CMS detector analysis tools ───────────────────────────────────────
from tools.cms import (
    # Data access
    UprootNanoAODTool,
    DASQueryTool,
    CMSOpenDataTool,
    # Object corrections
    CMSJetCorrectionTool,
    CMSBTagTool,
    CMSTauIDTool,
    CMSLeptonIDTool,
    CMSPileupTool,
    # Analysis
    CMSEventSelectionTool,
    CMSHistogramTool,
    DataCardTool,
    CMSCombineTool,
    # Plotting
    CMSPlotTool,
    LimitPlotTool,
)

# ─── System prompt ──────────────────────────────────────────────────────────
from prompts import load_prompt

CMS_EXPLORER_PROMPT_PATH = (
    REPO_ROOT
    / "prompts"
    / "examples"
    / "cms_analysis"
    / "system"
    / "cms_analysis_explorer_prompt.md"
)
system_prompt = CMS_EXPLORER_PROMPT_PATH.read_text()

# ─── Config ─────────────────────────────────────────────────────────────────
from config import (
    cms_software_path,
    combine_path,
    correctionlib_path,
    das_client_path,
)

# ─── Sandbox setup ──────────────────────────────────────────────────────────
from sandbox_utils import create_new_sandbox

DEMO_FILES_DIR = Path(__file__).resolve().parent / "cms_sandbox"
CREATE_NEW_SANDBOX = True

if CREATE_NEW_SANDBOX:
    base_directory, system_prompt = create_new_sandbox(
        DEMO_FILES_DIR, mode="explorer", system_prompt=system_prompt
    )
else:
    base_directory = str(DEMO_FILES_DIR / "sandbox000")

# ─── Tool registration ──────────────────────────────────────────────────────
tools = [
    # Core utilities
    RunCommandTool(base_directory=base_directory),
    WriteFileTool(base_directory=base_directory),
    ReadFileTool(base_directory=base_directory, show_line_numbers=True),
    RunPythonTool(base_directory=base_directory, timeout=600),
    FindFilesTool(base_directory=base_directory),
    WebSearchTool(),
    TodoRead(),
    TodoWrite(base_directory=base_directory),

    # ── CMS: data access ──────────────────────────────────────────────────
    UprootNanoAODTool(base_directory=base_directory),
    DASQueryTool(
        base_directory=base_directory,
        das_client_path=das_client_path,
    ),
    CMSOpenDataTool(base_directory=base_directory),

    # ── CMS: object corrections ───────────────────────────────────────────
    CMSPileupTool(
        base_directory=base_directory,
        correctionlib_path=correctionlib_path,
    ),
    CMSJetCorrectionTool(
        base_directory=base_directory,
        correctionlib_path=correctionlib_path,
    ),
    CMSBTagTool(
        base_directory=base_directory,
        correctionlib_path=correctionlib_path,
    ),
    CMSTauIDTool(
        base_directory=base_directory,
        correctionlib_path=correctionlib_path,
    ),
    CMSLeptonIDTool(
        base_directory=base_directory,
        correctionlib_path=correctionlib_path,
    ),

    # ── CMS: analysis ─────────────────────────────────────────────────────
    CMSEventSelectionTool(base_directory=base_directory),
    CMSHistogramTool(base_directory=base_directory),
    DataCardTool(base_directory=base_directory),
    CMSCombineTool(
        base_directory=base_directory,
        combine_path=combine_path,
    ),

    # ── CMS: plotting ─────────────────────────────────────────────────────
    CMSPlotTool(base_directory=base_directory),
    LimitPlotTool(base_directory=base_directory),

    # ── Existing HEPTAPOD kinematics (fully compatible with CMS events) ──
    CalculateInvariantMassTool(base_directory=base_directory),
    CalculateTransverseMomentumTool(base_directory=base_directory),
    CalculateDeltaRTool(base_directory=base_directory),
    ApplyCutsTool(base_directory=base_directory),
    GetHardestNTool(base_directory=base_directory),
    FilterByPDGIDTool(base_directory=base_directory),
    SortByPtTool(base_directory=base_directory),
    FilterByDeltaRTool(base_directory=base_directory),
    ResonanceReconstructionTool(base_directory=base_directory),
    EventJSONLToNumpyTool(base_directory=base_directory),
]

# ─── Output hooks ────────────────────────────────────────────────────────────
hooks = [TruncateOutputHook(max_length=10_000)]

# ─── Agent ──────────────────────────────────────────────────────────────────
agent = Agent(
    llm=Claude(),
    tools=tools,
    tool_hooks=hooks,
    system_prompt=system_prompt,
    debug=False,
)

# ─── Launch ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import app.server as app_server

    app_server.run_server(
        agent,
        host="127.0.0.1",
        port=8001,          # different from BSM demo (8000) — both can run simultaneously
        open_browser=True,
        max_tool_iterations=150,
    )
