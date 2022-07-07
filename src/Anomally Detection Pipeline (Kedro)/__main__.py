"""Anomaly Detection Pipeline (Kedro) file for ensuring the package is executable
as `Anomaly-Detection-Pipeline-Kedro` and `python -m anomaly_detection_pipeline_kedro`
"""
import importlib
from pathlib import Path

from kedro.framework.cli.utils import KedroCliError, load_entry_points
from kedro.framework.project import configure_project


class AnomalyDetectionRunner:
    def __init__(self, package_name):
        self.package_name = package_name

    def find_run_command(self):
        try:
            project_cli = importlib.import_module(f"{self.package_name}.cli")
            # Fail gracefully if cli.py does not exist
        except ModuleNotFoundError as exc:
            if f"{self.package_name}.cli" not in str(exc):
                raise
            plugins = load_entry_points("project")
            run = self._find_run_command_in_plugins(plugins) if plugins else None
            if run:
                # Use run command from an installed plugin if it exists
                return run
            # Use run command from the framework project
            from kedro.framework.cli.project import run

            return run
        # Fail badly if cli.py exists but has no `cli` in it
        if not hasattr(project_cli, "cli"):
            raise KedroCliError(f"Cannot load commands from {self.package_name}.cli")
        return project_cli.run

    @staticmethod
    def _find_run_command_in_plugins(plugins):
        for group in plugins:
            if "run" in group.commands:
                return group.commands["run"]

    def run(self):
        configure_project(self.package_name)
        run_command = self.find_run_command()
        run_command()


if __name__ == "__main__":
    package_name = Path(__file__).parent.name
    runner = AnomalyDetectionRunner(package_name)
    runner.run()

