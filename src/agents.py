def cfo_agent(summary: dict) -> dict:
    """
    CFO Agent for Supplier Cost Shock.
    Keeps compatibility with the first scenario.
    """

    profit_loss = summary["total_estimated_monthly_profit_loss"]
    margin_before = summary["avg_margin_before_pct"]
    margin_after = summary["avg_margin_after_pct"]
    margin_drop = summary["avg_margin_drop_pct_points"]

    if margin_drop >= 8:
        risk_level = "High"
    elif margin_drop >= 4:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    recommendation = (
        "Evaluate partial price increase and supplier renegotiation."
        if risk_level in ["Medium", "High"]
        else "Monitor margins without immediate price changes."
    )

    return {
        "agent": "CFO Agent",
        "focus": "Financial impact and profitability",
        "risk_level": risk_level,
        "analysis": (
            f"The supplier shock generates an estimated monthly profit loss of "
            f"{profit_loss:.2f}. Average margin decreases from {margin_before:.2f}% "
            f"to {margin_after:.2f}%, a drop of {margin_drop:.2f} percentage points."
        ),
        "recommendation": recommendation
    }


def coo_agent(affected_products_count: int, supplier_id: str) -> dict:
    """
    COO Agent for Supplier Cost Shock.
    Keeps compatibility with the first scenario.
    """

    if affected_products_count >= 3:
        risk_level = "High"
    elif affected_products_count == 2:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    return {
        "agent": "COO Agent",
        "focus": "Operations and supplier dependency",
        "risk_level": risk_level,
        "analysis": (
            f"The shock affects {affected_products_count} products linked to supplier {supplier_id}. "
            f"This indicates operational dependency and potential supply chain exposure."
        ),
        "recommendation": (
            "Identify alternative suppliers and review inventory coverage for affected products."
        )
    }


def sales_agent(customer_risk_count: int) -> dict:
    """
    Sales Agent for Supplier Cost Shock.
    Keeps compatibility with the first scenario.
    """

    if customer_risk_count >= 4:
        risk_level = "High"
    elif customer_risk_count >= 2:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    return {
        "agent": "Sales Agent",
        "focus": "Customer exposure and price sensitivity",
        "risk_level": risk_level,
        "analysis": (
            f"{customer_risk_count} customers are exposed to products affected by the supplier shock. "
            f"Any price increase should be evaluated carefully to avoid customer churn."
        ),
        "recommendation": (
            "Segment customers by price sensitivity before applying any price adjustment."
        )
    }


def supplier_risk_agent(summary: dict, customer_risk_count: int) -> dict:
    """
    Risk Agent for Supplier Cost Shock.
    Keeps compatibility with the first scenario.
    """

    margin_drop = summary["avg_margin_drop_pct_points"]

    if margin_drop >= 8 and customer_risk_count >= 4:
        risk_level = "Critical"
    elif margin_drop >= 6:
        risk_level = "High"
    elif margin_drop >= 3:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    return {
        "agent": "Risk Agent",
        "focus": "Enterprise risk and resilience",
        "risk_level": risk_level,
        "analysis": (
            f"The scenario combines a margin drop of {margin_drop:.2f} percentage points "
            f"with exposure across {customer_risk_count} customers. "
            f"This creates financial and commercial vulnerability."
        ),
        "recommendation": (
            "Prepare a mitigation plan with pricing, supplier diversification, and customer protection actions."
        )
    }


def run_boardroom_agents(simulation_result: dict) -> list:
    """
    Runs boardroom agents for Supplier Cost Shock.
    This function is preserved so the previous scenario does not break.
    """

    summary = simulation_result["summary"]
    affected_products = simulation_result["affected_products"]
    customer_risk = simulation_result["customer_risk"]

    agents_output = [
        cfo_agent(summary),
        coo_agent(
            affected_products_count=len(affected_products),
            supplier_id=summary["supplier_id"]
        ),
        sales_agent(
            customer_risk_count=len(customer_risk)
        ),
        supplier_risk_agent(
            summary=summary,
            customer_risk_count=len(customer_risk)
        )
    ]

    return agents_output


def demand_cfo_agent(summary: dict) -> dict:
    """
    CFO Agent for Demand Spike + Inventory Constraint.
    Evaluates revenue and profit at risk.
    """

    revenue_at_risk = summary["total_revenue_at_risk"]
    profit_at_risk = summary["total_profit_at_risk"]

    if profit_at_risk >= 8000:
        risk_level = "Critical"
    elif profit_at_risk >= 5000:
        risk_level = "High"
    elif profit_at_risk >= 2000:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    return {
        "agent": "CFO Agent",
        "focus": "Revenue at risk and profit protection",
        "risk_level": risk_level,
        "analysis": (
            f"The demand spike creates {revenue_at_risk:.2f} in revenue at risk "
            f"and {profit_at_risk:.2f} in profit at risk. "
            f"The company must protect margin while deciding which demand can realistically be fulfilled."
        ),
        "recommendation": (
            "Prioritize high-margin constrained products and avoid accepting demand that cannot be fulfilled profitably."
        )
    }


def demand_coo_agent(summary: dict) -> dict:
    """
    COO Agent for Demand Spike + Inventory Constraint.
    Evaluates inventory shortage and operational capacity.
    """

    constrained_count = summary["constrained_products_count"]
    shortage_units = summary["total_inventory_shortage_units"]
    service_level = summary["avg_service_level_pct"]

    if service_level < 60:
        risk_level = "Critical"
    elif service_level < 75:
        risk_level = "High"
    elif service_level < 90:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    return {
        "agent": "COO Agent",
        "focus": "Inventory constraint and fulfillment capacity",
        "risk_level": risk_level,
        "analysis": (
            f"{constrained_count} products are constrained, with {shortage_units:.2f} units of unmet demand. "
            f"The average service level is only {service_level:.2f}%, which indicates that operations "
            f"cannot fully absorb the demand spike."
        ),
        "recommendation": (
            "Prioritize production and replenishment for the most constrained products with the highest business impact."
        )
    }


def demand_sales_agent(customer_priority) -> dict:
    """
    Sales Agent for Demand Spike + Inventory Constraint.
    Evaluates which customers should be protected first.
    """

    customer_count = len(customer_priority)

    if customer_count == 0:
        return {
            "agent": "Sales Agent",
            "focus": "Customer prioritization",
            "risk_level": "Low",
            "analysis": (
                "No customer exposure was detected for constrained products."
            ),
            "recommendation": (
                "Continue monitoring customer demand."
            )
        }

    top_customer = customer_priority.iloc[0]["customer_name"]
    top_segment = customer_priority.iloc[0]["segment"]
    top_score = customer_priority.iloc[0]["priority_score"]

    if customer_count >= 4:
        risk_level = "High"
    elif customer_count >= 2:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    return {
        "agent": "Sales Agent",
        "focus": "Customer prioritization and retention",
        "risk_level": risk_level,
        "analysis": (
            f"{customer_count} customers are exposed to constrained products. "
            f"The highest-priority customer is {top_customer} from the {top_segment} segment "
            f"with a priority score of {top_score:.2f}."
        ),
        "recommendation": (
            "Allocate limited inventory first to strategic customers and communicate transparently with lower-priority accounts."
        )
    }


def demand_risk_agent(summary: dict) -> dict:
    """
    Risk Agent for Demand Spike + Inventory Constraint.
    Consolidates operational, financial and commercial risk.
    """

    final_risk = summary["final_risk"]
    service_level = summary["avg_service_level_pct"]
    constrained_count = summary["constrained_products_count"]

    return {
        "agent": "Risk Agent",
        "focus": "Enterprise resilience under constrained demand",
        "risk_level": final_risk,
        "analysis": (
            f"The scenario is classified as {final_risk}. "
            f"{constrained_count} products are constrained and the average service level is {service_level:.2f}%. "
            f"This creates a combined risk of lost revenue, customer dissatisfaction and operational overload."
        ),
        "recommendation": (
            "Activate a controlled allocation plan, prioritize strategic customers, and review production capacity immediately."
        )
    }


def run_demand_spike_boardroom_agents(simulation_result: dict) -> list:
    """
    Runs boardroom agents for Demand Spike + Inventory Constraint.
    This is the main scenario for the hackathon demo.
    """

    summary = simulation_result["summary"]
    customer_priority = simulation_result["customer_priority"]

    agents_output = [
        demand_cfo_agent(summary),
        demand_coo_agent(summary),
        demand_sales_agent(customer_priority),
        demand_risk_agent(summary)
    ]

    return agents_output