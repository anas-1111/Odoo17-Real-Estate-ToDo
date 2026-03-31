# 🏠 Odoo 17 Real Estate & To-Do Modules

This repository contains custom Odoo 17 modules developed for learning and practical implementation of business logic, ORM, views, and API development.

---

## 📦 Modules Included

### 1. app_one (Real Estate Management)
A custom module to manage real estate properties.

#### Features:
- Create & manage properties
- Property details (price, owner, bedrooms, etc.)
- Property lines (One2many relationship)
- State management (draft, pending, closed)
- Wizard for changing property state
- Custom reports (PDF)
- REST API endpoints

---

### 2. to_do (Task Management)
A simple task management system.

#### Features:
- Create tasks with description & due date
- Assign tasks to users (`res.partner`)
- Task status workflow:
  - New
  - In Progress
  - Completed
- Task lines (time tracking)
- Validation for total time vs estimated time
- Wizards for:
  - Changing state
  - Reassigning tasks

---

## 🛠️ Technologies Used

- Odoo 17 (Community)
- Python (Odoo ORM)
- XML (Views & Actions)
- PostgreSQL
- REST API (Controller-based)

---

## ⚙️ Installation

1. Clone the repository:
```bash
git clone https://github.com/anas-1111/odoo17-real-estate.git
