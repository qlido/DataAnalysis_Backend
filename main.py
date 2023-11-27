import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
from getDatas import trends
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense


def getTrendsGraph():
    df = None
    plt.clf()
    df = pd.DataFrame.from_dict(trends).transpose()
    # Step 1: Reconstruct the DataFrame to track rank changes for each keyword
    ranked_df = pd.DataFrame()

    for col in df.columns:
        for idx, keyword in df[col].items():
            if keyword not in ranked_df.columns:
                ranked_df[keyword] = np.nan
            ranked_df.at[idx, keyword] = col + 1

    # Step 2: Plot the rank changes for each keyword
    plt.figure(figsize=(20, 10))

    for column in ranked_df.columns:
        plt.plot(ranked_df.index, ranked_df[column], marker='', linewidth=1, alpha=0.9, label=column)
    plt.rc('font', family='Malgun Gothic')
    plt.legend(loc=2, ncol=2)
    plt.title("Keyword Rank Changes Over Time", loc='left', fontsize=12, fontweight=0, color='orange')
    plt.xlabel("Date")
    plt.ylabel("Rank")
    plt.gca().invert_yaxis()
    plt.yticks(range(11))

    return plt


def getShoppingGraph(data):
    df = None
    plt.clf()
    plt.figure(figsize=(20, 10))
    for result in data['results']:
        df = pd.DataFrame(result['data'])
        plt.plot(df['period'], df['ratio'], label=result['keyword'][0])
    plt.rc('font', family='Malgun Gothic')
    plt.xlabel('Date')
    plt.ylabel('Ratio')
    plt.title('Keyword Trends')
    plt.xticks(rotation=45)
    plt.legend()
    return plt

def train_and_evaluate_model(data):
    plt.clf()
    # 데이터 전처리
    df = pd.DataFrame(data['data'])
    df['period'] = pd.to_datetime(df['period'])
    df.set_index('period', inplace=True)
    df.sort_index(inplace=True)

    # 데이터 전처리 (LSTM 모델을 위한)
    scaler = MinMaxScaler()
    df_scaled = scaler.fit_transform(df[['ratio']])

    # 데이터를 X, y로 변환
    X, y = [], []
    for i in range(len(df_scaled) - 1):
        X.append(df_scaled[i])
        y.append(df_scaled[i + 1])

    X, y = np.array(X), np.array(y)

    # 데이터를 훈련 및 테스트 세트로 분할
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # LSTM 모델 생성
    model = Sequential()
    model.add(LSTM(50, activation='relu', input_shape=(X_train.shape[1], 1)))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')

    # 모델 학습
    model.fit(X_train, y_train, epochs=50, batch_size=16, verbose=2)

    # 모델 평가
    mse = model.evaluate(X_test, y_test, verbose=0)
    print(f'Mean Squared Error on Test Set: {mse}')
    predictions = model.predict(X_test)
    plt.plot(y_test, label='True Values')
    plt.plot(predictions, label='Predictions')
    plt.legend()

    # 투자 여부 판단 및 우상향 여부 확인
    # 투자 여부 및 우상향 여부 판단
    investable = mse >= 50.0
    slope = (predictions[-1] - predictions[0]) / (len(predictions) - 1)
    upward_trend = slope > 0

    print(slope)

    return slope, plt






