"""CLint command line interface."""

import click

from .runner import Runner


class Command:
    """Command class for CLI arguments parsing."""

    @staticmethod
    @click.command(no_args_is_help=True)
    @click.argument("message", type=click.STRING, required=False)
    def entrypoint(message):
        """CLint: A Conventional Commits Linter for your shell."""
        result = Runner.validate(message=message)
        Command.show_result(result=result)

    @staticmethod
    def show_result(result: str):
        """Print result values to the user."""
        click.echo(result)
