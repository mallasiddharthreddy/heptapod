# tools/dqm — CMS Data Quality Monitoring Tool Group

This directory extends HEPTAPOD with a `tools/dqm/` group for CMS Data Quality
Monitoring (DQM) workflows. The tools follow the exact BaseTool pattern from the
existing codebase and produce/consume `evtjsonl-1.0`-compatible JSON output so
that all existing HEPTAPOD analysis tools work unchanged on DQM data.

## Design Rationale

CMS DQM involves checking the health of every detector subsystem run-by-run using
histograms stored in DQMIO ROOT files. Today this requires physicists to manually
inspect thousands of histograms per run. The goal of this tool group is to let an
LLM agent automate that pipeline end-to-end:

1. Fetch histogram data from DQMIO ROOT files or the OMS/Run Registry APIs
2. Train an ML model (autoencoder or classifier) on known-good reference runs
3. Score new runs and flag anomalous detector channels
4. Optionally hook into live CMSSW harvesting for real-time monitoring

## Architecture: Four Sub-Directories

| Directory      | Purpose                                          |
|----------------|--------------------------------------------------|
| `data_access/` | Read DQMIO ROOT files, query OMS, Run Registry  |
| `training/`    | Train autoencoders, classifiers, feature models  |
| `inference/`   | Score new runs, tune thresholds                  |
| `deployment/`  | Version models, hook into live CMSSW harvesting  |

## Key Design Decisions

**Why four directories instead of a flat list?**
The split mirrors the natural ML pipeline order: get data, train, infer, deploy.
Each directory is independent — you can swap `DQMAutoencoderTrainTool` for a
different model type without touching `inference/`. The LLM benefits because it
can reason about pipeline stage from directory name alone.

**Why evtjsonl-1.0 as the internal format?**
`DQMIOReaderTool` converts DQMIO histograms to evtjsonl-1.0 immediately, so
existing HEPTAPOD tools (`CalculateInvariantMassTool`, `ApplyCutsTool`) can
operate on DQM histogram data without modification. The bridge layer is the reader;
nothing downstream needs to change.

**Why autoencoders for anomaly detection?**
CMS DQM has abundant reference data for good runs but very few labeled bad runs.
Unsupervised autoencoder reconstruction error is the standard approach in the
literature (see CMS-DP-2020-020) because it only needs good-run training data.

## Source Repositories

| Tool(s)                  | Source repository               |
|--------------------------|---------------------------------|
| DQMIOReaderTool          | cms-sw/cmssw (DQMIO format)     |
| RunRegistryQueryTool     | cms-cern-ch/runregistry-api     |
| OMSQueryTool             | cms-oms/oms-api-client          |
| Training tools           | PyTorch / scikit-learn          |
| Inference tools          | (model files from training/)    |
| DQMLiveMonitorTool       | cms-sw/cmssw (harvesting hooks) |

## Tool Count

19 tool classes across 4 sub-directories + 1 README + 5 `__init__.py` = 25 files.
