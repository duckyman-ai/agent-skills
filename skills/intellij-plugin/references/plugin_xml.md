# Plugin Configuration File (`plugin.xml`)

`META-INF/plugin.xml` is the plugin descriptor — the manifest the platform reads to identify, load, and wire up your plugin. It lives at `src/main/resources/META-INF/plugin.xml`.

## Minimal descriptor

```xml
<idea-plugin>
  <id>com.example.myplugin</id>
  <name>My Plugin</name>
  <vendor email="you@example.com" url="https://example.com">Example Inc.</vendor>
  <description><![CDATA[
    <h3>My Plugin</h3>
    A short, Markdown/HTML-friendly description shown on Marketplace and in the plugin settings.
  ]]></description>
  <change-notes><![CDATA[<ul><li>Initial release.</li></ul>]]></change-notes>

  <depends>com.intellij.modules.platform</depends>

  <extensions defaultExtensionNs="com.intellij">
    <!-- extension registrations -->
  </extensions>
</idea-plugin>
```

## Required metadata

| Tag | Required | Notes |
|-----|----------|-------|
| `<id>` | yes | Reverse-DNS id; must be unique on Marketplace; stable forever (never rename) |
| `<name>` | yes | Human display name |
| `<vendor>` | yes | Attributes `email`, `url`, plus name text content |
| `<description>` | yes | HTML inside `CDATA`; max ~4096 chars; rendered on Marketplace |
| `<change-notes>` | recommended | Per-release notes, HTML inside `CDATA` |
| `<idea-version>` | optional | Usually controlled by the Gradle plugin via `sinceBuild`/`untilBuild`; omit unless hand-packaging |
| `<product-descriptor>` | optional | Required only for **paid** Marketplace plugins (release code + optional eap) |

## Dependencies: `<depends>`

A dependency declares that a platform module (or another plugin) must be present for your plugin to load. Every plugin must depend on at least the base module:

```xml
<depends>com.intellij.modules.platform</depends>
```

Common modules:

| Module id | Provides |
|-----------|----------|
| `com.intellij.modules.platform` | Base APIs — always required |
| `com.intellij.modules.java` | Java PSI, refactoring, Java language support |
| `com.intellij.modules.lang` | Core language / PSI infrastructure |
| `com.intellij.modules.python` | Python support (PyCharm) |
| `com.intellij.modules.androidstudio` | Android Studio-specific APIs |

### Optional dependencies

If your plugin can work without another plugin but *enhances* it when present, mark the dependency optional and load extra config from a separate file only when that plugin is available:

```xml
<depends optional="true" config-file="plugin-with-git.xml">Git4Idea</depends>
```

When `Git4Idea` is installed, the platform additionally loads `META-INF/plugin-with-git.xml` (a *partial* descriptor — only the additional `<extensions>`, `<actions>`, etc., no top-level `<id>`/`<name>`).

## Extensions: `<extensions>`

Extensions are how a plugin contributes to platform **extension points (EPs)**. Most features are registered this way.

```xml
<extensions defaultExtensionNs="com.intellij">
  <!-- the notification group used by the Hello Action -->
  <notificationGroup id="Hello" displayType="BALLOON"/>

  <!-- a tool window -->
  <toolWindow id="MyTool" anchor="right" factoryClass="com.example.myplugin.MyToolWindowFactory"/>

  <!-- an application service -->
  <applicationService serviceImplementation="com.example.myplugin.AppSettings"/>

  <!-- a project service -->
  <projectService serviceImplementation="com.example.myplugin.MyProjectService"/>

  <!-- a settings page -->
  <applicationConfigurable parentId="tools"
                           instance="com.example.myplugin.MyConfigurable"
                           id="com.example.myplugin.configurable"
                           displayName="My Plugin"/>
</extensions>
```

- `defaultExtensionNs="com.intellij"` → target platform EPs. Drop it and qualify with the namespace when contributing to a third-party plugin's EP.
- Each EP defines which attributes it accepts (`serviceImplementation`, `factoryClass`, `implementation`, `instance`, etc.). The EP name in the XML (`<notificationGroup>`, `<toolWindow>`, ...) **is** the EP id.

See **[extensions_and_actions.md](extensions_and_actions.md)** for worked Kotlin examples of each common EP.

## Declaring your own extension points: `<extensionPoints>`

Let other plugins extend yours:

```xml
<extensionPoints>
  <extensionPoint
      name="myFeature"
      beanClass="com.intellij.util.KeyedLazyInstanceEP"
      area="IDEA_PROJECT">
    <with attribute="implementationClass"
          implements="com.example.myplugin.MyFeature"/>
  </extensionPoint>
</extensionPoints>
```

Then read contributors at runtime via `MyFeature.EP_NAME.extensions` (declare `com.intellij.openapi.extensions.ExtensionPointName<T>("com.example.myplugin.myFeature")` in Kotlin).

## Listeners

Register topic listeners declaratively (preferred over manual `ApplicationManager.getApplication()` connection for stable topics):

```xml
<applicationListeners>
  <listener class="com.example.myplugin.MyAppListener"
            topic="com.intellij.openapi.application.ApplicationListener"/>
</applicationListeners>

<projectListeners>
  <listener class="com.example.myplugin.MyProjectListener"
            topic="com.intellij.openapi.project.ProjectManagerListener"/>
</projectListeners>
```

## Actions: `<actions>`

Declare user-invoked commands and where they appear:

```xml
<actions>
  <group id="MyPlugin.Group" text="My Plugin" popup="true">
    <add-to-group group-id="ToolsMenu" anchor="last"/>
    <action id="MyPlugin.Hello" class="com.example.myplugin.HelloAction"
            text="Say Hello" description="Greets the user">
      <keyboard-shortcut keymap="$default" first-keystroke="ctrl alt H"/>
    </action>
  </group>
</actions>
```

- `add-to-group` places the action into an existing menu/toolbar group (`ToolsMenu`, `MainMenu`, `EditorPopupMenu`, ...).
- Use `<group>` to nest and create submenus; `popup="true"` makes it a submenu.
- Multiple `<keyboard-shortcut>` entries let you bind per keymap.

## Config file splitting

Keep `plugin.xml` readable by moving optional/product-specific registrations into separate files and including them via optional `<depends config-file="...">` or `<xi:include>`:

```xml
<idea-plugin>
  ...required metadata...
  <depends>com.intellij.modules.platform</depends>

  <xi:include href="/META-INF/plugin-java.xml" xpointer="xpointer(/idea-plugin/*)"/>
</idea-plugin>
```

`plugin-java.xml` then contains only the inner elements (`<extensions>`, `<actions>`, ...), wrapped in its own `<idea-plugin>` root for XPointer traversal.

## Validation checklist

- `<id>` matches your Gradle `pluginGroup` coordinates and is globally unique.
- At least `<depends>com.intellij.modules.platform</depends>` is present.
- `<description>` and `<change-notes>` are inside `CDATA` and valid HTML.
- Every class referenced in `<extensions>`/`<actions>`/`<applicationListeners>` exists and is on the classpath.
- No reference to `@ApiStatus.Internal` APIs — they will break across versions.
