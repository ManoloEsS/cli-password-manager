"""Empty service name in the modify flow must reprompt, not crash."""

import json
import os

import cli_password_manager.functions as functions


def _passwords_file():
    directory = os.path.dirname(os.path.abspath(functions.__file__))
    return os.path.join(directory, "passwords.json")


def test_empty_service_reprompts_instead_of_crashing(monkeypatch, capsys):
    path = _passwords_file()
    with open(path, "w") as f:
        json.dump({"svc": {"user": {"password": "encrypted"}}}, f)
    try:
        inputs = iter(["", "svc", "user"])
        monkeypatch.setattr("builtins.input", lambda *args: next(inputs))
        passkeys = iter(["", "word1 word2 word3 word4"])
        monkeypatch.setattr(
            "cli_password_manager.functions.getpass.getpass",
            lambda *args: next(passkeys),
        )
        functions.modify_remove_username()
        out = capsys.readouterr().out
        assert "Service name cannot be empty." in out
        with open(path) as f:
            assert json.load(f) == {}
    finally:
        if os.path.exists(path):
            os.remove(path)
