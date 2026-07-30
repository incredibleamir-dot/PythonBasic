# PythonBasic Vision

## Why PythonBasic Exists

PythonBasic was created with one simple goal:

> **To help students and hobbyists transition from Microsoft Small Basic to Python without leaving behind the programming environment they already know.**

Many programmers, including the author, discovered programming through Microsoft Small Basic. Its simple syntax and beginner-friendly libraries have inspired countless people to write their first programs.

However, as learners grow, they eventually reach a point where they need to move beyond Small Basic. That transition can be difficult. Students are often required to learn Python **and** an entirely new set of libraries at the same time, making the learning curve much steeper.

PythonBasic aims to make that transition easier.

By recreating the familiar Microsoft Small Basic API in Python, learners can focus on understanding Python itself while continuing to use libraries they already know, such as `GraphicsWindow`, `Turtle`, `TextWindow`, `Shapes`, and others.

Over time, they can gradually introduce standard Python modules into the same programs:

```python
from smallbasic import GraphicsWindow, Turtle

import math
import random
import json
import requests
```

Instead of replacing Small Basic, PythonBasic acts as a bridge between an educational programming environment and the full power of Python.

---

# Project Goals

The long-term goals of PythonBasic are:

* Recreate the Microsoft Small Basic standard library as faithfully as possible.
* Preserve the familiar programming experience for existing Small Basic users.
* Allow existing Small Basic programs to run with little or no modification after converting the language syntax to Python.
* Encourage learners to explore Python's standard library and third-party packages alongside familiar Small Basic APIs.
* Remain simple, approachable, and beginner-friendly.

This project values **compatibility** over cleverness. Wherever practical, the behavior of PythonBasic should match Microsoft Small Basic rather than following every Python convention.

---

# What PythonBasic Is

PythonBasic **is**:

* A compatibility library inspired by Microsoft Small Basic.
* A learning tool.
* A bridge from Small Basic to Python.
* An open-source educational project.

PythonBasic is **not** intended to replace Python's standard libraries or become a new programming language.

---

# Compatibility Philosophy

When implementing features, the preferred order of priorities is:

1. Match the Microsoft Small Basic API.
2. Match the observable behavior of Microsoft Small Basic.
3. Keep the library easy for beginners to understand.
4. Improve the internal implementation without breaking compatibility.

Whenever possible, existing Small Basic examples should require little more than translating Small Basic syntax into Python.

---

# How You Can Help

Contributions of all sizes are welcome.

You don't need to be an expert Python developer to contribute.

Some ways you can help include:

* Reporting bugs or unexpected behavior.
* Comparing PythonBasic with Microsoft Small Basic and identifying compatibility differences.
* Improving documentation.
* Writing tutorials or educational examples.
* Creating example programs.
* Improving performance.
* Adding automated tests.
* Helping implement missing Small Basic features.
* Reviewing pull requests and discussing ideas.

If you are familiar with Microsoft Small Basic, your knowledge is especially valuable because compatibility is one of the project's primary goals.

---

# Contribution Guidelines

When contributing, please keep these principles in mind:

* Preserve compatibility whenever possible.
* Avoid breaking existing APIs.
* Keep the code readable and beginner-friendly.
* Document new features and behavior changes.
* Prefer incremental improvements over large rewrites.
* Discuss major architectural changes before implementing them.

---

# Looking Ahead

PythonBasic is an evolving project.

Future development will continue to improve compatibility, graphics rendering, performance, documentation, and educational resources while maintaining the familiar Small Basic programming experience.

If PythonBasic helps even one new programmer make the journey from Microsoft Small Basic to Python with confidence, then it has achieved its purpose.

---

## A Personal Note

PythonBasic is a passion project.

Like many others, I discovered programming through Microsoft Small Basic. It was the language that introduced me to computational thinking, creativity, and software development.

This project is my way of giving back to the community that inspired me, while helping the next generation of programmers take their next step into Python.
