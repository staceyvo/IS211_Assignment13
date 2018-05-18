


DROP TABLE IF EXISTS Students;
CREATE TABLE Students(
FirstName VARCHAR(100),
LastName VARCHAR(100),
Student_ID INT
);

DROP TABLE IF EXISTS Quizzes;
CREATE TABLE Quizzes(
Quiz_ID INT,
Quiz_Name VARCHAR(100),
Grade INT,
Question_Number INT
);

DROP TABLE IF EXISTS Results;
CREATE TABLE Results(
Student_ID INT,
Quiz_ID INT,
Grade INT
);


