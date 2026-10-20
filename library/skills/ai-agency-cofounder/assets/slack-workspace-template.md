# Slack Workspace Template — Solo AI Agency

Fork this on day one. Do not add channels until you clear $20K MRR.

## Channel Setup Checklist

### WAR ROOM
- [ ] #standup — daily morning brief from agents (pin the standup prompt here)
- [ ] #wins — revenue events, signed clients, delivered milestones
- [ ] #fires — urgent issues, human-only, no bots in this channel

### OPERATIONS
- [ ] #ops — Roman's primary delivery channel, finished work drops here
- [ ] #revenue — connect Stripe webhook, MRR ping every Monday, churn alert on cancel
- [ ] #outreach — Apollo/Clay/Instantly replies route here, Roman handles triage
- [ ] #scheduling — Cal.com bookings, calendar conflicts, rescheduling alerts
- [ ] #ai-bots — bot scratchpad, debug logs, agent-to-agent chatter (not client-facing)

### CLIENTS (create on signing, archive on churn)
- [ ] #client-[name] — Slack Connect with client team, delivery channel
- [ ] #client-[name]-internal — internal QA channel, not shared with client

### CONTRACTORS (add only when headcount exists)
- [ ] #contractor-[name] — one channel per human contractor

---

## Pinned Items (Do This on Day One)

In every #client-[name] channel, pin:
1. **Service spec doc** — exact scope, what's in and out
2. **Delivery cadence** — when deliverables arrive, what format
3. **Escalation protocol** — when to tag a human vs. let the bot handle it
4. **Client glossary** — preferred terminology, brand voice notes

---

## The One Rule
Every bot response goes in the **thread** of the initial message.
No exceptions. No orphaned top-level bot messages.
This is the rule that keeps 12 channels from becoming chaos.
