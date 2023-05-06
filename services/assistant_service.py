import requests
import json
from exceptions.news_too_long_exception import NewsTooLongException


class AssistantService():
    def __init__(self,api_key:str):
        self.api_key = api_key
        self.model_engine = "gpt-3.5-turbo"

    def get_response(self, message):
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.api_key
        }
        data = {
            "model": self.model_engine,
            "messages": message,
            "temperature": 0.75,
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        return response.json()
    
    def set_config(self,language,words_number,soft_limit):
        self.language = language
        self.words_number = words_number
        self.soft_limit = soft_limit
    
    def get_news_resume(self,news):
        steps = [
            "These are your guidelines for the task: <START GUIDELINE>",
            "You have to resume news articles in {} language".format(self.language),
            "Your resume has to be {} words long as maximum".format(self.words_number),
            "You have to resume the following article: <START ARTICLE>",
            news['body'],
            "<END ARTICLE>",
            "<END GUIDELINE>"
        ]
        chat_history = [{
            "role":"system",
            "content": " \n".join(steps)
        }]
        try:
            response = self.get_response(chat_history)
            if response.get('error'):
                raise NewsTooLongException(response['error']['message'])
            news_summary = {'summary':response['choices'][0]["message"]["content"],'link': news['link'], 'title':news['title']}
            if not self.soft_limit:
                previous_tries = 0
                while len(news_summary['summary'].split()) > self.words_number and previous_tries < 2:
                    previous_tries += 1
                    steps = [
                        "These are your guidelines for the task: <START GUIDELINE>",
                        "You have to resume news articles in {} language".format(self.language),
                        "Your resume has to be {} words long as maximum".format(self.words_number - 5),
                        "You have to resume the following article: <START ARTICLE>",
                        "{}".format(news_summary["summary"]),
                        "<END ARTICLE>",
                        "<END GUIDELINE>"
                    ]
                    
                    response = self.get_response(chat_history)
                    news_summary = {'summary':response['choices'][0]["message"]["content"],'link': news['link'], 'title':news['title']} #it returns the IA message
        except NewsTooLongException as e:
            news_summary = None

        return news_summary 