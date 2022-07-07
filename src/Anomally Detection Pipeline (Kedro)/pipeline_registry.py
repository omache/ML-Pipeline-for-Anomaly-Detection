from typing import Dict
from kedro.pipeline import Pipeline

from anomaly_detection_pipeline_kedro.pipelines import (
    data_engineering as de,
    data_science as ds,
    model_evaluation as me,
)


class PipelineRegistry:
    def __init__(self):
        self.pipelines = {}

    def register_pipeline(self, name: str, pipeline: Pipeline):
        self.pipelines[name] = pipeline

    def get_pipelines(self) -> Dict[str, Pipeline]:
        return self.pipelines


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.
    """
    pipeline_registry = PipelineRegistry()

    data_engineering_pipeline = de.create_pipeline()
    data_science_pipeline = ds.create_pipeline()
    model_evaluation_pipeline = me.create_pipeline()

    pipeline_registry.register_pipeline("de", data_engineering_pipeline)
    pipeline_registry.register_pipeline("ds", data_science_pipeline)
    pipeline_registry.register_pipeline("me", model_evaluation_pipeline)
    pipeline_registry.register_pipeline(
        "__default__",
        data_engineering_pipeline + data_science_pipeline + model_evaluation_pipeline,
    )

    return pipeline_registry.get_pipelines()
