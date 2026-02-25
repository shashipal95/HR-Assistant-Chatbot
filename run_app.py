import os
import subprocess
import sys


def run_command(command_list):
    """Run a command safely without breaking on spaces."""
    subprocess.run(command_list)


def check_vector_db(path, ingest_script):
    if not os.path.exists(path):
        print(f"⚠️ {path} not found. Running {ingest_script}...")
        run_command([sys.executable, ingest_script])
    else:
        print(f"✅ Found vector DB: {path}")


def main():
    print("🚀 Starting HR Assistant Setup...\n")

    check_vector_db("employee_vectordb", "ingest_employees.py")
    check_vector_db("hr_vectordb", "ingest.py")

    print("\n🌐 Launching Streamlit app...\n")
    run_command([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"])


if __name__ == "__main__":
    main()
