from __future__ import annotations
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

class SteerableMockAgent:
    """Test-only agent that executes explicit CALL directives from the user message."""

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
        directives = _parse_directives(self._last_user_message(history))
        i = self._calls_since_last_user(history)
        if i < len(directives):
            tool, args = directives[i]
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
