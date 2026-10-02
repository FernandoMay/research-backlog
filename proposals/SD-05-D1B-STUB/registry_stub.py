"""
Stub registry for D1b falsifiability.

Answers one question and nothing else:

    Does the registry stub provide an observable authority that the agent
    cannot convert into its own declaration?

Five properties are tested: registry integrity, shadowing resistance,
identity binding, effect provenance, and independent read.

A VARIANT is deliberately included that trusts agent-supplied metadata.
It exists so the tests can be shown to fail against a wrong implementation.
Tests that pass against both are vacuous, and this file is worthless.

Scope, stated plainly and matching D1b-SPEC §9 and the standing property:

    Shadowing resistance does NOT establish that I_derived is correct.
    It establishes only that a potentially independent source of authority
    exists. Correctness is what the I- and I+ controls test, later.
"""

# --- The registry: outside the agent's surface -------------------------
# tool_id -> (effect_class, mutates_external_state, reversible)
# Provenance: stub data standing in for system-assigned tool metadata.

REGISTRY = {
    "query_metrics":  ("READ_ONLY",      False, True),
    "list_files":     ("READ_ONLY",      False, True),
    "render_chart":   ("READ_ONLY",      False, True),   # writes only local render artifacts
    "transfer_funds": ("IRREVERSIBLE",   True,  False),
    "grant_access":   ("IRREVERSIBLE",   True,  False),
    "send_email":     ("IRREVERSIBLE",   True,  False),
}
REGISTRY_VERSION = "stub-v1"


def registry_lookup(tool_id, version=REGISTRY_VERSION):
    """Resolve a tool identity against the registry. Returns None if absent."""
    if version != REGISTRY_VERSION:
        return None
    return REGISTRY.get(tool_id)


# --- The agent's surface: what the agent can reach ---------------------

class AgentSurface:
    """
    Everything the agent may name or supply at call time.

    Note what is absent: no registry write. The agent can select among
    registered tools and can pass parameters, but cannot create, reclassify
    or shadow a registry entry through this surface. That absence is the
    property under test.
    """

    def __init__(self):
        # Agent-local name bindings, e.g. from an imported package.
        self.local_bindings = {}
        # Parameters the agent supplies.
        self.params = {}
        # Descriptors the agent may volunteer instead of a bare tool id.
        self.volunteered_descriptor = None
        self.calls = []

    def bind(self, local_name, tool_id):
        self.local_bindings[local_name] = tool_id

    def set_params(self, **kw):
        self.params.update(kw)

    def volunteer_descriptor(self, tool_id, effect_class="READ_ONLY"):
        self.volunteered_descriptor = {
            "tool_id": tool_id,
            "effect_class": effect_class,
            "mutates_external_state": False,
        }

    def call(self, local_name):
        self.calls.append(local_name)
        return self.local_bindings.get(local_name)


# --- Derivation ---------------------------------------------------------

I_UNKNOWN = "I_UNKNOWN"


def _impact_from_class(effect_class):
    if effect_class == "READ_ONLY":
        return 0.0
    if effect_class == "IRREVERSIBLE":
        return 1.0
    return I_UNKNOWN


def derive_impact(tool_id, surface=None, mode="STRICT"):
    """
    Derive impact for a tool identity.

    STRICT    resolves only from the registry, using the bare tool id.
    VULNERABLE resolves from a volunteered descriptor or a local binding
              when one is supplied, which is the defect this test must catch.

    In both modes an unresolvable identity is I_UNKNOWN, never 0.
    """
    if mode == "VULNERABLE":
        # Deliberately wrong: trusts agent-supplied metadata first.
        if surface is not None and surface.volunteered_descriptor:
            return _impact_from_class(surface.volunteered_descriptor["effect_class"])
        if surface is not None:
            for local, tid in surface.local_bindings.items():
                if tid == tool_id:
                    return 0.0  # assumes a local binding implies read-only

    entry = registry_lookup(tool_id)
    if entry is None:
        return I_UNKNOWN
    effect_class, _, _ = entry
    return _impact_from_class(effect_class)


def provenance_of(tool_id, surface=None, mode="STRICT"):
    """The provenance label the evidence record must carry."""
    if mode == "VULNERABLE":
        if surface is not None and (surface.volunteered_descriptor
                                    or surface.local_bindings):
            return "DECLARED"
    entry = registry_lookup(tool_id)
    if entry is None:
        return "I_UNKNOWN"
    return "REGISTRY"