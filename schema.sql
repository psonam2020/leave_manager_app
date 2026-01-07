CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    password BLOB,
    role TEXT,
    is_active INTEGER DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE leave_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    total_per_year INTEGER,
    carry_forward INTEGER DEFAULT 0
);

CREATE TABLE leave_balances (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    leave_type_id INTEGER,
    balance INTEGER
);

CREATE TABLE leave_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    leave_type_id INTEGER,
    start_date DATE,
    end_date DATE,
    days INTEGER,
    reason TEXT,
    status TEXT,
    applied_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    actioned_at DATETIME
);

CREATE TABLE comp_off (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    date DATE,
    credit INTEGER DEFAULT 1
);
