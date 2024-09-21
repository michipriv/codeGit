# Filename: main.py

import argparse
import os
from modules.git_config_manager import GitConfigManager
from modules.github_repo_manager import GitHubRepoManager


def get_last_directory_name(directory_path):
    """
    Extrahiert den letzten Teil des Verzeichnispfads, um ihn als Repository-Namen zu verwenden.

    Args:
        directory_path (str): Der Pfad zum Verzeichnis.

    Returns:
        str: Der letzte Verzeichnisname.
    """
    return os.path.basename(os.path.normpath(directory_path))


def main():
    """
    Hauptfunktion, die den Benutzerinput verarbeitet und die entsprechenden Funktionen aufruft.
    """
    parser = argparse.ArgumentParser(
        description="Verzeichnis in ein privates GitHub-Repository hochladen oder Version wiederherstellen."
    )
    parser.add_argument("token", help="GitHub-Token für die Authentifizierung")
    parser.add_argument("directory_path", help="Pfad zum Verzeichnis")
    parser.add_argument(
        "-m", "--message", help="Commit-Nachricht für den Push", default="default"
    )
    parser.add_argument(
        "-l",
        "--log",
        action="store_true",
        help="Zeigt die eingecheckten Versionsnummern und Kommentare an",
    )
    parser.add_argument(
        "-r",
        "--restore",
        help="Stellt die angegebene Version wieder her (z.B. '5' oder Commit-Hash)",
    )

    args = parser.parse_args()

    # Git-Konfiguration festlegen
    git_config_manager = GitConfigManager()
    git_config_manager.setup_git_config()

    # Erhalte den letzten Verzeichnisnamen als Repository-Namen
    repo_name = get_last_directory_name(args.directory_path)

    # Erstelle GitHubRepoManager-Instanz
    github_repo_manager = GitHubRepoManager(args.token, repo_name)

    # Überprüfe, ob der Benutzer die Log anzeigen möchte
    if args.log:
        github_repo_manager.display_commit_log(args.directory_path)
        return

    # Überprüfe, ob der Benutzer eine Version wiederherstellen möchte
    if args.restore:
        github_repo_manager.restore_version(args.directory_path, args.restore)
        return

    # Erstelle oder aktualisiere das GitHub-Repository
    repo_url = github_repo_manager.create_or_update_github_repo()

    if repo_url:
        # Klone die neueste Version des Repositories, falls das Verzeichnis nicht existiert
        github_repo_manager.clone_latest_version(args.directory_path)

        # Verzeichnis zu GitHub pushen
        github_repo_manager.push_to_github(args.directory_path, args.message)


if __name__ == "__main__":
    main()

# EOF
