import os
import subprocess
import tempfile


def run_ruff_check(code: str) -> str:
    """
    Analyse le code Python avec Ruff.
    Retourne les erreurs détectées.
    """

    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = os.path.join(temp_dir, "code.py")

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(code)

        result = subprocess.run(
            ["ruff", "check", file_path],
            capture_output=True,
            text=True
        )

        if result.stdout:
            return result.stdout

        if result.stderr:
            return result.stderr

        return "Aucun problème détecté par Ruff."


def run_ruff_format(code: str) -> str:
    """
    Formate le code Python avec Ruff.
    Retourne le code formaté.
    """

    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = os.path.join(temp_dir, "code.py")

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(code)

        subprocess.run(
            ["ruff", "format", file_path],
            capture_output=True,
            text=True
        )

        with open(file_path, "r", encoding="utf-8") as file:
            formatted_code = file.read()

        return formatted_code