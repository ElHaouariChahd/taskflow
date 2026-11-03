import sqlite3


class TaskRepository:
    """Couche d'accès aux données : la seule qui parle à SQLite."""

    def __init__(self, db_path: str = "taskflow.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute(
            """CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                priority TEXT NOT NULL,
                done INTEGER NOT NULL DEFAULT 0)"""
        )
        self.conn.commit()

    def list_tasks(self, done=None):
        query, params = "SELECT * FROM tasks", ()
        if done is not None:
            query, params = query + " WHERE done = ?", (int(done),)
        rows = self.conn.execute(query + " ORDER BY id DESC", params).fetchall()
        return [self._to_dict(r) for r in rows]

    def get(self, task_id):
        row = self.conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        return self._to_dict(row) if row else None

    def create(self, title, priority):
        cur = self.conn.execute(
            "INSERT INTO tasks (title, priority) VALUES (?, ?)", (title, priority)
        )
        self.conn.commit()
        return self.get(cur.lastrowid)

    def update_done(self, task_id, done):
        self.conn.execute("UPDATE tasks SET done = ? WHERE id = ?", (int(done), task_id))
        self.conn.commit()
        return self.get(task_id)

    def delete(self, task_id):
        cur = self.conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.conn.commit()
        return cur.rowcount > 0

    @staticmethod
    def _to_dict(row):
        return {"id": row["id"], "title": row["title"],
                "priority": row["priority"], "done": bool(row["done"])}