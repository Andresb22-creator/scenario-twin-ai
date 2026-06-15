import os
from pathlib import Path
from typing import Dict, Any, List

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
KNOWLEDGE_BASE_DIR = BASE_DIR / "knowledge_base"

KNOWLEDGE_FILES = [
    "company_profile.md",
    "allocation_policy.md",
    "risk_policy.md",
    "agent_charters.md",
    "executive_decision_policy.md",
]


def load_knowledge_base() -> str:
    """
    Loads the local knowledge base documents.

    This is the local knowledge layer used by the MVP.
    In the real Foundry IQ integration, these documents can be connected
    as enterprise knowledge sources.
    """

    knowledge_sections = []

    for file_name in KNOWLEDGE_FILES:
        file_path = KNOWLEDGE_BASE_DIR / file_name

        if file_path.exists():
            content = file_path.read_text(encoding="utf-8")
            knowledge_sections.append(
                f"\n\n--- KNOWLEDGE SOURCE: {file_name} ---\n{content}"
            )

    return "\n".join(knowledge_sections)


def foundry_credentials_available() -> bool:
    """
    Checks whether external Foundry/Azure credentials are configured.

    The app continues working when credentials are missing.
    """

    load_dotenv()

    required_variables = [
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_OPENAI_API_KEY",
        "AZURE_OPENAI_DEPLOYMENT",
    ]

    return all(os.getenv(variable) for variable in required_variables)


def money(value) -> str:
    return f"S/ {float(value):,.2f}"


def number(value) -> str:
    return f"{float(value):,.0f}"


def pct(value) -> str:
    return f"{float(value):.2f}%"


def summarize_agents(agents_output: List[Dict[str, Any]]) -> str:
    """
    Converts boardroom agent outputs into a compact text summary.
    """

    agent_blocks = []

    for agent in agents_output:
        agent_blocks.append(
            "\n".join(
                [
                    f"Agent: {agent.get('agent', 'Unknown')}",
                    f"Focus: {agent.get('focus', 'N/A')}",
                    f"Risk level: {agent.get('risk_level', 'N/A')}",
                    f"Analysis: {agent.get('analysis', 'N/A')}",
                    f"Recommendation: {agent.get('recommendation', 'N/A')}",
                ]
            )
        )

    return "\n\n".join(agent_blocks)


def build_scenario_context(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extracts the most important scenario context for executive insight generation.
    """

    scenario_name = result.get("scenario_name", "Unknown Scenario")
    simulation = result.get("simulation_result", {})
    summary = simulation.get("summary", {})
    final_decision = result.get("final_decision", {})
    agents_output = result.get("agents_output", [])

    return {
        "scenario_name": scenario_name,
        "simulation": simulation,
        "summary": summary,
        "final_decision": final_decision,
        "agents_output": agents_output,
        "agents_summary": summarize_agents(agents_output),
    }


def get_top_product_by_metric(product_constraints, metric: str):
    """
    Returns the row of the product with the highest value for a metric.
    """

    if product_constraints is None or product_constraints.empty:
        return None

    if metric not in product_constraints.columns:
        return None

    return product_constraints.sort_values(
        by=metric,
        ascending=False
    ).iloc[0]


def get_top_customer(customer_priority):
    """
    Returns the top priority customer row.
    """

    if customer_priority is None or customer_priority.empty:
        return None

    return customer_priority.iloc[0]


def generate_demand_spike_business_grade_insight(result: Dict[str, Any]) -> Dict[str, str]:
    """
    Generates a richer executive insight for Demand Spike + Inventory Constraint.

    This version is designed to sound like an executive decision-support layer,
    not a generic summary.
    """

    context = build_scenario_context(result)

    simulation = context["simulation"]
    summary = context["summary"]
    final_decision = context["final_decision"]
    agents_output = context["agents_output"]

    product_constraints = simulation.get("product_constraints")
    customer_priority = simulation.get("customer_priority")

    final_risk = final_decision.get("final_risk", "Unknown")
    executive_decision = final_decision.get(
        "executive_decision",
        "No executive decision available."
    )
    strategic_action = final_decision.get(
        "strategic_action",
        "No strategic action available."
    )

    products_analyzed = summary.get("products_analyzed", 0)
    constrained_products = summary.get("constrained_products_count", 0)
    shortage_units = summary.get("total_inventory_shortage_units", 0)
    revenue_at_risk = summary.get("total_revenue_at_risk", 0)
    profit_at_risk = summary.get("total_profit_at_risk", 0)
    service_level = summary.get("avg_service_level_pct", 0)

    top_shortage_product = get_top_product_by_metric(
        product_constraints,
        "inventory_shortage_units"
    )
    top_revenue_product = get_top_product_by_metric(
        product_constraints,
        "revenue_at_risk"
    )
    top_profit_product = get_top_product_by_metric(
        product_constraints,
        "profit_at_risk"
    )
    top_customer = get_top_customer(customer_priority)

    if top_shortage_product is not None:
        top_shortage_product_name = top_shortage_product["product_name"]
        top_shortage_units = top_shortage_product["inventory_shortage_units"]
        top_shortage_service_level = top_shortage_product["service_level_pct"]
    else:
        top_shortage_product_name = "No constrained product"
        top_shortage_units = 0
        top_shortage_service_level = 0

    if top_revenue_product is not None:
        top_revenue_product_name = top_revenue_product["product_name"]
        top_revenue_product_value = top_revenue_product["revenue_at_risk"]
    else:
        top_revenue_product_name = "No revenue exposure product"
        top_revenue_product_value = 0

    if top_profit_product is not None:
        top_profit_product_name = top_profit_product["product_name"]
        top_profit_product_value = top_profit_product["profit_at_risk"]
    else:
        top_profit_product_name = "No profit exposure product"
        top_profit_product_value = 0

    if top_customer is not None:
        top_customer_name = top_customer["customer_name"]
        top_customer_segment = top_customer["segment"]
        top_customer_revenue = top_customer["exposed_revenue"]
        top_customer_products = top_customer["affected_products"]
        top_customer_score = top_customer["priority_score"]
    else:
        top_customer_name = "No exposed customer"
        top_customer_segment = "N/A"
        top_customer_revenue = 0
        top_customer_products = "N/A"
        top_customer_score = 0

    agent_risks = {
        agent.get("agent", "Unknown"): agent.get("risk_level", "Unknown")
        for agent in agents_output
    }

    executive_insight = (
        f"This is not only a sales growth opportunity; it is a constrained growth scenario. "
        f"Demand increased beyond what the company can realistically fulfill, leaving the business "
        f"with an average service level of {pct(service_level)}. The scenario is classified as "
        f"{final_risk} because {constrained_products} of {products_analyzed} analyzed products are constrained, "
        f"unmet demand reaches {number(shortage_units)} units, revenue at risk is {money(revenue_at_risk)}, "
        f"and profit at risk is {money(profit_at_risk)}. The executive issue is not whether demand exists, "
        f"but which demand should be fulfilled first without overcommitting the operation."
    )

    decision_rationale = (
        f"The recommended decision is: '{executive_decision}' This is consistent with the company profile, "
        f"allocation policy, risk policy, agent charters, and executive decision policy. The strongest business "
        f"rationale is that accepting all demand would create unrealistic fulfillment promises. The company should "
        f"use a controlled allocation plan, protect strategic customers, and focus replenishment on constrained "
        f"products with the highest business impact."
    )

    product_interpretation = (
        f"The most constrained product by shortage is {top_shortage_product_name}, with "
        f"{number(top_shortage_units)} units of unmet demand and a service level of "
        f"{pct(top_shortage_service_level)}. The product with the highest revenue exposure is "
        f"{top_revenue_product_name}, with {money(top_revenue_product_value)} at risk. The product with the "
        f"highest profit exposure is {top_profit_product_name}, with {money(top_profit_product_value)} at risk. "
        f"This means the company should not treat all product shortages equally; replenishment should be ranked "
        f"by shortage severity, customer dependency, revenue exposure, and profit impact."
    )

    customer_interpretation = (
        f"The highest-priority customer is {top_customer_name} from the {top_customer_segment} segment. "
        f"This customer has {money(top_customer_revenue)} in exposed revenue, a priority score of "
        f"{float(top_customer_score):,.2f}, and exposure to these constrained products: {top_customer_products}. "
        f"This customer should be protected first because the allocation policy prioritizes strategic value, "
        f"revenue exposure, customer relationship importance, and operational continuity."
    )

    boardroom_tradeoff = (
        f"The boardroom agents point to a clear trade-off. The CFO Agent is focused on protecting profit "
        f"and avoiding unprofitable fulfillment promises. The COO Agent highlights that the operation cannot "
        f"absorb the spike with a service level of only {pct(service_level)}. The Sales Agent prioritizes "
        f"strategic customer retention, especially {top_customer_name}. The Risk Agent classifies the scenario "
        f"as {final_risk}, warning that accepting all demand could create customer dissatisfaction, operational "
        f"overload, and reputational damage. These perspectives support a controlled allocation decision rather "
        f"than a broad acceptance of all orders."
    )

    viability_check = (
        f"The recommendation is viable because it respects the current inventory constraint, the low service "
        f"level, the customer priority ranking, and the financial exposure. It does not assume that demand can be "
        f"fulfilled just because demand exists. It also keeps the decision human-reviewable, which is required "
        f"for High or Critical risk scenarios."
    )

    what_not_to_do = (
        "The company should not accept all orders as normal growth, should not promise full fulfillment before "
        "checking replenishment capacity, should not allocate inventory only by order size, and should not ignore "
        "strategic customer exposure. The company should also avoid making automatic execution decisions without "
        "leadership review."
    )

    strategic_executive_decision = (
        "Treat the demand spike as a controlled allocation event, not as normal sales growth. "
        "Do not accept new full-fulfillment commitments until inventory recovery, customer priority, "
        "and replenishment capacity are validated by leadership."
    )

    twenty_four_hour_command_plan = (
        f"- Operations freezes unrestricted allocation and validates available stock by product.\n"
        f"- Sales contacts {top_customer_name} and other priority accounts with controlled fulfillment options.\n"
        f"- Finance reviews revenue and profit exposure by constrained product.\n"
        f"- Risk monitors service-level deterioration, customer dissatisfaction, and reputational exposure.\n"
        f"- Leadership approves the allocation plan before execution."
    )

    area_ownership_plan = (
        "Operations owns inventory availability, fulfillment feasibility, safety stock protection, and replenishment timing.\n"
        "Sales owns customer communication, strategic account prioritization, and expectation management.\n"
        "Finance owns profit exposure, margin protection, revenue-at-risk validation, and exception approval.\n"
        "Risk owns escalation criteria, reputational exposure, overcommitment risk, and human-review enforcement.\n"
        "Leadership owns final approval when service, profit, and customer retention priorities conflict."
    )

    cross_functional_execution_plan = (
        "The company must execute this scenario as a coordinated cross-functional response, not as isolated area actions. "
        "Sales cannot promise delivery before Operations validates available stock. Operations cannot reallocate scarce "
        "inventory without Sales confirming customer priority and Finance confirming business impact. Finance should not "
        "block fulfillment decisions using margin alone when Sales identifies strategic relationship risk. Risk must escalate "
        "any decision that creates overcommitment, service-level deterioration, or reputational exposure. Leadership resolves "
        "conflicts between service continuity, profitability, and customer retention."
    )

    decision_sequence = (
        "- Step 1: Operations confirms available stock, safety stock limits, and constrained products.\n"
        "- Step 2: Finance ranks constrained products by revenue at risk and profit at risk.\n"
        "- Step 3: Sales ranks exposed customers by strategic value, exposed revenue, and relationship risk.\n"
        "- Step 4: Risk validates whether the proposed allocation creates unacceptable second-order risk.\n"
        "- Step 5: Leadership approves allocation rules, exceptions, and customer communication before execution."
    )

    risks_if_no_action = (
        "If the company does not act, it may convert a growth opportunity into a service failure. "
        "The main risks are accepting orders that cannot be fulfilled, damaging strategic customer relationships, "
        "losing revenue and profit from constrained products, overloading operations, and creating inconsistent messages "
        "between Sales, Operations, Finance, and leadership."
    )

    decision_guardrails = (
        "- Do not promise full fulfillment until available stock and replenishment timing are confirmed.\n"
        "- Do not allocate inventory only by order size or customer pressure.\n"
        "- Do not override safety stock without leadership approval.\n"
        "- Do not let Sales, Operations, Finance, or Risk execute conflicting actions independently.\n"
        "- Do not treat the demand spike as normal growth while service level remains critically low.\n"
        "- Do not make the recommendation an automatic decision without human review."
    )

    recommended_next_actions = (
        "- Activate a controlled allocation plan.\n"
        f"- Protect {top_customer_name} and other strategic customers first.\n"
        f"- Prioritize replenishment for {top_shortage_product_name} and other critical constrained products.\n"
        "- Review partial fulfillment options instead of accepting all orders.\n"
        "- Communicate expected delays clearly to lower-priority or less exposed customers.\n"
        "- Monitor service level, lost demand, revenue at risk, and profit at risk daily.\n"
        "- Escalate the final allocation plan to human leadership before execution."
    )

    return {
        "source": "Local Knowledge Fallback",
        "mode": "fallback_safe_mode",
        "executive_insight": executive_insight,
        "decision_rationale": decision_rationale,
        "product_interpretation": product_interpretation,
        "customer_interpretation": customer_interpretation,
        "boardroom_tradeoff": boardroom_tradeoff,
        "viability_check": viability_check,
        "what_not_to_do": what_not_to_do,
        "recommended_next_actions": recommended_next_actions,
        "strategic_executive_decision": strategic_executive_decision,
        "twenty_four_hour_command_plan": twenty_four_hour_command_plan,
        "area_ownership_plan": area_ownership_plan,
        "cross_functional_execution_plan": cross_functional_execution_plan,
        "decision_sequence": decision_sequence,
        "risks_if_no_action": risks_if_no_action,
        "decision_guardrails": decision_guardrails,        
        "human_review_note": (
            "This is decision support only. Human leadership should review the recommendation before execution."
        ),
        "agent_risks": str(agent_risks),
    }


def generate_supplier_business_grade_insight(result: Dict[str, Any]) -> Dict[str, str]:
    """
    Generates a richer local executive insight for Supplier Cost Shock.
    """

    context = build_scenario_context(result)

    summary = context["summary"]
    final_decision = context["final_decision"]

    final_risk = final_decision.get("final_risk", "Unknown")
    executive_decision = final_decision.get(
        "executive_decision",
        "No executive decision available."
    )
    strategic_action = final_decision.get(
        "strategic_action",
        "No strategic action available."
    )

    affected_products = summary.get("affected_products_count", 0)
    profit_loss = summary.get("total_estimated_monthly_profit_loss", 0)
    margin_before = summary.get("avg_margin_before_pct", 0)
    margin_after = summary.get("avg_margin_after_pct", 0)
    margin_drop = summary.get("avg_margin_drop_pct_points", 0)

    executive_insight = (
        f"The supplier cost shock creates a {final_risk} business risk because it affects "
        f"{affected_products} products and produces an estimated monthly profit loss of "
        f"{money(profit_loss)}. Average margin decreases from {pct(margin_before)} to "
        f"{pct(margin_after)}, a drop of {margin_drop:.2f} percentage points."
    )

    decision_rationale = (
        f"The recommended decision is: '{executive_decision}' This is consistent with the company profile, "
        f"risk policy, and executive decision policy because the company should avoid absorbing the full cost "
        f"increase without mitigation and should avoid passing the full impact to customers without considering "
        f"price sensitivity."
    )

    product_interpretation = (
        "The affected products should be reviewed based on margin impact, monthly volume, customer exposure, "
        "and supplier dependency. The company should focus first on products with material profit loss and high "
        "customer exposure."
    )

    customer_interpretation = (
        "Customer communication should be segmented. High-value and price-sensitive customers should receive "
        "targeted communication before any price adjustment is implemented."
    )

    boardroom_tradeoff = (
        "The CFO Agent prioritizes margin protection, the COO Agent focuses on supplier dependency and continuity, "
        "the Sales Agent protects customer retention, and the Risk Agent evaluates enterprise vulnerability. "
        "The trade-off is between protecting profitability and avoiding customer churn."
    )

    viability_check = (
        "The recommendation is viable because it combines partial price action, supplier renegotiation, "
        "customer segmentation, and human review rather than relying on a single automatic response."
    )

    what_not_to_do = (
        "The company should not absorb the full cost increase without analysis, should not apply a blanket price "
        "increase to all customers, and should not ignore supplier dependency risk."
    )

    recommended_next_actions = (
        "- Quantify margin impact by affected product.\n"
        "- Renegotiate with the supplier.\n"
        "- Apply selective pricing actions only where justified.\n"
        "- Protect high-value customers with targeted communication.\n"
        "- Review supplier alternatives.\n"
        "- Escalate the final mitigation plan to human leadership."
    )

    return {
        "source": "Local Knowledge Fallback",
        "mode": "fallback_safe_mode",
        "executive_insight": executive_insight,
        "decision_rationale": decision_rationale,
        "product_interpretation": product_interpretation,
        "customer_interpretation": customer_interpretation,
        "boardroom_tradeoff": boardroom_tradeoff,
        "viability_check": viability_check,
        "what_not_to_do": what_not_to_do,
        "recommended_next_actions": recommended_next_actions,
        "human_review_note": (
            "This is decision support only. Human leadership should review the recommendation before execution."
        ),
        "agent_risks": "{}",
    }


def generate_local_fallback_insight(result: Dict[str, Any]) -> Dict[str, str]:
    """
    Generates a safe local executive insight when Foundry credentials are not configured.

    This fallback does not replace Foundry IQ.
    It keeps the MVP reliable during development and demos.
    """

    scenario_name = result.get("scenario_name", "")

    if scenario_name == "Demand Spike + Inventory Constraint":
        return generate_demand_spike_business_grade_insight(result)

    return generate_supplier_business_grade_insight(result)


def generate_foundry_iq_insight(result: Dict[str, Any]) -> Dict[str, str]:
    """
    Main entry point for the Foundry IQ insight layer.

    Current MVP behavior:
    - If Foundry/Azure credentials are not configured, use local fallback.
    - If credentials are configured, this function is ready to be extended
      with a real Foundry Agent / Foundry IQ call.
    """

    knowledge_base = load_knowledge_base()

    if not knowledge_base.strip():
        return {
            "source": "Knowledge Base Missing",
            "mode": "error_safe_mode",
            "executive_insight": (
                "Knowledge base documents were not found. The system cannot generate "
                "a grounded executive insight."
            ),
            "decision_rationale": "No knowledge base context available.",
            "product_interpretation": "No product context available.",
            "customer_interpretation": "No customer context available.",
            "boardroom_tradeoff": "No boardroom context available.",
            "viability_check": "Unable to validate recommendation viability.",
            "what_not_to_do": "Review knowledge_base/ files before making recommendations.",
            "recommended_next_actions": "- Review knowledge_base/ files.",
            "human_review_note": "Human review is required.",
            "agent_risks": "{}",
        }

    if not foundry_credentials_available():
        return generate_local_fallback_insight(result)

    # Placeholder for the real Microsoft Foundry / Foundry IQ integration.
    # In the next integration stage, this section will call the configured
    # Foundry Agent or Azure AI endpoint using credentials stored in .env.
    fallback_result = generate_local_fallback_insight(result)
    fallback_result["source"] = "Foundry IQ Ready - Local Fallback"
    fallback_result["mode"] = "foundry_ready_fallback"

    return fallback_result


if __name__ == "__main__":
    from orchestrator import run_enterprise_scenario_twin

    result = run_enterprise_scenario_twin(
        scenario_type="demand_spike",
        demand_spike_pct=40
    )

    insight = generate_foundry_iq_insight(result)

    print("\n=== FOUNDRY IQ EXECUTIVE INSIGHT V2 ===")
    print("Source:", insight["source"])
    print("Mode:", insight["mode"])

    print("\nExecutive Insight:")
    print(insight["executive_insight"])

    print("\nDecision Rationale:")
    print(insight["decision_rationale"])

    print("\nProduct Interpretation:")
    print(insight["product_interpretation"])

    print("\nCustomer Interpretation:")
    print(insight["customer_interpretation"])

    print("\nBoardroom Trade-Off:")
    print(insight["boardroom_tradeoff"])

    print("\nViability Check:")
    print(insight["viability_check"])

    print("\nWhat Not To Do:")
    print(insight["what_not_to_do"])

    print("\nRecommended Next Actions:")
    print(insight["recommended_next_actions"])

    print("\nHuman Review Note:")
    print(insight["human_review_note"])