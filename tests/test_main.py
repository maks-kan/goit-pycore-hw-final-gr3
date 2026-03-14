from main import format_team, format_title, main


def test_format_title_has_box_and_shadow() -> None:
    result = format_title("Hello")
    assert "╔" in result
    assert "║  Hello  ║" in result
    assert "╚" in result
    assert "░" in result


def test_format_team_lists_members() -> None:
    result = format_team("Team X", ["Alice", "Bob"])
    assert "Team X:" in result
    assert "● Alice" in result
    assert "● Bob" in result


def test_quit_command(monkeypatch, capsys) -> None:
    monkeypatch.setattr("builtins.input", lambda _: "quit")
    main()
    output = capsys.readouterr().out
    assert "Assistant Bot" in output
    assert "Good bye!" in output


def test_exit_command(monkeypatch, capsys) -> None:
    monkeypatch.setattr("builtins.input", lambda _: "exit")
    main()
    output = capsys.readouterr().out
    assert "Good bye!" in output


def test_close_command(monkeypatch, capsys) -> None:
    monkeypatch.setattr("builtins.input", lambda _: "close")
    main()
    output = capsys.readouterr().out
    assert "Good bye!" in output


def test_help_then_quit(monkeypatch, capsys) -> None:
    inputs = iter(["help", "quit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    main()
    output = capsys.readouterr().out
    assert output.count("Available commands:") == 2


def test_unknown_command(monkeypatch, capsys) -> None:
    inputs = iter(["foobar", "quit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    main()
    output = capsys.readouterr().out
    assert "Unknown command: foobar" in output


def test_eof_exits_gracefully(monkeypatch, capsys) -> None:
    def raise_eof(_: str) -> str:
        raise EOFError

    monkeypatch.setattr("builtins.input", raise_eof)
    main()
    output = capsys.readouterr().out
    assert "Good bye!" in output


def test_echo_command(monkeypatch, capsys) -> None:
    inputs = iter(["echo hello world", "quit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    main()
    output = capsys.readouterr().out
    assert "1: hello" in output
    assert "2: world" in output


def test_echo_with_quoted_args(monkeypatch, capsys) -> None:
    inputs = iter(['echo "hello world" foo', "quit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    main()
    output = capsys.readouterr().out
    assert "1: hello world" in output
    assert "2: foo" in output


def test_unmatched_quotes(monkeypatch, capsys) -> None:
    inputs = iter(['echo "hello', "quit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    main()
    output = capsys.readouterr().out
    assert "Invalid input: unmatched quotes." in output


def test_greeting_includes_all_sections(monkeypatch, capsys) -> None:
    monkeypatch.setattr("builtins.input", lambda _: "quit")
    main()
    output = capsys.readouterr().out
    assert "Assistant Bot" in output
    assert "Team #3:" in output
    assert "● Olga Shadrunova" in output
    assert "● Oleksandr Semychenkov" in output
    assert "Available commands:" in output
