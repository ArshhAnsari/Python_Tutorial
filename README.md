# Python Learning Workspace

Welcome to the **Python Learning Workspace**, a curated collection of hands‑on examples, tutorials, and a mini‑project to help you master Python from the basics through advanced features.

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Repository Structure](#repository-structure)
5. [Usage Examples](#usage-examples)
6. [Mini Project](#mini-project)
7. [Contributing](#contributing)
8. [License](#license)

---

## 🔍 Overview

This repo is your one‑stop workspace for:

* **Fundamentals**: Core syntax, data types, and control flow.
* **Functions & Modules**: Writing reusable code and leveraging Python’s standard library.
* **OOP Concepts**: Classes, inheritance, dunder methods, and encapsulation.
* **File I/O & Error Handling**: Reading/writing files and managing exceptions.
* **Advanced Features**: Type hints, pattern matching (`match`), lambdas, comprehensions, and more.
* **Mini‑Project**: A simple web app demonstrating Flask integration.

Whether you’re just starting out or brushing up on specific topics, you’ll find well‑documented examples here.

---

## 📦 Prerequisites

* **Python 3.8+** installed: [Download here](https://www.python.org/downloads/)
* (Optional) A virtual environment tool:

  ```bash
  python3 -m venv venv
  source venv/bin/activate   # macOS/Linux
  venv\Scripts\activate    # Windows PowerShell
  ```

---

## ⚙️ Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/ArshhAnsari/python_tutorial.git
   cd python_tutorial
   ```
2. **Install dependencies** (for the mini‑project)

   ```bash
   pip install -r requirements.txt
   ```

---

## 📂 Repository Structure

```
python_tutorial/
├── 1_Basics/
│   ├── 1_datatypes.py
│   ├── 2_operators.py
│   └── ...
├── 2_Conditional_Loops/
│   ├── 1_if_else_elif.py
│   └── 2_for_loop.py
├── 3_Functions/
│   ├── 1_basic_functions.py
│   └── 2_advanced_functions.py
├── 4_File/
│   ├── 1_file_read_write.py
│   └── 2_file_operations.py
├── 5_OOPs/
│   ├── 1_classes.py
│   ├── 2_class_static_methods.py
│   ├── 3_inheritance.py
│   └── 4_dunder_getter_setter.py
├── 6_More/
│   ├── 1_typing_hints.py
│   ├── 2_pattern_matching.py
│   ├── 3_exceptions.py
│   └── ...
├── MiniProject/
│   ├── app.py
│   ├── logic.py
│   └── templates/index.html
├── requirements.txt
└── README.md
```

> **Note**: Filenames have been updated to be more descriptive and consistent.

---

## 🚀 Usage Examples

For any topic folder, run the example scripts directly. For instance, to explore data types:

```bash
python3 1_Basics/1_datatypes.py
```

Browse and modify the code to experiment with different inputs and scenarios.

---

## 🕸️ Mini Project: Flask Web App

A simple Snake–Water–Gun game implemented with Flask:

1. **Install Flask** (if not already installed)

   ```bash
   pip install Flask
   ```
2. **Run the app**

   ```bash
   python3 MiniProject/app.py
   ```
3. **Open in your browser** Visit `http://127.0.0.1:5000/`

Feel free to extend the app with new features, styles, or deployment configurations.

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

* Add examples or deeper tutorials in existing directories.
* Improve documentation or fix typos.
* Enhance the mini‑project with additional functionality.

Please fork the repo, make your changes, and submit a pull request.

---
