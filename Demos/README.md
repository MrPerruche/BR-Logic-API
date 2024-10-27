# Hey! Go no further!
If you try to run any scripts in `Demos`, or any scripts in a directory inside of it, they'll error out!<br>
If you want to run these demos/tests, you'll have to copy them or move them to the same directory/folder that you put BRCI in.

Right now, the structure looks like this:

```
BRCI/
└── Demos/
    ├── tests/
    │   └── some_test_file.py
    └── your_file.py
```
In order to use, say, `your_file.py`, you'll have to move it to the same directory as BRCI. Like so:
```
..BRCI/
  ├── BRCI/
  │   └── Demos/
  │       └── tests/
  │           └── some_test_file.py
  └── your_file.py                  <-- Moved / copied over here!
```
Now, you can run the `your_file.py` script you moved or copied from `Demos` or `Demos/tests`.