# Complete Feature Example: Authentication

A complete auth feature implementation showing all three Clean Architecture layers working together. Use this as a reference when building similar features.

Data source implementations (HTTP clients, databases, etc.) are abstract — implement with Dio, http, GraphQL, Firebase, etc. as needed.

## Authentication Feature

### Domain Layer

**Entity** (domain/entities/auth_user.dart):
```dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'auth_user.freezed.dart';

@freezed
sealed class AuthUser with _$AuthUser {
  const factory AuthUser({
    required String id,
    required String email,
    required String name,
    String? avatarUrl,
    required DateTime createdAt,
  }) = _AuthUser;
}
```

**Repository** (domain/repositories/auth_repository.dart):
```dart
import 'package:fpdart/fpdart.dart';
import '../../core/errors/failures.dart';
import '../entities/auth_user.dart';

abstract class AuthRepository {
  Future<Either<Failure, AuthUser>> login(String email, String password);
  Future<Either<Failure, AuthUser>> register(String email, String password, String name);
  Future<Either<Failure, Unit>> logout();
  Future<Either<Failure, AuthUser>> getCurrentUser();
}
```

**UseCases** (domain/usecases/):

login_user.dart:
```dart
import 'package:fpdart/fpdart.dart';
import '../../core/errors/failures.dart';
import '../entities/auth_user.dart';
import '../repositories/auth_repository.dart';

class LoginUser {
  final AuthRepository repository;

  LoginUser(this.repository);

  Future<Either<Failure, AuthUser>> call(String email, String password) {
    return repository.login(email, password);
  }
}
```

### Data Layer

**Model** (data/models/auth_user_model.dart):
```dart
import 'package:freezed_annotation/freezed_annotation.dart';
import '../../domain/entities/auth_user.dart';

part 'auth_user_model.freezed.dart';
part 'auth_user_model.g.dart';

@freezed
sealed class AuthUserModel with _$AuthUserModel {
  const AuthUserModel._();

  const factory AuthUserModel({
    required String id,
    required String email,
    required String name,
    String? avatarUrl,
    required String createdAt,
  }) = _AuthUserModel;

  factory AuthUserModel.fromJson(Map<String, dynamic> json) =>
      _$AuthUserModelFromJson(json);

  AuthUser toEntity() => AuthUser(
    id: id,
    email: email,
    name: name,
    avatarUrl: avatarUrl,
    createdAt: DateTime.parse(createdAt),
  );
}
```

**DataSource Interface** (data/datasources/auth_datasource.dart):
```dart
import '../models/auth_user_model.dart';

/// Abstract data source - implement with your choice of HTTP client, database, etc.
abstract class AuthDataSource {
  Future<AuthUserModel> login(String email, String password);
  Future<AuthUserModel> register(String email, String password, String name);
  Future<void> logout();
  Future<String?> getToken();
}

/// Example implementation (replace with your actual data source)
class AuthRemoteDataSource implements AuthDataSource {
  @override
  Future<AuthUserModel> login(String email, String password) {
    throw UnimplementedError();
  }

  @override
  Future<AuthUserModel> register(String email, String password, String name) {
    throw UnimplementedError();
  }

  @override
  Future<void> logout() {
    throw UnimplementedError();
  }

  @override
  Future<String?> getToken() {
    throw UnimplementedError();
  }
}
```

**Repository Implementation** (data/repositories/auth_repository_impl.dart):
```dart
import 'package:fpdart/fpdart.dart';
import '../../core/errors/failures.dart';
import '../../domain/entities/auth_user.dart';
import '../../domain/repositories/auth_repository.dart';
import '../datasources/auth_datasource.dart';

class AuthRepositoryImpl implements AuthRepository {
  final AuthDataSource dataSource;

  AuthRepositoryImpl(this.dataSource);

  @override
  Future<Either<Failure, AuthUser>> login(String email, String password) async {
    try {
      final userModel = await dataSource.login(email, password);
      return Right(userModel.toEntity());
    } on Exception catch (e) {
      return Left(ServerFailure(e.toString()));
    } catch (e) {
      return Left(UnexpectedFailure(e.toString()));
    }
  }

  @override
  Future<Either<Failure, AuthUser>> register(String email, String password, String name) async {
    try {
      final userModel = await dataSource.register(email, password, name);
      return Right(userModel.toEntity());
    } on Exception catch (e) {
      return Left(ServerFailure(e.toString()));
    } catch (e) {
      return Left(UnexpectedFailure(e.toString()));
    }
  }

  @override
  Future<Either<Failure, Unit>> logout() async {
    try {
      await dataSource.logout();
      return const Right(unit);
    } catch (e) {
      return Left(UnexpectedFailure(e.toString()));
    }
  }

  @override
  Future<Either<Failure, AuthUser>> getCurrentUser() async {
    try {
      final token = await dataSource.getToken();
      if (token == null) {
        return const Left(CacheFailure('No token found'));
      }
      // Fetch current user from API - implement as needed
      return const Left(ServerFailure('Not implemented'));
    } catch (e) {
      return Left(UnexpectedFailure(e.toString()));
    }
  }
}
```

### Presentation Layer

**Provider** (presentation/providers/auth_provider.dart):
```dart
import 'package:riverpod_annotation/riverpod_annotation.dart';
import '../../domain/entities/auth_user.dart';
import '../../domain/usecases/login_user.dart';
import '../../data/datasources/auth_datasource.dart';
import '../../data/repositories/auth_repository_impl.dart';

part 'auth_provider.g.dart';

// Define your data source provider - implement with your choice
@riverpod
AuthDataSource authDataSource(Ref ref) {
  // Return your implementation: AuthRemoteDataSource(), AuthLocalDataSource(), etc.
  throw UnimplementedError('Provide your AuthDataSource implementation');
}

@riverpod
AuthRepositoryImpl authRepository(Ref ref) {
  return AuthRepositoryImpl(ref.watch(authDataSourceProvider));
}

@riverpod
LoginUser loginUser(Ref ref) {
  return LoginUser(ref.watch(authRepositoryProvider));
}

@riverpod
class AuthNotifier extends _$AuthNotifier {
  @override
  FutureOr<AuthUser?> build() => null;

  Future<void> login(String email, String password) async {
    state = const AsyncLoading();
    final result = await ref.read(loginUserProvider)(email, password);

    state = result.fold(
      (failure) => AsyncError(failure, StackTrace.current),
      (user) => AsyncData(user),
    );
  }

  Future<void> logout() async {
    final result = await ref.read(authRepositoryProvider).logout();
    result.fold(
      (failure) => state = AsyncError(failure, StackTrace.current),
      (_) => state = const AsyncData(null),
    );
  }
}
```

**Login Screen** (presentation/screens/login_screen.dart):
```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../providers/auth_provider.dart';
import '../../core/errors/failures.dart';

class LoginScreen extends ConsumerStatefulWidget {
  const LoginScreen({super.key});

  @override
  ConsumerState<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends ConsumerState<LoginScreen> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  void _handleLogin() async {
    if (_formKey.currentState!.validate()) {
      await ref.read(authNotifierProvider.notifier).login(
        _emailController.text,
        _passwordController.text,
      );

      final authState = ref.read(authNotifierProvider);

      if (authState.hasValue && authState.value != null) {
        if (mounted) {
          context.go('/home');
        }
      } else if (authState.hasError) {
        if (mounted) {
          final failure = authState.error as Failure;
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text(failure.message)),
          );
        }
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final authState = ref.watch(authNotifierProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('Login')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              TextFormField(
                controller: _emailController,
                decoration: const InputDecoration(
                  labelText: 'Email',
                  border: OutlineInputBorder(),
                ),
                keyboardType: TextInputType.emailAddress,
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter email';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: _passwordController,
                decoration: const InputDecoration(
                  labelText: 'Password',
                  border: OutlineInputBorder(),
                ),
                obscureText: true,
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter password';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 24),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: authState.isLoading ? null : _handleLogin,
                  child: authState.isLoading
                      ? const SizedBox(
                          height: 20,
                          width: 20,
                          child: CircularProgressIndicator(strokeWidth: 2),
                        )
                      : const Text('Login'),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
```

For pagination patterns, see **[provider_patterns.md](provider_patterns.md)** (Pattern 10) and **[presentation_layer.md](presentation_layer.md)** (List Screen patterns).