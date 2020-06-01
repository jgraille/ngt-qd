import pandas
import itertools


class Check:

    def __init__(self, filepath, exchange_rate):
        self._data = pandas.read_csv(filepath_or_buffer=filepath,
                                     parse_dates=[2])
        self._exchange_rate = exchange_rate

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        if isinstance(value, pandas.DataFrame):
            self._data = value
        else:
            raise TypeError("Value is not a dataframe")

    @property
    def exchange_rate(self):
        return self._exchange_rate

    @exchange_rate.setter
    def exchange_rate(self, value):
        if isinstance(value, dict):
            self._data = value
        else:
            raise TypeError("Value is not a dictionary")

    def checkone(self):
        """
        Checking duplicated rows
        Checking NA values
        :return: dict
        """
        out = []
        if not self._data[self._data.duplicated(keep=False)].empty:
            self._data.drop_duplicates(subset=None, keep='First', inplace=False)
            out.append(True)
        else:
            out.append(False)
        if self._data.isna().any(axis=None):
            out.append(self._data.isna().sum().to_dict())
        else:
            out.append(False)
        # self.data['count'] = self.data.groupby(['ISIN_Code', 'Valuation_Date']).transform('count')
        # print(self.data.loc[self.data['count'] > 1])
        return {'checkone': {'Action': 'Checking duplicated and Na values', 'duplicated': out[0], 'NA values': out[1]}}

    def checksecond(self):
        """
        Perform a currency conversion for shares to EUR
        Preparing the value to calculate the correlation
        :return: tuple(dict,dataframe)
        """
        for i, j in self._exchange_rate.items():
            self._data.loc[self._data['CCY_NAV_share'] == i, 'NAV_Per_Share'] = self._data.loc[self._data['CCY_NAV_share'] == i, 'NAV_Per_Share'].apply(lambda x: x/j)
        return {'checksecond': {'Action': 'Performing a currency conversion', 'Currency': self._exchange_rate}}, self._data

    def checkthird(self):
        """
        Performing outliers search for each isin
        :return: tuple(dict,list)
        """
        out = []
        isin = set(self._data['ISIN_Code'].values.tolist())
        features = self._data.columns
        features = [a for a in features if a in self._data.select_dtypes(include='number')]
        features.remove('Subfund_Code')
        for j in isin:
            data = self._data.loc[self.data['ISIN_Code'] == j].sort_values('Valuation_Date')

            data = data[features]
            n = int(0.70 * len(features))
            Q1 = data.quantile(q=0.25, axis=0)
            Q3 = data.quantile(q=0.75, axis=0)

            IQR = Q3 - Q1
            outlier_step = 1.5 * IQR
            indexes = []

            for i in features:
                # print('Processing column name: ', i)
                if (data[i] < Q1[i] - outlier_step[i]).any() or (data[i] > Q3[i] + outlier_step[i]).any():
                    res = data[i].loc[
                        (data[i] < Q1[i] - outlier_step[i]) | (data[i] > Q3[i] + outlier_step[i])].index.values
                    indexes.append(res.tolist())
            indexes = list(itertools.chain(*indexes))
            result = pandas.DataFrame(data=indexes, columns=['indexes'])
            result = result['indexes'].value_counts()
            result = result[result > n].index.values
            out.append(result)
        return {'checkthird': {'Action': 'Performing outliers search for each isin. For a 70% threshold, no outliers found'}}, out

"""
Try to overcome the "datetime.datetime not JSON serializable"
from bson import json_util
cannot import name 'json_util' from 'bson' (/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/bson/__init__.py)
"""








