# ScenarioTwin AI - Submission Description

## Project title

ScenarioTwin AI

## Short description

ScenarioTwin AI is a reasoning-agent prototype for executive decision support. It simulates business disruption scenarios, analyzes operational and financial impact, prioritizes customers, and generates a boardroom-ready action plan with Microsoft Foundry validation evidence and human review.

## Track

Reasoning Agents

## Project description

ScenarioTwin AI helps business leaders make better decisions during operational disruption.

The demo scenario focuses on a demand spike with inventory constraints. Customer demand increases by 40%, but available inventory is not enough to fulfill all orders. In this situation, accepting all demand without allocation rules can create stockouts, service failures, lost revenue, operational overload, and customer dissatisfaction.

ScenarioTwin AI simulates the scenario, calculates the business impact, identifies constrained products, ranks exposed customers, and uses executive reasoning agents to evaluate the decision from different perspectives.

The system includes four boardroom agents:

* CFO Agent: evaluates revenue at risk, profit at risk, and margin protection.
* COO Agent: evaluates inventory constraints, fulfillment capacity, and execution feasibility.
* Sales Agent: evaluates customer priority, retention, and strategic account impact.
* Risk Agent: evaluates overcommitment risk, enterprise resilience, and decision guardrails.

The final output is a boardroom-ready executive report with a recommended decision, risk explanation, decision sequence, next actions, and a human review note.

ScenarioTwin AI is not just a dashboard. It is a reasoning-agent system that helps leadership decide what to do next.

## Microsoft Foundry usage

ScenarioTwin AI includes Microsoft Foundry validation as part of the architecture.

The DeepSeek-V3.2 model was validated successfully in Microsoft Foundry Models. A Foundry IQ Knowledge Base was created and activated with 5 policy files, and Azure AI Search was connected.

During development, the Foundry Agent runtime experienced capacity limitations, so the live demo uses fallback-safe mode to ensure reliable execution. The architecture remains ready for Foundry-based reasoning while keeping the demo stable.

## Key demo results

* Demand spike: 40%
* Products analyzed: 6
* Constrained products: 6
* Unfulfilled units: 1,778
* Revenue at risk: S/ 21,691.40
* Profit at risk: S/ 9,600.40
* Average service level: 49.41%
* Top priority customer: Limpieza Total SAC
* Final risk level: Critical

## Final recommendation

Do not accept all demand without allocation rules.

The company should activate a controlled allocation plan, protect strategic customers first, prioritize replenishment of constrained high-impact products, and escalate the final allocation decision to human leadership before execution.

## GitHub repository

https://github.com/Andresb22-creator/scenario-twin-ai

## Demo video

https://vimeo.com/1201302599?share=copy&fl=sv&fe=ci
