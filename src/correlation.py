import pandas


class Corr:

    def __init__(self, data):
        self.data = data[['ISIN_Code', 'NAV_Per_Share', 'Valuation_Date']]

    def fill_date(self):
        """
        Fill the missing values with the mean because it wont alter the cov(X,Y) base on the E[X]
        :return: DataFrame
        """
        alldates = set(self.data['Valuation_Date'].unique())
        res = pandas.DataFrame(columns=['ISIN_Code', 'NAV_Per_Share', 'Valuation_Date'])
        isin = set(self.data['ISIN_Code'].values.tolist())
        for i in isin:
            data = self.data.loc[self.data['ISIN_Code'] == i].sort_values('Valuation_Date')
            existing_date = set(data['Valuation_Date'].unique())
            missingdates = {j for j in alldates if j not in existing_date}
            out_df = pandas.DataFrame(missingdates, columns=['Valuation_Date'])
            out_df['NAV_Per_Share'] = data.NAV_Per_Share.mean()
            out_df['ISIN_Code'] = i
            out_df = out_df[['ISIN_Code', 'NAV_Per_Share', 'Valuation_Date']]
            res = pandas.concat([res, out_df], ignore_index=True)
        return pandas.concat([res, self.data], ignore_index=True), isin

    def reshape(self):
        """
        Transposing the dataframe to be ready to apply the .corr() method.
        :return: DataFrame
        """
        data, isin = self.fill_date()
        res = pandas.DataFrame()
        for i in isin:
            tmp = data[data['ISIN_Code'] == i].sort_values('Valuation_Date')
            res[i] = tmp['NAV_Per_Share'].values.tolist()
        return res

    def calculate(self):
        """
        Applying the .corr() method
        :return: DataFrame
        """
        data = self.reshape()
        return data.corr(method='pearson')















