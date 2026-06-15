import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def load_data():
    """
    Loads the base company synthetic datasets.
    Used by the Supplier Cost Shock scenario.
    """

    products = pd.read_csv(DATA_DIR / "products.csv")
    suppliers = pd.read_csv(DATA_DIR / "suppliers.csv")
    customers = pd.read_csv(DATA_DIR / "customers.csv")
    sales = pd.read_csv(DATA_DIR / "sales.csv")

    return products, suppliers, customers, sales


def simulate_supplier_cost_shock(supplier_id: str, cost_increase_pct: float):
    """
    Simulates a supplier cost shock scenario.
    This remains as a secondary scenario / fallback.
    """

    products, suppliers, customers, sales = load_data()

    affected_products = products[products["main_supplier_id"] == supplier_id].copy()

    if affected_products.empty:
        return {
            "error": f"No products found for supplier {supplier_id}"
        }

    affected_products["old_unit_cost"] = affected_products["unit_cost"]
    affected_products["new_unit_cost"] = (
        affected_products["unit_cost"] * (1 + cost_increase_pct / 100)
    )

    affected_products["old_margin"] = (
        affected_products["current_price"] - affected_products["old_unit_cost"]
    )

    affected_products["new_margin"] = (
        affected_products["current_price"] - affected_products["new_unit_cost"]
    )

    affected_products["old_margin_pct"] = (
        affected_products["old_margin"] / affected_products["current_price"]
    )

    affected_products["new_margin_pct"] = (
        affected_products["new_margin"] / affected_products["current_price"]
    )

    affected_products["margin_drop_pct_points"] = (
        affected_products["old_margin_pct"] - affected_products["new_margin_pct"]
    )

    affected_products["monthly_profit_before"] = (
        affected_products["old_margin"] * affected_products["monthly_units_sold"]
    )

    affected_products["monthly_profit_after"] = (
        affected_products["new_margin"] * affected_products["monthly_units_sold"]
    )

    affected_products["estimated_monthly_profit_loss"] = (
        affected_products["monthly_profit_before"]
        - affected_products["monthly_profit_after"]
    )

    affected_product_ids = affected_products["product_id"].tolist()

    exposed_sales = sales[sales["product_id"].isin(affected_product_ids)].copy()

    exposed_customers = exposed_sales.merge(customers, on="customer_id", how="left")
    exposed_customers = exposed_customers.merge(
        affected_products[["product_id", "product_name"]],
        on="product_id",
        how="left"
    )

    customer_risk = (
        exposed_customers
        .groupby(
            [
                "customer_id",
                "customer_name",
                "segment",
                "price_sensitivity",
                "strategic_value"
            ]
        )
        .agg(
            exposed_revenue=("total_amount", "sum"),
            affected_products=("product_name", lambda x: ", ".join(sorted(set(x))))
        )
        .reset_index()
    )

    total_profit_loss = float(
        affected_products["estimated_monthly_profit_loss"].sum()
    )

    avg_margin_before = float(affected_products["old_margin_pct"].mean())
    avg_margin_after = float(affected_products["new_margin_pct"].mean())

    summary = {
        "supplier_id": supplier_id,
        "cost_increase_pct": cost_increase_pct,
        "affected_products_count": int(len(affected_products)),
        "total_estimated_monthly_profit_loss": round(total_profit_loss, 2),
        "avg_margin_before_pct": round(avg_margin_before * 100, 2),
        "avg_margin_after_pct": round(avg_margin_after * 100, 2),
        "avg_margin_drop_pct_points": round(
            (avg_margin_before - avg_margin_after) * 100,
            2
        ),
    }

    return {
        "summary": summary,
        "affected_products": affected_products.round(4),
        "customer_risk": customer_risk
    }


def load_demand_spike_data():
    """
    Loads datasets required by the Demand Spike + Inventory Constraint scenario.
    """

    products = pd.read_csv(DATA_DIR / "products.csv")
    customers = pd.read_csv(DATA_DIR / "customers.csv")
    sales = pd.read_csv(DATA_DIR / "sales.csv")
    inventory = pd.read_csv(DATA_DIR / "inventory.csv")
    demand_forecast = pd.read_csv(DATA_DIR / "demand_forecast.csv")

    return products, customers, sales, inventory, demand_forecast


def classify_inventory_constraint(row):
    """
    Classifies the inventory constraint level for each product.
    """

    shortage = row["inventory_shortage_units"]
    service_level = row["service_level_pct"]

    if shortage <= 0:
        return "Low"
    elif service_level < 70:
        return "Critical"
    elif service_level < 85:
        return "High"
    else:
        return "Medium"


def simulate_demand_spike_inventory_constraint(demand_spike_pct: float = 40):
    """
    Simulates a demand spike scenario where demand increases,
    but available inventory is limited.
    """

    products, customers, sales, inventory, demand_forecast = load_demand_spike_data()

    scenario = demand_forecast.merge(inventory, on="product_id", how="left")
    scenario = scenario.merge(products, on="product_id", how="left")

    scenario["scenario_demand_spike_pct"] = demand_spike_pct

    scenario["spike_weekly_demand"] = (
        scenario["baseline_weekly_demand"] * (1 + demand_spike_pct / 100)
    )

    scenario["available_stock_after_safety"] = (
        scenario["current_stock"] - scenario["safety_stock"]
    )

    scenario["available_stock_after_safety"] = scenario[
        "available_stock_after_safety"
    ].clip(lower=0)

    scenario["fulfillable_units"] = scenario[
        ["spike_weekly_demand", "available_stock_after_safety"]
    ].min(axis=1)

    scenario["inventory_shortage_units"] = (
        scenario["spike_weekly_demand"]
        - scenario["available_stock_after_safety"]
    ).clip(lower=0)

    scenario["service_level_pct"] = (
        scenario["fulfillable_units"] / scenario["spike_weekly_demand"] * 100
    )

    scenario["unfulfilled_demand_pct"] = (
        scenario["inventory_shortage_units"]
        / scenario["spike_weekly_demand"]
        * 100
    )

    scenario["unit_margin"] = (
        scenario["current_price"] - scenario["unit_cost"]
    )

    scenario["revenue_at_risk"] = (
        scenario["inventory_shortage_units"] * scenario["current_price"]
    )

    scenario["profit_at_risk"] = (
        scenario["inventory_shortage_units"] * scenario["unit_margin"]
    )

    scenario["constraint_level"] = scenario.apply(
        classify_inventory_constraint,
        axis=1
    )

    constrained_products = scenario[
        scenario["inventory_shortage_units"] > 0
    ].copy()

    constrained_product_ids = constrained_products["product_id"].tolist()

    exposed_sales = sales[
        sales["product_id"].isin(constrained_product_ids)
    ].copy()

    if exposed_sales.empty:
        customer_priority = pd.DataFrame(
            columns=[
                "customer_id",
                "customer_name",
                "segment",
                "price_sensitivity",
                "strategic_value",
                "exposed_revenue",
                "affected_products",
                "strategic_score",
                "sensitivity_score",
                "priority_score"
            ]
        )
    else:
        customer_priority = exposed_sales.merge(
            customers,
            on="customer_id",
            how="left"
        )

        customer_priority = customer_priority.merge(
            products[["product_id", "product_name"]],
            on="product_id",
            how="left"
        )

        customer_priority = (
            customer_priority
            .groupby(
                [
                    "customer_id",
                    "customer_name",
                    "segment",
                    "price_sensitivity",
                    "strategic_value"
                ]
            )
            .agg(
                exposed_revenue=("total_amount", "sum"),
                affected_products=(
                    "product_name",
                    lambda x: ", ".join(sorted(set(x)))
                )
            )
            .reset_index()
        )

        strategic_score_map = {
            "High": 3,
            "Medium": 2,
            "Low": 1
        }

        sensitivity_score_map = {
            "Low": 3,
            "Medium": 2,
            "High": 1
        }

        customer_priority["strategic_score"] = customer_priority[
            "strategic_value"
        ].map(strategic_score_map)

        customer_priority["sensitivity_score"] = customer_priority[
            "price_sensitivity"
        ].map(sensitivity_score_map)

        customer_priority["priority_score"] = (
            customer_priority["exposed_revenue"] * 0.01
            + customer_priority["strategic_score"] * 50
            + customer_priority["sensitivity_score"] * 20
        )

        customer_priority = customer_priority.sort_values(
            by="priority_score",
            ascending=False
        )

    total_shortage_units = float(scenario["inventory_shortage_units"].sum())
    total_revenue_at_risk = float(scenario["revenue_at_risk"].sum())
    total_profit_at_risk = float(scenario["profit_at_risk"].sum())
    avg_service_level = float(scenario["service_level_pct"].mean())
    constrained_products_count = int(len(constrained_products))

    if constrained_products_count >= 4 or avg_service_level < 75:
        final_risk = "Critical"
    elif constrained_products_count >= 3 or avg_service_level < 85:
        final_risk = "High"
    elif constrained_products_count >= 1:
        final_risk = "Medium"
    else:
        final_risk = "Low"

    summary = {
        "scenario_type": "Demand Spike + Inventory Constraint",
        "demand_spike_pct": demand_spike_pct,
        "products_analyzed": int(len(scenario)),
        "constrained_products_count": constrained_products_count,
        "total_inventory_shortage_units": round(total_shortage_units, 2),
        "total_revenue_at_risk": round(total_revenue_at_risk, 2),
        "total_profit_at_risk": round(total_profit_at_risk, 2),
        "avg_service_level_pct": round(avg_service_level, 2),
        "final_risk": final_risk
    }

    return {
        "summary": summary,
        "product_constraints": scenario.round(4),
        "customer_priority": customer_priority.round(4)
    }


if __name__ == "__main__":
    result = simulate_demand_spike_inventory_constraint(40)

    print("\n=== DEMAND SPIKE + INVENTORY CONSTRAINT SUMMARY ===")
    print(result["summary"])

    print("\n=== PRODUCT CONSTRAINTS ===")
    print(
        result["product_constraints"][
            [
                "product_id",
                "product_name",
                "baseline_weekly_demand",
                "spike_weekly_demand",
                "current_stock",
                "safety_stock",
                "available_stock_after_safety",
                "inventory_shortage_units",
                "service_level_pct",
                "revenue_at_risk",
                "profit_at_risk",
                "constraint_level"
            ]
        ]
    )

    print("\n=== CUSTOMER PRIORITY ===")
    print(result["customer_priority"])
    