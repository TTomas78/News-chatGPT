import mechanicalsoup
import requests
from services.filter_service import FilterService
from newsapi import NewsApiClient
import multiprocessing

class NewsConsumer():
    def get_all(self):
        pass

    def get_one(self):
        pass


class InfobaeNewsConsumer(NewsConsumer):

    def __init__(self):
        self.url = "https://infobae.com"
        self.browser = mechanicalsoup.Browser()
        self.author_filter = FilterService(r".*/autor/.*")
        self.base_link_filter = FilterService(r".*www.infobae.com*")



    def get_all(self):
        page = self.browser.get(self.url)
        news = page.soup.select('div.d23-story-card-info a')
        news_links = [data['href'] for data in news]
        news_links_cleaned = list(set(filter(self.author_filter.remove_by_regex, news_links)))
        if len(news_links_cleaned) > 50:
            news_links_cleaned = news_links_cleaned[0:50]
        with multiprocessing.Pool(processes=10) as pool:
            news_data = pool.map(self.get_one, news_links_cleaned)
        return news_data


    def get_one(self, link):
        #si el link contiene la palabra infobae es un link externo, sino es un link interno
        if self.base_link_filter.remove_by_regex(link):
            link = self.url + link
        page = self.browser.get(link)
        news_body = page.soup.select('p.paragraph ')
        news_body_i = page.soup.select('p.paragraph i')
        news_parent_i = [news_body_i_data.parent for news_body_i_data in news_body_i]
        news = list(set(news_body) - set(news_parent_i))
        news_text_array = [data.text for data in news]
        news_text = "\n".join(news_text_array)
        if news_text == "":
            return None
        news_title = page.soup.select('h1.d23-article-headline')[0].text
        return {'body':news_text, 'title':news_title, 'link':link}

class APINewsConsumer(NewsConsumer):
    def __init__(self, api_key):
        self.url = "https://newsapi.org/v2"
        self.newsapi = NewsApiClient(api_key='b1aa0ece161849b08ffa8502aa24b809')

    def get_all(self):
        #get news from news api
        sources = self.newsapi.get_top_headlines()
        return sources
    
    def get_one(self,link):
        raise NotImplementedError("This method is not allowed for this source")