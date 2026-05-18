# Riverpod 3.0+ & Freezed 3.0+ Migration Guide

Detailed before/after reference for projects upgrading or AI-generated code that uses outdated patterns.

Read this file when encountering errors related to `XxxRef`, missing `sealed` keyword, or `.map()`/`.when()` not found.

## Riverpod 2.x → 3.0+

### Unified `Ref` Type

`XxxRef` types removed in favor of unified `Ref`:

```dart
// Riverpod 2.x (OUTDATED)
@riverpod
SomeType someType(SomeTypeRef ref) { ... }

// Riverpod 3.x+
@riverpod
SomeType someType(Ref ref) { ... }
```

All provider-generated Ref types (`DioRef`, `UserRepositoryRef`, etc.) are replaced by `Ref`.

## Freezed 2.x → 3.0+

### 1. Required `sealed` / `abstract` Keyword

| Class Type | Freezed 2.x | Freezed 3.0+ |
|------------|-------------|--------------|
| Single constructor | `class Person` | `abstract class Person` |
| Union type | `class Result` | `sealed class Result` |

Single constructor:

```dart
// Freezed 2.x (OUTDATED)
@freezed
class Person with _$Person {
  const factory Person({
    required String firstName,
    required String lastName,
  }) = _Person;
}

// Freezed 3.0+
@freezed
abstract class Person with _$Person {
  const factory Person({
    required String firstName,
    required String lastName,
  }) = _Person;
}
```

Union type:

```dart
// Freezed 2.x (OUTDATED)
@freezed
class Result with _$Result {
  const factory Result.success(String data) = Success;
  const factory Result.error(String message) = Error;
}

// Freezed 3.0+
@freezed
sealed class Result with _$Result {
  const factory Result.success(String data) = Success;
  const factory Result.error(String message) = Error;
}
```

### 2. Pattern Matching (`.map` / `.when` Removed)

Freezed 3.0+ no longer generates `.map`/`.when` extensions. Use Dart 3's native pattern matching:

```dart
// Freezed 2.x (OUTDATED)
final res = model.map(
  first: (value) => 'first ${value.a}',
  second: (value) => 'second ${value.b} ${value.c}',
);

// Freezed 3.0+
final res = switch (model) {
  First(:final a) => 'first $a',
  Second(:final b, :final c) => 'second $b $c',
};
```

## Required Versions

- Dart 3.3+
- Riverpod 3.0+
- Freezed 3.0+

Check with: `flutter pub deps | grep -E 'riverpod|freezed'`