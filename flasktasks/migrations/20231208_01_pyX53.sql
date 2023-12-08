--
-- depends:

CREATE TABLE tasks (
    task_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    due_date DATE
)