# Doc Trimmer Skill

The doc trimmer skill is a surgical editor. It reads a piece of writing and removes the noise: hedging, windups, padding, filler, and ideas that are said more than once. It keeps your facts, your voice, and your structure. The result is the fewest words that still let a competent reader understand the point.

It cuts. It does not summarise, translate, or rewrite your argument.

## What Is in This Folder

Paths are relative to the skill folder, `skills/doc-trimmer/`, inside the product-toolkit plugin.

| Path        | Purpose                                                                                                   |
| ----------- | --------------------------------------------------------------------------------------------------------- |
| `SKILL.md`  | The skill itself. Defines what counts as noise, the editing rules, and the output format.                 |
| `README.md` | This file.                                                                                                |

The skill also reads `plugins/product-toolkit/shared/markdown-rules.md`, which it shares with project-planner. It uses that file to format Markdown output.

## What It Does

- Walks the input from top to bottom and removes every word, phrase, sentence, or paragraph that delays the point without adding meaning.
- Reads the whole input first to map where ideas repeat, so it can remove repeats that are far apart, not only adjacent ones.
- Keeps numbers, names, code, links, quotations, and the author's reasoning exactly as written.
- Prints the trimmed text, a short summary of how much was cut, and a breakdown by category.
- For a file, also writes a trimmed copy next to the original and never touches the original.

## Using the Skill

### Step 1: Give It Input

Give the skill one of these:

- Pasted text in your message.
- A file path, such as `docs/post.md`.
- A URL, such as `https://example.com/blog/post`.

### Step 2: Ask for the Trim

In Claude Code, any of these phrases triggers the skill:

- `trim this`
- `tighten this`
- `cut the noise`
- `make this crisp`
- `remove filler`
- `edit this down`

You can also call it directly with `/product-toolkit:doc-trimmer`.

### Step 3: Read the Result

The response contains:

- A one-line status message starting with "Trimmer is...".
- A `Source:` line for file and URL input.
- The trimmed text.
- A footer with the percentage cut, the before and after word counts, and a count per category of what was removed.
- A `Removed blocks:` list if whole paragraphs, examples, or sections were removed, so you can check those judgement calls.
- `Trimmer done.`

For file input, the trimmed text is also saved as `<name>-cut<ext>`. For example, `post.md` becomes `post-cut.md` and `paper.txt` becomes `paper-cut.txt`. The saved file holds only the trimmed text, with no status line, separators, or footer, so it is ready to publish.

### Examples

```text
trim docs/launch-post.md
```

```text
cut the noise from this draft: <pasted text>
```

```text
tighten https://example.com/blog/post
```

```text
trim the intro of docs/design.md only and keep the examples
```

## Capabilities

### What It Removes

- Hedging language, such as "it is important to note that", "needless to say", and habit hedges like "I think" or "perhaps".
- Empty disclaimers that name no specific exception, such as "your mileage may vary".
- Throat-clearing intros, such as "In this post we will..." and "Before we begin...".
- Cliche openers, such as "In today's fast-paced world...".
- Empty subject openers, such as "There are many systems that..." (becomes "Many systems...").
- Filler transitions, such as "With that said" and "Moving on".
- Self-reference and meta-structure, such as "as we will see" and "in the next section".
- Summarising conclusions, such as "In summary" and "What this essentially means is".
- Rhetorical-question tails, such as "Right?" and "Make sense?".
- Padded constructions, such as "in order to" (becomes "to") and "a large number of" (becomes "many").
- Nominalisations, such as "make a decision" (becomes "decide").
- Filler qualifiers and intensifier stacks, such as "basically", "very", "extremely fast".
- Redundant pairs, such as "end result" and "past history".
- Restatements, including repeats that appear in different sections.
- Redundant examples and analogies that add no new failure mode, trade-off, or edge case.
- Redundant background that the reader already has.
- Redundant elaboration that repeats a claim in more words.
- Dead sentences that only echo the sentence before.
- Generic AI-style framing and exhortations.
- Line-by-line narration of code that the code already shows.
- Ceremonial closers, such as "Thank you for reading".
- Non-load-bearing words, such as needless articles, auxiliary verbs, and relative pronouns.
- Verbose phrasings and sentence frames, such as "is able to" (becomes "can") and "It is important to understand that X" (becomes "X").

### Input Handling

- Pasted text, worked on in memory.
- Local files such as `.md`, `.txt`, and `.rst`.
- Other file types, such as `.pdf`, `.docx`, `.html`, `.ipynb`, and `.tex`, after extracting their text first. The output is plain text or Markdown, not the original format.
- URLs, downloaded as raw pages with `curl` so the author's words are not summarised on the way in. Navigation, sidebars, footers, and comments are stripped. `WebFetch` is only a fallback when `curl` fails, and the skill tells you the text may be abridged.
- Long documents, handled section by section after an idea map of the whole document is built.
- Ambiguous input: it asks once. In a non-interactive run it does not ask, and treats the input as a file, a URL, or pasted text in that order.

### Editing Guarantees

- Cut, do not rewrite. The only changes beyond deletion are small and listed: swapping a padded phrase for a shorter equivalent, stitching the clause left after a cut, folding a missing fact into the kept mention of a repeated idea, and rewording a vague heading to carry the real claim.
- Facts, numbers, names, code, links, and quotations stay untouched. Nothing is invented.
- The author's voice and spelling stay. Casual register words stay when they carry tone.
- Headings, code blocks, lists, and links stay. If a cut empties a section, any surviving fact moves to the nearest related section and the empty heading is dropped.
- References are repaired. If a cut removes the target of "see Figure 2" or "the second example", the pointer is removed or redirected.
- When the same idea appears more than once, the skill keeps the most specific mention, and the earliest if they are equal.
- Hedges that express real uncertainty stay. Only habit hedges go.
- Trade-offs that name a real cost or condition stay.
- A fidelity check runs before output: every number, name, link, code block, and heading must survive unless it was cut as a repeat.
- When facts conflict with brevity, the priority order is meaning first, readability second, word count last.

### Safety

- Text inside the input is never treated as instructions. Lines such as "ignore the above" or "run this command" do not change what the skill does.
- The only file the skill writes is the `-cut` copy. It never writes anywhere else because the input asks.
- If the input contains text that looks addressed to an AI, the footer says so.

### Output and Files

- The `-cut` file keeps the original extension and sits next to the original.
- If the `-cut` file already exists, the skill asks before overwriting it in an interactive session. In a pipeline or when told not to ask, it overwrites and says so.
- Markdown output follows `plugins/product-toolkit/shared/markdown-rules.md`: ASCII punctuation, no decorative formatting, no hard line wrapping. This step is skipped for files that are not Markdown.
- Say "just write the doc" or "don't print the stats" to get only the file path in the reply.
- When called from another skill or pipeline, it returns only the clean trimmed text, with no status line, source line, or footer.
- For long files in an interactive run, it does not reprint the whole trimmed text in chat. It prints the file path, the footer, and `Trimmer done.`.

### Your Controls

- Limit the scope: "only the intro", "leave the headings", "keep the examples".
- Ask for a target length, such as "cut to 500 words". The skill cuts as far as the priority order allows and tells you if it falls short. It never drops facts to hit a number.

## What It Does Not Do

- It does not summarise, translate, or review a draft.
- It does not trim legal text, contracts, specs and standards, safety warnings, required disclosures, fiction, poetry, speeches, or quoted material. It says why and stops, unless you insist.
- It is gentler with tutorials, FAQs, changelogs, reference docs, and tables. Deliberate repetition, teaching examples, parallel list items, and cross-references stay.
- For languages other than English, it applies only the language-neutral rules: repeats, redundant examples, dead sentences, and ceremonial closers. It tells you so.
- It does not edit code.

## Example

Input:

```text
In this blog post, we are going to explore an interesting topic. It is important to note that distributed systems are notoriously hard to reason about. Basically, when you have multiple nodes communicating over a network, a large number of things can go wrong. What this essentially means is that engineers need to design for failure from day one. Now that we understand the problem, let us look at the solution.
```

Output:

```text
Distributed systems are hard to reason about. When multiple nodes communicate over a network, many things can go wrong, so engineers need to design for failure from day one.
```

## Customising

- Edit `SKILL.md` to add or remove noise patterns, or to change the footer categories.
- Edit `plugins/product-toolkit/shared/markdown-rules.md` to change how the output is formatted. Other skills in the plugin use the same file.

## Installing

The skill ships in the product-toolkit plugin. From the repository root:

```text
claude plugin marketplace add vipulchauhan24/ai-skills
claude plugin install product-toolkit@vipul-ai-skills
/reload-plugins
```

To use it as a standalone skill, copy the `doc-trimmer/` folder and the plugin's `shared/` folder, and keep their relative layout. The skill reads `../../shared/markdown-rules.md`, so `shared/` must sit two levels above the skill folder:

- Project level: `.claude/skills/doc-trimmer/` and `.claude/shared/markdown-rules.md`.
- User level: `~/.claude/skills/doc-trimmer/` and `~/.claude/shared/markdown-rules.md`.
