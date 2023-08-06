# What is it?

This is very simple code to get system call numbers from Python level.

# Usage

Quite simple:

```python
#!/usr/bin/python3

import syscalls

system_calls = syscalls.syscalls()

for test_call in ['openat', 'osf_uadmin', 'nosuchcall']:
    try:
        print(f"System call '{test_call}' has number: {system_calls[test_call]}")
    except syscalls.NoSuchSystemCall:
        print(f"No such system call '{test_call}' on any architecture")
    except syscalls.NotSupportedSystemCall:
        print(f"System call '{test_call}' is not supported on this "
              "architecture")

for test_call in ['openat', 'osf_uadmin', 'nosuchcall']:
    try:
        print(f"System call '{test_call}' on arm64 has number: "
              f"{system_calls.get(test_call, 'arm64')}")
    except syscalls.NoSuchSystemCall:
        print(f"No such system call '{test_call}' on any architecture")
    except syscalls.NotSupportedSystemCall:
        print(f"System call '{test_call}' is not supported on this "
              "architecture")
```
