from flask import Flask, render_template , request, jsonify
import pandas as pd
import pickle


app = Flask(__name__)

model = pickle.load(open('..\\model_creation\\data\\model.pkl','rb'))


@app.route('/predict',methods=['POST'])
def predict():

    json_data = request.json
    start_date_year_month = json_data["start_date"]
    end_date_year_month = json_data["end_date"]

    if start_date_year_month and end_date_year_month:
        start_date= get_date(start_date_year_month)
        end_date= get_date(end_date_year_month)
        pred = graph_prediction(start_date, end_date)
        data_model = graph_data()
        full_data = join_datasets(data_model,pred)
        full_data.index = pd.to_datetime(full_data.index, format = '%Y/%m/%d').strftime('%m-%Y')
        full_data_json= full_data.to_json(orient="table")
        return jsonify(full_data_json)

    else:
        data_model = graph_data()
        data_model.index = pd.to_datetime(data_model.index, format = '%Y/%m/%d').strftime('%m-%Y')
        data_model_json = data_model.to_json(orient="table")
        return jsonify(data_model_json)

@app.route('/', methods=['GET', 'POST'])
def home ():
    return render_template('index.html', href='static/base_pic.svg')
def join_datasets(df1,df2):
    df = df1.append(df2)
    df = df.groupby('date').sum()
    return df.resample(rule='M').sum()

def get_process_data():
    df = pd.read_csv('..\\model_creation\\routes.csv')
    df['date'] = pd.to_datetime(df.date)
    df["year"] = pd.to_numeric(df["year"], downcast="integer")
    df["rev_passengers"] = pd.to_numeric(df["rev_passengers"], downcast="float")
    df = df.loc[(df['year'] <= 2019) ]
    df = df[['date', 'rev_passengers']]
    df = df.reset_index(drop=True)
    df = df.groupby('date').sum()
    return df.resample(rule='M').sum()

def graph_prediction(start_date,end_date):
    pred = model.predict(start=start_date, end=end_date)
    pred = pd.DataFrame(pred)
    pred.columns =['prediction']
    pred.index.name = 'date'
    pred['values'] = 0
    pred['prediction'] = pred['prediction'].astype('int64')
    return pred

def graph_data():
    data_model = get_process_data()
    dict = {'date': 'date',
    'rev_passengers': 'values'}
    data_model.rename(columns=dict, inplace=True)
    data_model['prediction'] = 0
    return data_model

def get_date(date_input):
  date_input = date_input+'-01'
  date_output= pd.Period(date_input,freq='M').end_time.date() 
  date_output = date_output.strftime("%Y-%m-%d")
  return date_output


