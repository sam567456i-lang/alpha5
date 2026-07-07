"""
Master E2E Certification Runner
Executes all 30 domains sequentially to certify phase freeze.
"""
import pytest
import sys

if __name__ == "__main__":
    sys.exit(pytest.main(["-v", "."]))
