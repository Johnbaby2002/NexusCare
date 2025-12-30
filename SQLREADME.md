# EHR System Database (MySQL)

This repository contains the complete database schema and sample data for our Electronic Health Record (EHR) system.  
It includes:

- Database name: **ehr_system**
- Tables:
  - `doctors`
  - `patients`
  - `ehr_records`
- Sample data:
  - 10 doctors
  - 30 patients
  - 30 EHR records

The file `ehr_system.sql` can be imported into any MySQL server to recreate the full database.

---

## 📦 Contents

### `ehr_system.sql`
This file contains:

- All `CREATE TABLE` statements  
- All foreign key relationships  
- All sample data (`INSERT` statements)  
- Timestamps and auto-increment values  

---

## 🛠 Requirements

To import and use this database, you need:

- **MySQL Server** (8.x recommended)
- **MySQL Workbench** (optional but recommended)
- OR Terminal access to MySQL

---

## 🚀 How to Import the Database

You can import the database in two ways:

---

## **Option 1: Import Using Terminal**

1. Place `ehr_system.sql` in any folder.
2. Open Terminal in that folder.
3. Run:

```bash
mysql -u root -p < ehr_system.sql
