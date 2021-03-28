import pandas as pd 
import numpy as np 
import pickle 
import yahoofinancials as yf 
from scipy.spatial.distance import cosine

class RecommendAndEvaluateStocks:
    def __init__(self):
        stocks_df = pd.read_csv('data/processed_data/processed_data.csv')
        stocks_df = stocks_df.rename(columns={'Unnamed: 0': 'symbol'})
        stocks_df.index = stocks_df['symbol']
        stocks_df.drop('symbol', axis=1, inplace=True)
        self.stocks_df = stocks_df

        prepared_stocks_data = np.load('data/processed_data/transformed_data.npy')
        self.prepared_stocks_df = pd.DataFrame(prepared_stocks_data, index = stocks_df.index, columns = stocks_df.columns[:-1])

        
        with open('model/pipeline', 'rb') as handle:
            self.pipeline = pickle.load(handle)
        
        clusters = np.array(stocks_df.cluster)
        with open('model/clusterer', 'rb') as handle:
            self.clusterer = pickle.load(handle)
        
    def n_most_similar_stocks(self, stocks, s, n):
        stock_similarities = []
        for ticker in stocks.index:
            stock = self.pipeline.transform(stocks.loc[[ticker]])
            stock_similarities.append((ticker, cosine(stock, s)))
        n_most_similar_stocks = sorted(stock_similarities, key=lambda x: x[1])[:n]
        n_most_similar_stock_tickers = [x[0] for x in n_most_similar_stocks]
        return self.stocks_df.loc[n_most_similar_stock_tickers]

    def get_stock_vector(self, ticker_bought):
        try:
            stock_data_df = self.stocks_df.drop('cluster', axis=1).loc[[ticker_bought]]
        except KeyError:
            columns = ['twoHundredDayAverage', 'averageDailyVolume10Day', 'fiftyDayAverage',
                    'averageVolume10days', 'beta', 'marketCap',
                    'priceToSalesTrailing12Months', 'fiftyTwoWeekHigh', 'forwardPE',
                    'fiftyTwoWeekLow']
            stock_data = yf.YahooFinancials(ticker_bought).get_summary_data()
            stock_data = pd.DataFrame.from_dict(stock_data, orient='index')
            stock_data_df = stock_data[columns]
        return stock_data_df

    def recommend_stock(self, future_risk_score, ticker_bought, amount_spent, amount_willing_to_spend):
        # prior risk score - how risky they think their purchase was
        # future risk score - how risky they want to be in the future
        if future_risk_score == 1:
            cluster = 1
        elif future_risk_score == 2:
            cluster = 4
        elif future_risk_score == 3:
            cluster = 3
        elif future_risk_score == 4:
            cluster = 0
        elif future_risk_score == 5:
            cluster = 2
        else:
            raise ValueError("Future risk score out of bounds.")
        
        stock = self.get_stock_vector(ticker_bought)
            
        spending_ratio = amount_willing_to_spend//amount_spent
        if spending_ratio == 0:
            n_stocks = 1
        elif 1 <= spending_ratio <= 3:
            n_stocks = 2
        elif 4 <= spending_ratio <= 7:
            n_stocks = 3
        elif 8 <= spending_ratio <= 10:
            n_stocks = 4
        else:
            n_stocks = 5
        
        stock_vector = self.pipeline.transform(stock)
        stocks_available = self.prepared_stocks_df[self.stocks_df.cluster == cluster]
        try:
            stocks_available = stocks_available.drop(ticker_bought)
        except KeyError:
            pass
        n_most_similar = self.n_most_similar_stocks(stocks_available, stock_vector, n_stocks)
        return n_most_similar
    
    def evaluate_perceived_risk(self, perceived_risk, ticker_bought):
        stock = self.get_stock_vector(ticker_bought)
        cluster = self.clusterer.predict(stock[['beta','marketCap']])[0]
        
        if cluster == 0:
            risk = 4
        elif cluster == 1:
            risk = 1
        elif cluster == 2:
            risk = 5
        elif cluster == 3:
            risk = 3
        elif cluster == 4:
            risk = 2
        
        risk_delta = risk - perceived_risk
        return risk_delta

if __name__ == "__main__":
    recs = RecommendAndEvaluateStocks()
    print(recs.evaluate_perceived_risk(1, 'GME'))
    print(list(recs.recommend_stock(5, 'GME', 100, 1000).index))
