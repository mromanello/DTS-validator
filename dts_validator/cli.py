import sys
import pytest

def main():
    args = sys.argv[1:]
    sys.exit(pytest.main(args))

if __name__ == "__main__":
    args = sys.argv[1:]
    sys.exit(pytest.main(args))
    