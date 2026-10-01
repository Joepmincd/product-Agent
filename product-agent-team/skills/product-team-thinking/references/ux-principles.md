# UX Principles Reference

Use these heuristics to explain product tradeoffs. They do not establish project facts, fixed interface limits, performance targets, or approval requirements. Apply the [shared workflow](../../../workflow.md) for decisions and the [P3–P6 principles](../../../产品经理交互体验能力项_P3-P6.md) for interaction, feedback, error handling, and state behavior.

---

## Foundational UX Laws (Applied)

### Hick's Law
**Principle:** Decision time increases with the number and complexity of choices.
**Apply when:** Reviewing navigation menus, onboarding steps, feature discovery, settings pages.
**PM/Design implication:** Every choice you add to a screen increases cognitive load. Progressive disclosure (reveal options when needed) beats showing everything at once.

### Jakob's Law
**Principle:** Users spend most of their time on other products and expect yours to work the same way.
**Apply when:** Designing navigation, form patterns, iconography, interaction patterns.
**PM/Design implication:** Deviating from convention requires paying a "novelty tax" — you have to teach users a new mental model. Only innovate when the benefit clearly outweighs that cost.

### Miller's Law
**Principle:** Working-memory capacity is limited and depends on the task, familiarity, and how information is grouped.
**Apply when:** Reviewing multi-step flows, menu lengths, data tables, onboarding sequences.
**PM/Design implication:** Group related information and reduce unnecessary recall. Do not use a fixed item or step count as a release criterion; preserve necessary tasks and evaluate the actual reading burden.

### Tesler's Law (Conservation of Complexity)
**Principle:** Every system has an irreducible complexity — it can be shifted between system and user, but not eliminated.
**Apply when:** Evaluating "simplified" UX that may have just moved complexity to an unexpected place.
**PM/Design implication:** The question isn't "how do we remove complexity" but "who should bear this complexity — the user or the system?"

### Doherty Threshold
**Principle:** Prompt feedback supports continuity during interaction; a commonly cited threshold is a heuristic, not a universal performance requirement.
**Apply when:** Reviewing any interaction with loading states, API calls, or animations.
**PM/Design implication:** Perceived speed matters as much as actual speed. Immediate progress feedback and clear processing states maintain engagement during real waits.

---

## Applying interaction principles

Use the shared P3–P6 reference for empty states, confirmation strength, actionable errors, progress, and recovery. It owns those definitions; this reference adds product-level interpretation rather than a second checklist. A product recommendation still needs evidence about the current task and its constraints.

---

## Product Decision Frameworks

### The Jobs-to-be-Done Frame
When evaluating a feature: "What job is the user hiring this product to do?"
- Functional job: The practical task
- Emotional job: How they want to feel
- Social job: How they want to be perceived

Features that only address the functional job often underperform. The emotional and social jobs often drive adoption.

### Activation vs. Engagement vs. Retention
Different product phases need different UX priorities:
- **Activation:** Help users reach their first "aha moment" as fast as possible. Reduce setup friction.
- **Engagement:** Create habit-forming loops. Ensure users see value on return visits.
- **Retention:** Reduce pain points that cause churn. Ensure users can pick up where they left off.

A feature designed for engagement may actually hurt activation if it adds upfront complexity.

### The Reversibility Principle
Rank design decisions by their reversibility:
- **Easily reversible:** Prefer a small experiment within the current task scope
- **Hard to reverse:** Assess affected rules and validate the important assumptions
- **Irreversible:** Explain consequences and follow the actual decision authority; do not invent a universal sign-off process

This applies to both product decisions and UX patterns (once users learn a pattern, changing it has a real cost).

---

## Onboarding tradeoffs

Assess these examples against the confirmed first task and its prerequisites:

1. **Verification before value:** Defer verification only when the initial task remains valid and its access requirements allow it. Otherwise explain why verification is needed and how to recover from failure.
2. **Team invitation before exploration:** Offer later invitation when a useful individual task exists. If the first outcome requires collaboration or shared access, retain the dependency and make the invitation step clear.
3. **Integration before first use:** Offer a skip path only when an approved sample, alternate source, or independent task can produce a valid result. If real integration is necessary, improve setup guidance and recovery instead of pretending the dependency can be skipped.
4. **Feature tour without context:** Choose timing based on task complexity and risk. Inline guidance may be sufficient for simple actions; necessary orientation can precede consequential operations.
5. **Signup questions:** Request information needed for the agreed initial task or its prerequisites, and defer unrelated information when doing so preserves the outcome.

These are conditional design examples, not evidence that a particular product loses users or must use a specific flow.
