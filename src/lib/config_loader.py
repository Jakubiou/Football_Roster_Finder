import json
import os
from src.db.db_exceptions import ConfigError


def load_config(config_path: str) -> dict:
    if not os.path.exists(config_path):
        raise ConfigError(
            "Konfigurační soubor config.json nebyl nalezen.\n"
            "Zkontrolujte, že se nachází ve stejné složce jako aplikace."
        )

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            content = f.read().strip()

            if not content:
                raise ConfigError(
                    "Konfigurační soubor config.json je prázdný.\n"
                    "Vyplňte connectionString."
                )

            return json.loads(content)

    except json.JSONDecodeError:
        raise ConfigError(
            "Konfigurační soubor config.json má neplatný formát.\n"
            "Musí se jednat o platný JSON."
        )
