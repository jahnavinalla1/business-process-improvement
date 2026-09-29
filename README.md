# Approval workflow and automation business case

**Independent portfolio case study · simulated data · no client affiliation**

Business analysis · requirements · SLA · ROI sensitivity

[Interactive dashboard](https://jahnavinalla1.github.io/analytics-projects/05-business-process-improvement/) · [Decision memo](results/report.md) · [SQL](analysis.sql) · [Python](analyze.py)

## Business problem

An operations sponsor needs to decide whether to fund a pilot for structured intake and approval routing.

## Reproduce

This is a self-contained repository. Python 3.10+ is the only dependency; no shared portfolio repository, API key, or third-party package is required.

```sh
git clone https://github.com/jahnavinalla1/business-process-improvement.git
cd business-process-improvement
python3 run.py
```

`run.py` regenerates the seeded dataset, rebuilds the dashboard and reports, and executes the tests. To analyze the included CSV without replacing it:

```sh
python3 analyze.py
python3 -m unittest discover -s tests -v
```

Open `index.html` in your browser to explore the dashboard. Its data is embedded, so no server is needed. The [hosted demo](https://jahnavinalla1.github.io/analytics-projects/05-business-process-improvement/) is also linked from the portfolio. `generate.py` intentionally overwrites `data.csv` with the same simulated sample; `analyze.py` only reads it and rebuilds outputs.

## Data and provenance

One completed request per row, 1,000 requests. Seed 5505. Stage durations are sequential elapsed hours including waiting, not employee touch effort. Data is authored by the deterministic generator in this folder. It contains no real people, company transactions, or external source material. Patterns in the simulation are intentionally constructed for analytical practice; they are not evidence about actual markets or employers.

| Field | Meaning |
|---|---|
| `request_id` | Unique request key |
| `team` | Sales, Operations or Finance |
| `route` | Standard or Complex |
| `intake_hours, review_hours, approval_hours, execution_hours` | Elapsed time in each sequential stage |
| `rework_hours` | Additional elapsed time caused by rework |
| `rework` | Binary indicator of rework |

## Metric contract and method

Cycle time is the sum of all five stages. SLA compliance is the share completed in ≤72 hours. p90 is the nearest-rank 90th percentile. Capacity value = assumed annual volume × touch hours saved × adoption × loaded hourly cost. Annual net value subtracts running cost; year-one net also subtracts build cost. Payback = build cost / monthly net benefit, unavailable if net benefit ≤0. This is capacity valuation, not realized cash savings.

`analysis.sql` is the actual executed SQL, not a decorative example. Python loads the CSV into constrained in-memory SQLite tables, executes named SQL blocks, validates key invariants, calculates any statistical/scenario outputs, and renders the result files. No network, API key, or paid BI license is needed.

## Stakeholders and decision ownership

Operations sponsor owns funding; team managers own process adoption; business analyst owns requirements; finance validates valuation assumptions.

## Data quality and acceptance

Request keys must be unique; durations non-negative; rework flags and hours consistent. The financial model must use touch-time assumptions separately from elapsed-time observations. See REQUIREMENTS.md for pilot acceptance criteria.

## Deliverables

- `data.csv`: complete reproducible source dataset.
- `generate.py`: seeded data-generation logic and business assumptions.
- `analysis.sql` / `analyze.py`: executable analytical logic.
- `index.html`: portable interactive dashboard with filtering and sorting.
- `results/metrics.json` and result CSVs: machine-readable, exportable outputs.
- `results/report.md`: computed findings, recommended actions and limitations.

## Interpretation

Read the decision memo for the actual computed results. Recommendations are proposals for a future pilot; no employer outcome, production deployment, cash saving, or measured improvement is claimed. Replacing the synthetic source requires revisiting schema constraints, hardcoded fixture sizes, missing-data policies and the metric contract.
