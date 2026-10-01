# Frontend Standards Extraction and QA

Use this reference when an HTML design or demo must continue an existing product, match a screenshot or design specification, or contain several related screens or states. Apply only the checks relevant to the user's static or clickable mode, target platform, and changed scope. This reference does not reopen the shared product workflow, require a second approval, or expand a local task into a whole-product implementation.

## Capability reuse map

| Reusable capability from `figma-master` | Demo-maker adaptation | Required evidence or output |
|---|---|---|
| Source-first design selection | Resolve relevant supplied files, `DESIGN.md`, screenshots, code/theme tokens, and explicit preferences before styling | Concise source notes where material, separating confirmed, inferred, unknown, and conflicting rules |
| Design Language Contract | Translate applicable visual rules into tokens and layout/state conventions | Existing design tokens or a compact internal contract |
| Reuse contract | Reuse existing HTML/CSS patterns, assets, component APIs, and theme tokens before inventing new ones | `reuse directly`, `recreate from observed pattern`, `create missing primitive`, `open questions` |
| Screenshot + PRD baseline | Preserve confirmed shell, density, copy, controls, and feedback placement; implement only PRD deltas | `keep`, `add`, `modify`, `remove`, `state to show` delta list |
| Impact assessment | Map a shared visual or interaction change to affected routes, states, components, tokens, and breakpoints | Relevant scope and regression checks; rollback detail only when warranted |
| Semantic tokens | Use CSS custom properties and a small component token layer instead of scattered raw values | Named tokens such as `--color-bg-surface`, `--text-primary`, `--space-300` |
| Auto Layout and hierarchy | Use semantic HTML with flex/grid, intrinsic sizing, explicit gaps, min/max constraints, and intentional overlay ownership | No coordinate-only page clones; responsive layout remains explainable |
| Component governance | Reuse components and props; use variants for predictable visual/state differences and props for content differences | Clear component names and no accidental visual duplicates |
| State visibility contract | Define what must show, hide, and not exist for every demo state | No empty pills, orphan labels, stale overlays, or hidden controls with active hit areas |
| Typography and copy resilience | Use confirmed fonts; disclose substitutions, treating them as blocking only when exact reproduction is required; test relevant copy extremes | No fixed-height text breakage or silent substitution of a required font |
| Visual quality gate | Render the representative screen at overview and 100% before scaling out; compare to the source when one exists | Screenshot/preview evidence and a fix-and-rerender loop |
| State-by-state QA | Test requested screens and important states, then inspect their connecting flow | Initial, empty, loading, success, error, recovery, permission, and destructive states as relevant |
| Responsive and accessibility audit | Test target viewport matrix, keyboard/focus, contrast, labels, target sizes, and non-color status cues | Pass/fail notes and unresolved decisions |
| Reuse and resilience audit | Stress-test long labels, empty data, error copy, optional media, and smallest/largest target size | Component fixes through layout/props, not manual nudges |
| Regression check | Verify affected routes, states, and shared consumers after changes | Evidence for applicable checks; unexecuted cases remain unverified |

## Source and evidence workflow

Classify each input before writing UI:

- A Figma file or library is the source of actual components, variables, styles, and assets.
- A `DESIGN.md`, theme file, or code token module is a documented system contract.
- A screenshot is visual evidence only; do not infer invisible component behavior from it.
- A PRD defines product intent and required deltas, not a license to redesign confirmed product chrome.
- An inferred visual preference covers unresolved gaps; the user's explicit current design decision takes priority as described below.

Use the [shared workflow](../../../workflow.md) for context decisions and the [product model/writeback boundary](../../../project-memory-rules.md#轻量产品模型与回写) for facts, assumptions, and baseline eligibility. A supplied screenshot is evidence of visible appearance, not proof of hidden behavior. Resolve material conflicts through the shared workflow; otherwise reuse the applicable design source and make reasonable choices for uncovered visual gaps.

For an existing product or a complex design, capture the applicable typography, spacing, semantic colors, shape, icon treatment, content resilience, overlays, responsiveness, and accessibility conventions. A compact internal contract or existing tokens are sufficient; simple tasks do not need separate source tables or contract documents. Track source substitutions and any limitations that affect the requested fidelity in delivery notes, outside the product surface.

## Frontend implementation rules

- For multiple screens, build a representative route first. For a local edit, work on the affected screen without recreating the whole demo.
- Define the container, safe margins, content column, responsive breakpoints, and overflow strategy before filling content.
- Prefer semantic HTML, flex/grid, intrinsic height, `min-width: 0`, `max-width`, and content-driven layout. Use absolute positioning only for owned overlays or decoration with a documented z-order and safe bound.
- Keep text blocks vertically auto-sized. Long copy must grow its parent, wrap, scroll in an explicit body region, or disclose more content; never clip it to preserve a one-line height.
- Use CSS tokens and component-level tokens. Do not retune global tokens to fix a local defect without assessing sibling routes and states.
- Keep component APIs small. Use state props for `default`, `hover`, `focus`, `pressed`, `disabled`, `loading`, `success`, and `error` where relevant; use content props for labels and copy.
- In clickable mode, give each in-scope interactive element a visible response. Omit out-of-scope actions or make their unavailable state clear. In static mode, shown controls are visual examples; do not claim they have implemented behavior.
- Use confirmed fonts and source icons. If a required source asset cannot be used, record the substitution and its impact; exact reproduction may remain unverified, while an ordinary concept design may use a suitable alternative.
- Keep the Demo Navigator out of the product surface or clearly mark it as review chrome. It must never be mistaken for product UI in screenshots or stakeholder review.
- Keep loading, error, success, and recovery feedback owned by one layer. Do not stack duplicate toasts, banners, modals, and inline errors unless the scenario explicitly requires it.

## State contract

For relevant interactive routes, use this matrix when it helps track the specified states. A static screen needs only its requested visible states; do not implement loading, error, or permission flows solely to fill this matrix:

| State | Must show | Must hide | Must not exist | Next action | Feedback/recovery |
|---|---|---|---|---|---|
| idle | primary content and entry action | transient feedback | stale previous result | primary action | none or contextual hint |
| loading | progress and disabled duplicate action | conflicting actions | infinite spinner path | wait/cancel if supported | resolves or explains failure |
| success | result and next useful action | loading/error surfaces | stale form submission affordance | continue, edit, or return | success confirmation |
| error | cause and recovery action | success-only content | dead-end message | retry, edit, or return | visible error + recovery |
| empty | empty explanation and first action | data-only controls | empty cards or undefined text | create, search, or refresh | guidance |

Extend the matrix only for applicable permission, realtime, destructive confirmation, nested overlays, and responsive differences. A hidden control must not leave a border, label, icon, hit area, or keyboard target behind.

## Rendered visual gate

When rendering tools are available, before expanding a multi-screen design (or delivering a local change):

1. Render the representative route at 100% and overview scale.
2. Compare against the source at a comparable scale when a source exists.
3. Check hierarchy, alignment, density, type metrics, contrast, image crop, whitespace, and grouping.
4. Check long-copy wrapping, button/select/table truncation, modal bounds, toast placement, and edge collisions.
5. Fix the smallest responsible layer, rerender, and recheck affected siblings.

If a visual problem remains, fix the responsible layer and verify the affected result. Offer alternatives only when a real unresolved design choice warrants them; do not force a fixed number of iterations or an additional approval.

## Frontend QA matrix

Run applicable checks for the requested pages, specified important states, and affected shared consumers. Existing unrelated flows do not need a full rebuild or repeat test. Static mode omits behavioral checks it does not claim to implement:

### Structure and layout

- No content, control, modal, toast, or overlay crosses its intended container or viewport.
- Multiline text grows without covering following content.
- Same-row labels, fields, and actions share a deliberate baseline or centerline.
- Repeated controls share height, padding, gap, radius, and icon alignment.
- Overlays have explicit owner, z-order, close/recovery behavior, and safe bounds.
- No duplicate DOM layer, stale component, old label, border, or hit area remains after a state change.

### Typography and content

- Font family and style follow the confirmed source or a disclosed reasonable design choice.
- Test relevant long/short, empty and error copy; include localization when it is in scope.
- No `undefined`, `null`, `[object Object]`, placeholder copy, or accidental lorem ipsum appears.
- Important text is not truncated or hidden by `overflow: hidden`.

### Interaction and state (clickable mode only)

- Arrive on the route and verify the initial state.
- Take the primary action and verify visible feedback.
- Repeat the action immediately and verify duplicate-submit protection.
- Submit empty or invalid data and verify error/recovery behavior.
- Navigate away and return; verify reset or persistence matches the contract.
- Test in-scope buttons, links, inputs, toggles, dropdowns, modals, and any existing Demo Navigator entries; do not add a navigator solely for testing.
- Verify loading resolves, success is legible, and error never ends in a dead end.

### Responsive and accessibility

- Test the agreed desktop/mobile/tablet viewport matrix, not only the default browser size.
- Verify layout transitions, wrapping, navigation collapse, scroll ownership, and touch target sizes.
- Verify keyboard reachability, visible focus, semantic labels, form associations, contrast, and non-color status cues.
- Do not claim responsive or accessible readiness when a required viewport or manual check is unverified.

## Change and regression protocol

Before changing a shared component, token, source rule, route shell, or state contract, identify the following internally or in a concise change note when useful:

- `Change`
- `Direct scope`
- `Indirect scope`
- `Risk`
- `Verification`
- `Rollback`

After editing, compare the actual diff with the intended scope. Reassess unexpected effects and fix the smallest responsible layer. Add a regression case only when it protects a meaningful behavior; do not add tests merely matching generated wording or harmless formatting.

For evidence and completion claims, use the [shared workflow’s verification and delivery rules](../../../workflow.md#修订验证与交付). Report only checks actually performed; a frontend simulation does not establish real backend behavior.
