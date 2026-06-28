---
name: intellij-plugin
description: >
  Build plugins for IntelliJ Platform–based IDEs (IntelliJ IDEA, Android Studio, PyCharm,
  WebStorm, GoLand, Rider, CLion, Fleet) using Kotlin and the IntelliJ Platform Gradle Plugin 2.x.
  Use this skill whenever the user is creating, scaffolding, debugging, or publishing an IntelliJ/IDEA
  plugin, writing plugin.xml, declaring extension points or actions, adding tool windows, settings,
  inspections, or services, configuring gradle.properties, running runIde/buildPlugin/verifyPlugin,
  signing a plugin, or publishing to the JetBrains Marketplace. Triggers on "IntelliJ plugin",
  "IDEA plugin", "plugin.xml", "IntelliJ Platform", "IntelliJ Platform SDK", "Gradle IntelliJ Plugin",
  "extension point", "runIde", "buildPlugin", "AnAction", "ToolWindowFactory", "Configurable",
  "plugin signing", or any request to extend or automate an IntelliJ-based IDE.
---

# IntelliJ Plugin Skill

Develop plugins for any IntelliJ Platform–based IDE with Kotlin, the IntelliJ Platform Gradle Plugin 2.x, and `plugin.xml` — from scaffolding through publishing to the JetBrains Marketplace.

> **Use Kotlin.** The IntelliJ Platform itself is written mostly in Kotlin, all new APIs target Kotlin first, and Java-only development is no longer supported. Target **JDK 21** on current platform builds.

## Core Concepts

The IntelliJ Platform is an application that hosts plugins. Understanding these building blocks prevents the most common mistakes:

- **Application** — the running IDE process; a singleton accessible via `ApplicationManager.getApplication()`. Never call read/write operations on it without the right threading model.
- **Project** — an open workspace; multiple Projects can exist at once. Code that holds project state must be per-project, not global.
- **Module** — a unit within a Project (a content root, SDK, dependencies).
- **Virtual File System (VFS)** — the platform's in-memory mirror of the physical file system. Always go through `VirtualFile`/`VfsUtil`, never `java.io.File`, for files the IDE manages.
- **PSI (Program Structure Interface)** — the syntax-tree layer over source files. `PsiFile`, `PsiElement`, `PsiClass` are how you inspect and modify code. PSI is language-aware (Java, Kotlin, XML, …).
- **Action** — a user-invoked command (menu item, toolbar button, shortcut) extending `AnAction`.
- **Service** — a managed singleton (`AppLevel`, `ProjectLevel`, `ModuleLevel`) obtained via `Service.getService(...)` / `project.getService(...)`. The lifecycle and threading rules are handled for you — prefer services over hand-rolled singletons.
- **Extension Point (EP)** — the platform's pluggability mechanism. Plugins contribute extensions to platform-defined EPs (`<extensions>`) or declare their own (`<extensionPoints>`) for other plugins to implement.

## Quick Start

Build a plugin in five steps. Detailed keys/tasks live in **[project_setup.md](references/project_setup.md)**.

### 1. Scaffold the project

Generate a project from the **JetBrains Platform Plugin Template** or the new-project wizard in IntelliJ IDEA (File → New → Project → **IDE Plugin**). The modern build is the **IntelliJ Platform Gradle Plugin 2.x** (`org.jetbrains.intellij.platform`) — *not* the legacy `org.jetbrains.intellij`.

### 2. Configure `gradle.properties`

```properties
# identity
pluginGroup       = com.example.myplugin
pluginName        = MyPlugin
pluginVersion     = 0.1.0

# target platform range (IDE major build numbers)
pluginSinceBuild  = 243
pluginUntilBuild  = 252.*

# platform to build against
platformType      = IC            # IC=IDEA Community, IU=Ultimate, PC=PyCharm, GO=GoLand, ...
platformVersion   = 2024.3
```

### 3. Author a minimal `plugin.xml`

`src/main/resources/META-INF/plugin.xml`:

```xml
<idea-plugin>
  <id>com.example.myplugin</id>
  <name>My Plugin</name>
  <vendor email="you@example.com" url="https://example.com">Example</vendor>
  <description><![CDATA[A short, Markdown-friendly description.]]></description>
  <change-notes><![CDATA[Initial release.]]></change-notes>

  <depends>com.intellij.modules.platform</depends>

  <extensions defaultExtensionNs="com.intellij">
    <!-- register your extensions here -->
  </extensions>
</idea-plugin>
```

Full tag reference and how to split config files: **[plugin_xml.md](references/plugin_xml.md)**.

### 4. Write your first Action

```kotlin
class HelloAction : AnAction("Say Hello") {
  override fun actionPerformed(e: AnActionEvent) {
    val project = e.project ?: return
    NotificationGroupManager.getInstance()
      .getNotificationGroup("Hello")
      .createNotification("Hello from MyPlugin!", NotificationType.INFORMATION)
      .notify(project)
  }
}
```

Register it in `plugin.xml`:

```xml
<actions>
  <action id="MyPlugin.Hello" class="com.example.myplugin.HelloAction"
          text="Say Hello" description="Greets the user">
    <add-to-group group-id="ToolsMenu" anchor="last"/>
    <keyboard-shortcut keymap="$default" first-keystroke="ctrl alt H"/>
  </action>
</actions>
```

More EPs (Tool Window, Settings, Inspection, Annotator, Line Marker): **[extensions_and_actions.md](references/extensions_and_actions.md)**.

### 5. Run it

```bash
./gradlew runIde            # launch a sandboxed IDE with the plugin loaded
./gradlew buildPlugin       # produce a distributable .zip in build/distributions
./gradlew verifyPlugin      # run the Plugin Verifier against target IDE builds
./gradlew test              # run unit/integration tests
```

## Project Structure

```
my-plugin/
├── build.gradle.kts
├── settings.gradle.kts
├── gradle.properties
├── src/
│   ├── main/
│   │   ├── kotlin/
│   │   │   └── com/example/myplugin/
│   │   │       ├── HelloAction.kt
│   │   │       └── MyToolWindowFactory.kt
│   │   └── resources/
│   │       ├── META-INF/
│   │       │   ├── plugin.xml            # main descriptor
│   │       │   └── plugin-[product].xml  # optional product-specific includes
│   │       ├── icons/
│   │       │   └── toolWindow.svg        # 13x13 SVG, current theme colors
│   │       └── inspectionDescriptions/
│   │           └── MyInspection.html
│   └── test/
│       └── kotlin/com/example/myplugin/
└── build/distributions/                  # output .zip from buildPlugin
```

## plugin.xml Essentials

| Tag | Purpose |
|-----|---------|
| `<id>` | Unique, reverse-DNS plugin id; must match `pluginGroup`/Gradle coordinates |
| `<name>` | Human-readable display name |
| `<vendor>` | `email`, `url`, plus name text |
| `<description>` | Markdown inside `CDATA`; shown on Marketplace |
| `<change-notes>` | Per-release notes |
| `<depends>` | Required module (e.g. `com.intellij.modules.platform`, `com.intellij.modules.java`) or optional dependency with `config-file` |
| `<idea-version>` | Optional; the Gradle plugin usually controls range via `pluginSinceBuild/UntilBuild` |
| `<extensions>` | Extensions contributed to platform/other plugins' EPs |
| `<extensionPoints>` | EPs this plugin exposes for others |
| `<applicationListeners>` / `<projectListeners>` | Topic listener registrations |
| `<actions>` | Action declarations and group placement |

## Testing

Use the IntelliJ Test Framework with light fixtures — no need to boot a full IDE.

```kotlin
class HelloActionTest : LightPlatformTestCase() {
  fun testActionShowsNotification() {
    val action = HelloAction()
    val e = TestActionEvent.createTestEvent { null }
    action.actionPerformed(e)
    // assert on notification/PSI/fixture state
  }
}
```

See **[testing.md](references/testing.md)** for `CodeInsightTestFixture` setup and PSI/VFS testing patterns.

## Publishing & Signing

Plugins uploaded to the JetBrains Marketplace (since the 2021.2 cycle) **must be signed**. The Gradle plugin handles signing if a certificate chain is provided.

- Sign a certificate chain, base64-encode it, and expose it (plus the private key) via environment variables read by `build.gradle.kts`.
- `./gradlew verifyPlugin` checks compatibility across your declared IDE build range.
- `./gradlew publishPlugin` uploads to Marketplace when `publishToken` is set.

Full flow and versioning rules: **[publishing.md](references/publishing.md)**.

## Best Practices

**DO**:
- Use Kotlin and target JDK 21 for current builds.
- Use the **IntelliJ Platform Gradle Plugin 2.x** (`org.jetbrains.intellij.platform`), not the legacy plugin.
- Keep `pluginUntilBuild` open-ended (`252.*`) unless you have tested compatibility boundaries.
- Interact with files through `VirtualFile`/VFS and code through PSI, never raw `java.io.File`.
- Use platform **services** for singletons; respect read/write-access threading rules.
- Register features via **extension points** rather than patching platform internals.
- Run `verifyPlugin` against the oldest build in your `sinceBuild` range before release.
- Provide 13×13 SVG icons using current-theme icon colors (`ColorPallete`, `IconLoader`).

**DON'T**:
- Reference internal/`@ApiStatus.Internal` APIs from the platform — they break without warning.
- Do heavy work on the EDT (Event Dispatch Thread); offload to background via `ProgressManager` / coroutines on a BGT.
- Hold long-lived references to `Project`/`PsiElement` in app-level state (causes leaks and stale data).
- Ship an unsigned plugin to Marketplace (it will be rejected).
- Hardcode absolute file paths — always resolve via `VirtualFile` and the project's base dir.
- Pin a single `platformVersion` older than what your `pluginSinceBuild` implies.

## Common Issues

| Issue | Solution |
|-------|----------|
| `ClassNotFoundException` / `NoClassDefFoundError` at runtime | A referenced class lives in a module you didn't `<depends>` on, or you used an `@Internal` API |
| Plugin not loaded in sandbox | Rebuild (`./gradlew runIde`) and check `idea.log` in the sandbox instance |
| `verifyPlugin` reports API breakages | Bump `pluginSinceBuild` or guard the call with `com.intellij.openapi.util.SystemInfo`/API checks |
| Notifications don't show | Register a `<notificationGroup>` extension; use `NotificationGroupManager` |
| Threading exception ("Access is allowed from event dispatch thread only") | Wrap PSI/file writes in `WriteCommandAction.runWriteCommandAction`; reads in a read action |
| Stale PSI after edit | Call `PsiDocumentManager.getInstance(project).commitDocument(doc)` before reading |
| Signing fails on upload | Ensure cert chain + private key env vars are set and base64-encoded |

## Knowledge References

- **IntelliJ Platform SDK**: official documentation at `plugins.jetbrains.com/docs/intellij`
- **IntelliJ Platform Gradle Plugin 2.x**: build system (`org.jetbrains.intellij.platform`)
- **Kotlin**: primary plugin language (JDK 21 baseline on current builds)
- **PSI**: program structure inspection and modification
- **JetBrains Marketplace**: distribution and signing

## References

- **[project_setup.md](references/project_setup.md)** — Gradle plugin 2.x setup, full `gradle.properties` keys, `build.gradle.kts` template, IDE version matrix, build/run tasks
- **[plugin_xml.md](references/plugin_xml.md)** — complete `plugin.xml` descriptor, depends/config-file, extensions/extensionPoints, listeners, actions, config splitting
- **[extensions_and_actions.md](references/extensions_and_actions.md)** — implementing common EPs with Kotlin: Action, Tool Window, Settings, Inspection, Annotator, Line Marker, Notification
- **[testing.md](references/testing.md)** — IntelliJ Test Framework, `CodeInsightTestFixture`, light test cases, manual `runIde` testing
- **[publishing.md](references/publishing.md)** — JetBrains Marketplace, plugin signing, `publishPlugin`/`verifyPlugin`, versioning & compatibility
