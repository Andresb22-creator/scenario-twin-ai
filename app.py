import sys
from pathlib import Path
from html import escape

import streamlit as st

# Allow app.py to import files from /src
BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"
sys.path.insert(0, str(SRC_DIR))

from orchestrator import run_enterprise_scenario_twin
from report_generator import generate_executive_report


st.set_page_config(
    page_title="ScenarioTwin AI",
    page_icon="🧠",
    layout="wide"
)


# -----------------------------
# Helper functions
# -----------------------------

def money(value):
    return f"S/ {float(value):,.2f}"


def number(value):
    return f"{float(value):,.0f}"


def pct(value):
    return f"{float(value):.2f}%"


def risk_class(risk_level: str) -> str:
    risk = risk_level.lower()

    if risk == "critical":
        return "risk-critical"
    if risk == "high":
        return "risk-high"
    if risk == "medium":
        return "risk-medium"

    return "risk-low"


def render_card(title: str, value: str, subtitle: str = ""):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">{escape(title)}</div>
            <div class="metric-value">{escape(value)}</div>
            <div class="metric-subtitle">{escape(subtitle)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_risk_card(risk_level: str):
    css_class = risk_class(risk_level)

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Final Risk</div>
            <div class="metric-value {css_class}">{escape(risk_level)}</div>
            <div class="metric-subtitle">Enterprise-level scenario severity</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def prepare_product_constraints_table(product_constraints):
    display_df = product_constraints[
        [
            "product_name",
            "spike_weekly_demand",
            "available_stock_after_safety",
            "inventory_shortage_units",
            "service_level_pct",
            "revenue_at_risk",
            "profit_at_risk",
            "constraint_level"
        ]
    ].copy()

    display_df = display_df.rename(
        columns={
            "product_name": "Product",
            "spike_weekly_demand": "Spike Demand",
            "available_stock_after_safety": "Available Stock",
            "inventory_shortage_units": "Shortage",
            "service_level_pct": "Service Level",
            "revenue_at_risk": "Revenue at Risk",
            "profit_at_risk": "Profit at Risk",
            "constraint_level": "Constraint"
        }
    )

    display_df["Spike Demand"] = display_df["Spike Demand"].map(number)
    display_df["Available Stock"] = display_df["Available Stock"].map(number)
    display_df["Shortage"] = display_df["Shortage"].map(number)
    display_df["Service Level"] = display_df["Service Level"].map(pct)
    display_df["Revenue at Risk"] = display_df["Revenue at Risk"].map(money)
    display_df["Profit at Risk"] = display_df["Profit at Risk"].map(money)

    return display_df


def prepare_customer_priority_table(customer_priority):
    display_df = customer_priority[
        [
            "customer_name",
            "segment",
            "strategic_value",
            "price_sensitivity",
            "exposed_revenue",
            "priority_score",
            "affected_products"
        ]
    ].copy()

    display_df = display_df.rename(
        columns={
            "customer_name": "Customer",
            "segment": "Segment",
            "strategic_value": "Strategic Value",
            "price_sensitivity": "Price Sensitivity",
            "exposed_revenue": "Exposed Revenue",
            "priority_score": "Priority Score",
            "affected_products": "Affected Products"
        }
    )

    display_df["Exposed Revenue"] = display_df["Exposed Revenue"].map(money)
    display_df["Priority Score"] = display_df["Priority Score"].map(
        lambda x: f"{float(x):,.2f}"
    )

    return display_df


# -----------------------------
# Visual style
# -----------------------------

st.markdown(
    """
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1250px;
        }

        .hero-title {
            font-size: 3rem;
            font-weight: 800;
            margin-bottom: 0.3rem;
        }

        .hero-subtitle {
            font-size: 1.4rem;
            font-weight: 600;
            margin-bottom: 1rem;
        }

        .demo-note {
            padding: 1rem 1.2rem;
            border-radius: 0.75rem;
            background: rgba(56, 139, 253, 0.12);
            border: 1px solid rgba(56, 139, 253, 0.35);
            margin-top: 1rem;
            margin-bottom: 1rem;
        }

        .metric-card {
            padding: 1.1rem 1.2rem;
            border-radius: 0.9rem;
            background: rgba(255, 255, 255, 0.045);
            border: 1px solid rgba(255, 255, 255, 0.12);
            min-height: 125px;
        }

        .metric-title {
            font-size: 0.9rem;
            font-weight: 600;
            opacity: 0.78;
            margin-bottom: 0.55rem;
        }

        .metric-value {
            font-size: 2rem;
            font-weight: 750;
            line-height: 1.1;
            margin-bottom: 0.4rem;
        }

        .metric-subtitle {
            font-size: 0.85rem;
            opacity: 0.65;
        }

        .risk-critical {
            color: #ff5c5c;
        }

        .risk-high {
            color: #ffb347;
        }

        .risk-medium {
            color: #ffd966;
        }

        .risk-low {
            color: #7bd88f;
        }

        .section-note {
            font-size: 1rem;
            opacity: 0.82;
            margin-bottom: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.header("Scenario Configuration")

scenario_label = st.sidebar.selectbox(
    "Scenario type",
    options=[
        "Demand Spike + Inventory Constraint",
        "Supplier Cost Shock"
    ],
    index=0
)

if scenario_label == "Demand Spike + Inventory Constraint":
    demand_spike_pct = st.sidebar.slider(
        "Demand spike (%)",
        min_value=10,
        max_value=80,
        value=40,
        step=5
    )

    supplier_id = "S001"
    cost_increase_pct = 18
    scenario_type = "demand_spike"

else:
    supplier_id = st.sidebar.selectbox(
        "Affected supplier",
        options=["S001", "S002", "S003", "S004"],
        index=0
    )

    cost_increase_pct = st.sidebar.slider(
        "Supplier cost increase (%)",
        min_value=1,
        max_value=50,
        value=18,
        step=1
    )

    demand_spike_pct = 40
    scenario_type = "supplier_cost_shock"


run_button = st.sidebar.button("Run Simulation")


# -----------------------------
# Header
# -----------------------------

st.markdown(
    """
    <div class="hero-title">🧠 ScenarioTwin AI</div>
    <div class="hero-subtitle">Enterprise Scenario Twin for Business Scenario Simulation</div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    ScenarioTwin AI simulates enterprise scenarios using synthetic company data,
    deterministic business impact calculations, and a multi-agent executive boardroom.
    """
)

if scenario_type == "demand_spike":
    st.markdown(
        f"""
        <div class="demo-note">
            <strong>Demo scenario:</strong> demand increases by <strong>{demand_spike_pct}%</strong>,
            but available inventory is not enough to fulfill all orders. The system recommends
            how to allocate limited stock, protect strategic customers, and reduce revenue at risk.
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        f"""
        <div class="demo-note">
            <strong>Demo scenario:</strong> supplier <strong>{supplier_id}</strong> increases costs by
            <strong>{cost_increase_pct}%</strong>. The system estimates margin impact and recommends
            pricing and supplier mitigation actions.
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()


# -----------------------------
# Run simulation
# -----------------------------

if run_button:
    st.session_state["result"] = run_enterprise_scenario_twin(
        scenario_type=scenario_type,
        demand_spike_pct=demand_spike_pct,
        supplier_id=supplier_id,
        cost_increase_pct=cost_increase_pct
    )

    st.session_state["scenario_type"] = scenario_type
    st.session_state["demand_spike_pct"] = demand_spike_pct
    st.session_state["supplier_id"] = supplier_id
    st.session_state["cost_increase_pct"] = cost_increase_pct


if "result" not in st.session_state:
    st.info("Configure the scenario in the sidebar and click **Run Simulation**.")

else:
    result = st.session_state["result"]
    scenario_type = st.session_state["scenario_type"]
    demand_spike_pct = st.session_state["demand_spike_pct"]
    supplier_id = st.session_state["supplier_id"]
    cost_increase_pct = st.session_state["cost_increase_pct"]

    if "error" in result:
        st.error(result["error"])

    else:
        simulation = result["simulation_result"]
        summary = simulation["summary"]
        agents_output = result["agents_output"]
        final_decision = result["final_decision"]

        overview_tab, impact_tab, customers_tab, boardroom_tab, foundry_tab, report_tab = st.tabs(
           [
                 "Overview",
                 "Operations Impact",
                 "Customer Priority",
                 "Boardroom Agents",
                 "Foundry IQ Insight",
                 "Executive Report"
            ]
      )

        # -----------------------------
        # Overview tab
        # -----------------------------

        with overview_tab:
            st.header("0. Scenario Input")

            col_a, col_b, col_c = st.columns(3)

            with col_a:
                render_card(
                    "Scenario",
                    result["scenario_name"],
                    "Selected enterprise simulation"
                )

            if scenario_type == "demand_spike":
                with col_b:
                    render_card(
                        "Demand Spike",
                        f"{demand_spike_pct}%",
                        "Unexpected demand increase"
                    )

                with col_c:
                    render_card(
                        "Products Analyzed",
                        str(summary["products_analyzed"]),
                        "Synthetic company product portfolio"
                    )

            else:
                with col_b:
                    render_card(
                        "Supplier",
                        supplier_id,
                        "Affected supplier"
                    )

                with col_c:
                    render_card(
                        "Cost Increase",
                        f"{cost_increase_pct}%",
                        "Supplier price increase"
                    )

            st.divider()

            st.header("1. Executive Decision")

            col1, col2, col3 = st.columns(3)

            with col1:
                render_risk_card(final_decision["final_risk"])

            if scenario_type == "demand_spike":
                with col2:
                    render_card(
                        "Revenue at Risk",
                        money(summary["total_revenue_at_risk"]),
                        "Potential revenue not fulfilled"
                    )

                with col3:
                    render_card(
                        "Average Service Level",
                        pct(summary["avg_service_level_pct"]),
                        "Expected fulfillment level"
                    )

            else:
                with col2:
                    render_card(
                        "Monthly Profit Loss",
                        money(summary["total_estimated_monthly_profit_loss"]),
                        "Estimated monthly impact"
                    )

                with col3:
                    render_card(
                        "Margin Drop",
                        f"{summary['avg_margin_drop_pct_points']:.2f} pts",
                        "Average margin compression"
                    )

            st.subheader("Recommended Executive Action")

            st.warning(final_decision["executive_decision"])
            st.info(final_decision["strategic_action"])

            if scenario_type == "demand_spike":
                st.success(final_decision["priority_customer_summary"])

            st.subheader("Business Impact Summary")
            st.write(final_decision["business_impact_summary"])

        # -----------------------------
        # Operations Impact tab
        # -----------------------------

        with impact_tab:
            st.header("2. Operations Impact")

            if scenario_type == "demand_spike":
                product_constraints = simulation["product_constraints"]
                display_product_df = prepare_product_constraints_table(
                    product_constraints
                )

                col1, col2, col3 = st.columns(3)

                with col1:
                    render_card(
                        "Unmet Demand",
                        f"{number(summary['total_inventory_shortage_units'])} units",
                        "Total demand that cannot be fulfilled"
                    )

                with col2:
                    render_card(
                        "Constrained Products",
                        str(summary["constrained_products_count"]),
                        "Products with inventory shortage"
                    )

                with col3:
                    render_card(
                        "Profit at Risk",
                        money(summary["total_profit_at_risk"]),
                        "Estimated profit exposure"
                    )

                st.subheader("Product Constraints - Demo View")
                st.markdown(
                    """
                    <div class="section-note">
                        This view focuses on the columns that matter most for executive decision-making.
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.dataframe(
                    display_product_df,
                    hide_index=True,
                    width="stretch"
                )

                with st.expander("Show full technical product table"):
                    st.dataframe(
                        product_constraints,
                        width="stretch"
                    )

            else:
                affected_products = simulation["affected_products"]

                st.subheader("Affected Products")

                st.dataframe(
                    affected_products[
                        [
                            "product_id",
                            "product_name",
                            "current_price",
                            "old_unit_cost",
                            "new_unit_cost",
                            "old_margin_pct",
                            "new_margin_pct",
                            "estimated_monthly_profit_loss"
                        ]
                    ],
                    width="stretch"
                )

        # -----------------------------
        # Customer Priority tab
        # -----------------------------

        with customers_tab:
            st.header("3. Customer Priority")

            if scenario_type == "demand_spike":
                customer_priority = simulation["customer_priority"]

                if customer_priority.empty:
                    st.info("No customer exposure detected.")
                else:
                    display_customer_df = prepare_customer_priority_table(
                        customer_priority
                    )

                    top_customer = customer_priority.iloc[0]["customer_name"]
                    top_segment = customer_priority.iloc[0]["segment"]
                    top_score = customer_priority.iloc[0]["priority_score"]

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        render_card(
                            "Top Priority Customer",
                            str(top_customer),
                            "Highest allocation priority"
                        )

                    with col2:
                        render_card(
                            "Segment",
                            str(top_segment),
                            "Customer segment"
                        )

                    with col3:
                        render_card(
                            "Priority Score",
                            f"{float(top_score):,.2f}",
                            "Composite prioritization score"
                        )

                    st.subheader("Customer Allocation Priority")

                    st.dataframe(
                        display_customer_df,
                        hide_index=True,
                        width="stretch"
                    )

                    with st.expander("Show full technical customer table"):
                        st.dataframe(
                            customer_priority,
                            width="stretch"
                        )

            else:
                customer_risk = simulation["customer_risk"]

                st.subheader("Customer Risk Exposure")

                st.dataframe(
                    customer_risk,
                    width="stretch"
                )

        # -----------------------------
        # Boardroom tab
        # -----------------------------

        with boardroom_tab:
            st.header("4. AI Boardroom Agent Analysis")

            st.markdown(
                """
                Each agent analyzes the same scenario from a different executive perspective.
                The final decision is produced by the Decision Orchestrator.
                """
            )

            for index, agent in enumerate(agents_output):
                with st.expander(
                    f"{agent['agent']} | Risk: {agent['risk_level']}",
                    expanded=(index == 0)
                ):
                    st.markdown(f"**Focus:** {agent['focus']}")
                    st.markdown(f"**Risk level:** {agent['risk_level']}")
                    st.markdown(f"**Analysis:** {agent['analysis']}")
                    st.markdown(f"**Recommendation:** {agent['recommendation']}")

        # -----------------------------
        # Foundry IQ tab
        # -----------------------------

        with foundry_tab:
            st.header("5. Foundry IQ Executive Insight")

            st.markdown("### Microsoft Foundry Integration Status")
 
            with st.container(border=True):
                st.markdown("#### ScenarioTwin AI - Microsoft Foundry Validation")

                status_col1, status_col2 = st.columns(2)

                with status_col1:
                    st.success("Foundry project: scenario-twin-ai-westus")
                    st.success("Model validated: DeepSeek-V3.2")
                    st.success("Foundry IQ / Knowledge Base: Active")
                    st.success("Knowledge source: scenario-twin-policy-files-v2")

                with status_col2:
                    st.success("Active policy files: 5 files")
                    st.success("AI Search connected: scenario-twin-ai-search-ncus")
                    st.warning("Foundry Agent runtime: too_many_requests / capacity issue")
                    st.info("Fallback-safe mode: Enabled for reliable live demo execution")

                st.caption(
                    "Demo strategy: the local Streamlit application is the primary live demo, "
                    "while Microsoft Foundry evidence is shown through the validated model, "
                    "active Knowledge Base, connected AI Search, and fallback-safe execution mode."
                )

            st.markdown(
                """
                This layer adds enterprise context from the local knowledge base and prepares the MVP
                for Microsoft Foundry IQ integration. It validates whether the recommendation is
                realistic, viable, explainable, and safe for human executive review.
                """
            )

            insight = result.get("foundry_iq_insight", {})

            col1, col2 = st.columns(2)

            with col1:
                render_card(
                    "Insight Source",
                    insight.get("source", "Not available"),
                    "Knowledge layer used for this recommendation"
                )

            with col2:
                render_card(
                    "Mode",
                    insight.get("mode", "Not available"),
                    "Fallback-safe or Foundry-ready mode"
                )

            st.divider()

            # -----------------------------
            # Executive Command Layer
            # -----------------------------

            st.subheader("Executive Command Layer")
            st.markdown(
                """
                This section translates the scenario analysis into an executable executive response.
                It defines what leadership should decide, what each area must do, and how teams must
                coordinate to avoid isolated actions or operational chaos.
                """
            )

            st.markdown("### Strategic Executive Decision")
            st.info(
                insight.get(
                    "strategic_executive_decision",
                    "No strategic executive decision available."
                )
            )

            st.markdown("### 24-Hour Command Plan")
            st.markdown(
                insight.get(
                    "twenty_four_hour_command_plan",
                    "No 24-hour command plan available."
                )
            )

            st.markdown("### Area Ownership")
            st.markdown(
                insight.get(
                    "area_ownership_plan",
                    "No area ownership plan available."
                )
            )

            st.markdown("### Cross-Functional Execution Plan")
            st.warning(
                insight.get(
                    "cross_functional_execution_plan",
                    "No cross-functional execution plan available."
                )
            )

            st.markdown("### Decision Sequence")
            st.markdown(
                insight.get(
                    "decision_sequence",
                    "No decision sequence available."
                )
            )

            st.markdown("### Risks If No Action Is Taken")
            st.error(
                insight.get(
                    "risks_if_no_action",
                    "No risk analysis available."
                )
            )

            st.markdown("### Decision Guardrails")
            st.markdown(
                insight.get(
                    "decision_guardrails",
                    "No decision guardrails available."
                )
            )

            st.divider()

            # -----------------------------
            # Executive Explanation Layer
            # -----------------------------

            st.subheader("Decision Explanation")
            st.markdown(
                """
                This section explains why the executive command was recommended, which products
                and customers are driving the decision, and how the boardroom agents evaluated
                the trade-offs.
                """
            )

            st.markdown("### Executive Diagnosis")
            st.info(
                insight.get(
                    "executive_insight",
                    "No executive insight available."
                )
            )

            st.markdown("### Decision Rationale")
            st.write(
                insight.get(
                    "decision_rationale",
                    "No decision rationale available."
                )
            )

            st.markdown("### Product-Level Interpretation")
            st.write(
                insight.get(
                    "product_interpretation",
                    "No product interpretation available."
                )
            )

            st.markdown("### Customer Prioritization Rationale")
            st.write(
                insight.get(
                    "customer_interpretation",
                    "No customer interpretation available."
                )
            )

            st.markdown("### Boardroom Trade-Off Analysis")
            st.write(
                insight.get(
                    "boardroom_tradeoff",
                    "No boardroom trade-off analysis available."
                )
            )

            st.markdown("### Viability Check")
            st.success(
                insight.get(
                    "viability_check",
                    "No viability check available."
                )
            )

            st.markdown("### What Not To Do")
            st.error(
                insight.get(
                    "what_not_to_do",
                    "No risk warning available."
                )
            )

            st.markdown("### Recommended Next Actions")
            st.markdown(
                insight.get(
                    "recommended_next_actions",
                    "No recommended next actions available."
                )
            )

            st.markdown("### Human Review Note")
            st.caption(
                insight.get(
                    "human_review_note",
                    "Human leadership should review the recommendation before execution."
                )
            )
        # -----------------------------
        # Report tab
        # -----------------------------

        with report_tab:
            st.header("6. Executive Report")

            report = generate_executive_report(result)

            st.download_button(
                label="Download Executive Report (.md)",
                data=report,
                file_name="scenario_twin_executive_report.md",
                mime="text/markdown"
            )

            with st.expander("Open full executive report", expanded=True):
                st.markdown(report)