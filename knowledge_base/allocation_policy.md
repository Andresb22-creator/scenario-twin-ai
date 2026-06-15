# Allocation Policy

## Purpose

This policy defines how Andes Clean Supply SAC should allocate limited inventory during demand spikes, stock shortages, or fulfillment constraints.

The goal is to support realistic and responsible executive decisions when the company cannot fulfill all customer demand.

## Core Principle

When inventory is limited, the company should not accept all demand without allocation rules.

ScenarioTwin AI should recommend a controlled allocation plan when available inventory is insufficient to fulfill all orders.

## Allocation Priorities

Limited inventory should be allocated based on the following priority factors:

1. Strategic customer value
2. Revenue exposure
3. Profit contribution
4. Product criticality
5. Service level risk
6. Customer relationship importance
7. Operational feasibility

No single factor should determine the full decision. The final recommendation should balance financial, operational, commercial, and risk considerations.

## Customer Priority Rules

Customers should receive higher allocation priority when they meet one or more of the following conditions:

* They have high strategic value.
* They represent significant exposed revenue.
* They belong to an important business segment.
* They depend on the product for operational continuity.
* They have an ongoing business relationship with the company.
* Losing or delaying service may create long-term commercial risk.

Customers with lower strategic value or lower exposed revenue may receive partial fulfillment or delayed fulfillment if inventory is constrained.

## Product Priority Rules

Products should receive higher replenishment or allocation priority when they meet one or more of the following conditions:

* They have critical inventory shortages.
* They generate high revenue at risk.
* They generate high profit at risk.
* They are required by high-priority customers.
* Their service level is significantly below acceptable thresholds.
* They are difficult to replenish quickly.

Products with lower shortage impact or lower customer dependency may be scheduled after critical products.

## Demand Spike Guidance

In a Demand Spike + Inventory Constraint scenario, ScenarioTwin AI should evaluate:

* Baseline demand
* Increased demand
* Available stock after safety stock
* Inventory shortage
* Service level
* Revenue at risk
* Profit at risk
* Customer priority
* Product constraint level

If demand exceeds available inventory, the system should recommend controlled allocation instead of full demand acceptance.

## Recommended Allocation Strategy

When the scenario risk is High or Critical, the recommended strategy should usually include:

1. Prioritize strategic customers first.
2. Allocate limited stock to products with the highest business impact.
3. Avoid accepting orders that cannot be fulfilled realistically.
4. Communicate proactively with customers that may receive delayed or partial fulfillment.
5. Accelerate replenishment for critical products.
6. Monitor service level and lost demand during the disruption.
7. Review the allocation plan with human leadership before execution.

## Partial Fulfillment

Partial fulfillment is acceptable when:

* It protects strategic customer relationships.
* It avoids complete service failure.
* It is communicated clearly to customers.
* It does not create unrealistic delivery promises.
* It supports better allocation of scarce inventory.

## Delayed Fulfillment

Delayed fulfillment is acceptable when:

* Inventory is insufficient.
* The customer has lower priority compared to strategic accounts.
* The delay is communicated clearly.
* The company has a realistic replenishment timeline.

## What ScenarioTwin AI Should Avoid

ScenarioTwin AI should avoid recommending:

* Accepting all demand when inventory is insufficient.
* Allocating inventory only based on revenue without considering strategic value.
* Ignoring operational capacity.
* Ignoring safety stock.
* Prioritizing low-impact orders over strategic customers.
* Making automatic final decisions without human review.
* Providing recommendations that are not actionable.

## Human Review Requirement

ScenarioTwin AI provides decision support only.

Final allocation decisions should be reviewed by human leadership before execution.

The system should clearly explain why a customer, product, or action is prioritized.
