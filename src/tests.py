import unittest
from main import setup_logging

from preprocessing.tests import *
from models.tests import *
from analysis.tests import *
from classifiers.tests import *
from services.tests import *
from api.tests import *
from noise.tests import *

if __name__ == "__main__":
    setup_logging()
    unittest.main()
