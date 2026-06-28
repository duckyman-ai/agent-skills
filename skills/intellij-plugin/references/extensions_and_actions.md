# Extensions & Actions

Worked Kotlin examples for the most common IntelliJ Platform extension points. For each: the Kotlin class to implement and the matching `plugin.xml` registration.

## Threading rules (read these first)

Most EP callbacks run on the **EDT** (Event Dispatch Thread). PSI/file mutations need a **write action**; reading PSI/files needs a **read action**. Never do long I/O on the EDT.

```kotlin
// read
ApplicationManager.getApplication().runReadAction { /* read PSI/VFS */ }

// write (also commits documents so PSI stays consistent)
WriteCommandAction.runWriteCommandAction(project) {
  // mutate PSI / files
}
```

---

## 1. Action (`AnAction`)

A user-invoked command — menu item, toolbar button, or shortcut.

```kotlin
class HelloAction : AnAction() {
  override fun actionPerformed(e: AnActionEvent) {
    val project = e.project ?: return
    NotificationGroupManager.getInstance()
      .getNotificationGroup("Hello")
      .createNotification("Hello!", NotificationType.INFORMATION)
      .notify(project)
  }

  // Optionally enable/disable visibility
  override fun update(e: AnActionEvent) {
    e.presentation.isEnabledAndVisible = e.project != null
  }
}
```

```xml
<actions>
  <action id="MyPlugin.Hello" class="com.example.myplugin.HelloAction"
          text="Say Hello" description="Greets the user">
    <add-to-group group-id="ToolsMenu" anchor="last"/>
    <keyboard-shortcut keymap="$default" first-keystroke="control alt H"/>
  </action>
</actions>
```

Prefer `AnAction` (constructor + `actionPerformed`). Use `update()` to gate visibility cheaply — heavy logic in `update()` freezes the UI.

---

## 2. Tool Window (`ToolWindowFactory`)

A dockable panel on the IDE edge.

```kotlin
class MyToolWindowFactory : ToolWindowFactory {
  override fun createToolWindowContent(project: Project, toolWindow: ToolWindow) {
    val panel = JBLabel("Hello from MyTool").apply { border = JBUI.Borders.empty(10) }
    val content = ContentFactory.getInstance()
      .createContent(panel, "Tab 1", false)
    toolWindow.contentManager.addContent(content)
  }
}
```

```xml
<extensions defaultExtensionNs="com.intellij">
  <toolWindow id="MyTool" anchor="right" icon="AllIcons.Toolwindows.ToolWindowProject"
              factoryClass="com.example.myplugin.MyToolWindowFactory"/>
</extensions>
```

`anchor` ∈ `left`, `right`, `bottom`.

---

## 3. Settings (`Configurable`)

A page under Settings/Preferences.

```kotlin
class MyConfigurable : Configurable {
  private val panel = JBPanel<JBPanel<*>>().apply {
    add(JBLabel("Some setting:"))
    add(JTextField())
  }

  override fun getDisplayName() = "My Plugin"
  override fun createComponent(): JComponent = panel
  override fun isModified() = false
  override fun apply() { /* persist via a service */ }
  override fun reset() { /* read from a service */ }
}
```

```xml
<extensions defaultExtensionNs="com.intellij">
  <applicationConfigurable
      parentId="tools"
      id="com.example.myplugin.configurable"
      instance="com.example.myplugin.MyConfigurable"
      displayName="My Plugin"/>
</extensions>
```

Pair it with an **application service** to persist state (`PersistentStateComponent`).

---

## 4. Services & persistent state

```kotlin
@Service(Service.Level.APP)
class AppSettings : PersistentStateComponent<AppSettings.State> {
  data class State(var greeting: String = "Hello")
  private var state = State()
  override fun getState() = state
  override fun loadState(s: State) { state = s }
}
```

```xml
<extensions defaultExtensionNs="com.intellij">
  <applicationService
      serviceImplementation="com.example.myplugin.AppSettings"/>
</extensions>
```

Access: `service<AppSettings>()` (Kotlin) or `ApplicationManager.getApplication().getService(AppSettings::class.java)`.

Use `@Service(Service.Level.PROJECT)` + `<projectService>` for project-scoped state.

---

## 5. Notifications

Register a group once, then post notifications:

```xml
<extensions defaultExtensionNs="com.intellij">
  <notificationGroup id="Hello" displayType="BALLOON"/>
</extensions>
```

```kotlin
NotificationGroupManager.getInstance()
  .getNotificationGroup("Hello")
  .createNotification("Title", "Body", NotificationType.INFORMATION)
  .notify(project)
```

`displayType` ∈ `BALLOON`, `NONE`, `STICKY_BALLOON`.

---

## 6. Inspection (code inspection)

A local inspection that highlights problems in the editor.

```kotlin
class MyLocalInspection : AbstractBaseJavaLocalInspectionTool() {
  override fun checkMethod(method: PsiMethod, manager: InspectionManager, isOnTheFly: Boolean): Array<ProblemDescriptor>? {
    // build ProblemDescriptors via manager.createProblemDescriptor(...)
    return null
  }
}
```

```xml
<extensions defaultExtensionNs="com.intellij">
  <localInspection language="JAVA"
                   displayName="My inspection"
                   groupPath="Java"
                   groupName="My Plugin"
                   enabledByDefault="true"
                   level="WARNING"
                   implementationClass="com.example.myplugin.MyLocalInspection"/>
</extensions>
```

Requires `<depends>com.intellij.modules.java</depends>`. Provide an HTML description file at `resources/inspectionDescriptions/MyInspection.html`.

---

## 7. Annotator (live in-editor analysis)

Faster than inspections for token-level highlighting across any language.

```kotlin
class MyAnnotator : Annotator {
  override fun annotate(element: PsiElement, holder: AnnotationHolder) {
    if (element !is PsiIdentifier) return
    if (element.text == "TODO_BAD") {
      holder.newAnnotation(HighlightSeverity.WARNING, "Don't use this name")
        .range(element.textRange)
        .create()
    }
  }
}
```

```xml
<extensions defaultExtensionNs="com.intellij">
  <annotator language="JAVA" implementationClass="com.example.myplugin.MyAnnotator"/>
</extensions>
```

---

## 8. Line marker provider

Gutter icons / actions tied to a line of code.

```kotlin
class MyLineMarkerProvider : RelatedItemLineMarkerProvider() {
  override fun collectNavigationMarkers(element: PsiElement, result: MutableCollection<in RelatedItemLineMarkerInfo<*>>) {
    if (element !is PsiMethod) return
    val marker = LineMarkerInfo(
      element, element.textRange, AllIcons.RunConfigurations.TestState.Run,
      { "Run ${element.name}" }, null, GutterIconRenderer.Alignment.RIGHT
    )
    result.add(marker)
  }
}
```

```xml
<extensions defaultExtensionNs="com.intellij">
  <codeInsight.lineMarkerProvider language="JAVA"
      implementationClass="com.example.myplugin.MyLineMarkerProvider"/>
</extensions>
```

---

## 9. Editor action (text editor command)

A command that operates on the active editor's selection/caret.

```kotlin
class UppercaseAction : AnAction() {
  override fun actionPerformed(e: AnActionEvent) {
    val editor = e.getData(CommonDataKeys.EDITOR) ?: return
    val doc = editor.document
    WriteCommandAction.runWriteCommandAction(e.project!!) {
      editor.selectionModel.run {
        if (hasSelection()) {
          doc.replaceString(selectionStart, selectionEnd,
            doc.getText(TextRange(selectionStart, selectionEnd)).uppercase())
        }
      }
    }
  }

  override fun update(e: AnActionEvent) {
    e.presentation.isEnabled = e.getData(CommonDataKeys.EDITOR)?.selectionModel?.hasSelection() == true
  }
}
```

Register via `<actions>` like any `AnAction`, typically adding to the editor popup menu:

```xml
<actions>
  <action id="MyPlugin.Uppercase" class="com.example.myplugin.UppercaseAction"
          text="Uppercase Selection">
    <add-to-group group-id="EditorPopupMenu" anchor="last"/>
  </action>
</actions>
```

---

## Reference: where each feature plugs in

| Feature | EP name | Class to implement |
|---------|---------|--------------------|
| Menu/toolbar command | (under `<actions>`) | `AnAction` |
| Dockable panel | `toolWindow` | `ToolWindowFactory` |
| Settings page | `applicationConfigurable` / `projectConfigurable` | `Configurable` |
| App/project state | `applicationService` / `projectService` | `PersistentStateComponent` |
| Notifications | `notificationGroup` | `NotificationGroupManager` (API, not a class) |
| Code inspection | `localInspection` | `LocalInspectionTool` / `AbstractBaseJavaLocalInspectionTool` |
| Live token highlight | `annotator` | `Annotator` |
| Gutter icon | `codeInsight.lineMarkerProvider` | `LineMarkerProvider` / `RelatedItemLineMarkerProvider` |

Browse the full list of platform extension points in the running IDE via the **Internal mode → "Extension Point Crawler"**, or in `plugin.xml` introspection docs.
