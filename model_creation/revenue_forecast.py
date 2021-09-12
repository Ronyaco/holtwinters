import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import pickle


df = pd.read_csv('D:\\Data Science\\Portfolio\Machine Learing Model Deploy in Flask\\model_creation\\routes.csv')
df['date'] = pd.to_datetime(df.date)
df["year"] = pd.to_numeric(df["year"], downcast="integer")
df["rev_passengers"] = pd.to_numeric(df["rev_passengers"], downcast="float")

df = df.loc[(df['year'] <= 2019) ]
data_model =df[['date', 'rev_passengers']]
data_model = data_model.reset_index(drop=True)

data_model = data_model.groupby('date').sum()

data_model = data_model.resample(rule='M').sum()#sampling, getting index out column date


model = ExponentialSmoothing(data_model, seasonal='mul', seasonal_periods=12).fit()#sesonality seems to be multiplicative

pickle.dump(model,open('D:\\Data Science\\Portfolio\\Machine Learing Model Deploy in Flask\\model_creation\\data\\model.pkl','wb'))
