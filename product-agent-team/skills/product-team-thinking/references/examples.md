# Worked Examples

Reference examples showing how to apply each workflow. Use these to calibrate output quality and format. These are hypothetical, scoped examples, not confirmed facts, mandatory output lengths, or evidence that a real product was tested. Reuse the reasoning structure, not the example's business rules. Use the shared [workflow](../../../workflow.md) and [evidence thresholds](../../product-audit/SKILL.md#主结论与证据阈值); these examples do not define separate confirmation, verdict, or diagram rules.

---

## Example 1: Edge Case Mapping — Card Freeze Feature

**User prompt:** "Map the edge cases for a card freeze feature in a fintech app."

**Output:**

### Happy Path
User taps "Freeze Card" → Confirmation prompt → Card is frozen → Card shows "Frozen" status → All new transactions are declined

### Edge Cases

**Input/State Variations**
- Card already frozen → Button should say "Unfreeze Card"; tapping shows different confirmation
- Multiple cards → Flow must clearly show *which* card is being frozen; accidental freeze of wrong card is high-risk
- Virtual vs. physical card → Freeze behavior may differ (virtual transactions vs. POS); must be explained to user

**Network & System**
- Freeze request times out → Show an unknown or pending result, not success. Query authoritative status; retry only if the product's confirmed idempotency and retry rules support it.
- Partial success (frontend shows frozen, backend failed) → Must reconcile; silent failure here = security risk
- User has no network → Explain that freeze is not confirmed and provide a supported next action. Offline queuing is an option only if explicitly supported; do not promise a later freeze without that capability.

**User Behavior**
- User freezes card during an in-flight transaction → Determine whether the confirmed payment rules allow an already authorized transaction to complete, and explain the effective boundary to the user.
- User freezes card while a recurring payment is pending → Should recurring payments be blocked? This needs a product decision
- User immediately unfreezes then re-freezes rapidly → Rate limiting consideration; fraud signal?

**Permission / Account States**
- Card reported stolen (not just frozen) → Different flow; freeze is temporary, report-stolen triggers replacement
- Account suspended → Verify which protective actions remain permitted; do not assume suspension disables freezing.

**Highest-impact risks in this example (not a required count):**
1. **Silent freeze failure** — User thinks card is frozen but it isn't. Security liability.
2. **Frozen card during in-flight transaction** — User makes a purchase, then freezes mid-authorization. Unclear outcome causes support tickets.
3. **No "pending" state** — Network lag means user taps freeze, nothing happens visually, taps again → double freeze request.

---

## Example 2: UX Review — Onboarding Flow

**User prompt:** "Review this onboarding flow: Sign up → Email verification → Create team → Set up integrations → Invite teammates → Start using product"

**Output:**

**Outcome: 证据不足.** The sequence alone does not establish the target users, first-session goal, mandatory controls, or actual screens. The following are questions and conditional recommendations, not verified defects or a full application audit.

### Potential High-impact Issues

**1. Email verification before value**
- **Observation:** The listed sequence puts verification before first use. No conversion data or verification requirements are provided.
- **Potential impact:** Switching apps can interrupt progress, but verification may be necessary for account safety or access control.
- **Suggestion:** If confirmed controls allow it, explore a limited preview before verification. Otherwise preserve verification and improve return-to-app recovery. Measure drop-off instead of inventing a percentage.

**2. Team creation as a required step**
- **Question:** Is a team the required ownership and permission container, or can a user complete the first task alone?
- **Potential impact:** Manual setup may add friction, but removing a required container can break the product's data model.
- **Suggestion:** If a personal mode is supported, consider optional team setup. If a space is mandatory, provide the lightest valid creation path and explain its purpose.

**3. Integration setup before core value**
- **Question:** Can the first task produce a meaningful result without an integration?
- **Potential impact:** Users without an account ready may be blocked; conversely, skipping a necessary data source can lead to an empty product.
- **Suggestion:** Allow skipping only when a valid alternative task or supported sample data exists. Otherwise explain the dependency and support resuming setup later.

### Important Issues

**4. No "aha moment" anchor**
- The flow ends with "Start using product" but doesn't define what success looks like for the first session. What should the user do first? What will make them feel like they made the right choice signing up?
- **Suggestion:** Define your activation event (e.g., "first X created") and design the flow to reach it as fast as possible.

### What the sequence suggests

- A linear progression is visible in the supplied description; the actual interface's orientation and progress feedback remain unverified.
- Invitation follows team creation; whether that timing is suitable depends on the first-session goal and shared-work prerequisites.

---

## Example 3: PRD Snippet — "See Less for 24 Hours" Feature

**User prompt:** "Write a PRD for a soft mute feature on a social feed — 'See less for 24 hours'"

**Output (abbreviated draft):** The following proposes a topic-level temporary hide. Whether “see less” means reduced ranking or complete hiding must be decided before treating this as implementation-ready; the user-facing label must match the selected behavior. The listed background and goals are hypotheses until supported by product context.

---

### Problem Statement
Users frequently encounter content on topics they're temporarily uninterested in — trending topics, live events, or recurring themes. Current options are binary: see everything, or permanently mute. This creates a friction point: users who don't want permanent mutes tolerate unwanted content, increasing scroll fatigue and reducing session satisfaction.

### Goals
- Reduce negative sentiment about unwanted trending content
- Increase session length / scroll depth for affected users
- Provide a reversible, low-commitment control mechanism

### Non-Goals
- Permanent topic muting (existing feature)
- Muting specific users or accounts
- Custom duration settings (v1 scope: 24 hours only)

### User Stories
- As a user, I want to stop seeing a trending topic for today without permanently blocking it, so I can stay in control of my feed without over-committing to a mute.
- As a user, I want to know when my temporary mute expires, so I can expect the topic to return.
- As a power user, I want to undo a soft mute I applied by mistake, so I don't lose content I wanted to see.

### Functional Requirements

**FR-1: Soft Mute Action**
- User can access "See less for 24 hours" from: (a) topic pill tap, (b) post overflow menu on a topic-tagged post
- Acceptance criteria: Action is available within 2 taps from the feed

**FR-2: Mute State**
- Posts matching the muted topic are hidden from main feed for 24 hours
- Acceptance criteria: Zero posts from muted topic appear in main feed during mute window

**FR-3: Edge Cases — Must Handle**
- User opens app after mute expires → topic posts reappear without notification (silent resumption)
- User applies mute to the same topic twice → Draft recommendation: preserve the current expiry and show "already muted until [time]"; this remains a rule decision until confirmed.
- Topic appears in a post with multiple topics → Define whether any matching topic or only a confirmed primary topic causes hiding. Do not defer this behavior-changing rule to implementation without a product decision.
- User wants to undo mute → accessible from settings > muted topics > temporary (not buried)

### Open Questions
1. Should soft mutes stack? (Mute same topic twice = 48 hours?)
2. Do soft mutes apply to Stories/Reels or feed only?
3. What happens to pinned/promoted posts for a muted topic?

**Internal readiness: 暂不通过 for implementation handoff.** This draft still contains explicit unresolved rules that determine visible behavior and acceptance criteria. This identifies document gaps, not defects observed in a real system.

---

*These examples illustrate the expected depth, specificity, and "why" orientation of outputs from this skill.*
