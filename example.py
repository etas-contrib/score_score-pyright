"""Example Python file to test score-pyright."""


def add_numbers(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b


def main() -> None:
    """Main function."""
    result = add_numbers(1, 2)
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
