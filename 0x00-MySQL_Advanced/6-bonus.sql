-- Write a SQL script that creates a stored procedure AddBonus that adds a new correction for a student.

-- Requirements:
--      Procedure AddBonus is taking 3 inputs (in this order):
--      user_id, a users.id value (you can assume user_id is linked to an existing users)
--      project_name, a new or already exists projects - if no projects.name found in the table, you should create it
--      score, the score value for the correction
DROP PROCEDURE IF EXISTS AddBonus;
DELIMITER $$
CREATE PROCEDURE AddBonus (user_id INT, project_name VARCHAR(255), score FLOAT)
BEGIN
    DECLARE project_count INT DEFAULT 0;
    DECLARE project_id INT DEFAULT 0;

    SELECT COUNT(id)
        INTO project_count
        FROM projects
        WHERE name = project_name;
    IF project_count = 0 THEN
        INSERT INTO projects(name)
            VALUES(project_name);
    END IF;
    SELECT id
        INTO project_id
        FROM projects
        WHERE name = project_name;
    INSERT INTO corrections(user_id, project_id, score)
        VALUES (user_id, project_id, score);
END $$
DELIMITER ;
