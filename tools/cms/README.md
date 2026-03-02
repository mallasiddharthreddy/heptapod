# tools/cms — CMS Detector Analysis Tools

This directory extends HEPTAPOD to handle real CMS detector data, complementing
the existing BSM Monte Carlo tools (`feynrules → mg5 → pythia`) with a full
CMS analysis chain.

---

## Why a Separate `tools/cms/` Group?

The existing HEPTAPOD tools are **theory-first**: they generate BSM events from
scratch and analyse the parton/hadron-level output. CMS detector analysis is
**data-first**: it starts from NanoAOD ROOT files produced by CMSSW and requires
corrections, calibrations, and statistical tools that are entirely CMS-specific.

Mixing these two concerns into the existing `tools/analysis/` directory would
make both harder to reason about. A separate `tools/cms/` group keeps the
boundary clean while still sharing the `evtjsonl-1.0` schema — once NanoAOD
events are converted by `UprootNanoAODTool`, every existing HEPTAPOD tool
(`CalculateInvariantMassTool`, `ApplyCutsTool`, `ResonanceReconstructionTool`, etc.)
works on them without modification.

---

## Directory Structure

```
tools/cms/
├── data_access/         # Get data in
│   ├── nanoaod_reader.py    UprootNanoAODTool, DASQueryTool
│   └── open_data.py         CMSOpenDataTool
│
├── objects/             # CMS-specific object corrections
│   ├── jet_corrections.py   CMSJetCorrectionTool   (JEC + JER)
│   ├── btagger.py           CMSBTagTool            (DeepJet)
│   ├── tau_id.py            CMSTauIDTool           (DeepTau v2p5)
│   ├── lepton_id.py         CMSLeptonIDTool        (EGamma + MuonPOG)
│   └── pileup.py            CMSPileupTool          (nPU reweighting)
│
├── analysis/            # Analysis-level tools
│   ├── event_selection.py   CMSEventSelectionTool  (HLT + object cuts)
│   ├── histograms.py        CMSHistogramTool       (1D distributions)
│   ├── datacard.py          DataCardTool           (combine input)
│   └── combine.py           CMSCombineTool         (CLs limits)
│
├── simulation/          # Running CMS simulation
│   ├── cmssw_runner.py      CMSSWTool              (cmsRun)
│   └── condor.py            HTCondorTool           (batch jobs)
│
└── plotting/            # Publication figures
    └── cms_style.py         CMSPlotTool, LimitPlotTool
```

---

## Source Repositories

Each tool group maps to one or more official CMS GitHub organisations:

| Sub-directory   | Source repo                                | What we use |
|-----------------|--------------------------------------------|-------------|
| `data_access/`  | [cms-sw](https://github.com/cms-sw)        | NanoAOD branch definitions |
| `data_access/`  | [cms-opendata-analyses](https://github.com/cms-opendata-analyses) | Open Data file access patterns |
| `objects/`      | [cms-jet](https://github.com/cms-jet)      | JEC/JER correctionlib JSON files |
| `objects/`      | [cms-btv-pog](https://github.com/cms-btv-pog) | DeepJet WPs and b-tag SFs |
| `objects/`      | [cms-tau-pog](https://github.com/cms-tau-pog) | DeepTau v2p5 WPs and SFs |
| `analysis/`     | [cms-analysis](https://github.com/cms-analysis) | HiggsAnalysis-CombinedLimit |
| `simulation/`   | [cms-sw](https://github.com/cms-sw)        | cmsRun/CMSSW framework |
| `simulation/`   | [FNALLPC](https://github.com/FNALLPC)      | LPC HTCondor job tools |
| `plotting/`     | [scikit-hep/mplhep](https://github.com/scikit-hep/mplhep) | CMS matplotlib style |

---

## Data Flow

```
CMS Open Data / DAS
        │
        ▼
UprootNanoAODTool       NanoAOD ROOT → evtjsonl-1.0
        │                (from here, all existing HEPTAPOD tools apply)
        ▼
CMSPileupTool           add pu_weight per event (MC)
        │
        ▼
CMSJetCorrectionTool    JEC L1+L2+L3 (+L2L3Residual for data)
        │
        ▼
CMSBTagTool             DeepJet flag + btag_sf per jet
CMSTauIDTool            DeepTau flag + tau_sf per tau
CMSLeptonIDTool         ID flag + lepton_sf per lepton
        │
        ▼
CMSEventSelectionTool   MET filters → HLT → object cuts → cutflow
        │
        ├── CalculateInvariantMassTool   ← existing HEPTAPOD tool
        ├── GetHardestNTool              ← existing HEPTAPOD tool
        ├── FilterByDeltaRTool           ← existing HEPTAPOD tool
        │
        ▼
CMSHistogramTool        fill analysis distributions
        │
        ▼
DataCardTool            write combine datacard
        │
        ▼
CMSCombineTool          95% CLs limits / significance
        │
        ▼
LimitPlotTool           Brazil-band exclusion plot
```

---

## Design Decisions

**Why `evtjsonl-1.0` as the bridge?**
The existing HEPTAPOD schema is already the right abstraction. Rather than
inventing a CMS-specific format, `UprootNanoAODTool` converts NanoAOD
branches into the same schema that `CalculateInvariantMassTool` and
`ResonanceReconstructionTool` already consume. CMS-specific metadata
(b-tag scores, ID flags, scale factors) is stored in a `cms_info` sub-dict
on each particle, which existing tools ignore safely.

**Why correctionlib for all scale factors?**
All CMS POGs (JME, BTV, TAU, EGamma, Muon) have migrated to
[correctionlib](https://cms-nanoaod.github.io/correctionlib/) JSON files
hosted in their respective `jsonpog-integration` repos. This means
`CMSJetCorrectionTool`, `CMSBTagTool`, `CMSTauIDTool`, and `CMSLeptonIDTool`
all share the same dependency and the same lookup pattern — reducing
the implementation surface significantly.

**Why keep `simulation/` and `analysis/` separate?**
`CMSSWTool` and `HTCondorTool` are infrastructure tools — they move bits
around and submit jobs. `DataCardTool` and `CMSCombineTool` are physics tools —
they produce physics results. Mixing them would make the LLM's tool-selection
task harder (the agent docstrings would become ambiguous).

---

## Configuration

Add to `config.py`:

```python
cms_software_path  = "/path/to/CMSSW_14_0_0/src"   # or "" if cmsRun is in PATH
combine_path       = "combine"                       # assumes CMSSW env sourced
correctionlib_path = "/path/to/cms_corrections"      # jsonpog-integration files
das_client_path    = "dasgoclient"                   # assumes in PATH
```

---

## Demo

See `examples/cms_workflows/cms_dilepton_demo.py` for a complete
dilepton resonance search driven by natural language using this tool group.
