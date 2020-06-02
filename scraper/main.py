from the_daily_scraper import TheDailyScraper
import pandas as pd

def main():
    scraper = TheDailyScraper()
    episode_data = scraper.get_episode_data()

    # write data to file
    THE_DAILY_DATA_FILE_NAME = 'data/the_daily_episode_data.csv'
    episode_data_df = pd.DataFrame.from_dict(episode_data)
    episode_data_df.to_csv(THE_DAILY_DATA_FILE_NAME, index=False)

if __name__ == "__main__":
    main()


