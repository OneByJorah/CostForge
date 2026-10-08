# CostForge — Persona

Archetype:        The Penny Auditor

One-line pitch:   Meters free AI traffic and prices what you didn't pay.

Voice:            precise · dry · understated. Never says "revolutionary". Never uses exclamation marks.

Sample sentences:
- "You spent nothing. Here is what it would have cost."
- "The proxy logs the request whether or not you were watching."
- "Zero dependencies is a feature; it is also the reason the dashboard ships prebuilt."

Palette:          primary #22c55e (accent green) · background #0b0f17 · panel #111827 · muted #6b7280
                  (taken from the actual dashboard stylesheet, not invented)

Typography:       UI sans stack (`ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto`)
                  for the dashboard; JetBrains Mono for token counts, rates and CLI output.

Emoji policy:     none

Banner concept:   The real dashboard header and its "savings meter" rendered against a dark
                  panel — captured from the running app, never stock art.

Do:
- Show real numbers from a real run, or show nothing.
- Keep the proxy transparent: metering must never alter the user's traffic.
- Say "zero dependencies" only where it is still true.

Don't:
- Claim a cost saving that was not measured.
- Add a dependency that could be replaced by the standard library.
- Let the dashboard imply data it is not actually receiving.

Target reader:    Homelab and self-host operators running local models (Ollama, LM Studio,
                  vLLM) or free-tier APIs who want to know the commercial value of that
                  traffic without paying for observability.
