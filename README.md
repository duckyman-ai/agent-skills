# 🤖 Agent Skills

> Collection of reusable skills for AI agents. Each skill is a self-contained module with documentation and examples.

## ✨ Available Skills

### 🎯 [flutter-clean-arch](skills/flutter-clean-arch/SKILL.md)

Generate Flutter applications using Clean Architecture with feature-first structure, Riverpod state management, Dio + Retrofit networking, and fpdart error handling.

- 🏗️ Clean Architecture (Domain/Data/Presentation layers)
- 🎛️ Riverpod 3.0+ with code generation
- 🌐 Dio + Retrofit for type-safe REST API calls
- ⚡ Functional error handling with Either type
- 📁 Feature-first project organization

### 📝 [git-convention](skills/git-convention/SKILL.md)

Generate conventional git commit messages following Angular commit convention format.

- 📋 Angular commit message format
- ⚠️ Breaking change handling
- 📜 Automatic changelog support
- 🔧 Commit linting configuration

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