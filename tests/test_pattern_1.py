import os
from tests.helpers import TestCWL

class TestPattern1(TestCWL):

    def setUp(self):
        super().setUp()
        self.entrypoint = "pattern-1"

    def tearDown(self):
        super().tearDown()

    def test_pattern_wrapped_cwl(self):
        self._wrapped_cwl_validation()
