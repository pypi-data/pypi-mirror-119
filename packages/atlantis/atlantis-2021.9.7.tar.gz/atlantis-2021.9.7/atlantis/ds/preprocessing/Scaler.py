from pyspark.sql import DataFrame
from pyspark.ml.feature import VectorAssembler, StandardScaler
from .disassemble import disassemble


class Scaler:
    def __init__(self, columns=None, with_mean=True, with_sd=True):
        """
        :type columns: list[str]
        :type with_mean: bool
        :type with_sd: bool
        """
        self._columns = columns
        self._assembler = None
        self._with_mean = with_mean
        self._with_sd = with_sd
        self._scaler = None
        self._fitted = False

    def fit(self, X):
        """
        :type X: DataFrame
        :rtype: Scaler
        """
        if self._columns is None:
            self._columns = X.columns
        self._assembler = VectorAssembler(inputCols=self._columns, outputCol='features')
        assembled = self._assembler.transform(X).select('features')
        self._scaler = StandardScaler(
            inputCol='features', outputCol='scaled_features',
            withMean=self._with_mean, withStd=self._with_sd
        ).fit(assembled)
        self._fitted = True
        return self

    def transform(self, X, return_vector=True):
        """
        :type X: DataFrame
        :type return_vector: bool
        :param return_vector: if True, the vector column will be returned
                            if False, the vector column will be disassembled
        :rtype: DataFrame
        """
        if not self._fitted:
            self.fit(X)

        assembled = self._assembler.transform(X).select(
            'features', *[col for col in X.columns if col not in self._columns]
        )
        df_scaled = self._scaler.transform(assembled).drop('features')
        if return_vector:
            return df_scaled
        else:
            names = [f'{col}_scaled' for col in self._columns]
            return disassemble(df_scaled, column='scaled_features', names=names, drop=True)

    fit_transform = transform
