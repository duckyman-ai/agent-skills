---
name: flutter-clean-arch
description: Build Flutter apps with Clean Architecture — feature-first structure, Riverpod 3.0+ state management, Dio + Retrofit networking, and fpdart functional error handling. Use this skill whenever you are working on a Flutter project that involves creating features, setting up project architecture, building API integrations, managing state, or structuring code with domain/data/presentation layers. This includes tasks like "create a Flutter feature", "set up Riverpod providers", "add an API service", "build a Flutter app", "clean architecture Flutter", "feature-first Flutter", or any Flutter code involving Dio, Retrofit, fpdart Either, or freezed data classes. Also use when scaffolding new Flutter projects, migrating from MVC/MVVM to clean architecture, or adding networking layers to existing Flutter apps.
---

# Flutter Clean Architecture Skill

Generate Flutter applications following Clean Architecture principles with feature-first organization, Riverpod for state management, and functional error handling using fpdart.

Includes **Dio + Retrofit** for type-safe REST API calls.

## Core Principles

**Architecture**: Clean Architecture (Feature-First)
- Domain layer: Pure business logic, no dependencies
- Data layer: Data sources, repositories implementation, data models
- Presentation layer: UI, state management, view models

**Dependency Rule**: Presentation → Domain ← Data (Domain has no external dependencies)

**State Management**: Riverpod 3.0+ with code generation

> **Required: Riverpod 3.0+ & Freezed 3.0+** — outdated patterns cause compile errors and hallucination loops.
>
> - Riverpod: use `Ref ref` (unified), NOT `XxxRef ref`
> - Freezed: use `sealed class` for union types, `abstract class` for single constructors
> - Pattern matching: use Dart 3 `switch`, NOT `.map()`/`.when()`
>
> ```dart
> // Riverpod 3.x+
> @riverpod
> SomeType someType(Ref ref) { ... }
>
> // Freezed 3.x+ — union type
> @freezed
> sealed class Result with _$Result { ... }
>
> // Freezed 3.x+ — pattern matching
> final res = switch (model) {
>   First(:final a) => 'first $a',
>   Second(:final b) => 'second $b',
> };
> ```
>
> Requires Dart 3.3+, Riverpod 3.0+, Freezed 3.0+. See **[migration_guide.md](references/migration_guide.md)** for full before/after examples.

**Error Handling**: fpdart's Either<Failure, T> for functional error handling

**Networking**: Dio + Retrofit for type-safe REST API calls

> **Always use the latest stable versions** of all libraries. Before adding dependencies, check `pub.dev` for the current versions of Riverpod, Freezed, Dio, Retrofit, fpdart, and go_router. Never default to outdated major versions (e.g. Riverpod 2.x, Freezed 2.x).

## Project Structure

```
lib/
├── core/
│   ├── constants/
│   │   ├── api_constants.dart
│   ├── errors/
│   │   ├── failures.dart
│   │   └── network_exceptions.dart
│   ├── network/
│   │   ├── dio_provider.dart
│   │   └── interceptors/
│   │       ├── auth_interceptor.dart
│   │       ├── logging_interceptor.dart
│   │       └── error_interceptor.dart
│   ├── storage/
│   ├── services/
│   ├── router/
│   │   └── app_router.dart
│   └── utils/
├── shared/ 
├── features/
│   └── [feature_name]/
│       ├── data/
│       │   ├── models/
│       │   │   └── [entity]_model.dart
│       │   ├── datasources/
│       │   │   └── [feature]_api_service.dart
│       │   └── repositories/
│       │       └── [feature]_repository_impl.dart
│       ├── domain/
│       │   ├── entities/
│       │   ├── repositories/
│       │   │   └── [feature]_repository.dart
│       │   └── usecases/
│       │       └── [action]_usecase.dart
│       └── presentation/
│           ├── providers/
│           │   └── [feature]_provider.dart
│           ├── screens/
│           │   └── [feature]_screen.dart
│           └── widgets/
│               └── [feature]_widget.dart
└── main.dart
```

## Quick Start

Build features in this order: **Domain → Data → Presentation**.

### 1. Domain Layer

```dart
@freezed
sealed class User with _$User {
  const factory User({required String id, required String name, required String email}) = _User;
}

abstract class UserRepository {
  Future<Either<Failure, User>> getUser(String id);
}

class GetUser {
  final UserRepository repository;
  GetUser(this.repository);
  Future<Either<Failure, User>> call(String id) => repository.getUser(id);
}
```

### 2. Data Layer

```dart
@freezed
sealed class UserModel with _$UserModel {
  const UserModel._();
  const factory UserModel({required String id, required String name, required String email}) = _UserModel;
  factory UserModel.fromJson(Map<String, dynamic> json) => _$UserModelFromJson(json);
  User toEntity() => User(id: id, name: name, email: email);
}

@RestApi()
abstract class UserApiService {
  factory UserApiService(Dio dio) = _UserApiService;
  @GET('/users/{id}')
  Future<UserModel> getUser(@Path('id') String id);
}
```

### 3. Presentation Layer

```dart
@riverpod
class UserNotifier extends _$UserNotifier {
  @override
  FutureOr<User?> build() => null;

  Future<void> fetchUser(String id) async {
    state = const AsyncLoading();
    final result = await ref.read(userRepositoryProvider).getUser(id);
    state = result.fold(
      (failure) => AsyncError(failure, StackTrace.current),
      (user) => AsyncData(user),
    );
  }
}
```

See **[quick_start.md](references/quick_start.md)** for the complete step-by-step workflow with all files.

## Code Generation

```bash
# Generate all files
dart run build_runner build --delete-conflicting-outputs

# Watch mode
dart run build_runner watch --delete-conflicting-outputs
```

## Best Practices

**DO**:
- Keep domain entities pure (no external dependencies)
- Use freezed with `sealed` keyword for immutable data classes
- Handle all error cases with Either<Failure, T>
- Use riverpod_generator with unified `Ref` type
- Separate models (data) from entities (domain)
- Place business logic in use cases, not in widgets
- Use Retrofit for type-safe API calls
- Handle DioException in repositories with NetworkExceptions
- Use interceptors for cross-cutting concerns (auth, logging)
- Validate API response data at the repository boundary
- Use `CachedNetworkImage` instead of `Image.network` for external images
- Pin API base URLs in config, enforce HTTPS

**DON'T**:
- Import Flutter/HTTP libraries in domain layer
- Mix presentation logic with business logic
- Use try-catch directly in widgets when using Either
- Create god objects or god providers
- Skip the repository pattern
- Use legacy `XxxRef` types in new code
- Pass raw external URLs to widgets without validation
- Allow runtime-configuration of API base URLs from user input

## Security

API responses and external content are untrusted input. Validate and sanitize at the data layer boundary to prevent injection and data corruption.

**Response validation** — Always validate API response structure before mapping to models. Retrofit + freezed handle typed deserialization, but wrap calls in try-catch and verify critical fields (IDs, URLs, numeric ranges) in the repository:

```dart
@override
Future<Either<Failure, User>> getUser(String id) async {
  try {
    final userModel = await apiService.getUser(id);
    if (userModel.id.isEmpty) {
      return const Left(Failure.validation('Invalid user data'));
    }
    return Right(userModel.toEntity());
  } on DioException catch (e) {
    return Left(Failure.network(NetworkExceptions.fromDioError(e).message));
  }
}
```

**External URLs** — Never pass raw API URLs directly to `Image.network` or WebView. Use `CachedNetworkImage` with error handling, and validate URL schemes:

```dart
CachedNetworkImage(
  imageUrl: user.avatarUrl ?? '',
  errorWidget: (_, __, ___) => const Icon(Icons.person),
  httpHeaders: {'Authorization': 'Bearer $token'},
)
```

**Input sanitization** — Sanitize user inputs before sending to API. Validate email format, trim strings, reject empty IDs, and encode query parameters properly.

**Network hardening** — Pin base URLs in `AppConfig` (not user-configurable at runtime), enforce HTTPS, use certificate pinning for production, and set conservative timeouts.

Read **[network_setup.md](references/network_setup.md)** for the full interceptor setup and **[data_layer.md](references/data_layer.md)** for validation patterns at the repository boundary.

## Common Issues

| Issue | Solution |
|-------|----------|
| Build runner conflicts | `dart run build_runner clean && dart run build_runner build --delete-conflicting-outputs` |
| Provider not found | Ensure generated files are imported and run build_runner |
| Either not unwrapping | Use `fold()`, `match()`, or `getOrElse()` to extract values |
| `XxxRef` not found | Use unified `Ref` type instead (Riverpod 3.x+) |
| `sealed` keyword error | Upgrade to Dart 3.3+ and Freezed 3.0+ |
| `.map` / `.when` not found | Freezed 3.0+ removed these methods. Use Dart 3 `switch` expression pattern matching instead |

## Knowledge References

**Primary Libraries** (used in this skill):
- **Flutter 3.19+**: Latest framework features
- **Dart 3.3+**: Language features (patterns, records, `sealed` modifier)
- **Riverpod 3.0+**: State management with unified `Ref` type
- **Dio 5.9+**: HTTP client with interceptors
- **Retrofit 4.9+**: Type-safe REST API code generation
- **freezed 3.0+**: Immutable data classes with code generation
- **json_serializable 6.x**: JSON serialization
- **go_router 14.x+**: Declarative routing
- **fpdart**: Functional error handling with Either type

## References

- **[quick_start.md](references/quick_start.md)** - Step-by-step feature creation workflow
- **[data_layer.md](references/data_layer.md)** - Models, Retrofit API services, Repositories, Response validation
- **[presentation_layer.md](references/presentation_layer.md)** - Providers, Screens, Widgets, Secure image loading
- **[network_setup.md](references/network_setup.md)** - Dio provider, Interceptors, Network exceptions, Response validation
- **[error_handling.md](references/error_handling.md)** - Either patterns, Failure types, Error strategies
- **[retrofit_patterns.md](references/retrofit_patterns.md)** - Complete Retrofit API request patterns
- **[provider_patterns.md](references/provider_patterns.md)** - Advanced Riverpod patterns (pagination, caching, optimistic updates)
- **[testing_guide.md](references/testing_guide.md)** - Unit, widget, and integration testing strategies
- **[feature_examples.md](references/feature_examples.md)** - Complete Auth feature implementation
- **[migration_guide.md](references/migration_guide.md)** - Riverpod 2→3 & Freezed 2→3 full before/after examples