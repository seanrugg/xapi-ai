"""Build ai_agent_actions_profile.json (AIAAP) as an xAPI Profile 1.0 document.

Run:  python3 tools/build_profile.py   (writes ../ai_agent_actions_profile.json)

0.9.0 vocabulary is kept unchanged (same IRIs). 0.10.0 adds the robotics /
physical-AI module used by Holocron (LTMS) exports, aligned with the I2IDL
Glossary of Digital Learning via SKOS match properties.
"""
import json
from pathlib import Path

BASE = "https://w3id.org/xapi/ai"
PROFILE = f"{BASE}/profile"
V09 = f"{PROFILE}/0.9.0"
V010 = f"{PROFILE}/0.10.0"
G = "https://id.i2idl.org/concepts/"   # I2IDL Glossary, publication v0.0.93
ADL = "http://adlnet.gov/expapi/verbs/"


def concept(kind, slug_path, label, definition, scheme, **extra):
    c = {"id": f"{BASE}/{slug_path}", "type": kind, "inScheme": scheme,
         "prefLabel": {"en": label}, "definition": {"en": definition}}
    c.update(extra)
    return c


# ---------------------------------------------------------------- 0.9.0
V09_VERBS = [
    ("instructed", "instructed", "Human or system issued an instruction to an AI agent to perform a task."),
    ("planned", "planned", "AI agent produced a plan or chain of steps prior to execution."),
    ("delegated", "delegated", "AI agent handed off a subtask to another agent."),
    ("invoked-tool", "invoked tool", "AI agent called a tool (e.g., via the MCP tools interface) with parameters."),
    ("read-resource", "read resource", "AI agent retrieved context from a resource (file, database, API, knowledge base)."),
    ("wrote-resource", "wrote resource", "AI agent persisted or updated content in a resource."),
    ("generated", "generated", "AI agent produced an output (text, code, image, report)."),
    ("evaluated", "evaluated", "AI agent assessed content or results against criteria or policy."),
    ("approved", "approved", "Human or supervising agent approved a plan or output."),
    ("rejected", "rejected", "Human or supervising agent rejected a plan or output."),
    ("terminated", "terminated", "Agent or human ended a run or session before completion."),
]
V09_TYPES = [
    ("agent", "AI Agent", "A software agent that acts on behalf of a human or another agent."),
    ("human", "Human Operator", "A person who instructs, supervises or approves agent work."),
    ("tool", "Tool", "A callable capability, such as an MCP tool server."),
    ("resource", "Resource", "A file, database table, API endpoint or other data source."),
    ("prompt", "Prompt", "An instruction or prompt given to a model."),
    ("model", "Model", "An AI model."),
    ("run", "Model Session / Run", "One model session or agent run."),
    ("task", "Task", "A unit of work an agent was asked to do."),
    ("policy", "Policy", "A rule or policy that constrains agent behavior."),
]
V09_EXT = [  # (slug, label, definition, kind)
    ("mcp-server-id", "MCP Server ID", "Identifier of the MCP server involved.", "ContextExtension"),
    ("mcp-client-id", "MCP Client ID", "Identifier of the MCP client involved.", "ContextExtension"),
    ("mcp-connection", "MCP Connection", "MCP transport: stdio, http or sse.", "ContextExtension"),
    ("tool-name", "Tool Name", "Name of the tool invoked.", "ContextExtension"),
    ("tool-parameters", "Tool Parameters", "Parameters passed to the tool (redact as needed).", "ContextExtension"),
    ("model-id", "Model ID", "Identifier of the model used.", "ContextExtension"),
    ("model-params", "Model Parameters", "Generation parameters (temperature, top_p, ...).", "ContextExtension"),
    ("input-tokens", "Input Tokens", "Number of input tokens.", "ResultExtension"),
    ("output-tokens", "Output Tokens", "Number of output tokens.", "ResultExtension"),
    ("latency-ms", "Latency (ms)", "Elapsed time in milliseconds.", "ResultExtension"),
    ("cost", "Cost", "Cost of the operation, if known.", "ResultExtension"),
    ("resource-uri", "Resource URI", "URI of the resource read or written.", "ContextExtension"),
    ("resource-hash", "Resource Hash", "Hash of the resource content.", "ContextExtension"),
    ("resource-version", "Resource Version", "Version of the resource.", "ContextExtension"),
    ("policy-ids", "Policy IDs", "Policies applied to the operation.", "ContextExtension"),
    ("risk-score", "Risk Score", "Risk score assigned to the operation.", "ResultExtension"),
    ("anomaly", "Anomaly", "Whether the operation was flagged as anomalous, with a reason.", "ResultExtension"),
    ("session-id", "Session ID", "Session identifier for traceability.", "ContextExtension"),
    ("run-id", "Run ID", "Run identifier for traceability.", "ContextExtension"),
    ("parent-run-id", "Parent Run ID", "Identifier of the parent run.", "ContextExtension"),
    ("trace-id", "Trace ID", "Distributed trace identifier.", "ContextExtension"),
]

# ---------------------------------------------------------------- 0.10.0: robotics / physical-AI module
# Verbs: one per Holocron record type. Glossary alignment uses the SKOS match
# properties xAPI Profiles allow (broadMatch, narrowMatch, relatedMatch, exactMatch); record types with no glossary concept are listed in GAPS.md.
V010_VERBS = [
    ("perceived", "perceived",
     "A robot or AI agent sensed something outside or inside its own body (camera, range sensor, battery, temperature).",
     {"broadMatch": [G + "artificial-intelligence-ai"]}),
    ("reasoned", "reasoned",
     "An agent reasoned without committing to act: a plan, prediction, question or interpretation.",
     {"relatedMatch": [G + "sensemaking", G + "metacognition"]}),
    ("decided", "decided", "An agent committed to act, or not to act.", {}),
    ("performed", "performed", "An agent did something in the world or in software; the result carries the outcome.", {}),
    ("communicated", "communicated", "An agent sent or received a message to or from another agent or a person.",
     {"relatedMatch": [G + "social-learning"]}),
    ("learned", "learned",
     "An agent drew a conclusion from experience that is meant to change its future behavior.",
     {"relatedMatch": [G + "experiential-learning", G + "knowledge-retention", G + "feedback-loop"]}),
    ("set-policy", "set policy", "An operator issued a rule that constrains agent or swarm behavior.", {}),
    ("reported", "reported", "The memory server recorded a system fact (startup, key change, integrity result).", {}),
]
V010_TYPES = [
    ("record", "Holocron Record",
     "One signed, hash-chained memory record from a robot or AI agent, identified by agent and sequence number.",
     {"relatedMatch": [G + "long-term-memory"]}),
    ("swarm", "Swarm",
     "A governed group of robots and agents with an appointed hub, used as a grouping context.", {}),
    ("place", "Place", "A named physical or logical location where a record was made.", {}),
    ("peer-role", "Peer (relevant type)",
     "contextAgents relevantType: an agent the record involved (sender, receiver, observed peer).", {}),
    ("relay-role", "Relay (relevant type)",
     "contextAgents relevantType: the hub that relayed the record to the memory server.", {}),
]
SCHEMA_TELEMETRY = {
    "type": "object",
    "required": ["kind"],
    "properties": {
        "kind": {"enum": ["pose", "navigation", "sensor"]},
        "frame": {"type": "string"},
        "sensor": {"type": "string"},
        "unit": {"type": "string"},
        "samples": {"type": "array", "items": {"type": "object"}},
        "goal": {},
        "status": {"enum": ["active", "reached", "failed", "cancelled"]},
        "distance_remaining_m": {"type": "number"},
        "progress": {"type": "number", "minimum": 0, "maximum": 1},
        "samples_count": {"type": "integer"},
        "truncated": {"type": "boolean"},
    },
}
V010_EXT = [  # (slug, label, definition, kind, extra)
    ("holocron/seq", "Record sequence", "The record's per-agent sequence number (integer >= 1).", "ContextExtension",
     {"inlineSchema": json.dumps({"type": "integer", "minimum": 1})}),
    ("holocron/hash", "Record hash", "SHA-256 of the signed record (lowercase hex). Verify against the memory server.",
     "ContextExtension", {"inlineSchema": json.dumps({"type": "string", "pattern": "^[0-9a-f]{64}$"})}),
    ("holocron/prev-hash", "Previous record hash", "Hash of the agent's previous record (hash chain).",
     "ContextExtension", {"inlineSchema": json.dumps({"type": "string", "pattern": "^[0-9a-f]{64}$"})}),
    ("holocron/payload-hash", "Payload hash", "SHA-256 of the record payload. The payload itself is not exported by default.",
     "ContextExtension", {"inlineSchema": json.dumps({"type": "string", "pattern": "^[0-9a-f]{64}$"})}),
    ("holocron/signature", "Record signature", "The author's Ed25519 signature over the record (hex).",
     "ContextExtension", {"inlineSchema": json.dumps({"type": "string"})}),
    ("holocron/record-type", "Record type",
     "The Holocron record type: communication, thought, decision, action, event, perception, lesson, policy or system.",
     "ContextExtension", {"inlineSchema": json.dumps({"enum": ["communication", "thought", "decision", "action", "event",
                                                               "perception", "lesson", "policy", "system"]})}),
    ("holocron/tags", "Record tags", "The record's tags, e.g. telemetry, internal.", "ContextExtension",
     {"inlineSchema": json.dumps({"type": "array", "items": {"type": "string"}})}),
    ("holocron/refs", "Record references",
     "Links to other records by role, e.g. {\"because\": \"robot-1:41\"}. Values are agent:seq strings or lists of them.",
     "ContextExtension", {"inlineSchema": json.dumps({"type": "object"})}),
    ("holocron/received-at", "Received at", "When the memory server accepted the record (ISO 8601).", "ContextExtension",
     {"inlineSchema": json.dumps({"type": "string", "format": "date-time"})}),
    ("holocron/mapping-version", "Mapping version",
     "Version of the record-to-statement mapping. Statement ids are derived per mapping version.", "ContextExtension",
     {"inlineSchema": json.dumps({"type": "string"})}),
    ("agent-kind", "Agent kind", "What the actor is: robot, ai-agent, relay or human.", "ContextExtension",
     {"inlineSchema": json.dumps({"enum": ["robot", "ai-agent", "relay", "human"]})}),
    ("software", "Software version", "The actor's software or firmware version string.", "ContextExtension",
     {"inlineSchema": json.dumps({"type": "string"})}),
    ("outcome", "Outcome",
     "How an action ended: success, partial, reflex_stop, stuck, abandoned or failed. result.success is true only for success.",
     "ResultExtension", {"inlineSchema": json.dumps({"enum": ["success", "partial", "reflex_stop", "stuck",
                                                               "abandoned", "failed"]})}),
    ("telemetry", "Telemetry window",
     "A periodic sensor window: pose, navigation or sensor samples. Large windows are exported as a summary "
     "(samples_count, truncated: true).", "ResultExtension", {"inlineSchema": json.dumps(SCHEMA_TELEMETRY)}),
]

# Record type -> verb (event uses ADL "experienced").
RECORD_VERBS = {
    "perception": f"{BASE}/verbs/perceived", "thought": f"{BASE}/verbs/reasoned",
    "decision": f"{BASE}/verbs/decided", "action": f"{BASE}/verbs/performed",
    "communication": f"{BASE}/verbs/communicated", "event": ADL + "experienced",
    "lesson": f"{BASE}/verbs/learned", "policy": f"{BASE}/verbs/set-policy",
    "system": f"{BASE}/verbs/reported",
}
EXT = f"{BASE}/extensions/"


def ctx_ext(slug):
    return f"$.context.extensions['{EXT}{slug}']"


def templates():
    out = []
    common = [
        {"location": "$.actor.account.homePage", "presence": "included"},
        {"location": "$.object.definition.type", "presence": "included", "all": [f"{BASE}/activity-type/record"]},
        {"location": "$.context.contextActivities.category[*].id", "presence": "included", "any": [V010]},
        {"location": ctx_ext("holocron/seq"), "presence": "included"},
        {"location": ctx_ext("holocron/hash"), "presence": "included"},
        {"location": ctx_ext("holocron/prev-hash"), "presence": "included"},
        {"location": ctx_ext("holocron/signature"), "presence": "included"},
        {"location": ctx_ext("holocron/mapping-version"), "presence": "included"},
    ]
    for rtype, verb in RECORD_VERBS.items():
        rules = common + [{"location": ctx_ext("holocron/record-type"), "presence": "included", "all": [rtype]}]
        if rtype == "action":
            rules.append({"location": f"$.result.extensions['{EXT}outcome']", "presence": "recommended"})
        if rtype == "communication":
            rules.append({"location": "$.context.contextAgents", "presence": "recommended"})
        out.append({
            "id": f"{BASE}/templates/holocron-{rtype}", "type": "StatementTemplate", "inScheme": V010,
            "prefLabel": {"en": f"Holocron {rtype} record"},
            "definition": {"en": f"A Holocron `{rtype}` record exported as a statement."},
            "verb": verb, "objectActivityType": f"{BASE}/activity-type/record", "rules": rules,
        })
    for kind, label in (("pose", "pose"), ("navigation", "navigation"), ("sensor", "sensor")):
        out.append({
            "id": f"{BASE}/templates/telemetry-{kind}", "type": "StatementTemplate", "inScheme": V010,
            "prefLabel": {"en": f"Telemetry: {label} window"},
            "definition": {"en": f"A perception record tagged telemetry whose payload is a {label} window."},
            "verb": RECORD_VERBS["perception"], "objectActivityType": f"{BASE}/activity-type/record",
            "rules": common + [
                {"location": ctx_ext("holocron/tags") + "[*]", "presence": "included", "any": ["telemetry"]},
                {"location": f"$.result.extensions['{EXT}telemetry'].kind", "presence": "included", "all": [kind]},
            ],
        })
    return out


def build():
    concepts = []
    concepts += [concept("Verb", f"verbs/{s}", l, d, V09) for s, l, d in V09_VERBS]
    concepts += [concept("ActivityType", f"activity-type/{s}", l, d, V09) for s, l, d in V09_TYPES]
    concepts += [concept(k, f"extensions/{s}", l, d, V09) for s, l, d, k in V09_EXT]
    concepts += [concept("Verb", f"verbs/{s}", l, d, V010, **x) for s, l, d, x in V010_VERBS]
    concepts += [concept("ActivityType", f"activity-type/{s}", l, d, V010, **x) for s, l, d, x in V010_TYPES]
    concepts += [concept(k, f"extensions/{s}", l, d, V010, **x) for s, l, d, k, x in V010_EXT]
    return {
        "@context": "https://w3id.org/xapi/profiles/context",
        "id": PROFILE,
        "type": "Profile",
        "conformsTo": "https://w3id.org/xapi/profiles#1.0",
        "prefLabel": {"en": "xAPI AI Agent Actions Profile (AIAAP)"},
        "definition": {"en": (
            "Captures human instructions and AI agent operations, including MCP tool calls, resource access, "
            "generation, delegation, evaluation, approvals and governance outcomes. Version 0.10.0 adds a robotics "
            "and physical-AI module for robots, hybrid AI and swarms: one verb per memory-record type, telemetry "
            "windows (pose, navigation, sensor), and provenance extensions that let any statement be verified against "
            "its signed source record. Concepts are aligned with the I2IDL Glossary of Digital Learning (v0.0.93) "
            "where a match exists.")},
        "seeAlso": "https://github.com/seanrugg/xapi-ai",
        "author": {"type": "Person", "name": "Sean Rugge", "url": "https://github.com/seanrugg"},
        "versions": [
            {"id": V010, "wasRevisionOf": [V09], "generatedAtTime": "2026-10-31T00:00:00Z"},
            {"id": V09, "generatedAtTime": "2026-02-13T16:48:25Z"},
        ],
        "concepts": concepts,
        "templates": templates(),
    }


def check(p):
    ids = [c["id"] for c in p["concepts"]] + [t["id"] for t in p["templates"]]
    assert len(ids) == len(set(ids)), "duplicate ids"
    versions = {v["id"] for v in p["versions"]}
    for c in p["concepts"]:
        for k in ("id", "type", "inScheme", "prefLabel", "definition"):
            assert c.get(k), (c.get("id"), k)
        assert c["inScheme"] in versions
        if "inlineSchema" in c:
            json.loads(c["inlineSchema"])
    verbs = {c["id"] for c in p["concepts"] if c["type"] == "Verb"} | {ADL + "experienced"}
    types = {c["id"] for c in p["concepts"] if c["type"] == "ActivityType"}
    for t in p["templates"]:
        assert t["verb"] in verbs and t["objectActivityType"] in types, t["id"]
        for r in t["rules"]:
            assert r["location"].startswith("$.") and r["presence"] in ("included", "excluded", "recommended")


if __name__ == "__main__":
    profile = build()
    check(profile)
    out = Path(__file__).resolve().parent.parent / "ai_agent_actions_profile.json"
    out.write_text(json.dumps(profile, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {out.name}: {len(profile['concepts'])} concepts, {len(profile['templates'])} templates")
