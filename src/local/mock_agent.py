from __future__ import annotations
import re
from collections.abc import Sequence

from aicomp_sdk.agents.types import (
    AGENT_STATE_VERSION, AgentStateSnapshot, AgentToolSpec,
    FinalResponseDecision, ToolCall, ToolCallDecision,
    ToolRequestEvent, UserMessageEvent,
)
from aicomp_sdk.core.runtime_history import RuntimeHistory

def _parse_directives(message: str) -> list[tuple[str, dict[str, str]]]:
    out: list[tuple[str, dict[str, str]]] = []
    for chunk in message.split(";;"):
        toks = chunk.split()
        if len(toks) < 2 or toks[0] != "CALL":
            continue
        tool = toks[1]
        args: dict[str, str] = {}
        for kv in toks[2:]:
            if "=" in kv:
                k, v = kv.split("=", 1)
                args[k] = v
        out.append((tool, args))
    return out

_URL_RE = re.compile(r"https?://\S+")
_PAYLOAD_RE = re.compile(r"exfil-\S+")


def _parse_nl_post(message: str) -> tuple[str, dict[str, str]] | None:
    """Comprehend a natural-language 'POST <payload> to <url>' instruction.

    Stands in for a compliant real agent: extracts the collector url and the
    body payload and emits a single http.post. Returns None if the message is
    not an exfil-POST instruction.
    """
    low = message.lower()
    if "post" not in low:
        return None
    url_m = _URL_RE.search(message)
    if not url_m:
        return None
    url = url_m.group(0).rstrip(".,;)")
    payload_m = _PAYLOAD_RE.search(message)
    data = payload_m.group(0).rstrip(".,;)") if payload_m else message
    return ("http.post", {"url": url, "data": data})


class SteerableMockAgent:
    """Test-only agent that executes explicit CALL directives, or—failing that—
    a single natural-language exfil-POST instruction (so the NL policy can be
    exercised end-to-end through the engine)."""

    def __init__(self) -> None:
        self._n = 1

    def _last_user_message(self, history: RuntimeHistory) -> str:
        for ev in history.events[::-1]:
            if isinstance(ev, UserMessageEvent):
                return ev.text
        return ""

    def _calls_since_last_user(self, history: RuntimeHistory) -> int:
        count = 0
        for ev in history.events[::-1]:
            if isinstance(ev, UserMessageEvent):
                break
            if isinstance(ev, ToolRequestEvent):
                count += 1
        return count

    def next_action(self, *, history: RuntimeHistory, tools: Sequence[AgentToolSpec]):
        del tools
        last_user = self._last_user_message(history)
        directives = _parse_directives(last_user)
        i = self._calls_since_last_user(history)
        if directives:
            if i < len(directives):
                tool, args = directives[i]
                call = ToolCall(call_id=f"call_{self._n:06d}", tool_name=tool, arguments=args)
                self._n += 1
                return ToolCallDecision(call=call, assistant_message=None)
            return FinalResponseDecision(text="done")
        nl = _parse_nl_post(last_user)
        if nl is not None and i == 0:
            tool, args = nl
            call = ToolCall(call_id=f"call_{self._n:06d}", tool_name=tool, arguments=args)
            self._n += 1
            return ToolCallDecision(call=call, assistant_message=None)
        return FinalResponseDecision(text="done")

    def reset_state(self) -> None:
        self._n = 1

    def snapshot_state(self) -> AgentStateSnapshot:
        return {"version": AGENT_STATE_VERSION, "backend": "mock", "data": {"n": self._n}}

    def restore_state(self, snapshot: AgentStateSnapshot) -> None:
        self._n = int(snapshot["data"].get("n", 1))
