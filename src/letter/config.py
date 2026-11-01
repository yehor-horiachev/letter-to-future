"""Конфігурація сервісу «Лист у майбутнє»: усі секрети беруться із середовища, а не з коду."""
import os
import sys

from dotenv import load_dotenv

REQUIRED = ["FUTURE_KEY", "DATABASE_URL"]
KEY_BEGIN = "-----BEGIN FUTURE KEY-----"
KEY_END = "-----END FUTURE KEY-----"


class ConfigError(SystemExit):
    """Зупинка застосунку з поясненням; значення секретів у повідомлення не потрапляють."""


def load_config(env_file: str | None = ".env") -> dict:
    if env_file:
        load_dotenv(env_file, override=False)  # локальний .env лише для комп'ютера розробника
    missing = [name for name in REQUIRED if not os.environ.get(name)]
    if missing:
        # називаємо змінні, але ніколи не друкуємо їх значень
        raise ConfigError(f"Не задано змінні середовища: {', '.join(missing)}. "
                          "Скопіюйте .env.example у .env і заповніть значення.")
    key = os.environ["FUTURE_KEY"].strip()
    if not (key.startswith(KEY_BEGIN) and key.endswith(KEY_END)):
        raise ConfigError("FUTURE_KEY має неправильний формат: очікується блок "
                          f"{KEY_BEGIN} … {KEY_END}.")
    return {
        "FUTURE_KEY": key,
        "DATABASE_URL": os.environ["DATABASE_URL"],
        "APP_ENV": os.environ.get("APP_ENV", "development"),
    }


if __name__ == "__main__":
    try:
        cfg = load_config()
    except ConfigError as e:
        sys.exit(str(e))
    print(f"Конфігурацію завантажено: APP_ENV={cfg['APP_ENV']}, FUTURE_KEY=***")
