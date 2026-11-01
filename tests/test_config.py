import pytest

from src.letter.config import ConfigError, load_config

# Явно тестовий ключ: однакові символи, жодного реального значення.
TEST_KEY = """-----BEGIN FUTURE KEY-----
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
-----END FUTURE KEY-----"""  # gitleaks:allow — тестовий ключ, не секрет


@pytest.fixture
def env(monkeypatch):
    monkeypatch.setenv("FUTURE_KEY", TEST_KEY)
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
    monkeypatch.delenv("APP_ENV", raising=False)
    return monkeypatch


def test_key_from_env(env):
    cfg = load_config(env_file=None)
    assert cfg["FUTURE_KEY"].startswith("-----BEGIN FUTURE KEY-----")
    assert cfg["APP_ENV"] == "development"


def test_missing_variable_names_it_but_hides_values(env):
    env.delenv("FUTURE_KEY")
    with pytest.raises(ConfigError) as e:
        load_config(env_file=None)
    assert "FUTURE_KEY" in str(e.value)
    assert "sqlite" not in str(e.value)


def test_wrong_key_format(env):
    env.setenv("FUTURE_KEY", "not-a-key")
    with pytest.raises(ConfigError) as e:
        load_config(env_file=None)
    assert "not-a-key" not in str(e.value)
