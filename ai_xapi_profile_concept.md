Below is a **proposed xAPI Profile** you can adopt (and iterate on) to **capture, evaluate, and visualize AI‑agent actions**—including human‑to‑AI instructions and AI‑to‑tool/AI‑to‑AI activity. It follows xAPI conventions (statements, IRIs, profiles, extensions) and maps naturally onto MCP concepts (tools, resources, prompts, streaming context). This is **not an official standard**—it’s a practical, implementation‑ready starting point aligned with xAPI’s specification and profile guidance. [\[adlnet.gov\]](https://adlnet.gov/research/performance-tracking-analysis/experience-api/), [\[github.com\]](https://github.com/adlnet/xAPI-Spec/blob/master/xAPI-Communication.md)

> **Why xAPI for AI oversight?**  
> xAPI is a mature, IEEE‑stewarded standard for interoperable activity tracking using structured **Actor–Verb–Object** statements stored in **Learning Record Stores (LRS)**. Its extensibility makes it ideal for logging *both* human and AI actions across systems for analytics and audit.   
> **Why reference MCP?**  
> MCP standardizes how AI agents discover tools and exchange context (tools/resources/prompts) in persistent, low‑latency sessions—perfect for multi‑agent, real‑time operations whose events we want to capture via xAPI. [\[xapi.com\]](https://xapi.com/overview/), [\[adlnet.gov\]](https://adlnet.gov/research/performance-tracking-analysis/experience-api/) [\[modelconte...rotocol.io\]](https://modelcontextprotocol.io/docs/learn/architecture), [\[developer.ibm.com\]](https://developer.ibm.com/articles/mcp-architecture-patterns-ai-systems)

***

## 1) Profile Overview

*   **Profile name:** *xAPI AI Agent Actions Profile* (AIAAP)
*   **Profile IRI (proposed, registerable):** `https://w3id.org/xapi/ai/profile`
*   **Version:** `0.9.0 (Draft)`
*   **Scope:** Capturing **human instructions**, **AI planning/decision steps**, **MCP tool calls**, **resource access**, **content generation**, **inter‑agent delegation**, and **outcomes** (success, error, cost, latency, tokens).
*   **Intended storage/analytics:** Any **LRS** or observability pipeline capable of xAPI ingestion, query, and dashboarding. [\[xapi.com\]](https://xapi.com/overview/), [\[adlnet.gov\]](https://adlnet.gov/research/performance-tracking-analysis/experience-api/)
*   **Design basis:** xAPI statement structure (Actor, Verb, Object, Result, Context, Attachments), IRI requirements, signed statements, and Profiles/Communities guidance. [\[github.com\]](https://github.com/adlnet/xAPI-Spec/blob/master/xAPI-Communication.md)

***

## 2) Conformance & Governance (Profile Rules)

*   **MUST** use **IRIs** for verbs, activity types, and extensions defined in this profile. [\[github.com\]](https://github.com/adlnet/xAPI-Spec/blob/master/xAPI-Communication.md)
*   **MUST** include the profile IRI in `context.contextActivities.category`. [\[github.com\]](https://github.com/adlnet/xAPI-Spec/blob/master/xAPI-Communication.md)
*   **SHOULD** populate `result.success`, `result.duration`, and token/cost/latency **extensions** for action statements where applicable. [\[github.com\]](https://github.com/adlnet/xAPI-Spec/blob/master/xAPI-Communication.md)
*   **MAY** use **signed statements** for audit chains and compliance. [\[github.com\]](https://github.com/adlnet/xAPI-Spec/blob/master/xAPI-Communication.md)
*   **MUST** adhere to xAPI serialization rules (JSON), timestamps (ISO‑8601), UUIDs, and language maps. [\[github.com\]](https://github.com/adlnet/xAPI-Spec/blob/master/xAPI-Communication.md)

***

## 3) Namespaces & Base IRIs (Proposed)

*   **Profile:** `https://w3id.org/xapi/ai/profile`
*   **Verbs:** `https://w3id.org/xapi/ai/verbs/`
*   **Activity Types:** `https://w3id.org/xapi/ai/activity-type/`
*   **Extensions:** `https://w3id.org/xapi/ai/extensions/`

> The **w3id** convention is widely used by xAPI profiles (e.g., xAPI Video Profile); IRIs are required and should resolve or be documented. [\[xapi.com.au\]](https://xapi.com.au/what-is-xapi/), [\[github.com\]](https://github.com/adlnet/xAPI-Spec/blob/master/xAPI-Communication.md)

***

## 4) Core Vocabulary

### 4.1 Verbs (selected)

> All verbs are **English display** examples; provide additional language maps as needed. [\[github.com\]](https://github.com/adlnet/xAPI-Spec/blob/master/xAPI-Communication.md)

*   **Instructed** — `https://w3id.org/xapi/ai/verbs/instructed`  
    *Human or system issued an instruction to an AI agent to perform a task.*

*   **Planned** — `https://w3id.org/xapi/ai/verbs/planned`  
    *AI agent produced a plan or chain of steps prior to execution.*

*   **Delegated** — `https://w3id.org/xapi/ai/verbs/delegated`  
    *AI agent handed off a subtask to another agent.*

*   **Invoked tool** — `https://w3id.org/xapi/ai/verbs/invoked-tool`  
    *AI agent called a tool (e.g., via MCP tools interface) with parameters.* [\[modelconte...rotocol.io\]](https://modelcontextprotocol.io/docs/learn/architecture), [\[developer.ibm.com\]](https://developer.ibm.com/articles/mcp-architecture-patterns-ai-systems)

*   **Read resource** — `https://w3id.org/xapi/ai/verbs/read-resource`  
    *AI agent retrieved context from a resource (file, DB, API, knowledge base).* [\[modelconte...rotocol.io\]](https://modelcontextprotocol.io/docs/learn/architecture)

*   **Wrote resource** — `https://w3id.org/xapi/ai/verbs/wrote-resource`  
    *AI agent persisted or updated content in a resource.*

*   **Generated** — `https://w3id.org/xapi/ai/verbs/generated`  
    *AI agent produced an output (text, code, image, report).*

*   **Evaluated** — `https://w3id.org/xapi/ai/verbs/evaluated`  
    *AI agent assessed content or results against criteria/policy.*

*   **Approved** — `https://w3id.org/xapi/ai/verbs/approved`  
    *Human or supervising agent approved a plan or output.*

*   **Rejected** — `https://w3id.org/xapi/ai/verbs/rejected`  
    *Human or supervising agent rejected a plan or output.*

*   **Terminated** — `https://w3id.org/xapi/ai/verbs/terminated`  
    *Agent or human ended a run/session before completion.*

> Use **language maps** for displays and **definition** fields per xAPI guidance. [\[github.com\]](https://github.com/adlnet/xAPI-Spec/blob/master/xAPI-Communication.md)

***

### 4.2 Activity Types

*   **AI Agent** — `https://w3id.org/xapi/ai/activity-type/agent`
*   **Human Operator** — `https://w3id.org/xapi/ai/activity-type/human`
*   **Tool** — `https://w3id.org/xapi/ai/activity-type/tool` *(e.g., MCP tool server)* [\[modelconte...rotocol.io\]](https://modelcontextprotocol.io/docs/learn/architecture)
*   **Resource** — `https://w3id.org/xapi/ai/activity-type/resource` *(file, DB table, API endpoint)* [\[modelconte...rotocol.io\]](https://modelcontextprotocol.io/docs/learn/architecture)
*   **Prompt** — `https://w3id.org/xapi/ai/activity-type/prompt`
*   **Model** — `https://w3id.org/xapi/ai/activity-type/model`
*   **Model Session / Run** — `https://w3id.org/xapi/ai/activity-type/run`
*   **Task** — `https://w3id.org/xapi/ai/activity-type/task`
*   **Policy** — `https://w3id.org/xapi/ai/activity-type/policy`

> Activities should include `definition.type` IRIs and optional metadata via `definition.extensions`. [\[github.com\]](https://github.com/adlnet/xAPI-Spec/blob/master/xAPI-Communication.md)

***

### 4.3 Extensions (key fields)

Use **extensions** for operational telemetry and provenance. (Types may be strings, numbers, booleans, arrays, or objects per xAPI rules.) [\[github.com\]](https://github.com/adlnet/xAPI-Spec/blob/master/xAPI-Communication.md)

*   **MCP / Invocation Context**
    *   `https://w3id.org/xapi/ai/extensions/mcp-server-id`
    *   `https://w3id.org/xapi/ai/extensions/mcp-client-id`
    *   `https://w3id.org/xapi/ai/extensions/mcp-connection` *(stdio|http|sse)* [\[developer.ibm.com\]](https://developer.ibm.com/articles/mcp-architecture-patterns-ai-systems)
    *   `https://w3id.org/xapi/ai/extensions/tool-name`
    *   `https://w3id.org/xapi/ai/extensions/tool-parameters` *(redact as needed)*

*   **Model & Generation**
    *   `https://w3id.org/xapi/ai/extensions/model-id`
    *   `https://w3id.org/xapi/ai/extensions/model-params` *(temperature, top\_p, etc.)*
    *   `https://w3id.org/xapi/ai/extensions/input-tokens` / `output-tokens`
    *   `https://w3id.org/xapi/ai/extensions/latency-ms`
    *   `https://w3id.org/xapi/ai/extensions/cost` *(if available)*

*   **Resources & Data**
    *   `https://w3id.org/xapi/ai/extensions/resource-uri`
    *   `https://w3id.org/xapi/ai/extensions/resource-hash`
    *   `https://w3id.org/xapi/ai/extensions/resource-version`

*   **Governance / Risk**
    *   `https://w3id.org/xapi/ai/extensions/policy-ids`
    *   `https://w3id.org/xapi/ai/extensions/risk-score`
    *   `https://w3id.org/xapi/ai/extensions/anomaly` *(true/false; reason)*

*   **Traceability**
    *   `https://w3id.org/xapi/ai/extensions/session-id`
    *   `https://w3id.org/xapi/ai/extensions/run-id`
    *   `https://w3id.org/xapi/ai/extensions/parent-run-id`
    *   `https://w3id.org/xapi/ai/extensions/trace-id`

> MCP distinguishes tools, resources, and prompts; these map cleanly into xAPI objects and extensions for traceability. [\[modelconte...rotocol.io\]](https://modelcontextprotocol.io/docs/learn/architecture), [\[spikeapi.com\]](https://www.spikeapi.com/blog/mcp-ai-explained)

***

## 5) Statement Design Patterns

> xAPI statements are JSON with **Actor–Verb–Object**, plus **Result** and **Context** (including `contextActivities` for parent/task/session and **category** for profile tags). [\[articulate.com\]](https://www.articulate.com/blog/what-is-xapi/), [\[github.com\]](https://github.com/adlnet/xAPI-Spec/blob/master/xAPI-Communication.md)

### Pattern A — Human **instructed** AI Agent to perform a Task

*   **Actor:** Human Operator (Agent)
*   **Verb:** `instructed`
*   **Object:** Task (Activity)
*   **Context:** category includes profile IRI; parent references a Session/Run; `instructor` may be set to human; extensions may include priority, due‑by, constraints.

### Pattern B — AI Agent **invoked tool** (MCP) with parameters

*   **Actor:** AI Agent (Agent)
*   **Verb:** `invoked-tool`
*   **Object:** Tool (Activity)
*   **Result:** success, duration; extensions for latency, token usage
*   **Context:** resource/prompt references, session/run IDs, MCP server/client identifiers. [\[modelconte...rotocol.io\]](https://modelcontextprotocol.io/docs/learn/architecture), [\[developer.ibm.com\]](https://developer.ibm.com/articles/mcp-architecture-patterns-ai-systems)

### Pattern C — AI Agent **generated** output and **wrote resource**

*   Two statements (or one with attachments):
    1.  `generated` (Object: Prompt or Task)
    2.  `wrote-resource` (Object: Resource, with hash/version)
*   Include `attachments` for artifacts when feasible; consider **signed statements** for audit chains. [\[github.com\]](https://github.com/adlnet/xAPI-Spec/blob/master/xAPI-Communication.md)

***

## 6) Example Statements (JSON)

> **Notes:** Examples illustrate required fields and key extensions. Adapt IDs to your environment. xAPI serialization, UUIDs, timestamps, and language maps per spec. [\[github.com\]](https://github.com/adlnet/xAPI-Spec/blob/master/xAPI-Communication.md)

### 6.1 Human instructed AI Agent

```json
{
  "id": "7c1f4d7d-25b4-4a7c-9b6d-5d6c2e9b1abc",
  "actor": {
    "objectType": "Agent",
    "name": "Rugge CIV Sean M US",
    "account": { "homePage": "https://id.example.mil", "name": "u-12345" }
  },
  "verb": {
    "id": "https://w3id.org/xapi/ai/verbs/instructed",
    "display": { "en": "instructed" }
  },
  "object": {
    "id": "https://ops.example.mil/tasks/ops-9087",
    "definition": {
      "type": "https://w3id.org/xapi/ai/activity-type/task",
      "name": { "en": "Generate weekly readiness report" }
    },
    "objectType": "Activity"
  },
  "context": {
    "contextActivities": {
      "parent": [{ "id": "https://ops.example.mil/sessions/sess-5577", "objectType": "Activity" }],
      "category": [{ "id": "https://w3id.org/xapi/ai/profile" }]
    },
    "extensions": {
      "https://w3id.org/xapi/ai/extensions/policy-ids": ["POL-RED-TEAM-01"],
      "https://w3id.org/xapi/ai/extensions/session-id": "sess-5577",
      "https://w3id.org/xapi/ai/extensions/priority": "high"
    }
  },
  "timestamp": "2026-01-29T18:05:12Z",
  "version": "1.0.3"
}
```

### 6.2 AI Agent invoked MCP tool

```json
{
  "id": "d2d287c1-8f34-4e9f-92b0-2f9d1a552233",
  "actor": {
    "objectType": "Agent",
    "name": "OpsAgent-Alpha",
    "account": { "homePage": "https://agents.example.mil", "name": "agent-alpha" }
  },
  "verb": {
    "id": "https://w3id.org/xapi/ai/verbs/invoked-tool",
    "display": { "en": "invoked tool" }
  },
  "object": {
    "id": "https://tools.example.mil/mcp/finance-summary",
    "definition": {
      "type": "https://w3id.org/xapi/ai/activity-type/tool",
      "name": { "en": "finance-summary" },
      "description": { "en": "Aggregates spend and readiness KPIs" }
    },
    "objectType": "Activity"
  },
  "result": {
    "success": true,
    "duration": "PT3.42S",
    "extensions": {
      "https://w3id.org/xapi/ai/extensions/latency-ms": 3421,
      "https://w3id.org/xapi/ai/extensions/input-tokens": 1280,
      "https://w3id.org/xapi/ai/extensions/output-tokens": 512,
      "https://w3id.org/xapi/ai/extensions/cost": 0.0132
    }
  },
  "context": {
    "contextActivities": {
      "parent": [{ "id": "https://ops.example.mil/runs/run-9012", "objectType": "Activity" }],
      "grouping": [{ "id": "https://ops.example.mil/sessions/sess-5577", "objectType": "Activity" }],
      "category": [{ "id": "https://w3id.org/xapi/ai/profile" }]
    },
    "extensions": {
      "https://w3id.org/xapi/ai/extensions/mcp-server-id": "mcp-finance@v1",
      "https://w3id.org/xapi/ai/extensions/mcp-client-id": "ops-orchestrator",
      "https://w3id.org/xapi/ai/extensions/mcp-connection": "sse",
      "https://w3id.org/xapi/ai/extensions/tool-parameters": {
        "fiscal_year": 2026,
        "units": "USD"
      },
      "https://w3id.org/xapi/ai/extensions/model-id": "gpt-x-ops-2026"
    }
  },
  "timestamp": "2026-01-29T18:05:16Z",
  "version": "1.0.3"
}
```

### 6.3 AI Agent generated and wrote resource

```json
{
  "id": "6be5f670-2e62-42f2-b8f0-3a6c9e4f0f50",
  "actor": {
    "objectType": "Agent",
    "name": "OpsAgent-Alpha",
    "account": { "homePage": "https://agents.example.mil", "name": "agent-alpha" }
  },
  "verb": {
    "id": "https://w3id.org/xapi/ai/verbs/generated",
    "display": { "en": "generated" }
  },
  "object": {
    "id": "https://ops.example.mil/prompts/report-template-v3",
    "definition": {
      "type": "https://w3id.org/xapi/ai/activity-type/prompt",
      "name": { "en": "Readiness report template" }
    },
    "objectType": "Activity"
  },
  "result": {
    "success": true,
    "extensions": {
      "https://w3id.org/xapi/ai/extensions/output-tokens": 1870,
      "https://w3id.org/xapi/ai/extensions/latency-ms": 4890
    }
  },
  "context": {
    "contextActivities": {
      "parent": [{ "id": "https://ops.example.mil/tasks/ops-9087", "objectType": "Activity" }],
      "category": [{ "id": "https://w3id.org/xapi/ai/profile" }]
    }
  },
  "attachments": [
    {
      "usageType": "http://id.tincanapi.com/attachment/supporting_media",
      "display": { "en": "Generated Report (PDF)" },
      "description": { "en": "Rendered readiness report" },
      "contentType": "application/pdf",
      "length": 245672,
      "sha2": "5f70bf18a08660b2c2eb...c57c6d" 
    }
  ],
  "timestamp": "2026-01-29T18:05:21Z",
  "version": "1.0.3"
}
```

> The use of **attachments**, **result**, **contextActivities**, **extensions**, and **language maps** conforms to xAPI patterns widely documented in the spec and examples (e.g., Video Profile). [\[github.com\]](https://github.com/adlnet/xAPI-Spec/blob/master/xAPI-Communication.md), [\[xapi.com.au\]](https://xapi.com.au/what-is-xapi/)

***

## 7) Reporting & Visualization Hints

*   Query by **profile category** to isolate AI‑related statements. Use **parent** (Task/Run) and **grouping** (Session) for timelines and spans. [\[github.com\]](https://github.com/adlnet/xAPI-Spec/blob/master/xAPI-Communication.md)
*   Surface **tool latency**, **token usage**, **cost**, and **policy risk** from **extensions** for operational dashboards (e.g., Power BI/Grafana).
*   Use **signed statements** to preserve non‑repudiation in regulated contexts. [\[github.com\]](https://github.com/adlnet/xAPI-Spec/blob/master/xAPI-Communication.md)
*   Map MCP “**tools/resources/prompts**” directly to **Object** activities/types; stream updates can emit multiple statements for progress and completion. [\[modelconte...rotocol.io\]](https://modelcontextprotocol.io/docs/learn/architecture), [\[developer.ibm.com\]](https://developer.ibm.com/articles/mcp-architecture-patterns-ai-systems)

***

## 8) Privacy & Security Guidance

*   Prefer **pseudonymous** identifiers for humans and agents; store sensitive PII outside statements where feasible. (xAPI Agents permit account identifiers.) [\[github.com\]](https://github.com/adlnet/xAPI-Spec/blob/master/xAPI-Communication.md)
*   Redact or hash sensitive **tool parameters** and resource URIs; include **resource hashes/versions** for integrity. [\[github.com\]](https://github.com/adlnet/xAPI-Spec/blob/master/xAPI-Communication.md)
*   Consider **signed statements** and controlled access to the LRS for audit integrity and role‑based visibility. [\[github.com\]](https://github.com/adlnet/xAPI-Spec/blob/master/xAPI-Communication.md)

***

## 9) Minimal JSON Profile Snippet (Publishable Vocabulary)

> A lightweight way to publish your controlled vocabulary (verbs, activity types, extensions). (Full xAPI Profile JSON can be expanded later.)

```json
{
  "id": "https://w3id.org/xapi/ai/profile",
  "type": "Profile",
  "prefLabel": { "en": "xAPI AI Agent Actions Profile (AIAAP)" },
  "definition": {
    "en": "Captures human instructions and AI agent operations, including MCP tool calls, resource access, generation, and governance outcomes."
  },
  "versions": [{ "id": "https://w3id.org/xapi/ai/profile/0.9.0" }],
  "concepts": [
    { "id": "https://w3id.org/xapi/ai/verbs/instructed", "type": "Verb", "prefLabel": { "en": "instructed" } },
    { "id": "https://w3id.org/xapi/ai/verbs/invoked-tool", "type": "Verb", "prefLabel": { "en": "invoked tool" } },
    { "id": "https://w3id.org/xapi/ai/activity-type/tool", "type": "ActivityType", "prefLabel": { "en": "Tool" } },
    { "id": "https://w3id.org/xapi/ai/activity-type/resource", "type": "ActivityType", "prefLabel": { "en": "Resource" } },
    { "id": "https://w3id.org/xapi/ai/extensions/model-id", "type": "Extension", "prefLabel": { "en": "Model ID" } },
    { "id": "https://w3id.org/xapi/ai/extensions/latency-ms", "type": "Extension", "prefLabel": { "en": "Latency (ms)" } }
  ]
}
```

> xAPI Profiles formalize shared vocabularies so communities can interoperate—define concepts as IRIs and publish them. [\[github.com\]](https://github.com/adlnet/xAPI-Spec/blob/master/xAPI-Communication.md)

***

## 10) Implementation Notes (MCP + xAPI)

*   **MCP Host/Client/Server** events (tool discovery, invocation, streaming progress) can be converted into xAPI statements at the orchestrator layer; treat MCP server endpoints as **Tool activities** and context sources as **Resource activities**. [\[modelconte...rotocol.io\]](https://modelcontextprotocol.io/docs/learn/architecture), [\[developer.ibm.com\]](https://developer.ibm.com/articles/mcp-architecture-patterns-ai-systems)
*   Persist statements in an **LRS** (or compatible event store) to enable cross‑system analytics and replay; xAPI is designed for interoperable storage and exchange. [\[xapi.com\]](https://xapi.com/overview/), [\[adlnet.gov\]](https://adlnet.gov/research/performance-tracking-analysis/experience-api/)
*   Leverage **IEEE xAPI** stewardship and open standard status for governance/assurance in enterprise/DoD environments. [\[xapi.com\]](https://xapi.com/overview/), [\[xapi.ieee-saopen.org\]](https://xapi.ieee-saopen.org/)

***

## Authoritative References

*   **xAPI (Experience API) — ADL/DoD overview**: purpose, analytics, interoperability, LRS concepts. [\[adlnet.gov\]](https://adlnet.gov/research/performance-tracking-analysis/experience-api/)
*   **xAPI Spec (GitHub)**: statements, profiles, MUST/SHOULD language, serialization, IRIs, signed statements, examples. [\[github.com\]](https://github.com/adlnet/xAPI-Spec/blob/master/xAPI-Communication.md)
*   **xAPI overview (Rustici/IEEE)**: standard status, LRS behavior, statement freedom, device/workflow freedom. [\[xapi.com\]](https://xapi.com/overview/)
*   **xAPI Video Profile** (example of profile practice and IRIs via w3id): statement patterning and extensions. [\[xapi.com.au\]](https://xapi.com.au/what-is-xapi/)
*   **MCP Architecture & Concepts** (tools/resources/prompts, client–server model). [\[modelconte...rotocol.io\]](https://modelcontextprotocol.io/docs/learn/architecture)
*   **MCP in multi‑agent systems** (persistent context, SSE streaming, architectural patterns). [\[developer.ibm.com\]](https://developer.ibm.com/articles/mcp-architecture-patterns-ai-systems)

***

## Want me to package this as a downloadable **JSON Profile document** and a set of **example xAPI statements** you can import into an LRS (plus a starter **Power BI** dashboard)? I can generate those artifacts next.
