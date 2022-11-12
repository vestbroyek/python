# helper
import inspect

def bind_args(function, *args, **kwargs):
    return inspect.signature(function).bind(*args, **kwargs).arguments

# define type checker
import functools

def check_types(severity = 1):
    def noop_decorator(function):
        return function
    def messaging(msg):
        if severity == 1:
            print(msg)
        if severity == 2:
            raise TypeError(msg)
    def checker(function):
        # check annotations
        annotations = function.__annotations__
        # if empty, forward through
        if len(annotations) == 0:
             return function
        else: 
            # ensure each annotation is a type
            for param_type in annotations.values():
                if param_type not in (int, str, bool, float):
                    raise TypeError('Wrong annotations types')
            @functools.wraps(function)
            def wrapper(*args, **kwargs):
                # bind args to the original function
                bound_args = bind_args(function, *args, **kwargs)
                # check them against the annotations
                if len(annotations) != 0:
                    for key, arg, expected_type in zip(bound_args.keys(), bound_args.values(), annotations.values()):
                        try:
                            # print(f"Checking if {bound_args[key]} is of type {annotations[key]}")
                            if type(bound_args[key]) != annotations[key]:
                                messaging(f"Type mismatch, expected {annotations[key]} but received {bound_args[key]}!")
                        except KeyError: pass
                # check return type
                expected_return_type = annotations['return']
                if expected_return_type:
                    actual_return_type = type(function(*args, **kwargs))
                    if expected_return_type != actual_return_type:
                        messaging(severity)
                return function(*args, **kwargs)
            return wrapper
    return noop_decorator if severity == 0 else checker

# test
@check_types(severity = 2)
def foo(a: int, b: str) -> bool:
    return b[a] == 'X'

# Legitimate function call, no issues - just returns result of call
print(foo(1, 'hello'))

# Problematic call, since b is list instead of str, but just makes the call because severity is set to 0
@check_types(severity = 0)
def foo(a: int, b: str) -> bool:
    return b[a] == 'X'

print(foo(1, ['foo', 'bar']))

# Problematic call with severity set to 1 - prints warning message
@check_types(severity = 1)
def foo(a: int, b: str) -> bool:
    return b[a] == 'X'

print(foo(1, ['foo', 'bar']))

# Problematic call with severity set to 2 - raises TypeError
@check_types(severity = 2)
def foo(a: int, b: str) -> bool:
    return b[a] == 'X'

print(foo(1, ['foo', 'bar']))