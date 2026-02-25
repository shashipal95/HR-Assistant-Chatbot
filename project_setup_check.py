import os

REQUIRED_FOLDERS = ["data", "employee_vectordb", "hr_vectordb"]

REQUIRED_FILES = [
    "streamlit_app.py",
    "hr_logic.py",
    "prepare_embeddings.py",
    "ingest_employees.py",
    "ingest.py",
    "pyproject.toml",
]


def check_folders():
    print("\n📁 Checking folders...")
    for folder in REQUIRED_FOLDERS:
        if not os.path.exists(folder):
            print(f"❌ Missing folder: {folder} → Creating it")
            os.makedirs(folder)
        else:
            print(f"✅ Folder exists: {folder}")


def check_files():
    print("\n📄 Checking core files...")
    for file in REQUIRED_FILES:
        if not os.path.exists(file):
            print(f"❌ Missing file: {file}")
        else:
            print(f"✅ File exists: {file}")


def check_vector_dbs():
    print("\n🧠 Checking vector databases...")
    emp_db = os.path.exists("employee_vectordb/chroma.sqlite3")
    hr_db = os.path.exists("hr_vectordb/chroma.sqlite3")

    if emp_db:
        print("✅ Employee vector DB exists")
    else:
        print("⚠️ Employee vector DB missing → Run: python ingest_employees.py")

    if hr_db:
        print("✅ HR policy vector DB exists")
    else:
        print("⚠️ HR policy vector DB missing → Run: python ingest.py")


def main():
    print("🔍 HR Assistant Project Setup Check")
    print("=" * 40)
    check_folders()
    check_files()
    check_vector_dbs()
    print("\n✨ Setup check complete!")


if __name__ == "__main__":
    main()
