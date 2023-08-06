
# Perm-Banana

#### A package to enable easy permission creation inside Python.

![test](https://github.com/TheJoeSmo/perm-banana/actions/workflows/tests.yml/badge.svg)

#### How to use it?

```python
from perm-banana import Permission, Check, banana

@banana
class MyPermission(Permission)
    can_read_messages = Check(Permission(0b1))
    can_write_messages = Check(Permission(0b10))
    basic_user = can_read_message | can_write_messages

user = MyPermission(0b11)
if user.basic_user:
    print("permission granted")
else:
    print("permission denied")
```
