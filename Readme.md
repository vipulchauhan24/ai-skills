# AI Skills

A collection of Claude Code skills by Vipul Chauhan.

## Skills

| Skill                                                                                       | How to use it                                                                                                                                                                                                       |
| ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [design-system-builder](plugins/product-toolkit/README.md) | Ask Claude to "create a design system" and give it a product brief, screenshots, a brand palette, or a mix. It confirms a direction with you, then writes tokens, light and dark themes, component specs, and a contrast report. |
| [project-planner](project-planner/README.md)                                                 | Write a spec with `templates/spec-template.md`, then ask Claude to "plan this project" using that file. It asks about high-stakes decisions and splits the spec into phases that a coding agent builds one at a time.   |

## Installing

The design-system-builder skill is published in the product-toolkit Claude Code plugin. Add the marketplace and install it:

```text
/plugin marketplace add vipulchauhan24/ai-skills
/plugin install product-toolkit@vipul-ai-skills
```

Invoke the skill with `/product-toolkit:design-system-builder`, or let Claude pick it up from a matching prompt.

The project-planner skill reads `rules/` and `templates/` by relative path. Keep those folders next to `project-planner/` when you copy it. See its README for details.

## Repository Layout

| Path                   | Contents                                                       |
| ---------------------- | -------------------------------------------------------------- |
| `plugins/`             | Plugins published through the marketplace.                     |
| `project-planner/`     | The project planner skill.                                     |
| `rules/`               | Engineering and Markdown rules used by the project planner.    |
| `templates/`           | Templates used by the project planner, such as the spec format. |
| `.claude-plugin/`      | The marketplace manifest.                                      |

## License

MIT. See [LICENSE](LICENSE).
