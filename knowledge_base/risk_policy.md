# Risk Policy

## Purpose

This policy defines how ScenarioTwin AI should evaluate risk during enterprise scenario simulations.

The goal is to classify risk consistently, explain the business impact clearly, and support safe executive decision-making.

## Risk Levels

ScenarioTwin AI uses four risk levels:

* Low
* Medium
* High
* Critical

Each risk level should be based on measurable business impact, operational constraints, customer exposure, and financial risk.

## Low Risk

A scenario may be classified as Low risk when:

* Inventory shortage is minimal or does not exist.
* Average service level remains high.
* Revenue at risk is low.
* Profit at risk is low.
* Few or no strategic customers are exposed.
* The company can respond using normal operating procedures.

Recommended response:

* Monitor the situation.
* Continue normal operations.
* Review metrics periodically.

## Medium Risk

A scenario may be classified as Medium risk when:

* Some products are constrained.
* Service level begins to deteriorate.
* Revenue or profit exposure is noticeable.
* Some customers may experience delays.
* Operational teams may need to adjust priorities.

Recommended response:

* Apply selective mitigation.
* Monitor affected products closely.
* Communicate with customers if delays are expected.
* Prepare replenishment or supplier actions.

## High Risk

A scenario may be classified as High risk when:

* Multiple products are constrained.
* Service level is significantly reduced.
* Revenue at risk is material.
* Profit at risk is material.
* Strategic customers are exposed.
* Normal operations are not enough to absorb the disruption.

Recommended response:

* Activate a controlled mitigation plan.
* Prioritize strategic customers.
* Focus inventory and replenishment on high-impact products.
* Review pricing, allocation, and fulfillment decisions.
* Escalate the scenario to executive leadership.

## Critical Risk

A scenario may be classified as Critical risk when:

* Most or all key products are constrained.
* Average service level is very low.
* Unmet demand is high.
* Revenue at risk is significant.
* Profit at risk is significant.
* Strategic customers are exposed.
* There is risk of customer dissatisfaction, reputational damage, or operational overload.

Recommended response:

* Do not accept all demand without allocation rules.
* Activate executive-level decision-making.
* Prioritize strategic customers and critical products.
* Use controlled allocation.
* Accelerate replenishment or production planning.
* Communicate proactively with affected customers.
* Review decisions with human leadership before execution.

## Demand Spike + Inventory Constraint Risk Criteria

In a Demand Spike + Inventory Constraint scenario, ScenarioTwin AI should evaluate:

* Demand increase percentage
* Products analyzed
* Number of constrained products
* Total inventory shortage
* Revenue at risk
* Profit at risk
* Average service level
* Customer exposure
* Strategic customer priority

### Suggested Risk Classification

A scenario is usually Low risk when:

* No products are constrained.
* Average service level is above 90%.
* Revenue and profit at risk are low.

A scenario is usually Medium risk when:

* At least one product is constrained.
* Average service level is between 75% and 90%.
* Revenue or profit exposure exists but is manageable.

A scenario is usually High risk when:

* Three or more products are constrained.
* Average service level is below 85%.
* Strategic customers are exposed.
* Revenue or profit exposure is material.

A scenario is usually Critical risk when:

* Four or more products are constrained.
* Average service level is below 75%.
* Revenue at risk and profit at risk are significant.
* Strategic customers are exposed.
* The company cannot realistically fulfill all demand.

## Supplier Cost Shock Risk Criteria

In a Supplier Cost Shock scenario, ScenarioTwin AI should evaluate:

* Supplier dependency
* Number of affected products
* Margin drop
* Estimated profit loss
* Customer exposure
* Price sensitivity
* Strategic customer value

### Suggested Risk Classification

A scenario is usually Low risk when:

* Few products are affected.
* Margin drop is limited.
* Profit loss is low.
* Customer exposure is low.

A scenario is usually Medium risk when:

* Multiple products are affected.
* Margin pressure is noticeable.
* Some customer exposure exists.
* Selective mitigation may be required.

A scenario is usually High risk when:

* Margin drop is significant.
* Profit loss is material.
* Several customers are exposed.
* Supplier dependency is high.

A scenario is usually Critical risk when:

* Margin drop is severe.
* High-value customers are exposed.
* The company risks losing profitability or customers.
* Supplier dependency creates strategic vulnerability.

## Risk Explanation Requirements

Whenever ScenarioTwin AI classifies risk, it should explain:

1. What caused the risk.
2. Which products or customers are affected.
3. What financial exposure exists.
4. What operational constraint exists.
5. Why the final risk level was selected.
6. What action should be reviewed by leadership.

## Human Review Requirement

ScenarioTwin AI provides risk analysis and decision support only.

It must not present risk recommendations as automatic final decisions.

All High and Critical risk recommendations should be reviewed by human leadership before execution.

## Safety and Reliability Notes

ScenarioTwin AI should:

* Use synthetic data in the MVP.
* Avoid confidential or customer-identifiable information.
* Avoid unsupported claims.
* Clearly separate calculated metrics from recommendations.
* Prefer transparent, traceable reasoning.
* Use fallback behavior when external AI services are unavailable.
