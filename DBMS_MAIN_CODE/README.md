# Training Institute Management System - DBMS UI

A simple Python Tkinter desktop UI connected to MySQL. It supports the three operations required for Presentation-III:

- View records
- Insert records
- Delete records

## 1. Requirements

- Python 3
- MySQL Server / MySQL Workbench
- `mysql-connector-python`

## 2. Create the database

Open MySQL Workbench and run `database_setup.sql` completely.

This creates the database:

`training_management`

and loads the sample records.

## 3. Configure MySQL password

Open `app.py` and edit:

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "YOUR_MYSQL_PASSWORD",
    "database": "training_management"
}
```

If your root account has no password, leave it as an empty string.

## 4. Install dependency

On macOS Terminal:

```bash
cd path/to/dbms_ui_project
python3 -m pip install -r requirements.txt
```

## 5. Run

```bash
python3 app.py
```

## Presentation demo flow

1. Open **View Records** and show an existing table such as `Learner`.
2. Open **Insert Record**, select `Learner`, add a new learner, and insert it.
3. Return to **View Records** and show that the new record appears.
4. Open **Delete Record**, select `Learner`, enter the same learner ID, and delete it.
5. Return to **View Records** and show that the record is gone.
6. In MySQL Workbench run `SELECT * FROM Learner;` after each operation if your faculty asks to see the database change directly.

## Notes

- The UI supports all 11 tables in the supplied project data.
- SQL values are passed using parameterized queries.
- The table name is selected only from a fixed internal list, which avoids arbitrary SQL table input.
- Database errors are shown in dialog boxes instead of crashing the program.
