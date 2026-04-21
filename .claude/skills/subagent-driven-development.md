# subagent-driven-development

Decompose a complex task into parallel sub-agents for faster, isolated execution.

## Usage

```
/subagent-driven-development <task description>
```

## Steps

1. **Decompose** — Break the task into independent sub-tasks (research, implementation, tests, docs).
2. **Spawn agents** — Launch each sub-task as a separate `Agent` tool call in a single message so they run concurrently.
3. **Collect results** — Wait for all agents to finish; gather their outputs.
4. **Synthesize** — Integrate the results, resolve conflicts, and produce the final deliverable.
5. **Report** — Summarize what each agent did and what was merged.

## Guidelines

- Use `subagent_type: "Explore"` for read-only research agents.
- Use `subagent_type: "general-purpose"` for implementation agents.
- Keep agent prompts self-contained — each agent has no memory of the conversation.
- Never delegate security-sensitive operations to sub-agents without explicit user approval.

## Notes

- Best suited for tasks with ≥ 3 independent work streams.
- For sequential tasks, use a single agent or chain calls instead.
