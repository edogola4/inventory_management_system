import click
from tabulate import tabulate
from colorama import Fore, Style

def print_success(message):
    """Print a success message in green."""
    click.echo(f"{Fore.GREEN}{message}{Style.RESET_ALL}")

def print_error(message):
    """Print an error message in red."""
    click.echo(f"{Fore.RED}Error: {message}{Style.RESET_ALL}")

def print_warning(message):
    """Print a warning message in yellow."""
    click.echo(f"{Fore.YELLOW}{message}{Style.RESET_ALL}")

def print_info(message):
    """Print an info message in blue."""
    click.echo(f"{Fore.BLUE}{message}{Style.RESET_ALL}")

def print_title(title):
    """Print a title in cyan with borders."""
    width = len(title) + 4
    click.echo(f"{Fore.CYAN}{'=' * width}")
    click.echo(f"= {title} =")
    click.echo(f"{'=' * width}{Style.RESET_ALL}")

def print_table(headers, rows):
    """Print data in table format."""
    if not rows:
        print_warning("No data to display")
        return
    click.echo(tabulate(rows, headers=headers, tablefmt="fancy_grid"))

def confirm_action(message="Are you sure?"):
    """Confirm an action with the user."""
    return click.confirm(message)

def get_input(prompt, validator=None, error_message="Invalid input"):
    """Get validated input from the user."""
    while True:
        value = click.prompt(prompt)
        if validator:
            try:
                validated = validator(value)
                return validated
            except ValueError as e:
                print_error(str(e) or error_message)
        else:
            return value

def validate_required_string(value, min_length=1):
    """Validate a required string."""
    if not value or len(value.strip()) < min_length:
        raise ValueError(f"Input must be at least {min_length} characters")
    return value.strip()

def validate_positive_number(value):
    """Validate a positive number."""
    try:
        num = float(value)
        if num < 0:
            raise ValueError()
        return num
    except (ValueError, TypeError):
        raise ValueError("Input must be a positive number")

def validate_positive_integer(value):
    """Validate a positive integer."""
    try:
        num = int(value)
        if num < 0:
            raise ValueError()
        return num
    except (ValueError, TypeError):
        raise ValueError("Input must be a positive integer")