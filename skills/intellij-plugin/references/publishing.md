# Publishing & Plugin Signing

How to release an IntelliJ plugin to the **JetBrains Marketplace** and the signing requirement that gates it.

## Prerequisites

- A JetBrains Account and a (free) **Marketplace** profile at `plugins.jetbrains.com`.
- A unique, stable plugin `<id>` — Marketplace ids are permanent; never rename one.
- `pluginSinceBuild`/`pluginUntilBuild` set (see [project_setup.md](project_setup.md)).

## Plugin Signing (required)

Since the 2021.2 release cycle, **every plugin uploaded to Marketplace must be cryptographically signed**. Unsigned plugins are rejected. Signing lets the IDE verify a plugin wasn't tampered with and was published by the claimed author.

### 1. Generate a certificate chain

The Marketplace portal can issue one for you (recommended): **Plugins → your plugin → Signing → Generate / Download certificate chain**. Store the returned:

- **Certificate chain** (PEM, base64-encoded into one string)
- **Private key** (PEM, base64-encoded)
- **Private key password** (if you set one)

Alternatively use a self-signed chain from your own CA, but Marketplace-issued is simplest.

### 2. Expose them via environment variables

```bash
export CERTIFICATE_CHAIN="MIICoz..."   # base64-encoded PEM chain
export PRIVATE_KEY="MIIEvQ..."         # base64-encoded PEM private key
export PRIVATE_KEY_PASSWORD=""         # optional
export PUBLISH_TOKEN="perm:xxxxx"      # Marketplace personal access token
```

Never commit these. Put them in CI secrets or a local env, not in `gradle.properties`.

### 3. Wire them into the Gradle plugin

```kotlin
intellijPlatform {
  signing {
    certificateChain = providers.environmentVariable("CERTIFICATE_CHAIN")
    privateKey       = providers.environmentVariable("PRIVATE_KEY")
    password         = providers.environmentVariable("PRIVATE_KEY_PASSWORD")
  }
  publishing {
    token = providers.environmentVariable("PUBLISH_TOKEN")
  }
}
```

## Verify before release

```bash
./gradlew verifyPlugin
```

Runs the **Plugin Verifier** against the IDE builds selected by `pluginVerification.ides` (e.g. `recommended()`). Reports:

- Missing classes/methods (your code uses APIs not in the target build)
- Overridden non-`@ApiStatus.OverrideOnly` APIs (overrides that aren't allowed)
- Internal API usage (`@ApiStatus.Internal`)

A clean verifier run is the strongest signal your plugin will load on the declared build range. Always run it before uploading.

## Build the distribution

```bash
./gradlew buildPlugin
```

Produces `build/distributions/<pluginName>-<version>.zip` — signed if signing env vars are present.

You can also publish to a local/preview channel without Marketplace:

```bash
./gradlew buildPlugin         # then drag the .zip into a real IDE via Settings → Plugins ⚙ → Install from Disk
```

## Upload to Marketplace

Two options:

1. **Manual** — Plugins → your plugin → Upload Version, choose the `.zip`.
2. **Automated** — `./gradlew publishPlugin` (uses `PUBLISH_TOKEN`). Optionally scope a release to a release channel:

   ```kotlin
   intellijPlatform {
     publishing { token = providers.environmentVariable("PUBLISH_TOKEN") }
     // optional: hidden/closed channel for staging
   }
   ```

   The `--channel=<name>` style of the legacy plugin maps to the `release` channel / visibility settings in the new plugin and Marketplace UI.

After upload, Marketplace runs its own verifier and shows compatibility per IDE build. Approval for first-time uploads is reviewed by JetBrains.

## Versioning & compatibility ranges

- **SemVer** for `pluginVersion` (e.g. `1.2.0`); bump on each release.
- `pluginSinceBuild` → oldest IDE build the plugin supports.
- `pluginUntilBuild` → `252.*` style = "all builds of branch 252 and not capped"; cap explicitly (`252.999`) only when you must.
- Releasing a hotfix for an old branch? Keep a separate git branch with an older `platformVersion` and a narrower range, and publish that version.

## Post-release checklist

- [ ] `verifyPlugin` green for every IDE build in range.
- [ ] `<change-notes>` updated for the new version.
- [ ] Distribution `.zip` is signed (`./gradlew signPlugin`).
- [ ] Compatibility range matches what the verifier actually validated.
- [ ] If a paid plugin: `<product-descriptor>` release code set and a trial configured.
