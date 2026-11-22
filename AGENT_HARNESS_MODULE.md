# AIAAP 0.12.0: agent harness module

An **agent harness** is the program an AI agent runs in: it holds the model connection, the tools and the session loop (for example Hermes Agent or OpenClaw). A harness sees every tool call as it happens, so a plugin in it can record what the agent **actually did**. That is not the same as what the model says it did. A small model can describe a tool result it never fetched; the harness record shows that no call happened.

0.12.0 adds two statement shapes for what a harness records:

1. **Tool calls.** Each call is one statement, using the 0.9.0 verb `invoked-tool`, with the tool as the object.
2. **Usage reports.** Each agent sends one statement per day of bounded counters, using the new verb `reported-usage`. They are safe to share because they carry counts, never content.

The machine-readable profile is `ai_agent_actions_profile.json` (built by `tools/build_profile.py`). Examples are in `examples/agent_harness_example_statements.ndjson`.

## What is reused and what is new

| Concept | Version | Use |
|---|---|---|
| verb `invoked-tool` | 0.9.0 | a tool call |
| activity type `tool` | 0.9.0 | the object of a tool call |
| `tool-name`, `tool-parameters`, `session-id`, `model-id` (context) | 0.9.0 | details of the call |
| `latency-ms`, `input-tokens`, `output-tokens` (result) | 0.9.0 | timing and tokens |
| `outcome` (result) and all `holocron/*` provenance extensions | 0.10.x | as for every record |
| verb `reported-usage` | **0.12.0** | a usage report |
| activity type `usage-report` | **0.12.0** | the object of a usage report |
| `harness` (context) | **0.12.0** | which harness and plugin recorded it |
| `tool-parameters-truncated` (context), `tool-result-truncated` (result) | **0.12.0** | the parameters or result were cut to a size limit |
| `usage` (result), `usage-period` (context) | **0.12.0** | the counters and the day they cover |

## Tool calls (template `harness-tool-call`)

Every rule from mapping version 1 still applies (`ROBOTICS_MODULE.md`), with these differences:

| Statement field | Value |
|---|---|
| `verb` | `https://w3id.org/xapi-ai/verbs/invoked-tool` |
| `object` | the tool: `<base>/tools/<tool name>`, `definition.type` = `…/activity-type/tool`, `definition.name.en` = the tool name |
| `context.contextActivities.other` | the source record `<base>/records/<agent>/<seq>` (type `…/activity-type/record`, name = the record summary) |
| `context.contextAgents` | the robot or agent the tool acted on, with relevant type `…/activity-type/peer-role` |
| `result.success` | from the record's `outcome` (`true` only for `success`); `EXT+outcome` as before |
| `result.duration` | the call's duration as ISO 8601, e.g. `PT1.25S` |
| `result.response` | the tool's raw result as text, when the harness recorded it; `EXT+tool-result-truncated` when cut |
| `result.extensions` | `EXT+latency-ms` |
| `context.extensions` | `EXT+tool-name`; `EXT+tool-parameters` (redacted by the harness) when recorded, with `EXT+tool-parameters-truncated` when cut; `EXT+session-id`; `EXT+model-id`; `EXT+harness`; every `holocron/*` provenance extension, with `holocron/mapping-version` = `"2"` |

**Why the object is the tool here.** Mapping version 1 makes the record the object of every statement. For tool calls, the tool is what an LRS consumer asks about: which tools an agent used, how often, how long they took, whether they worked. So the tool is the object, and the record moves to `contextActivities.other`. The record keeps every provenance extension, so the statement still verifies against the signed source.

A harness may record less: no parameters and no result, for example when tool content must stay on the device. The statement then omits `tool-parameters` and `result.response` and is still valid.

## Usage reports (template `agent-usage-report`)

One statement per agent per period, normally a UTC day. A usage report is built to be **shareable**. It carries bounded counters and coarse machine facts, and it must never contain:
- prompts or messages;
- tool parameters or results;
- file paths;
- setting values;
- error text.

The template excludes `result.response` and `tool-parameters` for this reason.

| Statement field | Value |
|---|---|
| `verb` | `https://w3id.org/xapi-ai/verbs/reported-usage` |
| `object` | `<base>/usage/<agent>/<period>`, type `…/activity-type/usage-report` |
| `result.extensions` | `EXT+usage`: the counters (schema below) |
| `context.extensions` | `EXT+usage-period` (`YYYY-MM-DD`), `EXT+harness`, and the `holocron/*` provenance extensions when the report came from a memory record |

The `usage` counters (`usage_schema: 1`):

| Field | Meaning |
|---|---|
| `sessions` | `started`, `completed`, `interrupted` |
| `tool_calls` | tool name → `{ok, error}`, for a bounded set of names; the rest are counted under `other` |
| `tool_errors` | reason → count, from a **fixed list**: `timeout`, `not_found`, `invalid_args`, `refused`, `unavailable`, `upstream_error`, `other` |
| `model_routes` | `"provider/model"` → `{calls, input_tokens, output_tokens, api_seconds}` |
| `api_errors` | `4xx`, `5xx`, `network`, `other` → count |
| `compactions` | how many times the harness compacted a session's context |
| `machine` | `arch`, `os`, `ram_gb` (whole GB), `harness_version`, `plugin_version` |

Error reasons come from a fixed list on purpose. That keeps reports comparable across agents and harnesses, and it means no error text, which can carry content, ever leaves the device.

## Mapping from memory records (mapping version 2)

A memory server that records harness activity (for example LTMS with its Hermes recorder) uses mapping version 2 for these two kinds of record only. Every other record maps exactly as in version 1.

| Record | Statement |
|---|---|
| `action` tagged `tool-call`, with a payload that names `tool_name` | `harness-tool-call` |
| `perception` tagged `agent-rollup` | `agent-usage-report`. This takes precedence over `sensed`, although such records also carry the `telemetry` tag |

Statement ids for these records use the mapping version 2 namespace, as the version 1 rule requires for a new mapping version:

`NS = uuid5(NAMESPACE_URL, "https://w3id.org/xapi-ai/profile/0.12.0/holocron-mapping/2")` = `31b68372-c7b5-5262-a399-635efc86bdbe`

The id is still `uuid5(NS, record.hash)`.
