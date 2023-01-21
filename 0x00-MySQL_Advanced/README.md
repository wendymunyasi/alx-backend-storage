# Project Name
**0x00. MySQL advanced**

## Author's Details
Name: *Wendy Munyasi.*

Email: *wendymunyasi@gmail.com*

Tel: *+254707240068.*

##  Requirements

### Scripts
*   Allowed editors: `vi`, `vim`, `emacs`.
*   All your files will be executed on Ubuntu 20.04 LTS using `MySQL 5.7`).
*   All your files should end with a new line.
*   The first line of all your files should be a comment describing the task.
*   The length of your files will be tested using `wc`.
*   All SQL keywords should be in uppercase (`SELECT`, `WHERE`…).

## More Info
### Comments for your SQL file:
```
$ cat my_script.sql
-- 3 first students in the Batch ID=3
-- because Batch 3 is the best!
SELECT id, name FROM students WHERE batch_id = 3 ORDER BY created_at DESC LIMIT 3;
$
```

## Project Description

* **0. We are all unique!** - Write a SQL script that creates a table `users` following the given requirements. - `0-uniq_users.sql`.
* **1. In and not out** - Write a SQL script that creates a table `users` following the given requirements. - `1-country_users.sql`.
* **2. Best band ever!** - Write a SQL script that ranks country origins of bands, ordered by the number of (non-unique) fans. - `2-fans.sql`.
* **3. Old school band** - Write a SQL script that lists all bands with `Glam rock` as their main style, ranked by their longevity. - `3-glam_rock.sql`.
* **4. Buy buy buy** - Write a SQL script that creates a trigger that decreases the quantity of an item after adding a new order. - `4-store.sql`.
* **5. Email validation to sent** - Write a SQL script that creates a trigger that resets the attribute `valid_email` only when the `email` has been changed. - `5-valid_email.sql`.
* **6. Add bonus** - Write a SQL script that creates a stored procedure `AddBonus` that adds a new correction for a student. - `6-bonus.sql`.
* **7. Average score** - Write a SQL script that creates a stored procedure `ComputeAverageScoreForUser` that computes and store the average score for a student. - `7-average_score.sql`.
* **8. Optimize simple search** - Write a SQL script that creates an index `idx_name_first` on the table `names` and the first letter of `name`. - `8-index_my_names.sql`.
* **9. Optimize search and score** - Write a SQL script that creates an index `idx_name_first_score` on the table `names` and the first letter of `name` and the `score`. - `9-index_name_score.sql`.
* **10. Safe divide** - Write a SQL script that creates a function `SafeDiv` that divides (and returns) the first by the second number or returns 0 if the second number is equal to 0. - `10-div.sql`.
* **11. No table for a meeting** - Write a SQL script that creates a view `need_meeting` that lists all students that have a score under 80 (strict) and no `last_meeting` or more than 1 month. - `11-need_meeting.sql`.


## Collaborate

To collaborate, reach me through my email address wendymunyasi@gmail.com.
