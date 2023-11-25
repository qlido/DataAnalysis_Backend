import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from getDatas import trends


def getTrendsGraph():
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
    for result in data['results']:
        df = pd.DataFrame(result['data'])
        plt.plot(df['period'], df['ratio'], label=result['keyword'][0])
    plt.rc('font', family='Malgun Gothic')
    plt.xlabel('Date')
    plt.ylabel('Ratio')
    plt.title('Keyword Trends')
    plt.legend()
    return plt
