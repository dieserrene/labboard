# initialises the MySQL Database. First checks if already present.
from db import get_connection

TABLES = [
    """
    CREATE TABLE IF NOT EXISTS users (
        id            INT AUTO_INCREMENT PRIMARY KEY,
        username      VARCHAR(50)  NOT NULL,
        email         VARCHAR(100) NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        role          ENUM('admin','operator','viewer') NOT NULL DEFAULT 'viewer',
        created_at    TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT email UNIQUE (email),
        CONSTRAINT username UNIQUE (username)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS servers (
        id          INT AUTO_INCREMENT PRIMARY KEY,
        name        VARCHAR(100) NOT NULL,
        hostname    VARCHAR(150) NOT NULL,
        ip_address  VARCHAR(45)  NOT NULL,
        environment ENUM('production','staging','homelab') NOT NULL DEFAULT 'homelab',
        description TEXT NULL,
        created_at  TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at  TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        CONSTRAINT hostname UNIQUE (hostname)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS services (
        id          INT AUTO_INCREMENT PRIMARY KEY,
        server_id   INT NOT NULL,
        name        VARCHAR(100) NOT NULL,
        port        INT NULL,
        service_url VARCHAR(255) NULL,
        status      ENUM('active','inactive','maintenance') NOT NULL DEFAULT 'active',
        created_at  TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
        INDEX server_id (server_id),
        CONSTRAINT services_ibfk_1
            FOREIGN KEY (server_id) REFERENCES servers (id) ON DELETE CASCADE
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS server_access (
        user_id   INT NOT NULL,
        server_id INT NOT NULL,
        can_edit  TINYINT(1) NOT NULL DEFAULT 0,
        PRIMARY KEY (user_id, server_id),
        INDEX server_id (server_id),
        CONSTRAINT server_access_ibfk_1
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
        CONSTRAINT server_access_ibfk_2
            FOREIGN KEY (server_id) REFERENCES servers (id) ON DELETE CASCADE
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS maintenance_tasks (
        id                  INT AUTO_INCREMENT PRIMARY KEY,
        server_id           INT NOT NULL,
        assigned_to_user_id INT NULL,
        title               VARCHAR(150) NOT NULL,
        status              ENUM('pending','in_progress','done') NOT NULL DEFAULT 'pending',
        due_date            DATE NULL,
        created_at          TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
        INDEX assigned_to_user_id (assigned_to_user_id),
        INDEX server_id (server_id),
        CONSTRAINT maintenance_tasks_ibfk_1
            FOREIGN KEY (server_id) REFERENCES servers (id) ON DELETE CASCADE,
        CONSTRAINT maintenance_tasks_ibfk_2
            FOREIGN KEY (assigned_to_user_id) REFERENCES users (id) ON DELETE SET NULL
    )
    """,
]

def init_db():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            for statements in TABLES:
                cur.execute(statements)
        conn.commit()

    except Exception as e:
        print(f"error initialising the database: {e}")
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    init_db()
    print("Tabellen initialisiert.")
