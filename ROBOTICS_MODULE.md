# AIAAP 0.10.0: robotics and physical-AI module

AIAAP 0.9.0 covers software agents acting for people (instructions, tool calls, generation, approvals). Version 0.10.0 adds what a **body in the world** and a **swarm** need: one verb per memory-record type, telemetry windows, and provenance extensions so any statement can be checked against the signed record it came from.

It was designed for [LTMS / Holocron](https://github.com/seanrugg/ai_si_ltm), a signed, hash-chained memory server for robots and AI agents, but nothing in it is specific to one deployment. The machine-readable profile is `ai_agent_actions_profile.json` (built by `tools/build_profile.py`); examples are in `examples/robotics_example_statements.ndjson`.

## Principles

- **The memory server stays the log of record.** Statements are a derived, shareable view. Each carries the record's hash, previous hash and signature, so a reader can verify it against the source. Verification always goes back to the source.
- **One record, one statement**, and the record is the statement's object (a uniform rule, easy to query).
- **No payloads by default.** Only telemetry windows (below) export payload data, and large windows are summarized.
- **Vocabulary authority:** where the [I2IDL Glossary of Digital Learning](https://id.i2idl.org/) has a matching concept, the profile links it with SKOS match properties. Gaps are listed in `GAPS.md`.

## Verbs (record type → verb)

| Record type | Verb | IRI |
|---|---|---|
| `perception` | perceived | `https://w3id.org/xapi/ai/verbs/perceived` |
| `thought` | reasoned | `https://w3id.org/xapi/ai/verbs/reasoned` |
| `decision` | decided | `https://w3id.org/xapi/ai/verbs/decided` |
| `action` | performed | `https://w3id.org/xapi/ai/verbs/performed` |
| `communication` | communicated | `https://w3id.org/xapi/ai/verbs/communicated` |
| `event` | experienced (ADL) | `http://adlnet.gov/expapi/verbs/experienced` |
| `lesson` | learned | `https://w3id.org/xapi/ai/verbs/learned` |
| `policy` | set policy | `https://w3id.org/xapi/ai/verbs/set-policy` |
| `system` | reported | `https://w3id.org/xapi/ai/verbs/reported` |

## Mapping rules (mapping version 1)

`<base>` is the memory server's public base URL (configuration, e.g. `https://ltms.example.org`). `EXT` = `https://w3id.org/xapi/ai/extensions/`.

| Statement field | Value |
|---|---|
| `id` | `uuid5(NS, record.hash)` with `NS = uuid5(NAMESPACE_URL, "https://w3id.org/xapi/ai/profile/0.10.0/holocron-mapping/1")` = `31bddff3-c274-5e19-ba21-56836b977ee6`. A new mapping version gets a new namespace. |
| `actor` | Agent `{"account": {"homePage": <base>, "name": record.agent}}` |
| `verb` | from the table above, `display.en` = the verb label |
| `object` | Activity `<base>/records/<agent>/<seq>`, `definition.type` = `…/activity-type/record`, `definition.name.en` = `summary` (omitted when there is none) |
| `timestamp` | record `ts`, unchanged |
| `version` | the endpoint's xAPI version (`2.0.0` or `1.0.3`) |
| `result` | **action:** `success` = `outcome == "success"`, and `EXT+outcome` = the outcome string, when `outcome` is set. **telemetry:** `EXT+telemetry` (below). Otherwise omitted. |
| `context.contextActivities.category` | the profile version `https://w3id.org/xapi/ai/profile/0.10.0` (definition type `http://adlnet.gov/expapi/activities/profile`) |
| `context.contextActivities.grouping` | the author's swarm at write time `<base>/swarms/<name>` (type `…/activity-type/swarm`), and `place` as `<base>/places/<place>` (type `…/activity-type/place`); each only when present |
| `context.contextAgents` (2.0.0) | each `peer` with relevant type `…/activity-type/peer-role`; the relaying hub with `…/activity-type/relay-role`. For 1.0.3 endpoints, peers go in `EXT+holocron/refs` only and `contextAgents` is omitted. |
| `context.extensions` | `EXT+holocron/seq`, `/hash`, `/prev-hash`, `/payload-hash`, `/signature`, `/record-type`, `/received-at`, `/mapping-version` (`"1"`), `EXT+agent-kind`; plus `/tags`, `/refs`, `EXT+software` when present |

## Telemetry windows

A `perception` record tagged `telemetry` whose payload has a `kind` of `pose`, `navigation` or `sensor` exports that payload as `result.extensions[EXT+telemetry]`. Payload conventions:

```json
{"kind": "pose", "frame": "map", "samples": [{"t": 0.0, "x": 1.2, "y": 0.4, "yaw": 1.57}]}
{"kind": "navigation", "goal": "dock", "status": "active", "distance_remaining_m": 1.8, "progress": 0.4}
{"kind": "sensor", "sensor": "battery", "unit": "percent", "samples": [{"t": 0, "v": 71}]}
```

`t` is seconds from the record's `ts`. If the payload's canonical JSON is over **16 KiB**, only `{"kind", "frame"/"sensor"/"unit" when present, "samples_count", "truncated": true}` is exported. Telemetry with any other `kind`, or none, exports no payload. An LRS endpoint can still leave telemetry out entirely through its scope.

## Statement templates

`holocron-<type>` for each of the nine record types, plus `telemetry-pose`, `telemetry-navigation` and `telemetry-sensor`. Every template requires the record provenance extensions and the profile version in `category`.
