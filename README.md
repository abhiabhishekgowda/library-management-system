# 📚 Library Management System (Pro)
**Month 2: Relational Database & Persistence Milestone**

A professional-grade console application built to master **Relational Databases (RDBMS)** and **Python-SQL Integration**. This project marks the transition from flat-file storage (JSON) to structured data management.

## 🛠️ Technical Stack
- **Language:** Python 3.x
- **Database Engine:** SQLite3
- **Architecture:** Procedural Logic moving toward Object-Oriented Programming (OOP)

## 🚀 Professional Features
- **Relational Schema:** Tables for `Books` and `Members` with Primary/Foreign Key relationships.
- **ACID Compliant Transactions:** Ensuring data is never lost during "Issue" or "Return" operations.
- **Advanced Querying:** SQL-based search logic (Filtering by Author, Title, or ISBN).
- **Persistent Inventory:** Real-time database updates that survive program restarts.
- **Input Validation:** SQL Parameterization to prevent "SQL Injection" attacks.

## 📊 Database Schema (The Logic)
The system operates on a relational model:
- **Books Table:** `id`, `title`, `author`, `isbn`, `status` (Available/Borrowed).
- **Users Table:** `user_id`, `name`, `active_loans`.

## 📅 Monthly Roadmap
- **Week 1:** Database Initialization & Book CRUD (Create, Read, Update, Delete).
- **Week 2:** Search algorithms using SQL `LIKE` and `WHERE` clauses.
- **Week 3:** Transactional Logic: Handling "Borrow" and "Return" events.
- **Week 4:** Data reporting (viewing all borrowed books) and final code refactoring.

---
*Completed as part of a 6-month Backend Roadmap | March 2026*

