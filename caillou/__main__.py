import sys

from caillou import cli


def main() -> None:
    """Main function required for the script"""
    rc = 1
    try:
        cli()
        rc = 0
    except Exception as e:
        print("Error: %s" % e, file=sys.stderr)
    sys.exit(rc)


main()
