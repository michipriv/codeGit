# Filename: modules/github_api.py

from github import Github, GithubException


class GitHubAPI:
    """
    Verwaltet die Interaktion mit der GitHub-API mithilfe von PyGithub.
    """

    def __init__(self, token):
        """
        Initialisiert die GitHubAPI.

        Args:
            token (str): Der GitHub-Token für die Authentifizierung.
        """
        self.token = token
        self.github = Github(token)
        self.user = self.github.get_user()

    def repository_exists(self, repo_name):
        """
        Überprüft, ob ein Repository existiert.

        Args:
            repo_name (str): Der Name des Repositories.

        Returns:
            bool: True, wenn das Repository existiert, sonst False.
        """
        try:
            self.user.get_repo(repo_name)
            return True
        except GithubException as e:
            if e.status == 404:
                return False
            else:
                print(f"Fehler beim Überprüfen des Repositories: {e}")
                return False

    def create_repository(self, repo_name):
        """
        Erstellt ein neues privates Repository.

        Args:
            repo_name (str): Der Name des Repositories.

        Returns:
            bool: True, wenn das Repository erfolgreich erstellt wurde, sonst False.
        """
        try:
            self.user.create_repo(repo_name, private=True)
            print(f"Repository '{repo_name}' wurde erfolgreich erstellt.")
            return True
        except GithubException as e:
            print(f"Fehler beim Erstellen des Repositories: {e}")
            return False

    def get_commits(self, repo_name):
        """
        Ruft die Commits eines Repositories ab.

        Args:
            repo_name (str): Der Name des Repositories.

        Returns:
            list: Eine Liste von Commits oder None bei Fehler.
        """
        try:
            repo = self.user.get_repo(repo_name)
            commits = repo.get_commits()
            return commits
        except GithubException as e:
            print(f"Fehler beim Abrufen der Commits: {e}")
            return None


# EOF
