from the_daily_parser import TheDailyParser

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import json

class Indexer:
    def __init__(self, key, endpoint):
        self.client = self.authenticate_client(key, endpoint)
        self.parser = TheDailyParser()
    
    def authenticate_client(self, key, endpoint):
        ta_credential = AzureKeyCredential(key)
        text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=ta_credential)
        return text_analytics_client
    
    def index_documents(self):
        df = self.parser.episode_info_as_df().head(1)
        dates = df["date"].tolist()
        descriptions = df["description"].tolist()
        titles = df["title"].tolist()
        durations = df["duration"].tolist()
        links = df["link"].tolist()

        try:
            key_phrases_response = self.client.extract_key_phrases(documents = descriptions)
            for i in range(0, len(key_phrases_response)):
                doc = key_phrases_response[i]

                to_persist = {}
                to_persist["title"] = titles[i]
                to_persist["date"] = dates[i]
                to_persist["description"] = descriptions[i]
                to_persist["link"] = links[i]
                to_persist["duration"] = durations[i]

                if not doc.is_error:
                    to_persist["keyPhrases"] = doc.key_phrases
                else:
                    print(doc.id, doc.error)
                
        except Exception as err:
            print("Encountered exception. {}".format(err))
