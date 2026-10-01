# Demo Maker Regression Tests

These are behavioral evaluation scenarios, not an automatically executed test runner. Select relevant cases after a material change to `product-team-html-demo/SKILL.md`, its references, shared conventions, or delivery behavior. A local demo edit needs the affected product checks, not every scenario in this catalog. Record which evaluations actually ran and their evidence; do not report this list as a passing automated suite.

## Case 1 — Source-first product continuation

Prompt: Build an interactive settings demo from a supplied `DESIGN.md`, screenshot, and PRD.

Expected:

- The agent reads and prioritizes the supplied sources before styling.
- It records confirmed, inferred, unknown, and conflicting rules.
- The PRD is converted into `keep`, `add`, `modify`, `remove`, and `state to show` deltas.
- Confirmed shell, typography, density, icon treatment, and feedback placement are preserved.

Fail if the demo invents a generic dashboard, silently substitutes a font, or redesigns confirmed product chrome.

## Case 2 — Insufficient evidence gate

Prompt: “Make a polished clickable demo” with no product, platform, user, visual reference, or behavioral detail.

Expected:

- The agent asks only the missing decisions that materially change the demo.
- It does not present assumed product rules or brand requirements as confirmed facts.
- Once product and scope are clear, lack of a visual reference alone does not trigger another approval; a reasonable design may be chosen.
- If the user explicitly requests a preview with material decisions still open, delivery notes identify it as a draft and state those limits outside the product surface.

Fail if the agent invents critical product rules, treats design assumptions as confirmed brand requirements, or requires a full interview for a local static screen.

## Case 3 — Representative visual gate and resilience

Prompt: Build a multi-screen demo with a table, modal, long labels, empty data, and error recovery.

Expected:

- The densest route is rendered and inspected before sibling routes are scaled.
- Long text, modal bounds, table width, action alignment, loading/error/success states, and recovery are checked.
- The agent rerenders after fixes and does not rely on DOM creation alone.

Fail if text is clipped, actions overflow, or only the happy path is validated.

## Case 4 — Interaction and state regression

Prompt: Build a form flow with async submission, permission denial, retry, and success.

Expected:

- Initial, loading, empty/invalid, permission-denied, error, retry, and success states are reachable.
- Double submit is guarded, feedback is visible, and recovery is explicit.
- Hidden state content does not leave stale controls, labels, or hit areas.

Fail if a state is listed in the Demo Navigator but does not work, or any action ends silently.

## Case 5 — Responsive and accessibility regression

Prompt: Build the same flow for desktop and mobile review.

Expected:

- Agreed viewport sizes are tested with intentional layout transitions.
- Keyboard focus, labels, contrast, touch targets, and non-color status cues are checked.
- Horizontal overflow and clipped controls are fixed or explicitly documented as a product decision.

Fail if “responsive” means only a CSS media query exists without rendered verification.

## Case 6 — Change-impact and rollback

Prompt: Change a shared button token and add a new error state after an existing demo is approved.

Expected:

- Direct and indirect routes/states/components are identified before editing.
- Risk, exact verification, and smallest rollback unit are recorded.
- Existing paths and other consumers affected by the shared token are regression-tested after the change, without retesting unrelated product areas.

Fail if the change is treated as local without checking shared consumers.

## Case 7 — Static and local scope

Prompt: “Change only this pet profile header and give me a static HTML page to inspect. Keep the existing flow.”

Expected:

- The agent reuses the existing artifact and updates the header and affected layout only.
- It does not add a backend, rebuild onboarding, implement every button, or request confirmation of the whole product.
- It checks the requested viewport and any directly affected shared elements.
- Delivery includes a working file link and a concise statement that this is static, with actual checks and material limitations.

Fail if a static request becomes a full clickable application, the final file link is forbidden, or unexecuted browser checks are claimed as passed.

## Case 8 — Tools unavailable

Prompt: Build an already specified single-page HTML preview in an environment with file tools but no browser or screenshot tool.

Expected:

- The agent creates and reads back the HTML, checking supported structural properties.
- It delivers the preview and states that rendered appearance and interaction remain unverified.
- It does not fabricate screenshots, mark browser tests as passed, or repeatedly ask for approval to resolve unavailable tools.

Fail if it claims verified visual acceptance or refuses all supported artifact work solely because it cannot render.
