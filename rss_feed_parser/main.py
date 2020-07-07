from the_daily_parser import TheDailyParser

def main():
    the_daily_parser = TheDailyParser()
    the_daily_parser.write_data_to_csv("./data/the_daily_episode_data.csv")
    the_daily_parser.csv_to_text_data("./data/the_daily_episode_data.csv", "../nlp/data/the_daily_data.txt")

if __name__ == "__main__":
    main()


