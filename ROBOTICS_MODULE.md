# AIAAP 0.10.0: robotics and physical-AI module

AIAAP 0.9.0 covers software agents acting for people (instructions, tool calls, generation, approvals). Version 0.10.0 adds what a **body in the world** and a **swarm** need: one verb per memory-record type, telemetry windows, and provenance extensions so any statement can be checked against the signed record it came from.

It was designed for [LTMS / Holocron](https://github.com/seanrugg/ai_si_ltm), a signed, hash-chained memory server for robots and AI agents, but nothing in it is specific to one deployment. The machine-readable profile is `ai_agent_actions_profile.json` (built by `tools/build_profile.py`); examples are in `examples/robotics_example_statements.ndjson`.

## Principles

- **The memory server stays the log of record.** Statements are a derived, shareable view. Each carries the record's hash, previous hash and signature, so a reader can verify it against the source. Verification always goes back to the source.
- **One record, one statement**, and the record is the statement's object (a uniform rule, easy to query).
- **Full payloads (0.10.1).** Anything the memory server receives is exported. Sensor data goes in the `telemetry` result extension; every other payload goes in `holocron/payload`. The exact signed header travels as `holocron/header`, so a statement verifies offline.
- **Vocabulary authority:** where the [I2IDL Glossary of Digital Learning](https://id.i2idl.org/) has a matching concept, the profile links it with SKOS match properties. Gaps are listed in `GAPS.md`.

## Verbs (record type → verb)

| Record type | Verb | IRI |
|---|---|---|
| `perception` tagged `telemetry` | **sensed** (0.10.1) | `https://w3id.org/xapi-ai/verbs/sensed` |
| `perception` (any other) | perceived | `https://w3id.org/xapi-ai/verbs/perceived` |
| `thought` | reasoned | `https://w3id.org/xapi-ai/verbs/reasoned` |
| `decision` | decided | `https://w3id.org/xapi-ai/verbs/decided` |
| `action` | performed | `https://w3id.org/xapi-ai/verbs/performed` |
| `communication` | communicated | `https://w3id.org/xapi-ai/verbs/communicated` |
| `event` | experienced (ADL) | `http://adlnet.gov/expapi/verbs/experienced` |
| `lesson` | learned | `https://w3id.org/xapi-ai/verbs/learned` |
| `policy` | set policy | `https://w3id.org/xapi-ai/verbs/set-policy` |
| `system` | reported | `https://w3id.org/xapi-ai/verbs/reported` |

## Mapping rules (mapping version 1)

`<base>` is the memory server's public base URL (configuration, e.g. `https://ltms.example.org`). `EXT` = `https://w3id.org/xapi-ai/extensions/`.

| Statement field | Value |
|---|---|
| `id` | `uuid5(NS, record.hash)` with `NS = uuid5(NAMESPACE_URL, "https://w3id.org/xapi-ai/profile/0.10.0/holocron-mapping/1")` = `19413c7a-d33c-5129-b99b-07d709cef285`. A new mapping version gets a new namespace. |
| `actor` | Agent `{"account": {"homePage": <base>, "name": record.agent}}` |
| `verb` | from the table above, `display.en` = the verb label |
| `object` | Activity `<base>/records/<agent>/<seq>`, `definition.type` = `…/activity-type/record`, `definition.name.en` = `summary` (omitted when there is none) |
| `timestamp` | record `ts`, unchanged |
| `version` | the endpoint's xAPI version (`2.0.0` or `1.0.3`) |
| `result` | **action:** `success` = `outcome == "success"`, and `EXT+outcome` = the outcome string, when `outcome` is set. **telemetry:** `EXT+telemetry` (below). Otherwise omitted. |
| `context.contextActivities.category` | the profile version `https://w3id.org/xapi-ai/profile/0.10.0` (definition type `http://adlnet.gov/expapi/activities/profile`) |
| `context.contextActivities.grouping` | the author's swarm at write time `<base>/swarms/<name>` (type `…/activity-type/swarm`), and `place` as `<base>/places/<place>` (type `…/activity-type/place`); each only when present |
| `context.contextAgents` (2.0.0) | each `peer` with relevant type `…/activity-type/peer-role`; the relaying hub with `…/activity-type/relay-role`. For 1.0.3 endpoints, peers go in `EXT+holocron/refs` only and `contextAgents` is omitted. |
| `context.extensions` | `EXT+holocron/seq`, `/hash`, `/prev-hash`, `/payload-hash`, `/signature`, `/record-type`, `/received-at`, `/mapping-version` (`"1"`), `EXT+agent-kind`; plus `/tags`, `/refs`, `EXT+software` when present |

## Sensed and perceived (0.10.1)

**Sensed** is data from a sensor: what the body measured. **Perceived** is an interpretation of that data: what the agent concluded is true. "12 readings from the front time-of-flight sensor, 118 to 131 mm" is sensed. "Obstacle ahead" is perceived. Both are `perception` records in the memory server; the `telemetry` tag selects "sensed".

### Any sensor

A sensed record's payload goes, whole, in `result.extensions[EXT+telemetry]`. `kind` is free: `pose`, `navigation`, `sensor`, or anything a device defines. For readings, use the `sensor` kind:

```json
{"kind": "sensor", "sensor": "front-tof", "modality": "range", "unit": "mm", "rate_hz": 10,
 "samples": [{"t": 0.0, "v": 131}, {"t": 0.1, "v": 118}],
 "stats": {"min": 118, "max": 131, "mean": 124.5, "count": 2}}
```

- `sensor`: the sensor's name on this device. `modality`: what it measures (range, imu, temperature, battery, sound-level, light, gps, encoder, force, image-features…). `unit`: a UCUM code where one exists (`mm`, `Cel`, `%`, `m/s2`).
- `samples[].t` is seconds from the record's `ts`. `samples[].v` may be a number, a list (an IMU's `[ax, ay, az]`) or an object, so any sensor's data element fits.
- Raw media (images, audio) isn't telemetry. Send what the device extracted from it (`image-features`, `sound-level`), not the media.
- Pose and navigation keep their 0.10.0 shapes. No window is truncated.

### How sensing feeds learning

Each step of experience is its own statement, and `refs` link them, so a learning analyst can follow one chain from a sensor reading to a lesson:

| Step | Verb | Typical `refs` |
|---|---|---|
| Sensor data | sensed | |
| Interpretation | perceived | `derived_from`: the sensed records |
| Reasoning | reasoned | `because`: the perception |
| Commitment | decided | `because`: the perception or thought |
| Act and outcome | performed | `because`: the decision |
| Conclusion | learned | `because`: the outcome(s) |

The same chain answers questions at three levels: what an individual robot learned from which senses, what a swarm learned when one member's sensing informed another's decision (references across agents), and how the controlling intelligence's reasoning used its body's data. `holocron/refs` carries all references; exporters may also put `because` in `context.statement` as a StatementRef.

## Statement templates

`holocron-<type>` for each of the nine record types (`holocron-perception` excludes telemetry), `sensed` for data from any sensor, and `telemetry-pose`, `telemetry-navigation` and `telemetry-sensor`, which refine `sensed`. Every record template requires the record provenance extensions and the profile version (0.10.0 or 0.10.1) in `category`. `dataset-read` (0.11.0) is described below.

## Fleet datasets: reading reference material (0.11.0)

A fleet's memory server can hold **datasets**: versioned reference material
(documents, tables, sensor logs) that any member may read, often during a
**dream cycle** while it rests or charges. Members read; they are not trained
on the data. Every read becomes one statement, using the existing 0.9.0 verb
**read resource**:

| Part | Value |
|---|---|
| verb | `https://w3id.org/xapi-ai/verbs/read-resource` |
| object | the item, activity type `dataset-item`, id `<server>/datasets/<id>/v/<version>/items/<key>` |
| `contextActivities.parent` | the dataset version, activity type `dataset` |
| `contextActivities.grouping` | the fleet, activity type `fleet` |
| `registration` | the dream cycle's UUID, when the read happened in one |
| extensions | `resource-version` (0.9.0), `resource-hash` (0.9.0, the item's SHA-256), `read-source` (`served` or `reported`) |

The `dataset-read` template checks these. A lesson that came from reading cites
the items in its payload (`sources`), so the chain from *read* to *learned* to
*performed* can be followed across statements. An example is the last line of
`examples/robotics_example_statements.ndjson`.
