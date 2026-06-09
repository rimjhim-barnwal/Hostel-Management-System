# 🏠 Hostel Management System

A menu-driven **Python + MySQL** console application for managing hostel students, rooms, and fees. Built with OOP principles and clean SQL schema design.

---

## 📁 Folder Structure

```
hostel-management-system/
├── main.py            ← Entry point, menu loop, UI layer
├── database.py        ← MySQL connection wrapper (Database class)
├── models/
│   ├── student.py     ← Student CRUD (register, search, update, delete)
│   ├── room.py        ← Room availability queries
│   └── fee.py         ← Fee recording and reporting
├── sql/
│   └── schema.sql     ← DDL: creates hostel_db + all tables + seed data
└── README.md
```

---

## ⚙️ Technologies Used

| Technology           | Purpose                        |
|----------------------|--------------------------------|
| Python 3.10+         | Core application language      |
| MySQL 8.0+           | Relational database            |
| mysql-connector-python | MySQL ↔ Python bridge        |
| ANSI escape codes    | Coloured terminal output       |

---

## 🚀 Installation & Setup

### 1. Prerequisites

- Python 3.10 or higher
- MySQL Server 8.0+ running locally
- pip

### 2. Install Python Dependencies

```bash
pip install mysql-connector-python
```

### 3. Set Up the Database

Open MySQL Workbench or your MySQL CLI and run:

```bash
mysql -u root -p < sql/schema.sql
```

Or paste the contents of `sql/schema.sql` into MySQL Workbench and execute.

### 4. Configure the Connection

Edit `database.py` and update the `DB_CONFIG` dict:

```python
DB_CONFIG = {
    "host":     "localhost",
    "user":     "root",
    "password": "YOUR_MYSQL_PASSWORD",   # ← change this
    "database": "hostel_db",
    "port":     3306,
}
```

Alternatively, set environment variables:

```bash
export DB_USER=root
export DB_PASS=yourpassword
```

### 5. Run the Application

```bash
python main.py
```

---

## 🖥️ Features

| Feature                  | Description                                              |
|--------------------------|----------------------------------------------------------|
| **Student Registration** | Add student with name, room, phone, email, course        |
| **View All Students**    | Tabular display with colour-coded fee status             |
| **Search**               | Search by name, phone, or room number                    |
| **Update Student**       | Edit any mutable field, keep current values if blank     |
| **Delete Student**       | Removes student + auto-frees the room                    |
| **Fee Management**       | Record payments, update status, view pending, history    |
| **Room Status**          | Summary of total / occupied / available rooms            |

---

## 🗃️ Database Design

```
students        fee_records     rooms
─────────────   ─────────────   ─────────────
id (PK)         id (PK)         room_number (PK)
name            student_id(FK)  capacity
room_number(FK) amount          occupied
phone           payment_date    floor
email           remarks         type
course
fee_status
join_date
```

---

## 📌 Resume Bullet Points

- Designed and implemented a **Python + MySQL console application** using OOP with model classes for Student, Room, and Fee
- Built a reusable **Database wrapper** with context-manager support, parameterized queries, and rollback error handling
- Designed a **normalized 3-table schema** with foreign keys, ENUM constraints, and cascading deletes
- Implemented **full CRUD** with search, fee tracking, room allocation management, and colour-coded CLI output

---

## 📝 GitHub Repository Description

> Console-based Hostel Management System built with Python and MySQL. Features student registration, room allocation, fee tracking, and full CRUD operations. Demonstrates OOP design, normalized SQL schema, and clean layered architecture.

---

## 🔀 Git Commit History

```
feat: initialise project structure and SQL schema with rooms seed data
feat: add Database wrapper class with context manager and error handling
feat: implement Student, Room, Fee models with full OOP CRUD methods
feat: build menu-driven console UI with colour output and fee sub-menu
```

---

## 🎤 Interview Explanation

> "I built a Hostel Management System in Python with a MySQL backend. The architecture is layered: `main.py` handles the menu loop and UI, `database.py` wraps the MySQL connection with a clean API (execute, fetchone, fetchall), and the `models/` folder contains three OOP classes — Student, Room, and Fee — each responsible for one domain. The SQL schema is normalised into three tables with foreign key constraints and cascading deletes so that removing a student automatically cleans up related fee records. I used ENUM types for fee_status and a join table pattern for payments. The key technical concept is separation of concerns: the UI never touches SQL directly — it calls model methods which call the database wrapper."

---

## 🖼️ Screenshot Descriptions

1. **Main Menu** — ANSI-coloured menu with 8 options in a box border
2. **Student Table** — tabular output with green "Paid" / red "Pending" fee status
3. **Room Status** — summary counts + full room list with occupied flags
4. **Fee Sub-menu** — nested menu showing payment recording and history view
