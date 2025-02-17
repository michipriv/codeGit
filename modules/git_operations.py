# Filename: modules/git_operations.py

import os
import subprocess


class GitOperations:
    """
    Führt lokale Git-Operationen durch.
    """

    def __init__(self, token, repo_url):
        """
        Initialisiert die GitOperations.

        Args:
            token (str): Der GitHub-Token für die Authentifizierung.
            repo_url (str): Die URL des GitHub-Repositories.
        """
        self.token = token
        self.repo_url = repo_url

    def clone_repository(self, directory_path):
        """
        Klont das Repository in das angegebene Verzeichnis.

        Args:
            directory_path (str): Der Pfad zum Verzeichnis.
        """
        try:
            print(f"Klone Repository in {directory_path}...")
            correct_repo_url = self.repo_url.replace(
                "https://", f"https://{self.token}@"
            )
            subprocess.run(
                ["git", "clone", correct_repo_url, directory_path], check=True
            )
            print(f"Repository erfolgreich geklont nach {directory_path}.")
        except subprocess.CalledProcessError as e:
            print(f"Fehler beim Klonen des Repositories: {e}")

    def initialize_repository(self, directory_path):
        """
        Initialisiert ein Git-Repository, falls nicht vorhanden.

        Args:
            directory_path (str): Der Pfad zum Verzeichnis.
        """
        os.chdir(directory_path)
        if not os.path.exists(".git"):
            subprocess.run(["git", "init"], check=True)
            print("Git-Repository initialisiert.")
        else:
            print("Git-Repository existiert bereits.")

    def add_all(self):
        """
        Fügt alle Änderungen dem Index hinzu.
        """
        subprocess.run(["git", "add", "."], check=True)

    def commit(self, message):
        """
        Erstellt einen Commit mit der angegebenen Nachricht.

        Args:
            message (str): Die Commit-Nachricht.
        """
        subprocess.run(["git", "commit", "-m", message], check=True)

    def set_remote(self):
        """
        Setzt das Remote-Repository auf 'origin'.
        """
        subprocess.run(["git", "remote", "remove", "origin"], check=False)
        subprocess.run(["git", "remote", "add", "origin", self.repo_url], check=False)

    def push_all(self):
        """
        Pusht alle Branches zum Remote-Repository.
        """
        correct_repo_url = self.repo_url.replace("https://", f"https://{self.token}@")
        subprocess.run(["git", "push", correct_repo_url, "--all"], check=True)

    def get_commit_count(self):
        """
        Gibt die Anzahl der Commits zurück.

        Returns:
            int: Die Anzahl der Commits.
        """
        result = subprocess.run(
            ["git", "rev-list", "--count", "HEAD"],
            stdout=subprocess.PIPE,
            text=True,
            check=True,
        )
        return int(result.stdout.strip())

    def get_commit_logs(self):
        """
        Gibt die Commit-Historie zurück.

        Returns:
            list: Eine Liste von Commit-Logs.
        """
        result = subprocess.run(
            ["git", "log", "--pretty=format:%H - %s"],
            stdout=subprocess.PIPE,
            text=True,
            check=True,
        )
        return result.stdout.strip().split("\n")

    def checkout(self, commit_hash):
        """
        Checkt den angegebenen Commit aus.

        Args:
            commit_hash (str): Der Hash des Commits.
        """
        subprocess.run(["git", "checkout", commit_hash], check=True)
        print(f"Checked out commit {commit_hash}.")

    def checkout_branch(self, branch_name):
        """
        Checkt den angegebenen Branch aus.

        Args:
            branch_name (str): Der Name des Branches.
        """
        subprocess.run(["git", "checkout", branch_name], check=True)
        print(f"Checked out branch {branch_name}.")

    def reset_hard(self, commit_hash):
        """
        Setzt den aktuellen Branch hart auf einen spezifischen Commit zurück.

        Args:
            commit_hash (str): Der Hash des Commits.
        """
        subprocess.run(["git", "reset", "--hard", commit_hash], check=True)
        print(f"Branch hart auf Commit {commit_hash} zurückgesetzt.")

    def create_or_checkout_branch(self, branch_name):
        """
        Erstellt oder checkt einen Branch aus.

        Args:
            branch_name (str): Der Name des Branches.
        """
        try:
            # Versuche, zum Branch zu wechseln
            subprocess.run(["git", "checkout", branch_name], check=True)
            print(f"Branch '{branch_name}' ausgecheckt.")
        except subprocess.CalledProcessError:
            # Branch existiert nicht, also erstellen wir ihn
            subprocess.run(["git", "checkout", "-b", branch_name], check=True)
            print(f"Branch '{branch_name}' erstellt und ausgecheckt.")

    def force_push(self, branch_name):
        """
        Force-Pusht den aktuellen Branch zum Remote-Repository.

        Args:
            branch_name (str): Der Name des Branches.
        """
        correct_repo_url = self.repo_url.replace("https://", f"https://{self.token}@")
        subprocess.run(
            ["git", "push", correct_repo_url, branch_name, "--force"], check=True
        )
        print(f"Branch '{branch_name}' wurde zum Remote-Repository gepusht (force).")


# EOF
