import os
from tests.helpers import TestCWL

class TestPattern2(TestCWL):

    def setUp(self):
        super().setUp()
        self.entrypoint = "pattern-2"

    def tearDown(self):
        super().tearDown()

    def test_pattern_wrapped_cwl(self):
        self._wrapped_cwl_validation()
