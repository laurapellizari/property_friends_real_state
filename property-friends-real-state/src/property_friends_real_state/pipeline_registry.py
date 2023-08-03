from kedro.pipeline import Pipeline
from property_friends_real_state.pipelines import model_run

def register_pipelines() -> dict:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """
    def _model_run():
        return model_run()

    return {
        '__default__': _model_run(),
    }
