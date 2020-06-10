import pandas as pd

THE_DAILY_DATA_FILE_PATH= "../rss_feed_parser/data/the_daily_episode_data.csv"

def main():
    episode_data_df = pd.read_csv(THE_DAILY_DATA_FILE_PATH)

    # write title and description to a different file
    titles = episode_data_df["title"].tolist()
    descriptions = episode_data_df["description"].tolist()

    # print(titles)
    # print(descriptions)



if __name__ == "__main__":
    main()

