# main.py
import argparse
from cli.cli import start_cl_interface
from utils.utils import my_quit_fn, Constants
from utils.utils_cli import exitProgram, printOutput


def main():
    parser = argparse.ArgumentParser(
        description="Your freedom-inspired ENIGMA machine emulator"
    )

    # Create mutually exclusive group for message/file
    operation_group = parser.add_mutually_exclusive_group()
    operation_group.add_argument(
        "-m", "--message", nargs="+", help="Message to encrypt"
    )
    operation_group.add_argument("-f", "--file", help="File to encrypt")

    # GUI flag
    parser.add_argument("--gui", action="store_true", help="Run in GUI mode")
    # Output file flag - only used with -m or -f
    parser.add_argument("-w", "--write", help="Output file to write results to")

    args = parser.parse_args()

    # Validate -w is only used with -m or -f
    if args.write and not (args.message or args.file):
        parser.error("The -w option can only be used with -m or -f")
    # Handle GUI mode first
    if args.gui:
        Constants.is_gui_mode = True
        print(printOutput("I am very sorry, but for now there is no GUI"))
        my_quit_fn()
        return  # Add return to prevent further execution

    # Handle CLI operations
    if args.message or args.file:
        Constants.is_cli_mode = True
        result = None

        if args.message:
            print("Sorry, message encryption not implemented yet")
            # full_message = " ".join(args.message)
            # result = encrypt_message(full_message)
            result = " ".join(args.message)  # Placeholder
        else:  # args.file must be True
            print("Sorry, file encryption not implemented yet")
            # result = encrypt_file(args.file)
            result = f"Encrypted content of {args.file}"  # Placeholder

        # Handle output
        if args.write:
            pass
            # write_to_file(result, args.write)
        else:
            printOutput(result)
    else:
        # Interactive CLI mode
        Constants.is_cli_mode = True
        printOutput("Running in CLI mode")
        start_cl_interface()


if __name__ == "__main__":
    try:
        main()
    finally:
        exitProgram()
