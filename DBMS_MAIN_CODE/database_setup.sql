CREATE DATABASE IF NOT EXISTS training_management;
USE training_management;

-- Run this script on a fresh database.

CREATE TABLE Course (
    course_id VARCHAR(10) PRIMARY KEY,
    course_name VARCHAR(100),
    duration_weeks INT,
    fee DECIMAL(10,2)
);

INSERT INTO Course VALUES
('C001', 'Python Programming', 8, 12000),
('C002', 'Data Analytics', 10, 18000),
('C003', 'Web Development', 12, 22000),
('C004', 'Database Management', 6, 10000),
('C005', 'Machine Learning', 14, 28000),
('C006', 'Cloud Computing', 8, 20000),
('C007', 'Cyber Security', 10, 24000),
('C008', 'Java Programming', 8, 15000);

CREATE TABLE Module (
    module_id VARCHAR(10) PRIMARY KEY,
    course_id VARCHAR(10),
    module_name VARCHAR(100)
);
INSERT INTO Module VALUES
('M001', 'C001', 'Python Basics'),('M002', 'C001', 'Functions and OOP'),('M003', 'C001', 'File Handling'),
('M004', 'C002', 'Excel and Statistics'),('M005', 'C002', 'Python for Data Analysis'),('M006', 'C003', 'HTML and CSS'),
('M007', 'C003', 'JavaScript'),('M008', 'C004', 'SQL Fundamentals'),('M009', 'C004', 'Database Design'),
('M010', 'C005', 'Machine Learning Basics'),('M011', 'C005', 'Regression'),('M012', 'C006', 'Cloud Fundamentals'),
('M013', 'C006', 'AWS Services'),('M014', 'C007', 'Network Security'),('M015', 'C007', 'Ethical Hacking'),
('M016', 'C008', 'Java Basics');

CREATE TABLE Session (
    session_id VARCHAR(10) PRIMARY KEY,
    module_id VARCHAR(10),
    session_date DATE,
    topic VARCHAR(100)
);
INSERT INTO Session VALUES
('S001', 'M001', '2026-08-03', 'Variables and Data Types'),('S002', 'M001', '2026-08-05', 'Conditional Statements'),
('S003', 'M002', '2026-08-10', 'Functions'),('S004', 'M002', '2026-08-12', 'Classes and Objects'),
('S005', 'M004', '2026-08-04', 'Descriptive Statistics'),('S006', 'M005', '2026-08-11', 'Pandas Basics'),
('S007', 'M008', '2026-08-06', 'SELECT and WHERE'),('S008', 'M009', '2026-08-13', 'ER Diagrams'),
('S009', 'M010', '2026-08-18', 'Introduction to ML'),('S010', 'M011', '2026-08-20', 'Linear Regression'),
('S011', 'M012', '2026-08-17', 'Cloud Concepts'),('S012', 'M013', '2026-08-19', 'AWS EC2'),
('S013', 'M014', '2026-08-21', 'Network Security'),('S014', 'M015', '2026-08-23', 'Ethical Hacking Basics'),
('S015', 'M016', '2026-08-22', 'Java Fundamentals');

CREATE TABLE Trainer (
    trainer_id VARCHAR(10) PRIMARY KEY,
    trainer_name VARCHAR(100),
    specialization VARCHAR(100),
    phone VARCHAR(15)
);
INSERT INTO Trainer VALUES
('T001', 'Arjun Mehta', 'Python', '9876543210'),('T002', 'Priya Sharma', 'Data Analytics', '9876543211'),
('T003', 'Rahul Verma', 'Web Development', '9876543212'),('T004', 'Sneha Rao', 'Database Management', '9876543213'),
('T005', 'Karan Singh', 'Machine Learning', '9876543214'),('T006', 'Neha Kapoor', 'Cloud Computing', '9876543215'),
('T007', 'Vikram Patel', 'Cyber Security', '9876543216'),('T008', 'Divya Nair', 'Java Programming', '9876543217');

CREATE TABLE Batch (
    batch_id VARCHAR(10) PRIMARY KEY,
    course_id VARCHAR(10),
    trainer_id VARCHAR(10),
    batch_name VARCHAR(100),
    start_date DATE,
    end_date DATE,
    capacity INT
);
INSERT INTO Batch VALUES
('B001', 'C001', 'T001', 'Python-A', '2026-08-01', '2026-09-26', 30),('B002', 'C002', 'T002', 'Analytics-A', '2026-08-05', '2026-10-14', 25),
('B003', 'C003', 'T003', 'WebDev-A', '2026-08-10', '2026-11-02', 30),('B004', 'C004', 'T004', 'DBMS-A', '2026-08-03', '2026-09-14', 25),
('B005', 'C005', 'T005', 'ML-A', '2026-08-15', '2026-11-20', 20),('B006', 'C006', 'T006', 'Cloud-A', '2026-08-18', '2026-10-10', 25),
('B007', 'C007', 'T007', 'Cyber-A', '2026-08-20', '2026-10-30', 20),('B008', 'C008', 'T008', 'Java-A', '2026-08-22', '2026-10-17', 30);

CREATE TABLE Learner (
    learner_id VARCHAR(10) PRIMARY KEY,
    learner_name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(15)
);
INSERT INTO Learner VALUES
('L001', 'Ananya Reddy', 'ananya@gmail.com', '9000000001'),('L002', 'Rohan Kumar', 'rohan@gmail.com', '9000000002'),
('L003', 'Meera Nair', 'meera@gmail.com', '9000000003'),('L004', 'Aditya Rao', 'aditya@gmail.com', '9000000004'),
('L005', 'Ishita Sharma', 'ishita@gmail.com', '9000000005'),('L006', 'Arjun Patel', 'arjun@gmail.com', '9000000006'),
('L007', 'Kavya Singh', 'kavya@gmail.com', '9000000007'),('L008', 'Dev Malhotra', 'dev@gmail.com', '9000000008'),
('L009', 'Nisha Verma', 'nisha@gmail.com', '9000000009'),('L010', 'Varun Shah', 'varun@gmail.com', '9000000010'),
('L011', 'Aarav Gupta', 'aarav@gmail.com', '9000000011'),('L012', 'Diya Joshi', 'diya@gmail.com', '9000000012'),
('L013', 'Rahul Reddy', 'rahul@gmail.com', '9000000013'),('L014', 'Sneha Kapoor', 'sneha@gmail.com', '9000000014'),
('L015', 'Manav Jain', 'manav@gmail.com', '9000000015'),('L016', 'Pooja Menon', 'pooja@gmail.com', '9000000016'),
('L017', 'Harsh Vardhan', 'harsh@gmail.com', '9000000017'),('L018', 'Aditi Shah', 'aditi@gmail.com', '9000000018'),
('L019', 'Kiran Das', 'kiran@gmail.com', '9000000019'),('L020', 'Riya Mehta', 'riya@gmail.com', '9000000020');

CREATE TABLE Enrollment (
    enrollment_id VARCHAR(10) PRIMARY KEY,
    learner_id VARCHAR(10),
    batch_id VARCHAR(10),
    enrollment_date DATE,
    status VARCHAR(20)
);
INSERT INTO Enrollment VALUES
('E001', 'L001', 'B001', '2026-07-28', 'Active'),('E002', 'L002', 'B001', '2026-07-29', 'Active'),
('E003', 'L003', 'B001', '2026-07-30', 'Active'),('E004', 'L004', 'B002', '2026-08-01', 'Active'),
('E005', 'L005', 'B002', '2026-08-02', 'Active'),('E006', 'L006', 'B003', '2026-08-05', 'Active'),
('E007', 'L007', 'B003', '2026-08-06', 'Active'),('E008', 'L008', 'B004', '2026-07-30', 'Active'),
('E009', 'L009', 'B004', '2026-07-31', 'Active'),('E010', 'L010', 'B005', '2026-08-10', 'Active'),
('E011', 'L011', 'B005', '2026-08-11', 'Active'),('E012', 'L012', 'B006', '2026-08-12', 'Active'),
('E013', 'L013', 'B006', '2026-08-13', 'Active'),('E014', 'L014', 'B007', '2026-08-14', 'Active'),
('E015', 'L015', 'B007', '2026-08-15', 'Active'),('E016', 'L016', 'B008', '2026-08-16', 'Active'),
('E017', 'L017', 'B008', '2026-08-17', 'Active'),('E018', 'L018', 'B001', '2026-08-01', 'Active'),
('E019', 'L019', 'B004', '2026-08-02', 'Completed'),('E020', 'L020', 'B005', '2026-08-12', 'Active');

CREATE TABLE Attendance (
    attendance_id VARCHAR(10) PRIMARY KEY,
    enrollment_id VARCHAR(10),
    session_id VARCHAR(10),
    status VARCHAR(10)
);
INSERT INTO Attendance VALUES
('A001', 'E001', 'S001', 'Present'),('A002', 'E001', 'S002', 'Present'),('A003', 'E001', 'S003', 'Present'),('A004', 'E001', 'S004', 'Absent'),
('A005', 'E002', 'S001', 'Present'),('A006', 'E002', 'S002', 'Absent'),('A007', 'E002', 'S003', 'Present'),('A008', 'E002', 'S004', 'Present'),
('A009', 'E003', 'S001', 'Present'),('A010', 'E003', 'S002', 'Present'),('A011', 'E003', 'S003', 'Absent'),('A012', 'E003', 'S004', 'Present'),
('A013', 'E004', 'S005', 'Present'),('A014', 'E004', 'S006', 'Present'),('A015', 'E005', 'S005', 'Present'),('A016', 'E005', 'S006', 'Absent'),
('A017', 'E006', 'S007', 'Present'),('A018', 'E006', 'S008', 'Present'),('A019', 'E007', 'S007', 'Absent'),('A020', 'E007', 'S008', 'Present'),
('A021', 'E008', 'S007', 'Present'),('A022', 'E008', 'S008', 'Present'),('A023', 'E009', 'S007', 'Absent'),('A024', 'E009', 'S008', 'Present'),
('A025', 'E010', 'S009', 'Present'),('A026', 'E010', 'S010', 'Present'),('A027', 'E011', 'S009', 'Present'),('A028', 'E011', 'S010', 'Absent'),
('A029', 'E012', 'S011', 'Present'),('A030', 'E012', 'S012', 'Present'),('A031', 'E013', 'S011', 'Absent'),('A032', 'E013', 'S012', 'Present'),
('A033', 'E014', 'S013', 'Present'),('A034', 'E014', 'S014', 'Present'),('A035', 'E015', 'S013', 'Present'),('A036', 'E015', 'S014', 'Absent'),
('A037', 'E016', 'S015', 'Present'),('A038', 'E017', 'S015', 'Absent');

CREATE TABLE Assessment (
    assessment_id VARCHAR(10) PRIMARY KEY,
    enrollment_id VARCHAR(10),
    assessment_name VARCHAR(100),
    score INT
);
INSERT INTO Assessment VALUES
('AS001', 'E001', 'Python Test 1', 88),('AS002', 'E002', 'Python Test 1', 76),('AS003', 'E003', 'Python Test 1', 92),
('AS004', 'E004', 'Statistics Test', 81),('AS005', 'E005', 'Statistics Test', 69),('AS006', 'E006', 'Web Test 1', 95),
('AS007', 'E007', 'Web Test 1', 72),('AS008', 'E008', 'DBMS Test 1', 91),('AS009', 'E009', 'DBMS Test 1', 68),
('AS010', 'E010', 'ML Test 1', 86),('AS011', 'E011', 'ML Test 1', 94),('AS012', 'E012', 'Cloud Test 1', 79),
('AS013', 'E013', 'Cloud Test 1', 88),('AS014', 'E014', 'Security Test 1', 91),('AS015', 'E015', 'Security Test 1', 73),
('AS016', 'E016', 'Java Test 1', 84),('AS017', 'E017', 'Java Test 1', 67),('AS018', 'E018', 'Python Test 1', 95),
('AS019', 'E019', 'DBMS Test 1', 82),('AS020', 'E020', 'ML Test 1', 78);

CREATE TABLE Fees (
    fee_id VARCHAR(10) PRIMARY KEY,
    enrollment_id VARCHAR(10),
    amount DECIMAL(10,2),
    payment_date DATE,
    payment_status VARCHAR(20)
);
INSERT INTO Fees VALUES
('F001', 'E001', 12000, '2026-07-28', 'Paid'),('F002', 'E002', 12000, '2026-07-29', 'Paid'),
('F003', 'E003', 12000, '2026-07-30', 'Paid'),('F004', 'E004', 18000, '2026-08-01', 'Paid'),
('F005', 'E005', 18000, '2026-08-02', 'Partial'),('F006', 'E006', 22000, '2026-08-05', 'Paid'),
('F007', 'E007', 22000, '2026-08-06', 'Pending'),('F008', 'E008', 10000, '2026-07-30', 'Paid'),
('F009', 'E009', 10000, '2026-07-31', 'Pending'),('F010', 'E010', 28000, '2026-08-10', 'Paid'),
('F011', 'E011', 28000, '2026-08-11', 'Paid'),('F012', 'E012', 20000, '2026-08-12', 'Partial'),
('F013', 'E013', 20000, '2026-08-13', 'Paid'),('F014', 'E014', 24000, '2026-08-14', 'Paid'),
('F015', 'E015', 24000, '2026-08-15', 'Pending'),('F016', 'E016', 15000, '2026-08-16', 'Paid'),
('F017', 'E017', 15000, '2026-08-17', 'Partial'),('F018', 'E018', 12000, '2026-08-01', 'Paid'),
('F019', 'E019', 10000, '2026-08-02', 'Paid'),('F020', 'E020', 28000, '2026-08-12', 'Pending');

CREATE TABLE Certificate (
    certificate_id VARCHAR(10) PRIMARY KEY,
    enrollment_id VARCHAR(10),
    certificate_number VARCHAR(30) UNIQUE,
    issue_date DATE,
    eligibility_status VARCHAR(20)
);
INSERT INTO Certificate VALUES
('CERT001', 'E001', 'CERT-PY-001', '2026-09-27', 'Eligible'),('CERT002', 'E002', 'CERT-PY-002', '2026-09-27', 'Eligible'),
('CERT003', 'E003', 'CERT-PY-003', '2026-09-27', 'Eligible'),('CERT004', 'E008', 'CERT-DB-001', '2026-09-15', 'Eligible'),
('CERT005', 'E010', 'CERT-ML-001', '2026-11-21', 'Eligible'),('CERT006', 'E011', 'CERT-ML-002', '2026-11-21', 'Eligible'),
('CERT007', 'E014', 'CERT-CY-001', '2026-10-31', 'Eligible'),('CERT008', 'E016', 'CERT-JAVA-001', '2026-10-18', 'Eligible');
