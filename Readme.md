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
/plugin marketplace add vipulchauhan24/ai-skills
/plugin install product-toolkit@vipul-ai-skills
/plugin update product-toolkit@vipul-ai-skills
/reload-plugins
```

Invoke the skills with `/product-toolkit:design-system-builder` and `/product-toolkit:project-planner`, or let Claude pick them up from a matching prompt.

## Repository Layout

| Path                   | Contents                                                       |
| ---------------------- | -------------------------------------------------------------- |
| `plugins/`             | Plugins published through the marketplace.                     |
| `.claude-plugin/`      | The marketplace manifest.                                      |

## License

MIT. See [LICENSE](LICENSE).
