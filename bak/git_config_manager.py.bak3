# Filename: modules/git_config_manager.py

import subprocess


class GitConfigManager:
    """
    Verwaltet die Git-Konfiguration für den Benutzer.
    """

    def setup_git_config(self):
        """
        Setzt die Git-Konfiguration für den globalen Benutzername und die E-Mail-Adresse.

        Die Werte sind festgelegt auf:
        - Name: Michael Mader
        - E-Mail: m.mader@hellpower.at
        """
        try:
            subprocess.run(
                ["git", "config", "--global", "user.name", "Michael Mader"], check=True
            )
            subprocess.run(
                ["git", "config", "--global", "user.email", "m.mader@hellpower.at"],
                check=True,
            )
            print("Git-Konfiguration erfolgreich festgelegt.")
        except subprocess.CalledProcessError as e:
            print(f"Fehler beim Setzen der Git-Konfiguration: {e}")


# EOF
