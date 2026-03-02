# CMS Dilepton Resonance Search — Task Pipeline
# HEPTAPOD Todo-mode workflow for the CMS dilepton analysis demo.

**IMPORTANT:** Use RELATIVE paths. All paths are relative to the sandbox root.

**TODO LIST RULES:**
- DO NOT modify task descriptions before completing them
- Check off items ONE AT A TIME after full completion (`[ ]` → `[x]`)
- Summarise the completed task and plan next step before proceeding

---

## Phase 1: Data Discovery

- [ ] **Find DoubleMuon 2018 NanoAOD dataset**

  Call `DASQueryTool` with:
  ```
  query: "dataset=/DoubleMuon/Run2018D-UL2018_MiniAODv2_NanoAODv9/NANOAOD"
  ```
  OR for public open data, call `CMSOpenDataTool` with:
  ```
  action: "search"
  query: "DoubleMuon 2018 NanoAOD"
  ```
  Record the dataset name and the first 3 file xrootd URLs for Phase 2.

---

## Phase 2: Data Ingestion → evtjsonl-1.0

- [ ] **Convert NanoAOD to evtjsonl-1.0**

  Call `UprootNanoAODTool` with:
  ```
  nanoaod_path: <first_file_from_phase_1>
  output_path:  "data/events/raw_events.jsonl"
  object_types: ["Muon", "Jet", "MET"]
  n_events:     10000
  ```
  Verify output: check `schema` field is `"evtjsonl-1.0"` and particles
  include both Muon (id=13/-13) and Jet (id=0) entries.

---

## Phase 3: Object Corrections

- [ ] **Apply Jet Energy Corrections (data)**

  Call `CMSJetCorrectionTool` with:
  ```
  jets_jsonl:        "data/events/raw_events.jsonl"
  output_path:       "data/events/jec_corrected.jsonl"
  era:               "Run2018D_V19_DATA"
  correction_levels: ["L1FastJet", "L2Relative", "L3Absolute", "L2L3Residual"]
  apply_jer:         false
  ```
  Note: L2L3Residual is required for real data (not MC).

- [ ] **Apply tight muon identification and isolation**

  Call `CMSLeptonIDTool` with:
  ```
  leptons_jsonl: "data/events/jec_corrected.jsonl"
  output_path:   "data/events/muon_id.jsonl"
  lepton_type:   "Muon"
  id_wp:         "Tight"
  iso_cut:       0.15
  era:           "2018"
  apply_sf:      false
  ```

---

## Phase 4: Event Selection

- [ ] **Apply HLT trigger + kinematic selection**

  Call `CMSEventSelectionTool` with:
  ```
  events_jsonl:    "data/events/muon_id.jsonl"
  output_path:     "data/events/selected.jsonl"
  trigger_paths:   ["HLT_IsoMu24", "HLT_IsoMu27"]
  lepton_selection: {"min_pt": 26, "max_eta": 2.4, "id": "tight", "max_iso": 0.15}
  jet_selection:    {"min_pt": 30, "max_eta": 4.7}
  apply_met_filters: true
  ```
  Report the cutflow table: note how many events pass each stage
  and the total selection efficiency.

---

## Phase 5: Dimuon Invariant Mass

- [ ] **Select 2 hardest muons per event**

  Call `GetHardestNTool` with:
  ```
  input_path:  "data/events/selected.jsonl"
  output_path: "data/objects/hardest_2_muons.jsonl"
  n_hardest:   2
  pdgids:      [13, -13]
  ```

- [ ] **Compute dimuon invariant mass**

  Call `CalculateInvariantMassTool` with:
  ```
  input_file:  "data/objects/hardest_2_muons.jsonl"
  output_file: "analysis/mll.npy"
  ```
  Use `RunPythonTool` to print the mean and RMS of the mass distribution.

---

## Phase 6: Histogram

- [ ] **Fill dimuon mass histogram**

  Call `CMSHistogramTool` with:
  ```
  events_jsonl:  "data/events/selected.jsonl"
  output_path:   "analysis/histograms.json"
  observables:   ["dimuon_mass", "leading_lepton_pt", "HT", "n_jets"]
  bins:          {"dimuon_mass": [15, 120, 105]}
  weight_branch: null
  output_format: "json"
  ```

---

## Phase 7: Statistical Analysis

- [ ] **Create combine datacard**

  Estimate signal yield from MC (or use placeholder 5.0 events for testing).
  Call `DataCardTool` with:
  ```
  output_path:       "analysis/datacard.txt"
  channels:          ["SR_mumu"]
  signal_name:       "Z_prime_2000"
  observed_yields:   {"SR_mumu": <n_obs_from_phase_5>}
  signal_yields:     {"SR_mumu": 5.0}
  background_yields: {"SR_mumu": {"DY": <n_obs - 5.0>}}
  systematics:       [{"name": "lumi_2018", "type": "lnN",
                       "value": {"Z_prime_2000": 1.025, "DY": 1.025}}]
  ```

- [ ] **Set 95% CLs expected limits**

  Call `CMSCombineTool` with:
  ```
  datacard_path: "analysis/datacard.txt"
  output_dir:    "analysis/combine_output"
  method:        "AsymptoticLimits"
  mass:          2000
  ```
  Record: expected limit, −2σ, −1σ, +1σ, +2σ bands.

---

## Phase 8: Publication Plot

- [ ] **Generate dimuon mass distribution plot**

  Call `CMSPlotTool` with:
  ```
  histogram_path: "analysis/histograms.json"
  output_path:    "plots/dimuon_mass.pdf"
  observable:     "dimuon_mass"
  plot_type:      "hist1d"
  x_label:        "m(μμ) [GeV]"
  lumi:           59.7
  cms_label:      "Preliminary"
  ```

- [ ] **Generate Brazil-band exclusion limit plot**

  First, use `WriteFileTool` to create `analysis/limits.json` from the
  combine output in Phase 7 with format:
  ```json
  [{"mass": 2000, "obs": <obs>, "exp": <exp>,
    "m2s": <m2s>, "m1s": <m1s>, "p1s": <p1s>, "p2s": <p2s>}]
  ```
  Then call `LimitPlotTool` with:
  ```
  limits_json:  "analysis/limits.json"
  output_path:  "plots/exclusion_limit.pdf"
  x_label:      "m(Z') [GeV]"
  lumi:         59.7
  cms_label:    "Preliminary"
  ```
  Verify the output: `.pdf` file present in `plots/` with CMS label.
