---
name: design-md
description: >
  Create and maintain DESIGN.md files that define a visual identity and design system
  for software projects. Use this skill when the user asks to create a DESIGN.md,
  set up a design system document, define brand colors/typography/spacing as code,
  generate design tokens, or establish visual identity guidelines for a project.
  Also use when the user mentions "design system", "design tokens", "visual identity",
  "brand guidelines", "DESIGN.md", or wants to document their app's look and feel
  in a machine-readable format that AI agents can follow.
---

# DESIGN.md Skill

Create self-contained DESIGN.md files that define a project's visual identity as structured design tokens and human-readable guidance. Based on the [DESIGN.md spec](https://github.com/google-labs-code/design.md/blob/main/docs/spec.md) by Google Labs.

## What is DESIGN.md

A plain-text design system document that serves as a living source of truth for both humans and AI agents. It contains:

- **YAML frontmatter** — machine-readable design tokens (colors, typography, spacing, etc.)
- **Markdown body** — human-readable design rationale and usage guidance

## File Structure

```markdown
---
version: alpha
name: <Design System Name>
colors:
  primary: "#..."
  secondary: "#..."
typography:
  h1:
    fontFamily: ...
    fontSize: ...
    fontWeight: ...
    lineHeight: ...
    letterSpacing: ...
spacing:
  base: ...
  sm: ...
  md: ...
  lg: ...
rounded:
  sm: ...
  md: ...
  full: ...
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "#..."
    rounded: "{rounded.md}"
---

# Design System Name

## Overview
...

## Colors
...

## Typography
...

## Layout
...

## Elevation & Depth
...

## Shapes
...

## Components
...

## Do's and Don'ts
...
```

## Frontmatter Schema

### Top-level

```yaml
version: <string>          # optional, current version: "alpha"
name: <string>             # required, name of the design system
description: <string>      # optional
colors:                    # map<string, Color>
  <token-name>: <Color>
typography:                # map<string, Typography>
  <token-name>: <Typography>
rounded:                   # map<string, Dimension>
  <scale-level>: <Dimension>
spacing:                   # map<string, Dimension | number>
  <scale-level>: <Dimension | number>
components:                # map<string, map<string, string>>
  <component-name>:
    <token-name>: <string | token reference>
```

### Types

**Color**: Hex string starting with `#` in SRGB (e.g., `"#1A1C1E"`, `"#F7F5F280"`).

**Typography**:

```yaml
fontFamily: <string>           # e.g., "Inter", "Public Sans"
fontSize: <Dimension>          # e.g., "48px", "2rem"
fontWeight: <number>           # e.g., 400, 600, 700
lineHeight: <Dimension | number>  # e.g., "24px", 1.6
letterSpacing: <Dimension>     # e.g., "-0.02em", "0.1em"
fontFeature: <string>          # optional, font-feature-settings
fontVariation: <string>        # optional, font-variation-settings
```

**Dimension**: String with unit suffix. Valid units: `px`, `em`, `rem`.

**Token Reference**: Wrapped in curly braces pointing to another token. Example: `{colors.primary}`, `{typography.body-md}`, `{rounded.md}`.

## Sections

Sections appear in this order. Omit sections that are not relevant to the project.

### 1. Overview (also "Brand & Style")

Holistic description of the product's look and feel. Defines brand personality, target audience, and the emotional response the UI should evoke. Guides the agent's high-level stylistic decisions when a specific rule isn't explicitly defined.

```markdown
## Overview

Minimalist fintech dashboard targeting professional traders. The design conveys
trust, precision, and clarity through a dark theme with high-contrast data
elements and restrained use of accent color.
```

### 2. Colors

Defines color palettes and their semantic roles. At minimum `primary` must be defined.

```markdown
## Colors

A dark theme with high-contrast accents for maximum readability of financial data.

- **Primary (#0A0E17):** Deep navy background evoking institutional trust.
- **Secondary (#1A1F2E):** Elevated surface color for cards and panels.
- **Accent (#3B82F6):** Electric blue used exclusively for interactive elements and CTAs.
- **Success (#10B981):** Green for positive financial indicators.
- **Danger (#EF4444):** Red for negative indicators and destructive actions.
- **Neutral (#94A3B8):** Muted slate for secondary text and borders.
```

### 3. Typography

Defines typography levels with semantic roles. Most systems have 9-15 levels.

Common naming: `headline-display`, `headline-lg`, `headline-md`, `body-lg`, `body-md`, `body-sm`, `label-lg`, `label-md`, `label-sm`, `caption`.

```markdown
## Typography

Uses **Inter** exclusively for a clean, modern feel. Weight variation creates hierarchy.

- **Headlines:** Semi-Bold (600) for section titles and key metrics.
- **Body:** Regular (400) at 16px for content and descriptions.
- **Labels:** Medium (500) at 12px with uppercase tracking for metadata and tags.
```

### 4. Layout (also "Layout & Spacing")

Describes grid system, spacing scale, and responsive behavior.

```markdown
## Layout

12-column grid on desktop, 4-column on mobile. Max content width 1280px.
8px base spacing scale with 4px half-step for micro-adjustments.
Cards use 24px internal padding. 32px gap between major sections.
```

### 5. Elevation & Depth

How visual hierarchy is conveyed — shadows, tonal layers, or flat alternatives.

```markdown
## Elevation & Depth

Depth through tonal layers rather than shadows. Each elevation level darkens
the background by one shade. No box-shadow used anywhere in the system.
```

### 6. Shapes

Border radius and shape language for UI elements.

```markdown
## Shapes

Minimal corner radius throughout. 4px for inputs and small elements,
8px for cards and modals, full (9999px) for pills and avatars.
```

### 7. Components

Style guidance for component atoms. Common types: buttons, chips, lists, tooltips, checkboxes, radio buttons, input fields.

Components can have variants for states (hover, active, disabled) using related keys:

```yaml
components:
  button-primary:
    backgroundColor: "{colors.accent}"
    textColor: "#FFFFFF"
    rounded: "{rounded.md}"
    padding: "12px 24px"
  button-primary-hover:
    backgroundColor: "#2563EB"
  button-primary-active:
    backgroundColor: "#1D4ED8"
```

Component property tokens: `backgroundColor`, `textColor`, `typography`, `rounded`, `padding`, `size`, `height`, `width`.

### 8. Do's and Don'ts

Practical guardrails.

```markdown
## Do's and Don'ts

- Do use accent color only for the primary action per screen
- Do maintain WCAG AA contrast (4.5:1 for normal text, 3:1 for large text)
- Don't use more than two font weights on a single screen
- Don't mix rounded and sharp corners in the same component group
- Don't use pure black (#000) or pure white (#FFF) in dark theme — use tinted values instead
```

## Recommended Token Names

These are commonly used but not required:

- **Colors:** `primary`, `secondary`, `tertiary`, `neutral`, `surface`, `on-surface`, `error`
- **Typography:** `headline-display`, `headline-lg`, `headline-md`, `body-lg`, `body-md`, `body-sm`, `label-lg`, `label-md`, `label-sm`
- **Rounded:** `none`, `sm`, `md`, `lg`, `xl`, `full`

## How to Create a DESIGN.md

When asked to create a DESIGN.md:

1. **Gather requirements** — ask about brand personality, target audience, color preferences, and any existing brand assets
2. **Choose a name** — pick a descriptive name for the design system
3. **Define tokens** — start with colors and typography, then spacing, rounded, and components
4. **Write prose sections** — explain the rationale behind each design decision
5. **Add Do's and Don'ts** — provide practical guardrails for consistent implementation
6. **Validate** — ensure all token references resolve, hex colors are valid, and dimensions have units

## Conversion Tips

DESIGN.md tokens are compatible with:

- **Tailwind** — map tokens to `tailwind.config.js` theme values
- **Figma Variables** — export/import via Figma's variable system
- **tokens.json** — convert to Design Token JSON spec format
- **CSS Custom Properties** — generate `:root` variables from tokens

## Complete Example

```markdown
---
version: alpha
name: Daylight Prestige
colors:
  primary: "#1A1C1E"
  secondary: "#6C7278"
  tertiary: "#B8422E"
  neutral: "#F7F5F2"
  surface: "#FFFFFF"
  on-surface: "#1A1C1E"
typography:
  h1:
    fontFamily: Public Sans
    fontSize: 48px
    fontWeight: 600
    lineHeight: 1.1
    letterSpacing: -0.02em
  h2:
    fontFamily: Public Sans
    fontSize: 36px
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: -0.01em
  body-md:
    fontFamily: Public Sans
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.6
  label-caps:
    fontFamily: Space Grotesk
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1
    letterSpacing: 0.1em
spacing:
  base: 16px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 32px
  xl: 64px
  gutter: 24px
  margin: 32px
rounded:
  sm: 4px
  md: 8px
  lg: 12px
  full: 9999px
components:
  button-primary:
    backgroundColor: "{colors.tertiary}"
    textColor: "#FFFFFF"
    rounded: "{rounded.md}"
    padding: 12px 24px
  button-primary-hover:
    backgroundColor: "#9A3726"
  button-secondary:
    backgroundColor: "transparent"
    textColor: "{colors.primary}"
    rounded: "{rounded.md}"
    padding: 12px 24px
---

# Daylight Prestige

## Overview

A refined editorial design system for a luxury lifestyle publication.
The aesthetic balances warmth and sophistication through high-contrast
neutrals paired with a single evocative accent. Every element is crafted
to feel intentional, readable, and quietly confident.

## Colors

The palette is rooted in high-contrast neutrals and a single, evocative accent color.

- **Primary (#1A1C1E):** A deep ink for headlines and core text — maximum
  readability with a sense of permanence.
- **Secondary (#6C7278):** A sophisticated slate for borders, captions, and metadata.
- **Tertiary (#B8422E):** A vibrant earthy red — used exclusively for primary
  actions and critical highlights.
- **Neutral (#F7F5F2):** A warm limestone foundation for all pages, softer than
  pure white.

## Typography

Two typefaces create a clear voice hierarchy.

- **Headlines:** Public Sans Semi-Bold establishes an institutional, trustworthy voice.
- **Body:** Public Sans Regular at 16px ensures contemporary professionalism
  and long-form readability.
- **Labels:** Space Grotesk in uppercase with generous tracking for technical
  data, timestamps, and metadata.

## Layout

Fluid grid on mobile, fixed max-width (1200px) on desktop. 8px spacing scale
with 4px half-step for micro-adjustments. Cards use 24px internal padding
to emphasize the soft, approachable nature of the brand.

## Elevation & Depth

Depth through tonal layers — not shadows. Background uses warm off-white,
primary content sits on pure white cards. Subtle but clear visual hierarchy.

## Shapes

Architectural sharpness: 4px corner radius on interactive elements, containers,
and inputs. Modern but rigid, engineered aesthetic.

## Components

### Buttons

Primary buttons use the tertiary red on white text. Secondary buttons are
outlined with transparent backgrounds. Both share 8px radius and consistent
horizontal padding.

### Cards

White surface on neutral background. 12px radius. 24px internal padding.
No border — elevation is achieved through color contrast alone.

## Do's and Don'ts

- Do use the tertiary color only for the single most important action per screen
- Do maintain WCAG AA contrast ratios (4.5:1 for normal text)
- Don't mix rounded and sharp corners in the same view
- Don't use more than two font weights on a single screen
- Don't introduce colors outside the defined palette
```

## Auto-Loading DESIGN.md

Claude Code reads **CLAUDE.md** automatically at the start of every session, but does **not** automatically read DESIGN.md. To ensure the agent always applies the design system, add an instruction in the project's CLAUDE.md:

```markdown
# CLAUDE.md
Always read and follow DESIGN.md before making any UI or styling changes.
```

Without this, DESIGN.md is only read when the user explicitly asks or when the design-md skill is triggered.

## Spec Reference

Full specification: https://github.com/google-labs-code/design.md/blob/main/docs/spec.md
