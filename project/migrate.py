import os
import shutil
import subprocess

def delete_migration_files():
    migrations_path = os.path.join("app", "migrations")

    if not os.path.exists(migrations_path):
        print("Migrations folder not found:", migrations_path)
        return

    for root, dirs, files in os.walk(migrations_path):
        # Remove __pycache__ directories
        if "__pycache__" in dirs:
            pycache_path = os.path.join(root, "__pycache__")
            print("Removing:", pycache_path)
            shutil.rmtree(pycache_path)

        # Remove all migration files except __init__.py
        for file in files:
            if file != "__init__.py":
                file_path = os.path.join(root, file)
                print("Removing:", file_path)
                os.remove(file_path)


def delete_database():
    db_path = "db.sqlite3"
    if os.path.exists(db_path):
        print("Removing database:", db_path)
        os.remove(db_path)
    else:
        print("Database not found:", db_path)


def run_management_commands():
    commands = [
        ["python", "manage.py", "makemigrations"],
        ["python", "manage.py", "migrate"],
        ["python", "manage.py", "runserver"]
    ]

    for cmd in commands:
        print("Executing:", " ".join(cmd))
        subprocess.run(cmd)


if __name__ == "__main__":
    print("Cleaning migrations...")
    delete_migration_files()

    print("Deleting database...")
    delete_database()

    print("Running Django commands...")
    run_management_commands()
