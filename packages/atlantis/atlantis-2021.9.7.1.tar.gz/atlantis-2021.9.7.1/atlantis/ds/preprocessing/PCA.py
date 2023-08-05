from pyspark.sql import DataFrame
from pyspark.ml.feature import VectorAssembler, PCA as SparkPCA
from .Scaler import Scaler
from .disassemble import disassemble


class PCA:
	def __init__(self, k=None, columns=None, scale=False, scale_with_means=True, scale_with_sd=True):
		"""

		:type k: int or NoneType
		:type columns: NoneType or list[str]
		:type scale: bool
		:type scale_with_means: bool
		:type scale_with_sd: bool
		"""
		self._columns = columns
		self._scale = scale
		self._assembler = None
		self._k = k

		self._scaler = None
		self._scale_with_means = scale_with_means
		self._scale_with_sd = scale_with_sd

		self._fitted = False

	def fit(self, X):
		"""
		:type X: DataFrame
		:rtype: PCA
		"""
		if self._columns is None:
			self._columns = X.columns

		if self._scale:
			self._scaler = Scaler(columns=self._columns, with_mean=self._scale_with_means, with_sd=self._scale_with_sd)
			scaled = self._scaler.fit_transform(X=X, return_vector=True)
			self._pca = SparkPCA(k=self._k, inputCol='scaled_features', outputCol='pca_features').fit(scaled)

		else:
			self._assembler = VectorAssembler(inputCols=self._columns, outputCol='features')
			assembled = self._assembler.transform(X).select('features')
			self._pca = SparkPCA(k=self._k, inputCol='features', outputCol='pca_features').fit(assembled)

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
			self.fit(X=X)

		if self._scale:
			scaled = self._scaler.transform(X=X, return_vector=True)
		else:
			scaled = self._assembler.transform(X).select(
				'features', *[col for col in X.columns if col not in self._columns]
			)

		transformed = self._pca.transform(X=scaled)
		if return_vector:
			return transformed

		else:
			names = [f'pca_{i}' for i in range(1, self._k + 1)]
			return disassemble(transformed, column='pca_features', names=names, drop=True)

	fit_transform = transform
