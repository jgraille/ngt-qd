from src.checks import Check
from src.correlation import Corr
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
filepath = BASE_DIR + '/data/ngt_file.csv'
CURRENCY_RATE_2018 = {'CZK': 25.6503, 'NOK': 9.603432, 'SGD': 1.53, 'USD': 1.18}


def main():
    cred = credentials.Certificate(BASE_DIR + '/cloudfunction/serviceaccountkey.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://ngttest-64cd5.firebaseio.com/'
    })
    check = Check(filepath=filepath, exchange_rate=CURRENCY_RATE_2018)
    check_second = check.checksecond()
    # Sending the file
    # check_second[1]['Valuation_Date'] = check_second[1]['Valuation_Date'].dt.strftime('%Y-%d-%m')
    correlation = Corr(data=check_second[1]).calculate()
    ref = db.reference('/')
    ref.set([check.checkone(), check_second[0], check.checkthird()[0], correlation.to_dict()])


if __name__ == '__main__':
    main()
