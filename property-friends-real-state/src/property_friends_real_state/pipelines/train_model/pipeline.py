from .nodes.train_model import train_model, predict_model
from .nodes.metrics import evaluate_model
from .nodes.get_train_cols import get_train_cols
from kedro.pipeline import Pipeline, node, pipeline

def model_run(**kwargs) -> Pipeline:
    return Pipeline(
        [   
            node(
                func=get_train_cols,
                inputs=['train', 'params:cols_drop'],
                outputs='train_cols',
                name="build_features",
            ),
            node(
                func=train_model,
                inputs=['train', 'train_cols', 'params:target', 'params:categorical_cols', 'params:hyper_params'],
                outputs='pipeline',
                name="train_model",
            ),
            node(
                func=predict_model,
                inputs=['pipeline', 'test', 'train_cols', 'params:target'],
                outputs=['test_target', 'test_predictions'],
                name="predict_model",
            ),
            node(
                func=evaluate_model,
                inputs=['test_target', 'test_predictions'],
                outputs='metrics',
                name="evaluate_model",
            )
        ]
    )