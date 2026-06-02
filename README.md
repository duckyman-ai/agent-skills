# 🤖 Agent Skills

> Collection of reusable skills for AI agents. Each skill is a self-contained module with documentation and examples.

## ✨ Available Skills

### 🎬 [capcut-editor](skills/capcut-editor/SKILL.md)

Read, analyze, and create CapCut desktop (macOS) video editing projects programmatically.

- 📚 Read & analyze CapCut project files
- 🎬 Create new video projects programmatically
- ✨ Add video effects (zoom, blur, sparkle, etc.)
- 🎞️ Insert transitions between clips
- 🎨 Apply color grading with HSL presets
- 📝 Add text overlays with custom fonts

### 🎯 [flutter-clean-arch](skills/flutter-clean-arch/SKILL.md)

Build Flutter apps with Clean Architecture — feature-first structure, Riverpod 3.0+ state management, Dio + Retrofit networking, and fpdart functional error handling.

- 🏗️ Clean Architecture with Domain/Data/Presentation layers
- 🎛️ Riverpod 3.0+ state management with code generation
- 🔌 Dio + Retrofit for type-safe REST API calls
- ⚡ fpdart Either for functional error handling
- ❄️ Freezed for immutable data classes
- 🧪 Testing strategies across all layers

### 🎨 [design-md](skills/design-md/SKILL.md)

Create DESIGN.md files that define a project's visual identity as structured design tokens and human-readable guidance, based on the [Google Labs DESIGN.md spec](https://github.com/google-labs-code/design.md).

- 🎨 YAML design tokens (colors, typography, spacing, rounded)
- 📐 8 standard sections (Overview, Colors, Typography, Layout, Elevation, Shapes, Components, Do's & Don'ts)
- 🔗 Token references for DRY design systems
- 🔄 Compatible with Tailwind, Figma Variables, and CSS Custom Properties

### 📝 [git-convention](skills/git-convention/SKILL.md)

Write conventional git commit messages that are machine-readable, enable automatic changelog generation, and drive semantic versioning.

- 📋 Angular commit message format (`feat`, `fix`, `docs`, etc.)
- ⚠️ Breaking change handling (`!` notation and footer)
- 📜 Automatic changelog generation support
- 🔧 Commit linting tooling by ecosystem (JS, Python, Flutter, Go, etc.)

## 📂 Project Structure

```
agent-skills/
├── skills/
│   └── [skill-name]/
│       ├── SKILL.md           # Main skill documentation
│       └── references/        # Additional docs and examples
├── .gitignore
├── LICENSE
└── README.md
```

## 🚀 Usage

Each skill can be loaded individually by AI agents that support skill-based workflows. The `SKILL.md` file contains:

- 🏷️ Skill name and description
- 🔎 Trigger words for auto-loading
- 📖 Implementation patterns and code examples
- ✅ Best practices and common issues

## ➕ Adding New Skills

Create a new directory under `skills/` with:

1. **SKILL.md** - Main documentation with frontmatter:
   ```yaml
   ---
   name: skill-name
   description: Brief description of when to use this skill
   ---
   ```

2. **references/** (optional) - Additional documentation and examples

## 🤝 Contributing

Contributions welcome! Feel free to add new skills or improve existing ones.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-skill`)
3. Commit your changes (`git commit -m 'feat: add amazing skill'`)
4. Push to the branch (`git push origin feature/amazing-skill`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

Made with ❤️ for the AI community

[⬆ Back to Top](#-agent-skills)

</div>