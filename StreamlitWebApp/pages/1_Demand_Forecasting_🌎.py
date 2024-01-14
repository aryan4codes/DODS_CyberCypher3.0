# Required Libraries and Settings

import numpy as np 
import pandas as pd 
from matplotlib import pyplot as plt
import seaborn as sns
from catboost import CatBoostRegressor
import streamlit as st
import warnings

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
warnings.filterwarnings('ignore')

# Load dataset
train = pd.read_csv(r'C:\AIML\CyberCypher3.0_Project\data\train.csv', parse_dates=['date'])
test = pd.read_csv(r'C:\AIML\CyberCypher3.0_Project\data\test.csv', parse_dates=['date'])
df = pd.concat([train, test], sort=False)  # Combine test and train for data preprocessing

st.title("Demand Forecasting App with CatBoost")
df.quantile([0, 0.05, 0.25, 0.50, 0.75, 0.95, 0.99, 1]).T
df["date"].min()
df["date"].max()

# Sales distribution
df["sales"].describe([0.10, 0.30, 0.50, 0.70, 0.80, 0.90, 0.95, 0.99])

# Number of stores
df["store"].nunique()

# Number of items
df["item"].nunique() 

# Are there an equal number of unique items in each store?
df.groupby(["store"])["item"].nunique()

# Sales statistics by store-item breakdown
df.groupby(["store", "item"]).agg({"sales": ["sum", "mean", "median", "std"]})

# Which month had sales?
df['month'] = df.date.dt.month

# Which day of the month had sales?
df['day_of_month'] = df.date.dt.day

# Which day of the year had sales?
df['day_of_year'] = df.date.dt.dayofyear 

# Which week of the year had sales?
df['week_of_year'] = df.date.dt.weekofyear

# Which day of the week had sales?
df['day_of_week'] = df.date.dt.dayofweek

# Which year had sales?
df['year'] = df.date.dt.year

# Is it a weekend or not?
df["is_wknd"] = df.date.dt.weekday // 4

# Is it the start of the month?
df['is_month_start'] = df.date.dt.is_month_start.astype(int)

# Is it the end of the month?
df['is_month_end'] = df.date.dt.is_month_end.astype(int) 

df.head()
st.write("Loading..")

# Sales statistics by store-item-month breakdown
df.groupby(["store", "item", "month"]).agg({"sales": ["sum", "mean", "median", "std"]})

def random_noise(dataframe):
    return np.random.normal(scale=1.6, size=(len(dataframe),))

df.sort_values(by=['store', 'item', 'date'], axis=0, inplace=True)
df.head()

def lag_features(dataframe, lags):
    for lag in lags:
        dataframe['sales_lag_' + str(lag)] = dataframe.groupby(["store", "item"])['sales'].transform(
            lambda x: x.shift(lag)) + random_noise(dataframe)
    return dataframe

df = lag_features(df, [91, 98, 105, 112, 119, 126, 182, 364, 546, 728])

def roll_mean_features(dataframe, windows):
    for window in windows:
        dataframe['sales_roll_mean_' + str(window)] = dataframe.groupby(["store", "item"])['sales']. \
                                                          transform(
            lambda x: x.shift(1).rolling(window=window, min_periods=10, win_type="triang").mean()) + random_noise(
            dataframe)
    return dataframe

df = roll_mean_features(df, [365, 546, 730])

def ewm_features(dataframe, alphas, lags):
    for alpha in alphas:
        for lag in lags:
            dataframe['sales_ewm_alpha_' + str(alpha).replace(".", "") + "_lag_" + str(lag)] = \
                dataframe.groupby(["store", "item"])['sales'].transform(lambda x: x.shift(lag).ewm(alpha=alpha).mean())
    return dataframe

alphas = [0.99, 0.95, 0.9, 0.8, 0.7, 0.5]
lags = [91, 98, 105, 112, 180, 270, 365, 546, 728]

df = ewm_features(df, alphas, lags)

# One-Hot Encoding
df = pd.get_dummies(df, columns=['day_of_week', 'month'])

# Converting sales to log(1+sales)
df['sales'] = np.log1p(df["sales"].values)

# Splitting the data into train and validation sets
train = df.loc[(df["date"] < "2017-01-01"), :]
val = df.loc[(df["date"] >= "2017-01-01") & (df["date"] < "2017-04-01"), :]

# Independent variables for train set
cols = [col for col in train.columns if col not in ['date', 'id', "sales", "year"]]

# Dependent variable for train set
Y_train = train['sales']

# Independent variables for train set
X_train = train[cols]

# Dependent variable for validation set
Y_val = val['sales']

# Independent variables for validation set
X_val = val[cols]

# Check shapes
Y_train.shape, X_train.shape, Y_val.shape, X_val.shape

# CatBoost parameters
catboost_params = {
    'iterations': 1000,
    'learning_rate': 0.05,
    'depth': 10,
    'l2_leaf_reg': 3,
    'loss_function': 'MAE',
    'verbose': 200,
    'random_seed': 42,
}

# Final Model using CatBoost

# Train CatBoost model
model = CatBoostRegressor(**catboost_params)
model.fit(X_train, Y_train, eval_set=(X_val, Y_val), use_best_model=True, plot=True)

# Predict on the testing set
test_preds = model.predict(X_val)

# Forecast for Store 1, Item 1
forecast = pd.DataFrame({
    "date": test["date"],
    "store": test["store"],
    "item": test["item"],
    "sales": test_preds
})

# Streamlit app
st.title("Sales Forecasting App with CatBoost")
st.write("Welcome to the World of Price Analysis")
# User input for store and item
store_input = st.slider("Select Store", min_value=1, max_value=df["store"].max(), value=1)
item_input = st.slider("Select Item", min_value=1, max_value=df["item"].max(), value=1)

# Button to trigger forecast generation
if st.button("Generate Forecast"):
    # Generate and display forecast
    input_data = X_val[(X_val['store'] == store_input) & (X_val['item'] == item_input)]
    forecast_data = pd.DataFrame({
        "date": input_data["date"],
        "store": input_data["store"],
        "item": input_data["item"],
        "sales": model.predict(input_data)
    })

    st.subheader(f"Forecast for Store {store_input}, Item {item_input}")
    st.line_chart(forecast_data.set_index("date")["sales"])
