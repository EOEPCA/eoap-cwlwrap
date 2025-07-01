import os
from tests.helpers import TestCWL

class TestPattern5(TestCWL):

    def setUp(self):
        super().setUp()
        self.app_cwl_file = os.path.join(os.path.dirname(__file__), "pattern-5/workflow.cwl")
        self.entrypoint = "pattern-5"

    def tearDown(self):
        super().tearDown()

    def test_pattern_validation(self):
        self._cwl_validation(self.app_cwl_file)

    def test_pattern_wrapped_cwl(self):
        self._wrapped_cwl_validation()
