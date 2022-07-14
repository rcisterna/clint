"""CLint command line interface."""
import sys
from typing import TextIO

import click

from .. import __version__
from ..result import Result
from .runner import Runner


class Command:
    """Command class for CLI arguments parsing."""

    @staticmethod
    def get_message(
        ctx: click.Context, param: click.Parameter, value: str
    ) -> str:  # pylint: disable=unused-argument
        """Get the commit message, from parameter value or from stdin stream."""
        if not value and not click.get_text_stream("stdin").isatty():
            return click.get_text_stream("stdin").read().strip()
        if value is None:
            raise click.exceptions.MissingParameter(ctx=ctx, param=param)
        return value

    @staticmethod
    @click.command()
    @click.argument(
        "message", callback=get_message.__func__, type=click.STRING, required=False
    )
    @click.option(
        "-f",
        "--file",
        type=click.File(),
        help="File path containing the commit message.",
    )
    @click.option(
        "--enable-hook/--disable-hook",
        default=None,
        help="Enable/Disable CLint as a handler for git 'commit-msg' hook.",
    )
    @click.version_option(__version__)
    def entrypoint(
        message: click.STRING,
        file: TextIO,
        enable_hook: click.BOOL,
    ):
        """CLint: A Conventional Commits Linter for your shell."""
        result: Result = None
        if enable_hook is None:
            if message:
                result = Runner.validate(message=message)
            elif file:
                result = Runner.validate(message=file.read())
        else:
            result = Runner.change_hook_handler(is_enabling=enable_hook)
        Command.show_result(result=result)
        sys.exit(result.return_code)

    @staticmethod
    def show_result(result: Result):
        """Print result values to the user."""
        for action, message in result.actions.items():
            click.echo(f"{action}: {message}")
