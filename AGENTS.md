\# AGENTS.md — ScenarioTwin AI



\## Project Overview



ScenarioTwin AI is an enterprise scenario simulation system designed to help leadership teams analyze business disruptions, quantify operational and financial impact, and generate coordinated executive decision-support outputs.



The MVP focuses on a Demand Spike + Inventory Constraint scenario.



Core scenario:



\* Demand increases by 40%.

\* 6 products are analyzed.

\* 6 products are constrained.

\* Total unmet demand: 1,778 units.

\* Revenue at risk: S/ 21,691.40.

\* Profit at risk: S/ 9,600.40.

\* Average service level: 49.41%.

\* Top priority customer: Limpieza Total SAC.



ScenarioTwin AI must not make automatic business decisions. It provides decision-support recommendations for human leadership review.



\## Product Positioning



ScenarioTwin AI is not a chatbot and not just a dashboard.



It combines:



\* Deterministic scenario simulation.

\* Boardroom-style agent reasoning.

\* Executive orchestration.

\* Microsoft Foundry model validation.

\* Foundry IQ-ready enterprise knowledge grounding.

\* Fallback-safe mode for reliability.



The goal is to help leaders understand what is happening, what is at risk, which areas must coordinate, and what decision guardrails should be followed.



\## Main Architecture



The project should preserve this architecture:



1\. Synthetic business data

2\. Scenario engine

3\. Operational and financial impact metrics

4\. Boardroom agents

5\. Executive orchestrator

6\. Foundry model layer

7\. Foundry IQ-ready knowledge base

8\. Executive decision report

9\. Human review note

10\. Fallback-safe mode



\## Current Microsoft Foundry Context



Microsoft Foundry setup:



\* Foundry project: scenario-twin-ai-westus

\* Model validated: DeepSeek-V3.2

\* Agent created: scenario-twin-executive-insight-agent-westus

\* Foundry IQ knowledge base created and active

\* Knowledge source: scenario-twin-policy-files-v2

\* 5 synthetic policy files active

\* Azure AI Search connected: scenario-twin-ai-search-ncus



Important limitation:

Foundry Agent runtime may fail due to temporary capacity or too\_many\_requests errors. The local app must remain stable through fallback-safe mode.



Do not remove fallback-safe mode.



\## Safety Rules



Codex must follow these rules:



\* Do not add real customer data.

\* Do not add personal data.

\* Do not add secrets, API keys, tokens, credentials, or connection strings.

\* Do not hardcode environment variables.

\* Do not remove `.env.example`.

\* Do not weaken the human review requirement.

\* Do not present AI recommendations as automatic final decisions.

\* Do not make the app fully dependent on an external model runtime.

\* Preserve fallback-safe mode.



\## Coding Guidelines



Use simple, readable Python.



Prefer:



\* Clear function names.

\* Modular files inside `src/`.

\* Deterministic calculations for scenario metrics.

\* Streamlit UI improvements that are easy to understand.

\* Defensive error handling.

\* Clear labels explaining Microsoft Foundry integration status.



Avoid:



\* Overengineering.

\* Large unnecessary dependencies.

\* Complex cloud integrations unless explicitly requested.

\* Rewriting the entire app without need.

\* Removing existing working functionality.



\## Important Files



\* `app.py`: Main Streamlit interface.

\* `src/scenario\_engine.py`: Scenario calculations.

\* `src/agents.py`: Boardroom agent logic.

\* `src/orchestrator.py`: Executive orchestration.

\* `src/foundry\_iq\_client.py`: Foundry IQ / fallback-safe logic.

\* `src/report\_generator.py`: Executive report generation.

\* `data/`: Synthetic business data.

\* `knowledge\_base/`: Synthetic enterprise policy files.

\* `README.md`: Project documentation.



\## Development Commands



Run the app:



```bash

streamlit run app.py

```



Install dependencies:



```bash

pip install -r requirements.txt

```



Basic syntax check:



```bash

python -m py\_compile app.py src/scenario\_engine.py src/agents.py src/orchestrator.py src/foundry\_iq\_client.py src/report\_generator.py

```



\## Preferred Improvement Priorities



When improving the project, prioritize in this order:



1\. Improve reliability and avoid runtime crashes.

2\. Improve the Streamlit demo experience.

3\. Improve executive report clarity.

4\. Improve Microsoft Foundry integration status visibility.

5\. Improve README and architecture documentation.

6\. Improve modularity and code readability.

7\. Add tests only if they are simple and useful.

8\. Add new scenarios only after the current MVP is stable.



\## UI Requirements



The Streamlit app should clearly show:



\* ScenarioTwin AI title and value proposition.

\* Scenario configuration.

\* Key impact metrics.

\* Operations impact.

\* Customer priority.

\* Boardroom agent analysis.

\* Microsoft Foundry Integration Status.

\* Foundry Model Layer: DeepSeek-V3.2 validated.

\* Foundry IQ Knowledge Base: active.

\* Azure AI Search: connected.

\* Fallback-safe mode: enabled when external runtime is unavailable.

\* Executive report.

\* Human review note.



\## Executive Output Requirements



Executive recommendations should include:



1\. Executive Command Layer

2\. Cross-Functional Execution Plan

3\. Decision Explanation

4\. Decision Guardrails

5\. Human Review Note



The output must coordinate:



\* Operations

\* Sales

\* Finance

\* Risk

\* Leadership



\## Demo Goal



The final hackathon demo should show that ScenarioTwin AI can:



\* Simulate a business disruption.

\* Quantify business impact.

\* Generate cross-functional executive recommendations.

\* Use Microsoft Foundry model validation and Foundry IQ-ready knowledge grounding.

\* Remain reliable through fallback-safe mode.

\* Keep humans in control for critical business decisions.



\## Change Style



For every meaningful change, Codex should explain:



\* What was changed.

\* Why it was changed.

\* Which files were modified.

\* How to test it.

\* Any limitations or follow-up work.



Do not make large unrelated changes in a single task.



