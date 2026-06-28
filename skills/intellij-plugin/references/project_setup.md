# Project Setup

How to scaffold, configure, and build an IntelliJ Platform plugin with the **IntelliJ Platform Gradle Plugin 2.x** (`org.jetbrains.intellij.platform`).

> The legacy `org.jetbrains.intellij` (1.x) plugin is deprecated for new projects. Use the 2.x plugin unless you have a specific reason not to.

## Scaffolding

Two supported paths:

1. **IDE wizard** — IntelliJ IDEA → File → New → Project → **IDE Plugin**. Generates Gradle (Kotlin DSL) + a sample `plugin.xml` + an Action.
2. **Platform Plugin Template** — JetBrains' GitHub template repo, kept in sync with the latest Gradle plugin and CI for verification/publishing.

Either way you end up with this layout:

```
my-plugin/
├── settings.gradle.kts
├── build.gradle.kts
├── gradle.properties
├── src/main/{kotlin,resources/META-INF/plugin.xml}
└── src/test/kotlin
```

## `build.gradle.kts`

```kotlin
plugins {
  id("java")
  id("org.jetbrains.kotlin.jvm") version "2.0.21"
  id("org.jetbrains.intellij.platform") version "2.2.0"
}

group = providers.gradleProperty("pluginGroup").get()
version = providers.gradleProperty("pluginVersion").get()

repositories {
  mavenCentral()
  intellijPlatform { defaultRepositories() }
}

dependencies {
  intellijPlatform {
    create(providers.gradleProperty("platformType"), providers.gradleProperty("platformVersion"))
    bundledPlugins(providers.gradleProperty("platformBundledPlugins").get().split(','))
    plugins(providers.gradleProperty("platformPlugins").get().split(','))
    pluginVerifier()
    zipSigner()
    testFramework(org.jetbrains.intellij.platform.gradle.TestFrameworkType.Platform)
  }
  testImplementation(kotlin("test"))
}

intellijPlatform {
  pluginConfiguration {
    name = providers.gradleProperty("pluginName")
    version = providers.gradleProperty("pluginVersion")
    ideaVersion {
      sinceBuild = providers.gradleProperty("pluginSinceBuild")
      untilBuild = provider { providers.gradleProperty("pluginUntilBuild").get() }
    }
  }
  signing {
    certificateChain = providers.environmentVariable("CERTIFICATE_CHAIN")
    privateKey = providers.environmentVariable("PRIVATE_KEY")
    password = providers.environmentVariable("PRIVATE_KEY_PASSWORD")
  }
  publishing {
    token = providers.environmentVariable("PUBLISH_TOKEN")
  }
  pluginVerification {
    ides {
      recommended()
    }
  }
}
```

## `gradle.properties` keys

| Key | Required | Example | Notes |
|-----|----------|---------|-------|
| `pluginGroup` | yes | `com.example.myplugin` | Maven group; matches plugin id prefix |
| `pluginName` | yes | `MyPlugin` | Display/distribution name |
| `pluginVersion` | yes | `0.1.0` | SemVer; bumped each release |
| `pluginSinceBuild` | yes | `243` | Oldest supported IDE build (2024.3 = 243) |
| `pluginUntilBuild` | yes | `252.*` | Upper bound; `.*` = open-ended to all builds of that branch |
| `platformType` | yes | `IC` | Build against this product: `IC` IDEA Community, `IU` Ultimate, `PC` PyCharm Community, `PY` PyCharm Pro, `GO` GoLand, `WS` WebStorm, `RD` Rider, `CL` CLion, `AI` Android Studio |
| `platformVersion` | yes | `2024.3` | Exact build version to compile/test against |
| `platformPlugins` | no | `` | Comma-separated 3rd-party plugins (with `@version`) to depend on at build time |
| `platformBundledPlugins` | no | `com.intellij.java,Git4Idea` | Comma-separated bundled plugin ids to depend on |

## IDE build numbers

The platform uses a `BRANCH.BUILD` scheme. The **branch** (first three digits, e.g. `243`) is what you put in `pluginSinceBuild`:

| Release | Branch | Example build |
|---------|--------|---------------|
| 2024.3 | 243 | 243.21565 |
| 2025.1 | 251 | 251.23774 |
| 2025.2 | 252 | 252.x |

Always look up the exact `platformVersion` on the [IntelliJ SDK builds page](https://plugins.jetbrains.com/docs/intellij/intellij-platform-artifacts-repositories.html) — never guess.

## Build & run tasks

| Task | What it does |
|------|--------------|
| `runIde` | Launches a sandboxed IDE instance with the current plugin loaded, against `platformVersion` |
| `buildPlugin` | Compiles and packages a distributable `.zip` into `build/distributions/` |
| `verifyPlugin` | Runs the Plugin Verifier against the IDE builds in `pluginVerification.ides`; reports missing/changed APIs |
| `signPlugin` | Signs the distribution `.zip` using the configured certificate chain |
| `publishPlugin` | Uploads the signed plugin to JetBrains Marketplace (needs `PUBLISH_TOKEN`) |
| `test` | Runs unit and integration tests via the IntelliJ Test Framework |
| `listProductsReleases` | Lists available IDE builds you can verify against |

### Compatibility rules

- Your compiled code is bound by the platform APIs available in **`platformVersion`** (the IDE you build against), not `pluginSinceBuild`.
- `pluginSinceBuild`/`pluginUntilBuild` only declare which **end-user IDE builds** may install the plugin; they don't add/remove APIs.
- The Plugin Verifier (`verifyPlugin`) is the source of truth for whether your plugin actually runs on a target build. Run it before every release.
- Keep `untilBuild` open (`252.*`) when you have no concrete reason to cap it — capping causes plugins to be disabled after IDE auto-updates until you publish a new version.

## Sandbox & logging

`runIde` runs against a throwaway sandbox (`~/.gradle/...` or under `build/idea-sandbox/`) so your real IDE config isn't touched. Find the sandbox instance's `idea.log` there when debugging load failures.

## JDK

- Build with **JDK 21** (the platform baseline for 2024.2+). Configure via Gradle toolchain or `org.gradle.java.home`.
- Set `javaVersion` in `kotlin { jvmToolchain(21) }` so the compiled bytecode matches the platform's expected version.
