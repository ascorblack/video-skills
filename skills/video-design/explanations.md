# Explanations in the frame: term + applied example

## Term and example [Визуал]

Keep the terms: for a viewer who knows them it is quicker. But every term needs an applied example — a concrete case after which it is clear what is happening on the screen.

- **A permanent two-line panel on every slide:** "what is happening" — one sentence in plain words; "for example" — a concrete scenario. The place and size of the panel are the same on all slides, only the words change.
- **An example is a scene with a participant, an action and a number**, not a paraphrase of the definition. Bad: "resources are limited". Good: "the query "logs for a day" returned hundreds of kilobytes — more than the model can read, and the provider answers with an error".
- **Convert units into familiar ones:** tokens — into an approximate number of words, bytes — into "a day's log", hours of waiting — into "the engineer replies from a phone in the evening".
- **Show what would break without the mechanism.** One "naive variant" line (a repeated deploy, a provider failure) explains the value better than any praise.
- **Replace infrastructure jargon with what the viewer sees:** "pod" → "server", "cell" → "square". Identifiers and commands leave as they are, that is the proof.
- **One idea per slide.** If an example needs two sentences about different things, that is two slides.

## Numbers [Визуал]

- Numbers — only those verified by the team, and worded as what was actually verified: "N tests built" if the tests were not run but only built.
- Do not carry outdated figures from the README into the frame without checking them against the code.

## One source of text

- [Видео] On-screen text and the narrator's text — from one source. The title and the phrase under it are what is read aloud. Generate the narrator's file from the same list from which the slides are assembled, then they will not diverge.
- [Визуал] Translation — from one source. All strings are kept in pairs "original → translation", and both the page with a language switcher and the video in the other language are assembled from them. Code, commands, identifiers are not translated. Checking of meaning — by a table per chapter.
