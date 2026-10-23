# <Project Name> - PRD

<!--
How to use: replace every <placeholder> with a concrete answer. Delete a bullet or section that does not apply to the project, and add sections the project needs. Write "Not required" or "No" rather than leaving a line blank: an explicit answer tells the planner the decision is made. Link to references (screenshots, docs, repos) instead of describing them.
-->

## Overview

<One or two sentences: what is being built, who it is for, and the value it delivers.>

### Success criteria

- Primary audience: <who the product must serve first>
- Observable outcome that makes launch a success: <a measurable result, with a number and a timeframe>
- Non-goals: <what is explicitly out of scope>

## Requirements

### References and inspiration

- Reference: <product, site, repo, or design to take inspiration from> (<link>)
  - Taken from it: <the specific part to reuse, such as layout, flow, or behaviour> (<link or screenshot>)
- When a reference conflicts with <design system / standard / constraint>, the winner is: <name>

### Design system and UI

- Design system: <name and link, or "none">
  - How the project consumes it: <package / submodule / copied files / inspiration only>
  - What it provides: <tokens / components / both>
  - Version or commit to pin to: <tag or commit hash>
- Themes: <list of themes, or "single theme">
  - Default theme: <theme>
  - First-time visitor sees: <rule, such as following the OS preference>
  - Returning visitor sees: <rule, such as the saved choice>
  - Where the choice persists: <localStorage / cookie / server / none>
  - How a flash of the wrong theme on first load is avoided: <approach>
- Responsive targets: <breakpoints or devices that must work>

### Tech stack and platform

- Stack: <framework, language, rendering model (SSG / SSR / SPA), runtime>
- Measurable performance bar before launch: <metric and target, such as a Lighthouse score, Core Web Vitals, or p95 latency>
- Discoverability items required: <metadata / Open Graph / sitemap / canonical URLs / structured data, or "not applicable">
- Constraints: <mandated services, versions, licences, budget, or hosting limits>

### Content and data

- Where content or data comes from: <files in the repo / CMS / database / API / manual entry>
  - Required fields or schema: <field names, and which are required>
  - Behaviour when an entry violates the schema: <fail the build / skip / reject with an error>
  - URL structure or API routes: <list each route pattern>
  - In scope: <features to build, such as drafts, tags, search, images, pagination>
  - Out of scope: <features not to build>
- Volume at launch: <number of items>
  - Does the real content exist today? <yes / no>
  - If not, does launch wait for it? <yes / no>
  - Placeholder content: <what is used instead, and how it is kept out of production indexes or user-facing views>
- Placeholder data to replace later: <what, where it lives, and the format the manual edit targets>
  - What stops placeholders from shipping: <marker / launch gate / noindex / feature flag>
  - Owner and date for replacing them: <name and date, or "Not required">

### Pages, screens, and features

- Structure: <how the product is split, such as single page plus a separate section, or a list of screens>
- Ordered list of sections or screens: <name each one in display order, or "match <reference>">
- Primary user actions: <what a user must be able to do on each screen>
- How a user contacts the owner or gets help: <email / form / socials / chat>
  - Spam or abuse handling, if a form: <approach, or "not applicable">
- Source of truth for each content block: <file path or link, and the shape to follow>

### Delivery and operations

- Hosting and deploy: <platform and how a deploy is triggered>
  - Branch that maps to production: <branch name>
  - Checks that must pass before a push goes live: <build / lint / tests / link check / none>
  - Preview deploys and rollback approach: <approach, or "Not required">
- Domain, DNS, and canonical host: <domain, and www or apex>
- Environments and secrets: <list of environments and where secrets are stored, or "none">

## Cross-cutting

- Accessibility standard: <such as WCAG 2.2 AA, keyboard navigation, contrast in every theme, and who is responsible for each>
- Analytics: <tool and events, or "No">
- Privacy and consent: <cookie consent, data retention, and compliance needs, or "No">
- Security: <authentication, authorization, and data-handling requirements, or "Not applicable">
- Internationalization: <languages and locales, or "English only">
- Error and empty states: <404 page, offline state, or failure messages, with a link to a design or screenshot>
- Browser and device support: <minimum versions or platforms>
