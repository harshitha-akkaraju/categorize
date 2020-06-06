from the_daily_parser import TheDailyParser

def main():
    the_daily_parser = TheDailyParser()
    episode_data_df = the_daily_parser.episode_info_as_df()

    THE_DAILY_DATA_FILE_NAME= "data/the_daily_episode_data.csv"
    episode_data_df.to_csv(THE_DAILY_DATA_FILE_NAME, index=False)

if __name__ == "__main__":
    main()


