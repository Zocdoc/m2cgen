import sys
import lightgbm
import pytest
import numpy as np
import xgboost
from sklearn import linear_model, svm
from sklearn import tree
from sklearn import ensemble

from tests import utils
from tests.e2e import executors


RECURSION_LIMIT = 5000


# pytest marks
PYTHON = pytest.mark.python
JAVA = pytest.mark.java
C = pytest.mark.c
GO = pytest.mark.go
JAVASCRIPT = pytest.mark.javascript
REGRESSION = pytest.mark.regr
CLASSIFICATION = pytest.mark.clf


# Set of helper functions to make parametrization less verbose.
def regression(model):
    return (
        model,
        utils.train_model_regression_random_data,
        REGRESSION,
    )


def classification(model):
    return (
        model,
        utils.train_model_classification_random_data,
        CLASSIFICATION,
    )


def classification_binary(model):
    return (
        model,
        utils.train_model_classification_binary_random_data,
        CLASSIFICATION,
    )


# Absolute tolerance. Used in np.isclose to compare 2 values.
# We compare 6 decimal digits.
ATOL = 1.e-6

RANDOM_SEED = 1234
XGBOOST_PARAMS = dict(base_score=0.6, n_estimators=100, max_depth=12,
                      random_state=RANDOM_SEED)
LIGHT_GBM_PARAMS = dict(n_estimators=100, num_leaves=100, max_depth=64,
                    random_state=RANDOM_SEED)


@utils.cartesian_e2e_params(
    # These are the languages which support all models specified in the
    # next list.
    [
        (executors.PythonExecutor, PYTHON),
        (executors.JavaExecutor, JAVA),
        (executors.CExecutor, C),
        (executors.GoExecutor, GO),
        (executors.JavascriptExecutor, JAVASCRIPT),
    ],

    # These models will be tested against each language specified in the
    # previous list.
    [
        # LightGBM
        regression(lightgbm.LGBMRegressor(**LIGHT_GBM_PARAMS)),
        classification(lightgbm.LGBMClassifier(**LIGHT_GBM_PARAMS)),
        classification_binary(lightgbm.LGBMClassifier(**LIGHT_GBM_PARAMS)),

        # XGBoost
        regression(xgboost.XGBRegressor(**XGBOOST_PARAMS)),
        classification(xgboost.XGBClassifier(**XGBOOST_PARAMS)),
        classification_binary(xgboost.XGBClassifier(**XGBOOST_PARAMS)),
    ],

    # Following is the list of extra tests for languages/models which are
    # not fully supported yet.

    # <empty>
)
def test_e2e_large_tress(estimator, executor_cls, model_trainer, is_fast):
    sys.setrecursionlimit(RECURSION_LIMIT)

    X_test, y_pred_true = model_trainer(estimator)
    executor = executor_cls(estimator)

    idxs_to_test = [0] if is_fast else range(len(X_test))

    with executor.prepare_then_cleanup():
        for idx in idxs_to_test:
            y_pred_executed = executor.predict(X_test[idx])
            print("expected={}, actual={}".format(y_pred_true[idx],
                                                  y_pred_executed))
            res = np.isclose(y_pred_true[idx], y_pred_executed, atol=ATOL)
            assert res if isinstance(res, bool) else res.all()
