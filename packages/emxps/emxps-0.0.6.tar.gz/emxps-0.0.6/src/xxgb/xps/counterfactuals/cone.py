import numpy as np
from tqdm import tqdm

from emutils.utils import keydefaultdict, np_sample
from emutils.geometry.cone import find_decision_boundary_between_multiple_points

from .api import BaseDiverseCounterfactualMethod

__all__ = ['ConeCounterfactuals']


class ConeCounterfactuals(BaseDiverseCounterfactualMethod):
    def __init__(
        self,
        model,
        data,
        normalizer=None,
        method=None,
        num_iters=100,
        earlystop_error=1e-8,
        scaler=None,
        max_samples=None,
        nb_diverse_counterfactuals=10,
        random_state=0,
        verbose=1,
        **kwargs
    ):

        if scaler is not None:
            raise NotImplementedError('Scaling is not supported by Cone.')

        super().__init__(model, scaler)

        self.normalizer = normalizer
        self.method = method
        self.num_iters = num_iters
        self.earlystop_error = earlystop_error
        self.kwargs = kwargs

        self._max_samples = min(max_samples or np.inf, nb_diverse_counterfactuals)
        self._nb_diverse_counterfactuals = nb_diverse_counterfactuals
        self._random_state = random_state

        self.data = data
        self.verbose = verbose

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        if data is not None:
            self._raw_data = self.preprocess(data)
            self._preds = self.model.predict(self._raw_data)

            self._data = keydefaultdict(
                lambda pred:
                np_sample(self._raw_data[self._preds != pred], n=self._max_samples, safe=True, seed=self._random_state)
            )
        else:
            self._raw_data = None
            self._preds = None
            self._data = None

    def __get_counterfactuals(self, x, pred):
        if self.data is not None:
            return np.array(
                find_decision_boundary_between_multiple_points(
                    x=x,
                    Y=self.data[pred],
                    model=self.model,
                    normalizer=self.normalizer,
                    norm_method=self.method,
                    num=self.num_iters,
                    error=self.earlystop_error,
                    method='counterfactual',
                    desc=None,
                    **self.kwargs,
                )
            )
        else:
            raise ValueError('Invalid state. `self.data` must be set.')

    def get_diverse_counterfactuals(self, X):
        X = self.preprocess(X)
        preds = self.model.predict(X)
        X_counter = []
        iters = tqdm(zip(X, preds)) if self.verbose else zip(X, preds)
        for x, pred in iters:
            X_counter.append(self.__get_counterfactuals(x, pred))

        return self.diverse_postprocess(X, X_counter)
