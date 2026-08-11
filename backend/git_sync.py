import os
import subprocess


def push_to_github(app_name):
    repo_dir = os.path.expanduser("~/cloudoptima/generated")

    try:
        # Check that this is a Git repository
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            cwd=repo_dir,
            check=True,
            stdout=subprocess.DEVNULL,
        )

        # Stage generated IaC
        subprocess.run(
            ["git", "add", "."],
            cwd=repo_dir,
            check=True,
        )

        # Commit changes
        commit_msg = f"Auto-generated IaC for app: {app_name}"

        commit = subprocess.run(
            ["git", "commit", "-m", commit_msg],
            cwd=repo_dir,
            text=True,
            capture_output=True,
        )

        # Exit code 1 simply means there was nothing new to commit
        if commit.returncode != 0:
            if "nothing to commit" not in commit.stdout.lower():
                print("Git commit failed:")
                print(commit.stdout)
                print(commit.stderr)
                return False

        # Push using the already authenticated GitHub CLI/Git credentials
        subprocess.run(
            ["git", "push", "origin", "main"],
            cwd=repo_dir,
            check=True,
        )

        print(f"SUCCESS: Pushed IaC for {app_name} to GitHub")
        return True

    except subprocess.CalledProcessError as e:
        print(f"ERROR pushing to GitHub: {e}")
        return False
