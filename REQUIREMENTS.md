# Structured intake and approval pilot: business requirements

**Proposed solution, not an implemented workflow product.** The delivered project is the analysis, dashboard and business case. All baselines use synthetic data; thresholds below are proposed pilot criteria.

## Problem and scope

Requests travel through intake → review → approval → execution, with an additional rework loop. Long review queues and incomplete intake are hypotheses to investigate. The pilot covers a single team's standard requests. Complex, regulated or exceptional requests retain manual review. Automating decisions outside that scope is excluded.

## Future process

Requester submits required fields → validation flags missing information → rules route a complete request → reviewer accepts or requests changes → authorized approver records a decision → executor closes the request. Rejections and overrides record a reason. A timeout escalates to a named manager without automatically approving the request.

| ID | User story / requirement | Acceptance evidence | Owner |
|---|---|---|---|
| BR-01 | As a requester, I need required fields validated before submission. | Missing required fields prevent submission and identify each missing field; drafts remain editable. | Product owner |
| BR-02 | As a manager, I need standard requests routed to the correct queue. | A versioned route table maps every allowed team/type; unmatched combinations enter a visible exception queue. | Operations |
| BR-03 | As an approver, I need decisions restricted to authorized reviewers. | Requesters cannot approve their own requests; attempts and approved overrides are auditable. | Engineering |
| BR-04 | As an analyst, I need reliable timestamps for each stage. | Each transition records UTC time, actor, previous state, new state and route version; stage durations reconcile to total elapsed time. | Data owner |
| BR-05 | As a sponsor, I need a trustworthy pilot comparison. | Report counts, route mix, p50/p90, SLA, rework and open backlog for pilot and comparison teams using the same window. | Analyst |
| BR-06 | As an operator, I need to reverse a failed rollout. | Routing can be disabled and queued requests exported to manual review without losing their histories. | Engineering |

## Proposed pilot evaluation

Use a two-week baseline and four-week pilot, recording all arrivals and open requests, not only completions. Prefer randomized eligible requests; if operationally impossible, use a matched comparison team and acknowledge confounding. Define the analysis window, volume requirement and route strata before launch.

- Primary target: at least 15% lower p90 cycle time versus the agreed comparison, with uncertainty reported.
- Guardrails: rework must not increase more than 2 percentage points; no unauthorized approvals or lost requests.
- Business-case gate: measured touch-time reduction should meet the assumed 0.20 hours per adopted request; finance validates whether capacity is redeployed or spending reduced.
- Stop and investigate any authorization failure, lost request, or material backlog growth. Revert to manual routing if unresolved.

Targets are proposed success criteria, not achieved results. A small pilot may not establish statistical significance; report uncertainty rather than declaring success from a point estimate.

## Assumptions and unresolved questions

Annual demand of 12,000 requests, $45/hour loaded cost, $25,000 build cost and $12,000 annual run cost require sponsor validation. Is review delay due to staffing, missing information, approval policy, or queue batching? Which exception types require additional controls? Is 72 hours a calendar or business-hour obligation? This analysis uses elapsed calendar hours; a business-hour SLA needs a holiday/calendar model.

## Responsibilities

Sponsor: funding and scope approval. Business analyst: requirement traceability and acceptance evidence. Operations: process ownership and training. Engineering: access control, routing and rollback. Finance: cost assumptions and benefit realization. Analytics: metric definitions, data quality and evaluation.
