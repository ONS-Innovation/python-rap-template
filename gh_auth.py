# This script checks if GitHub CLI is installed and authenticated.
import subprocess
import sys

def is_gh_installed():
    try:
        subprocess.run(["gh", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False

def is_gh_authenticated():
    try:
        result = subprocess.run(["gh", "auth", "status"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return "You are logged into" in result.stdout.decode()
    except subprocess.CalledProcessError:
        return False

def authenticate_gh():
    print("GitHub CLI is installed but not authenticated.")
    print("Please follow the prompts to authenticate with GitHub CLI.")
    subprocess.run(["gh", "auth", "login"])

def main():
    if not is_gh_installed():
        print("GitHub CLI (gh) is not installed. Please install it from https://cli.github.com/")
        sys.exit(1)
    if not is_gh_authenticated():
        authenticate_gh()
    else:
        print("GitHub CLI is installed and authenticated.")

if __name__ == "__main__":
    main()