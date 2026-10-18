# AI Skills

A collection of Claude Code skills by Vipul Chauhan.

## Skills

| Skill                                                                                       | How to use it                                                                                                                                                                                                       |
| ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [design-system-builder](plugins/product-toolkit/README.md) | Ask Claude to "create a design system" and give it a product brief, screenshots, a brand palette, or a mix. It confirms a direction with you, then writes tokens, light and dark themes, component specs, and a contrast report. |
| [project-planner](plugins/product-toolkit/skills/project-planner/README.md)                                                 | Write a spec with `skills/project-planner/templates/spec-template.md`, then ask Claude to "plan this project" using that file. It asks about high-stakes decisions and splits the spec into phases that a coding agent builds one at a time.   |

## Installing

The design-system-builder and project-planner skills are published in the product-toolkit Claude Code plugin. Add the marketplace and install it:

```text
claude plugin marketplace add vipulchauhan24/ai-skills
claude plugin install product-toolkit@vipul-ai-skills
claude plugin update product-toolkit@vipul-ai-skills
/reload-plugins
```

Invoke the skills with `/product-toolkit:design-system-builder` and `/product-toolkit:project-planner`, or let Claude pick them up from a matching prompt.

## Using the skills with other providers

Each skill is a folder with a `SKILL.md` (the open Agent Skills format) plus the files it references, so it is not tied to Claude. Always copy the whole folder, not just `SKILL.md`, because the skill reads sibling files by relative path (`rules/`, `templates/`, `references/`, `scripts/`). The skills live in `plugins/product-toolkit/skills/`.

```bash
git clone https://github.com/vipulchauhan24/ai-skills.git
cd ai-skills/plugins/product-toolkit/skills
```

### Gemini CLI

Install into your user skills (`~/.gemini/skills/`) or a single project (`.gemini/skills/`):

```bash
gemini skills install ./design-system-builder
gemini skills install ./project-planner

# or, for one project only
gemini skills install ./design-system-builder --scope workspace
```

Check they were found with `gemini skills list` (or `/skills list` inside a session), then ask for the task in plain words, such as "create a design system" or "plan this project". Gemini loads the skill when the prompt matches its description.

### OpenAI Codex

Copy the folders into a skills directory Codex scans. Use `~/.agents/skills/` for all projects, or `.agents/skills/` at the root of a repo to share them with that project:

```bash
mkdir -p ~/.agents/skills
cp -r design-system-builder project-planner ~/.agents/skills/
```

Restart Codex, then name the skill in your prompt or describe the task. Some Codex versions read `~/.codex/skills/` instead; if the skills do not show up, check the [Codex skills docs](https://developers.openai.com/codex/skills) for the current path.

### Other agents that support `SKILL.md`

Cursor, GitHub Copilot, opencode and similar tools load the same folder format from their own skills directory. Copy the two folders there; see each tool's docs for the path.

### Chat apps and APIs without skill support

ChatGPT, Gemini web, or a raw OpenAI or Gemini API call have no skills loader, so supply the files yourself:

1. Paste the contents of `SKILL.md` as the system prompt, custom instructions, or the first message.
2. Attach the files the skill points to:
   - project-planner: `rules/project-rules.md`, `rules/markdown-rules.md`, `templates/spec-template.md`
   - design-system-builder: `references/tokens.example.css`
3. Send your request (a spec to plan, or a brief, screenshots or palette to build from).

### What to expect outside Claude Code

- design-system-builder ends by running `python3 -I scripts/check_contrast.py design-system/tokens.css`. This needs an agent with shell access and Python. In a plain chat, run the script yourself on the generated `tokens.css`, or the contrast check is skipped.
- Screenshot mode needs a model that accepts image input.
- The `/product-toolkit:...` commands are Claude Code only. Elsewhere, trigger the skills with a prompt.

## Repository Layout

| Path                   | Contents                                                       |
| ---------------------- | -------------------------------------------------------------- |
| `plugins/`             | Plugins published through the marketplace.                     |
| `.claude-plugin/`      | The marketplace manifest.                                      |

## License

MIT. See [LICENSE](LICENSE).
