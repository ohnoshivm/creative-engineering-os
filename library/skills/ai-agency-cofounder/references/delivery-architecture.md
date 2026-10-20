# Phase 5: Delivery Architecture — The Channel Is the Org Chart

## THE WORKSPACE TOPOLOGY (Fork This)

```
my-agency-workspace/
├── # WAR ROOM
│   ├── #standup           ← daily morning brief from agents
│   ├── #wins              ← revenue + delivery wins
│   └── #fires             ← anything urgent, human-only
├── # OPERATIONS
│   ├── #ops               ← Roman delivers finished work here
│   ├── #revenue           ← Stripe webhooks, MRR pings, churn alerts
│   ├── #outreach          ← Apollo/Clay/Instantly, reply triage
│   ├── #scheduling        ← Cal.com bookings + calendar conflicts
│   └── #ai-bots           ← bot-to-bot scratchpad, debug, logs
├── # CLIENTS (one channel per active retainer)
│   ├── #client-acme       ← shared with client + their team (Slack Connect)
│   ├── #client-beta       ← shared with client
│   └── #client-gamma
└── # CONTRACTORS
    ├── #editor-jenna      ← human VA / editor
    └── #dev-priya         ← part-time engineer
```

~12 channels. The entire org chart of a solo agency at 5-figure MRR.

### The One Unbreakable Rule
> Every bot response goes in the **thread** of the initial message. No exceptions.

Without threading, the multi-bot pattern turns channels into a wall of agent chatter and
the human router problem comes back. You're right back to copy-pasting context between
tools instead of letting channels carry it.

---

## THE 8-STEP CANONICAL DELIVERY LOOP

**From client message to shipped deliverable:**

**1. Intake**
Client posts a request in #client-acme, OR a scheduled cron triggers it
(example: "every monday 9am, run last week's content audit")

**2. Classify**
@delivery-bot reads the message, checks against the pinned service spec doc,
posts a clarifying question if the request is out of scope

**3. Execute**
Bot pulls the memory layer for client context, runs the delivery template, drafts output

**4. QA Gate**
Bot runs the internal QA checklist against the draft, posts draft + checklist results
to #client-acme-internal with an :eyes: reaction

**5. Human Ship Gate**
You review. :rocket: to ship. Or request a revision in the thread.
This gate stays human. Always.

**6. Deliver**
Bot posts the final artifact to #client-acme with a thread link to the audit log entry

**7. Log**
Run appended to the client's audit dataset:
- Timestamp
- Input
- Model and tools used
- Output
- QA results
- Reviewer ID

**8. Update Memory**
Memory layer ingests the run for next time.
The agent gets slightly better at this specific client.

---

## THE QA GATE CHECKLIST (Wire Once, Forget)

Your agent automatically checks every draft against:
- ✓ Pinned service spec compliance
- ✓ Voice match against client memory layer profile
- ✓ Citation density on every numeric claim
- ✓ Format compliance against client's canonical output template
- ✓ Client glossary / preferred terminology check
- ✓ Scrub for agent self-references and other-client PII leaks
- ✓ Audit log entry exists with all required fields populated

**If any check fails**:
- Agent writes a one-line diagnosis
- Posts to #client-X-internal with a :warning: reaction
- Refuses to ship the deliverable into the client channel until resolved

The human ship gate stays human, but the gate itself is held by the agent.

---

## WEEKLY CLIENT REPORTS (Zero Human Touch)

Every Friday, agent drops weekly reports into each shared client channel:
- Pulled from their HubSpot, Stripe, analytics stack
- Written, formatted, posted automatically
- No human involvement required

---

## TRANSPARENCY AS TRUST SIGNAL

> Clients in 2026 already assume AI is somewhere in the loop.
> Operators trying to hide it are losing to operators who show it.

`[AI-drafted, human-approved]` tags on deliverables = **higher renewal rates**
than operators trying to pass everything off as fully hand-typed.

The tag is a trust signal, not a confession.

---

## THE LOCK-IN MECHANISM

After 6 months of context, audit logs, and agent memory inside a shared client channel:
- Switching costs are no longer your contract
- They are 18 months of agent-curated context that walks out the door if they leave

**The renewal conversation at month 12 is about what they would lose, not about price.**
They almost never leave.

---

## WHY SLACK IS THE OPERATING SYSTEM

Three things converged in late 2025 / early 2026:

1. **Late 2025**: Anthropic ships interactive apps inside Claude.ai with Slack as one of
   9 launch integrations — you can draft and post a Slack message without leaving Claude

2. **Early 2026**: Slack ships its MCP server. Claude Desktop, Claude Code, Perplexity,
   Cursor can now talk to Slack natively. Slack reports 25x increase in MCP tool calls
   since October 2025 limited release. 50+ context-aware agents shipped against the surface.

3. **March 2026**: Salesforce ships 30 new AI features in Slack, turns Slackbot into a
   full MCP client. Slack stops being a chat app and becomes the agent execution layer.

**The result**: Slack is the only place where the operator, the autonomous coworker,
channel-bound bots, deal data from Apollo/Clay/Stripe, project state from Linear/Notion,
and meeting transcripts all sit in the same searchable, permissioned, agent-readable index.

That is the operating system argument. Everything else is feature comparison.
