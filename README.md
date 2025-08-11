# Python Learning Workspace

Welcome to the **Python Learning Workspace**, a curated collection of hands‑on examples, tutorials, and mini‑projects to help you master Python from basics through advanced features.

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Repository Structure](#repository-structure)
5. [Usage Examples](#usage-examples)
6. [Mini‑Projects](#mini-projects)

---

## 🔍 Overview

This repo is your one‑stop workspace for:

* **Fundamentals**: Core syntax, data types, and control flow.
* **Functions & Modules**: Writing reusable code and leveraging Python’s standard library.
* **OOP Concepts**: Classes, inheritance, dunder methods, and encapsulation.
* **File I/O & Error Handling**: Reading/writing files and managing exceptions.
* **Advanced Features**: Type hints, pattern matching (`match`), lambdas, comprehensions, and more.
* **Mini‑Projects**: Small applications showcasing Flask web development and voice‑activated assistants.

Whether you’re a beginner or an experienced coder brushing up on specific topics, you’ll find clear, documented examples here.

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
2. **Install dependencies** (for all mini‑projects)

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
│   |── 4_dunder_getter_setter.py
|   └── ... 
├── 6_More/
│   ├── 1_typing_hints.py
│   ├── 2_pattern_matching.py
│   ├── 3_exceptions.py
│   └── ...
├── MiniProject/
│   ├── snake_water_gun/
│   │   ├── app.py
│   │   ├── templates/index.html
│   │   └── requirements.txt
│   └── jarvis/
│       ├── jarvis.py
│       └── requirements.txt
└── README.md  # This file
```

> **Note**: Each mini‑project lives in its own subfolder under `MiniProject/`.

---

## 🚀 Usage Examples

To run any example or project, specify its path. For instance, to explore data types:

```bash
python3 1_Basics/1_datatypes.py
```

---

## 🕸️ Mini‑Projects

### 1. Snake–Water–Gun Game

A Flask web app where you play a Rock‑Paper‑Scissors variant against the computer.

```bash
cd MiniProject/snake_water_gun
python app.py
```

Then visit `http://127.0.0.1:5000` in your browser.

### 2. Jarvis Personal Assistant

A voice‑activated assistant using speech recognition and Windows SAPI for speech output.

```bash
cd MiniProject/jarvis
conda activate jarvis      # if using Conda
python jarvis.py
```

Say “Jarvis” to wake it, then use commands like “Open YouTube” or “Open GitHub.”

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

* Add new examples or deeper tutorials in existing directories.
* Improve documentation or fix typos.
* Enhance mini‑projects with additional features.

Please fork the repo, create a branch, and submit a pull request.

---