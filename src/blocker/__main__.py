"""Command-line interface."""
import fire

from .blocker import Blocker


def main():
    """Main entry point for the command line interface of Blocker."""
    fire.Fire(Blocker().lookup)


if __name__ == "__main__":
    main()
