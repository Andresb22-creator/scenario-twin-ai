from scenario_engine import (
    simulate_supplier_cost_shock,
    simulate_demand_spike_inventory_constraint
)

from agents import (
    run_boardroom_agents,
    run_demand_spike_boardroom_agents
)

from foundry_iq_client import generate_foundry_iq_insight


def generate_supplier_final_decision(
    simulation_result: dict,
    agents_output: list
) -> dict:
    """
    Decision Orchestrator for Supplier Cost Shock.
    Preserved as secondary scenario / fallback.
    """

    summary = simulation_result["summary"]

    risk_levels = [agent["risk_level"] for agent in agents_output]

    if "Critical" in risk_levels:
        final_risk = "Critical"
    elif risk_levels.count("High") >= 2:
        final_risk = "High"
    elif "High" in risk_levels or risk_levels.count("Medium") >= 2:
        final_risk = "Medium"
    else:
        final_risk = "Low"

    if final_risk in ["Critical", "High"]:
        decision = "Do not absorb the full supplier cost increase."
        strategic_action = (
            "Apply a controlled partial price increase, renegotiate supplier terms, "
            "and protect high-value customers with targeted commercial actions."
        )
    elif final_risk == "Medium":
        decision = "Apply selective mitigation."
        strategic_action = (
            "Monitor affected products, review pricing on high-exposure items, "
            "and prepare alternative supplier options."
        )
    else:
        decision = "Monitor the scenario without immediate structural changes."
        strategic_action = (
            "Continue tracking margins and supplier dependency."
        )

    return {
        "scenario_type": "Supplier Cost Shock",
        "final_risk": final_risk,
        "executive_decision": decision,
        "strategic_action": strategic_action,
        "business_impact_summary": (
            f"The scenario affects {summary['affected_products_count']} products. "
            f"Estimated monthly profit loss is "
            f"{summary['total_estimated_monthly_profit_loss']:.2f}. "
            f"Average margin drops from {summary['avg_margin_before_pct']:.2f}% "
            f"to {summary['avg_margin_after_pct']:.2f}%."
        )
    }


def generate_demand_spike_final_decision(
    simulation_result: dict,
    agents_output: list
) -> dict:
    """
    Decision Orchestrator for Demand Spike + Inventory Constraint.
    This is the main hackathon demo scenario.
    """

    summary = simulation_result["summary"]
    customer_priority = simulation_result["customer_priority"]

    final_risk = summary["final_risk"]

    if not customer_priority.empty:
        top_customer = customer_priority.iloc[0]["customer_name"]
        top_segment = customer_priority.iloc[0]["segment"]
    else:
        top_customer = "No exposed customer"
        top_segment = "N/A"

    if final_risk in ["Critical", "High"]:
        decision = "Do not accept all demand without allocation rules."
        strategic_action = (
            "Activate a controlled allocation plan, prioritize strategic customers, "
            "focus inventory on constrained high-impact products, and accelerate replenishment."
        )
    elif final_risk == "Medium":
        decision = "Accept demand selectively and monitor fulfillment capacity."
        strategic_action = (
            "Prioritize products with moderate shortages and protect customers with high strategic value."
        )
    else:
        decision = "Accept the demand spike with standard monitoring."
        strategic_action = (
            "Continue monitoring inventory and service levels."
        )

    return {
        "scenario_type": "Demand Spike + Inventory Constraint",
        "final_risk": final_risk,
        "executive_decision": decision,
        "strategic_action": strategic_action,
        "business_impact_summary": (
            f"The demand spike affects {summary['products_analyzed']} products, "
            f"with {summary['constrained_products_count']} products constrained. "
            f"Total unmet demand is {summary['total_inventory_shortage_units']:.2f} units. "
            f"Revenue at risk is {summary['total_revenue_at_risk']:.2f}, "
            f"profit at risk is {summary['total_profit_at_risk']:.2f}, "
            f"and average service level is {summary['avg_service_level_pct']:.2f}%."
        ),
        "priority_customer_summary": (
            f"The top priority customer is {top_customer} from the {top_segment} segment."
        )
    }


def run_supplier_cost_shock_scenario(
    supplier_id: str = "S001",
    cost_increase_pct: float = 18
) -> dict:
    """
    Runs the Supplier Cost Shock scenario.
    Secondary scenario / fallback.
    """

    simulation_result = simulate_supplier_cost_shock(
        supplier_id=supplier_id,
        cost_increase_pct=cost_increase_pct
    )

    if "error" in simulation_result:
        return simulation_result

    agents_output = run_boardroom_agents(simulation_result)

    final_decision = generate_supplier_final_decision(
        simulation_result=simulation_result,
        agents_output=agents_output
    )

    result = {
        "scenario_name": "Supplier Cost Shock",
        "simulation_result": simulation_result,
        "agents_output": agents_output,
        "final_decision": final_decision
    }

    result["foundry_iq_insight"] = generate_foundry_iq_insight(result)

    return result


def run_demand_spike_scenario(
    demand_spike_pct: float = 40
) -> dict:
    """
    Runs the Demand Spike + Inventory Constraint scenario.
    Main hackathon demo scenario.
    """

    simulation_result = simulate_demand_spike_inventory_constraint(
        demand_spike_pct=demand_spike_pct
    )

    if "error" in simulation_result:
        return simulation_result

    agents_output = run_demand_spike_boardroom_agents(simulation_result)

    final_decision = generate_demand_spike_final_decision(
        simulation_result=simulation_result,
        agents_output=agents_output
    )

    result = {
        "scenario_name": "Demand Spike + Inventory Constraint",
        "simulation_result": simulation_result,
        "agents_output": agents_output,
        "final_decision": final_decision
    }

    result["foundry_iq_insight"] = generate_foundry_iq_insight(result)

    return result


def run_enterprise_scenario_twin(
    scenario_type: str = "demand_spike",
    demand_spike_pct: float = 40,
    supplier_id: str = "S001",
    cost_increase_pct: float = 18
) -> dict:
    """
    Main entry point for the Enterprise Scenario Twin MVP.
    """

    if scenario_type == "supplier_cost_shock":
        return run_supplier_cost_shock_scenario(
            supplier_id=supplier_id,
            cost_increase_pct=cost_increase_pct
        )

    return run_demand_spike_scenario(
        demand_spike_pct=demand_spike_pct
    )


if __name__ == "__main__":
    result = run_enterprise_scenario_twin(
        scenario_type="demand_spike",
        demand_spike_pct=40
    )

    print("\n=== ENTERPRISE SCENARIO TWIN ===")

    print("\n--- SCENARIO ---")
    print(result["scenario_name"])

    print("\n--- FINAL DECISION ---")
    print(result["final_decision"])

    print("\n--- BOARDROOM AGENTS ---")
    for agent in result["agents_output"]:
        print(f"\n{agent['agent']} | Risk: {agent['risk_level']}")
        print(agent["analysis"])
        print("Recommendation:", agent["recommendation"])

    print("\n--- FOUNDRY IQ EXECUTIVE INSIGHT ---")
    insight = result["foundry_iq_insight"]
    print("Source:", insight["source"])
    print("Mode:", insight["mode"])
    print("\nExecutive Insight:")
    print(insight["executive_insight"])
    print("\nDecision Rationale:")
    print(insight["decision_rationale"])
    print("\nViability Check:")
    print(insight["viability_check"])