# Filename: modules/github_repo_manager.py

import os
import shutil
import subprocess
from modules.github_api import GitHubAPI
from modules.git_operations import GitOperations
from github import GithubException


class GitHubRepoManager:
    """
    Verwaltet die Interaktion mit dem GitHub-Repository.
    """

    def __init__(self, token, repo_name):
        """
        Initialisiert den GitHubRepoManager.

        Args:
            token (str): Der GitHub-Token für die Authentifizierung.
            repo_name (str): Der Name des Repositories.
        """
        self.token = token
        self.repo_name = repo_name
        self.github_api = GitHubAPI(token)
        self.repo_url = (
            f"https://github.com/{self.github_api.user.login}/{repo_name}.git"
        )
        self.git_ops = GitOperations(token, self.repo_url)

    def create_or_update_github_repo(self):
        """
        Erstellt oder aktualisiert ein privates GitHub-Repository.

        Returns:
            str: Die URL des GitHub-Repositories oder None bei Fehler.
        """
        if self.github_api.repository_exists(self.repo_name):
            print(f"Repository '{self.repo_name}' existiert bereits.")
            return self.repo_url
        else:
            if self.github_api.create_repository(self.repo_name):
                print(f"Privates Repository '{self.repo_name}' erfolgreich erstellt.")
                return self.repo_url
            else:
                print("Fehler beim Erstellen des Repositories.")
                return None

    def clone_latest_version(self, directory_path):
        """
        Klont die neueste Version des Repositories, wenn das Verzeichnis nicht existiert.

        Args:
            directory_path (str): Der Pfad zum Verzeichnis.
        """
        if not os.path.exists(directory_path):
            self.git_ops.clone_repository(directory_path)
        else:
            print(f"Verzeichnis {directory_path} existiert bereits.")

    def push_to_github(self, directory_path, commit_message):
        """
        Pusht Änderungen zum GitHub-Repository.

        Args:
            directory_path (str): Der Pfad zum Verzeichnis.
            commit_message (str): Die Commit-Nachricht.
        """
        self.git_ops.initialize_repository(directory_path)
        self.git_ops.add_all()
        version_number = self.get_next_version_number(directory_path)
        full_commit_message = f"Version {version_number}: {commit_message}"
        try:
            self.git_ops.commit(full_commit_message)
        except subprocess.CalledProcessError as e:
            print("Keine Änderungen zum Committen gefunden.")
            return
        self.git_ops.set_remote()
        self.git_ops.push_all()
        print(f"Push erfolgreich: {full_commit_message}")

    def get_next_version_number(self, directory_path):
        """
        Bestimmt die nächste Versionsnummer.

        Args:
            directory_path (str): Der Pfad zum Verzeichnis.

        Returns:
            int: Die nächste Versionsnummer.
        """
        os.chdir(directory_path)
        try:
            count = self.git_ops.get_commit_count()
            return count + 1
        except subprocess.CalledProcessError:
            return 1

    def display_commit_log(self, directory_path):
        """
        Zeigt die eingecheckten Versionsnummern und Kommentare an.

        Args:
            directory_path (str): Der Pfad zum Verzeichnis.
        """
        if os.path.exists(directory_path) and os.path.exists(
            os.path.join(directory_path, ".git")
        ):
            os.chdir(directory_path)
            logs = self.git_ops.get_commit_logs()
            print("Commit-Historie (lokal):")
            for log in logs:
                print(log)
        else:
            commits = self.github_api.get_commits(self.repo_name)
            if commits:
                print("Commit-Historie (remote):")
                for commit in commits:
                    sha = commit.sha[:7]
                    message = commit.commit.message
                    print(f"{sha} - {message}")
            else:
                print("Keine Commits gefunden.")

    def restore_version(self, directory_path, version_identifier):
        """
        Stellt die angegebene Version wieder her und aktualisiert den master-Branch.

        Args:
            directory_path (str): Der Pfad zum Verzeichnis.
            version_identifier (str): Die Versionsnummer oder der Commit-Hash.
        """
        # Überprüfen, ob das Verzeichnis existiert und ggf. sichern
        if os.path.exists(directory_path):
            backup_path = f"{directory_path}.bak"
            try:
                if os.path.exists(backup_path):
                    shutil.rmtree(backup_path)
                os.rename(directory_path, backup_path)
                print(f"Bestehendes Verzeichnis wurde nach {backup_path} verschoben.")
            except Exception as e:
                print(f"Fehler beim Verschieben des Verzeichnisses: {e}")
                return
        else:
            print(
                f"Verzeichnis {directory_path} existiert nicht. Es wird neu erstellt."
            )

        # Klonen des Repositories
        self.clone_latest_version(directory_path)

        os.chdir(directory_path)

        # Überprüfen, ob es ein Git-Repository ist
        if not os.path.exists(".git"):
            print("Kein Git-Repository vorhanden.")
            return

        # Bestimmen des Commit-Hashes
        if version_identifier.isdigit():
            commit_hash = self.get_commit_hash_by_version_number(
                int(version_identifier)
            )
            if not commit_hash:
                print(f"Keine Version mit der Nummer {version_identifier} gefunden.")
                return
        else:
            commit_hash = version_identifier

        try:
            # Erstellen oder Wechseln zum 'master'-Branch
            self.git_ops.create_or_checkout_branch("master")

            # Setze den 'master'-Branch hart auf den gewünschten Commit zurück
            self.git_ops.reset_hard(commit_hash)

            # Force-Push des 'master'-Branches zum Remote-Repository
            self.git_ops.force_push("master")

            print(
                f"Version {version_identifier} wurde erfolgreich wiederhergestellt und zum 'master'-Branch gepusht."
            )

        except subprocess.CalledProcessError as e:
            print(f"Fehler beim Wiederherstellen der Version: {e}")
        except Exception as e:
            print(f"Allgemeiner Fehler: {e}")

    def get_commit_hash_by_version_number(self, version_number):
        """
        Findet den Commit-Hash für eine gegebene Versionsnummer.

        Args:
            version_number (int): Die Versionsnummer.

        Returns:
            str: Der Commit-Hash oder None, falls nicht gefunden.
        """
        logs = self.git_ops.get_commit_logs()
        for log_entry in logs:
            commit_hash, message = log_entry.split(" - ", 1)
            if message.startswith(f"Version {version_number}:"):
                return commit_hash
        return None


# EOF
