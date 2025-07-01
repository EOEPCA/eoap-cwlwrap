import os
import unittest
from cwltool.main import main as cwlmain
from cwltool.context import LoadingContext, RuntimeContext
from cwltool.executors import NoopJobExecutor
from io import StringIO
from click.testing import CliRunner
from eoap_cwlwrap import builder as app

class TestCWL(unittest.TestCase):

    def validate_cwl_file(self, cwl_file) -> int:
        args = ["--enable-ext", "--validate", cwl_file]

        stream_err = StringIO()
        stream_out = StringIO()

        result = cwlmain(
            args,
            stdout=stream_out,
            stderr=stream_err,
            executor=NoopJobExecutor(),
            loadingContext=LoadingContext(),
            runtimeContext=RuntimeContext(),
        )
        if result != 0:
            print(stream_out.getvalue())
            raise RuntimeError(f"Validation failed with exit code {result}")
        return result

    def setUp(self):
        self.stagein_cwl_file = os.path.join(os.path.dirname(__file__), "templates/directory-stage-in.cwl")
        self.stageout_cwl_file = os.path.join(os.path.dirname(__file__), "templates/stage-out.cwl")

        self.app_cwl_file = None    
        self.entrypoint = None

    def tearDown(self):
        if os.path.exists(".wrapped.cwl"):
            os.remove(".wrapped.cwl")

    def _cwl_validation(self, app_cwl_file):
        return self.validate_cwl_file(app_cwl_file)

    def _wrapped_cwl_validation(self):

        # assert stage-in.cwl exists
        assert os.path.exists(self.stagein_cwl_file), f"Stage-in CWL file {self.stagein_cwl_file} does not exist"
        assert os.path.exists(self.stageout_cwl_file), f"Stage-out CWL file {self.stageout_cwl_file} does not exist"
        assert os.path.exists(self.app_cwl_file), f"App CWL file {self.app_cwl_file} does not exist"

        runner = CliRunner()
        result = runner.invoke(
            app.main,
            [
                "--directory-stage-in",
                self.stagein_cwl_file,
                "--stage-out",
                self.stageout_cwl_file,
                "--workflow-id",
                self.entrypoint,
                "--workflow",
                self.app_cwl_file,
                "--output",
                ".wrapped.cwl",
            ],
        )

        self.assertEqual(result.exit_code, 0, f"Wrapped CWL {self.app_cwl_file} validation failed: {result.output}")
        self.assertEqual(self._cwl_validation(".wrapped.cwl"), 0)
