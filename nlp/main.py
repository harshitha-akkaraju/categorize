import pandas as pd

THE_DAILY_DATA_FILE_PATH = "../rss_feed_parser/data/the_daily_episode_data.csv"
TITLE_DESCRIPTION_DATA = "./data/the_daily_data.txt"

def main():
    episode_data_df = pd.read_csv(THE_DAILY_DATA_FILE_PATH)

    # write title and description to a different file
    titles = episode_data_df["title"].tolist()
    descriptions = episode_data_df["description"].tolist()

    writer = open(TITLE_DESCRIPTION_DATA,'w')
    for i in range(0, len(titles)):
        line = titles[i] + descriptions[i] + "\n"
        writer.write(line)
    
    writer.close()



if __name__ == "__main__":
    main()

