from db.database import execute

def migrate():
    # users
    execute("""
    CREATE TABLE IF NOT EXISTS users (
      id BIGINT PRIMARY KEY AUTO_INCREMENT,
      name VARCHAR(120) NOT NULL,
      email VARCHAR(190) NOT NULL UNIQUE,
      password_hash VARCHAR(255) NOT NULL,
      role ENUM('participant','admin','judge','volunteer') NOT NULL DEFAULT 'participant',
      status ENUM('active','inactive') NOT NULL DEFAULT 'active',
      created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    # sessions
    execute("""
    CREATE TABLE IF NOT EXISTS sessions (
      id BIGINT PRIMARY KEY AUTO_INCREMENT,
      user_id BIGINT NOT NULL,
      session_token VARCHAR(128) NOT NULL UNIQUE,
      expires_at DATETIME NOT NULL,
      created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
      INDEX(user_id),
      CONSTRAINT fk_sessions_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    # site config
    execute("""
    CREATE TABLE IF NOT EXISTS site_config (
      id BIGINT PRIMARY KEY AUTO_INCREMENT,
      `key` VARCHAR(120) NOT NULL UNIQUE,
      `value` TEXT NULL,
      updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    # participant applications
    execute("""
    CREATE TABLE IF NOT EXISTS participant_applications (
      id BIGINT PRIMARY KEY AUTO_INCREMENT,
      user_id BIGINT NOT NULL,
      data_json JSON NULL,
      status ENUM('pending','approved','rejected') NOT NULL DEFAULT 'pending',
      created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
      INDEX(user_id),
      CONSTRAINT fk_app_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    # projects
    execute("""
    CREATE TABLE IF NOT EXISTS projects (
      id BIGINT PRIMARY KEY AUTO_INCREMENT,
      participant_id BIGINT NOT NULL,
      title VARCHAR(255) NULL,
      description TEXT NULL,
      team_members_json JSON NULL,
      updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
      UNIQUE KEY uniq_participant (participant_id),
      CONSTRAINT fk_project_participant FOREIGN KEY (participant_id) REFERENCES users(id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    # submissions
    execute("""
    CREATE TABLE IF NOT EXISTS submissions (
      id BIGINT PRIMARY KEY AUTO_INCREMENT,
      project_id BIGINT NOT NULL,
      file_path VARCHAR(500) NOT NULL,
      status ENUM('submitted','reviewed') NOT NULL DEFAULT 'submitted',
      submitted_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
      INDEX(project_id),
      CONSTRAINT fk_sub_project FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    # rooms
    execute("""
    CREATE TABLE IF NOT EXISTS rooms (
      id BIGINT PRIMARY KEY AUTO_INCREMENT,
      name VARCHAR(120) NOT NULL UNIQUE,
      created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    # room users
    execute("""
    CREATE TABLE IF NOT EXISTS room_users (
      id BIGINT PRIMARY KEY AUTO_INCREMENT,
      room_id BIGINT NOT NULL,
      user_id BIGINT NOT NULL,
      role_in_room ENUM('judge','volunteer') NOT NULL,
      UNIQUE KEY uniq_room_user_role (room_id, user_id, role_in_room),
      CONSTRAINT fk_ru_room FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE CASCADE,
      CONSTRAINT fk_ru_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    # room projects
    execute("""
    CREATE TABLE IF NOT EXISTS room_projects (
      id BIGINT PRIMARY KEY AUTO_INCREMENT,
      room_id BIGINT NOT NULL,
      project_id BIGINT NOT NULL,
      UNIQUE KEY uniq_room_project (room_id, project_id),
      CONSTRAINT fk_rp_room FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE CASCADE,
      CONSTRAINT fk_rp_project FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    # evaluations
    execute("""
    CREATE TABLE IF NOT EXISTS evaluations (
      id BIGINT PRIMARY KEY AUTO_INCREMENT,
      judge_id BIGINT NOT NULL,
      project_id BIGINT NOT NULL,
      score INT NOT NULL,
      comment TEXT NULL,
      created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
      UNIQUE KEY uniq_judge_project (judge_id, project_id),
      CONSTRAINT fk_ev_judge FOREIGN KEY (judge_id) REFERENCES users(id) ON DELETE CASCADE,
      CONSTRAINT fk_ev_project FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    # default admin (if not exists)
    from db.database import query_one, execute as exec2
    exists = query_one("SELECT id FROM users WHERE email=%s", ("admin@gmail.com",))
    if not exists:
        from auth.security import hash_password
        exec2(
            "INSERT INTO users (name,email,password_hash,role) VALUES (%s,%s,%s,%s)",
            ("Admin", "admin@gmail.com", hash_password("admin123"), "admin")
        )

if __name__ == "__main__":
    migrate()
    print("✅ Migration complete")
