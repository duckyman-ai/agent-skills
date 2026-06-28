# Testing IntelliJ Plugins

The platform ships an in-process test framework so you can assert against real PSI/VFS/project state without launching a full IDE.

## Dependency

Add the platform test framework via the Gradle plugin's DSL (see [project_setup.md](project_setup.md)):

```kotlin
dependencies {
  intellijPlatform {
    testFramework(org.jetbrains.intellij.platform.gradle.TestFrameworkType.Platform)
  }
}
```

For Java-language inspections/refactorings add `TestFrameworkType.Plugin.Java` as well.

## Light test cases (fast, no full project)

`LightPlatformTestCase` (and the more capable `CodeInsightFixtureTestCase` via a fixture) boots a minimal in-memory project. Use it for PSI, inspections, annotators, completion, and actions.

```kotlin
import com.intellij.testFramework.fixtures.CodeInsightTestFixture
import com.intellij.testFramework.fixtures.LightJavaCodeInsightFixtureTestCase

class HelloActionTest : LightJavaCodeInsightFixtureTestCase() {

  fun testActionDoesNotCrashWithNoSelection() {
    myFixture.configureByText("Main.java", "class Main { }")
    val action = HelloAction()
    val event = TestActionEvent.createTestEvent { null }
    // no exception = pass
    action.actionPerformed(event)
  }

  fun testInspectionFlagsBadName() {
    myFixture.configureByText("Main.java", "class <warning>TODO_BAD</warning> { }")
    myFixture.enableInspections(MyLocalInspection())
    myFixture.checkHighlighting(true, false, false)
  }
}
```

- `myFixture` (a `CodeInsightTestFixture`) is provided by `CodeInsightFixtureTestCase`. It exposes `configureByText`, `performCompletion`, `launchAction`, `checkResultByFile`, `findClass`, etc.
- The `<warning>` / `<info>` / `<error>` markers in the expected file drive `checkHighlighting`.

## Heavy tests (full project on disk)

When you need real files, facets, or an actual build (rare), extend `HeavyPlatformTestCase` / `CodeInsightFixtureTestCase` with `IdeaTestExecutionPolicy`. These spin up a fuller environment and are slower — prefer light tests.

## Testing actions directly

```kotlin
val e = TestActionEvent.createTestEvent { dataId ->
  when (dataId) {
    CommonDataKeys.PROJECT.name -> project
    CommonDataKeys.EDITOR.name  -> myFixture.editor
    CommonDataKeys.VIRTUAL_FILE.name -> myFixture.file.virtualFile
    else -> null
  }
}
assert(action.actionPerformedAndUpdateBeforeActionInTestMode(e)) { "action should be enabled" }
```

`update()` visibility is testable the same way.

## Manual testing with `runIde`

For anything visual (tool windows, settings UI, notification balloons, icons), nothing replaces the eye:

```bash
./gradlew runIde
```

This boots a sandboxed IDE instance with your plugin loaded against `platformVersion`. Iterate code → the sandbox reloads on next `runIde`. Inspect `idea.log` in the sandbox dir (`build/idea-sandbox/$platformVersion/log/idea.log`) when things don't load.

## What to test (checklist)

- **Actions** — enable/disable logic (`update()`), and the effect of `actionPerformed()` on PSI/documents/notifications.
- **Inspections / annotators** — `myFixture.checkHighlighting` with marker files.
- **Completion / refactoring** — `myFixture.completeBasic()` / `myFixture.testRename(...)` with before/after files.
- **Services / state** — instantiate the service, call `loadState`/`getState`, assert round-trip.
- **Persistence** — `PersistentStateComponent` XML via `SerializationTestUtil` patterns where available.

## Common pitfalls

| Symptom | Fix |
|---------|-----|
| `IllegalStateException: getProject() … test mode` | Extend a `…FixtureTestCase`, don't construct `Application` manually |
| Inspection not asserted | `myFixture.enableInspections(YourInspection())` before `checkHighlighting` |
| `update()` always disabled in test | Pass the relevant `CommonDataKeys` via `TestActionEvent` data context |
| Slow suite | Prefer `Light*TestCase`; keep heavy tests isolated |
| PSI edits not visible | `WriteCommandAction` wraps edits; `PsiDocumentManager.getInstance(project).commitAllDocuments()` before reading |
