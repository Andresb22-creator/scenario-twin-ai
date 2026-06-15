from datetime import datetime


def get_insight_value(insight: dict, key: str, fallback: str = "Not available.") -> str:
    """
    Safely reads a Foundry IQ insight field.
    """

    if not insight:
        return fallback

    return insight.get(key, fallback)


def generate_supplier_report(result: dict) -> str:
    """
    Generates a CEO-ready report for Supplier Cost Shock.
    Preserved as fallback scenario.
    """

    simulation = result["simulation_result"]
    summary = simulation["summary"]
    agents = result["agents_output"]
    decision = result["final_decision"]
    insight = result.get("foundry_iq_insight", {})

    report_date = datetime.now().strftime("%Y-%m-%d %H:%M")

    report = f"""
# Enterprise Scenario Twin Report

## Executive Summary

Generated at: {report_date}

Scenario analyzed:
Supplier Cost Shock

Supplier:
{summary["supplier_id"]}

Cost increase:
{summary["cost_increase_pct"]}%

Final risk level:
{decision["final_risk"]}

Executive decision:
{decision["executive_decision"]}

Strategic action:
{decision["strategic_action"]}

## Business Impact

{decision["business_impact_summary"]}

Key metrics:

- Affected products: {summary["affected_products_count"]}
- Estimated monthly profit loss: {summary["total_estimated_monthly_profit_loss"]:.2f}
- Average margin before shock: {summary["avg_margin_before_pct"]:.2f}%
- Average margin after shock: {summary["avg_margin_after_pct"]:.2f}%
- Average margin drop: {summary["avg_margin_drop_pct_points"]:.2f} percentage points

## Foundry IQ Executive Insight

Insight source:
{get_insight_value(insight, "source")}

Mode:
{get_insight_value(insight, "mode")}

### Executive Diagnosis

{get_insight_value(insight, "executive_insight")}

### Decision Rationale

{get_insight_value(insight, "decision_rationale")}

### Product-Level Interpretation

{get_insight_value(insight, "product_interpretation")}

### Customer Prioritization Rationale

{get_insight_value(insight, "customer_interpretation")}

### Boardroom Trade-Off Analysis

{get_insight_value(insight, "boardroom_tradeoff")}

### Viability Check

{get_insight_value(insight, "viability_check")}

### What Not To Do

{get_insight_value(insight, "what_not_to_do")}

### Recommended Next Actions

{get_insight_value(insight, "recommended_next_actions")}

## Boardroom Agent Analysis
"""

    for agent in agents:
        report += f"""

### {agent["agent"]}

Focus:
{agent["focus"]}

Risk level:
{agent["risk_level"]}

Analysis:
{agent["analysis"]}

Recommendation:
{agent["recommendation"]}
"""

    report += """

## Safety and Reliability Notes

- This simulation uses synthetic company data only.
- The recommendation is decision support, not an automatic business decision.
- The deterministic simulation engine calculates business impact before agents reason over the scenario.
- Agent recommendations are separated by role to improve traceability.
- Final decisions should be reviewed by human leadership before execution.
"""

    return report


def generate_demand_spike_report(result: dict) -> str:
    """
    Generates a CEO-ready report for Demand Spike + Inventory Constraint.
    Main hackathon demo scenario.
    """

    simulation = result["simulation_result"]
    summary = simulation["summary"]
    agents = result["agents_output"]
    decision = result["final_decision"]
    insight = result.get("foundry_iq_insight", {})

    report_date = datetime.now().strftime("%Y-%m-%d %H:%M")

    report = f"""
# Enterprise Scenario Twin Report

## Executive Summary

Generated at: {report_date}

Scenario analyzed:
Demand Spike + Inventory Constraint

Demand spike:
{summary["demand_spike_pct"]}%

Final risk level:
{decision["final_risk"]}

Executive decision:
{decision["executive_decision"]}

Strategic action:
{decision["strategic_action"]}

Priority customer insight:
{decision["priority_customer_summary"]}

## Business Impact

{decision["business_impact_summary"]}

Key metrics:

- Products analyzed: {summary["products_analyzed"]}
- Constrained products: {summary["constrained_products_count"]}
- Total unmet demand: {summary["total_inventory_shortage_units"]:.2f} units
- Revenue at risk: {summary["total_revenue_at_risk"]:.2f}
- Profit at risk: {summary["total_profit_at_risk"]:.2f}
- Average service level: {summary["avg_service_level_pct"]:.2f}%

## Foundry IQ Executive Insight

Insight source:
{get_insight_value(insight, "source")}

Mode:
{get_insight_value(insight, "mode")}

## Executive Command Layer

This section translates the scenario analysis into an executable executive response. It defines what leadership should decide, what each area must do, and how teams must coordinate to avoid isolated actions or operational chaos.

### Strategic Executive Decision

{get_insight_value(insight, "strategic_executive_decision")}

### 24-Hour Command Plan

{get_insight_value(insight, "twenty_four_hour_command_plan")}

### Area Ownership

{get_insight_value(insight, "area_ownership_plan")}

### Cross-Functional Execution Plan

{get_insight_value(insight, "cross_functional_execution_plan")}

### Decision Sequence

{get_insight_value(insight, "decision_sequence")}

### Risks If No Action Is Taken

{get_insight_value(insight, "risks_if_no_action")}

### Decision Guardrails

{get_insight_value(insight, "decision_guardrails")}

## Decision Explanation

This section explains why the executive command was recommended, which products and customers are driving the decision, and how the boardroom agents evaluated the trade-offs.

### Executive Diagnosis

{get_insight_value(insight, "executive_insight")}

### Decision Rationale

{get_insight_value(insight, "decision_rationale")}

### Product-Level Interpretation

{get_insight_value(insight, "product_interpretation")}

### Customer Prioritization Rationale

{get_insight_value(insight, "customer_interpretation")}

### Boardroom Trade-Off Analysis

{get_insight_value(insight, "boardroom_tradeoff")}

### Viability Check

{get_insight_value(insight, "viability_check")}

### What Not To Do

{get_insight_value(insight, "what_not_to_do")}

### Recommended Next Actions

{get_insight_value(insight, "recommended_next_actions")}

### Human Review Note

{get_insight_value(insight, "human_review_note")}

## Boardroom Agent Analysis
"""

    for agent in agents:
        report += f"""

### {agent["agent"]}

Focus:
{agent["focus"]}

Risk level:
{agent["risk_level"]}

Analysis:
{agent["analysis"]}

Recommendation:
{agent["recommendation"]}
"""

    report += """

## Safety and Reliability Notes

- This simulation uses synthetic company data only.
- No confidential, customer-identifiable, or real business data is used.
- The recommendation is decision support, not an automatic business decision.
- The deterministic simulation engine calculates inventory, revenue, and profit impact before agents reason over the scenario.
- Foundry IQ Insight is grounded in the local knowledge base during fallback mode and is prepared for Microsoft Foundry IQ integration.
- The Executive Command Layer is designed to avoid isolated area actions by coordinating Operations, Sales, Finance, Risk, and Leadership.
- Final decisions should be reviewed by human leadership before execution.
"""

    return report


def generate_executive_report(result: dict) -> str:
    """
    Main report generator.
    Automatically selects the correct report based on scenario type.
    """

    scenario_name = result.get("scenario_name", "")

    if scenario_name == "Demand Spike + Inventory Constraint":
        return generate_demand_spike_report(result)

    return generate_supplier_report(result)