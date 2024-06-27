import unittest
import logging
import os

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="tests.log",
    encoding="utf-8",
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
)


if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = loader.discover(os.path.curdir, pattern='test_*.py')
    runner = unittest.TextTestRunner()
    runner.run(suite)
