from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import List
from pydantic import BaseModel, Field, constr
import uvicorn
import configparser
from exceptions.news_too_long_exception import NewsTooLongException
from services.assistant_service import AssistantService
from services.news_consumer import InfobaeNewsConsumer, APINewsConsumer
from schemas.schemas import GetAllNewsRequest, GetAllNewsResponse, GetOneNewsRequest, AllowedSource
import multiprocessing
import json


config = configparser.ConfigParser()
config.read('config.ini')
# configuration space

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
#services initialization
assistant_api_key = config['DEFAULT']['API-KEY']
news_api_key = config['DEFAULT']['API-KEY']
news_number = int(config['DEFAULT']['NEWS-NUMBER'])
assistant = AssistantService(assistant_api_key)
news_consumers = {
    AllowedSource.INFOBAE:InfobaeNewsConsumer(),
    AllowedSource.NEWSAPI: APINewsConsumer(news_api_key)
}


class NewsController():

        
    @app.get("/get-all-news/{source}")
    def get_all_news(source: AllowedSource, words_number: int, language: str, soft_limit: bool):

        request_object= GetAllNewsRequest(source=source, words_number=words_number, language=language, soft_limit=soft_limit)
        assistant.set_config(request_object.language, request_object.words_number, request_object.soft_limit)
        news_consumer = news_consumers[request_object.source]
        news_data = news_consumer.get_all()
        #removing the news without body (based on photos or videos)
        news_data = list(filter(lambda x: x is not None, news_data))
        news_summaries = []
        index = 0
        while len(news_summaries) < news_number and index < len(news_data):
            if index == 0:
                news = news_data[index:news_number]
                index += news_number
            else:
                news = news_data[previous_index:index]
            with multiprocessing.Pool(processes=news_number) as pool:
                news_summary = pool.map(assistant.get_news_resume,news)
            #filter the news that were not resumed
            news_summary_data = list(filter(lambda x: x is not None, news_summary))
            news_summaries.extend(news_summary_data)
            if len(news_summaries) < news_number:
            
                previous_index = index
                index += news_number-len(news_summaries)
            object_list = []
            for news in news_summaries:
                object_list.append(GetAllNewsResponse.NewsData(summary=news['summary'],link="{}".format(news['link']), title=news['title']))
        return GetAllNewsResponse(news=object_list)


    
    @app.get("/get-one-news/{source}")
    def get_news(source: AllowedSource, link: str, words_number: int, language: str, soft_limit: bool):
        try:
            request_object= GetOneNewsRequest(source=source, link=link, words_number=words_number, language=language, soft_limit=soft_limit)
            news_consumer = news_consumers[request_object.source]
            assistant.set_config(request_object.language, request_object.words_number, request_object.soft_limit)
            news_data = news_consumers[request_object.source].get_one(request_object.link)
            if news_data is None:
                raise Exception("The news doesn't have a text body")
            news_summary = assistant.get_news_resume(news_data)
            if news_summary is None:
                raise Exception("The news is too long to be summarized")

            return GetAllNewsResponse.NewsData(summary=news_summary['summary'],link="{}".format(news_summary['link']), title=news_summary['title'])
        except Exception as error:
            return {'error':error.args[0]}
    
    @app.get("/mock-one")
    def mock_one():
        return GetAllNewsResponse.NewsData(summary="El dólar Senebi se convierte en la principal cotización libre del mercado cambiario argentino, debido a la regulación del Banco Central y la Comisión Nacional de Valores. El Senebi es un tipo de cambio que no tiene límites al volumen que se puede operar y no cuenta con intervención del BCRA. Esta cotización surge de la negociación entre compradores y vendedores, sin intervención oficial. Los precios obtenidos en Senebi no son necesariamente los más competitivos, pero se busca liquidez. La operación se realiza en el segmento de Negociación Bilateral u OTC, que surge de la compra y venta de bonos.",link="https://www.infobae.com/economia/2023/05/01/volvio-el-dolar-senebi-que-es-cuanto-vale-y-quienes-podran-comprarlo")
    
    @app.get("/mock-all")
    def mock_one():
        return GetAllNewsResponse(news=[GetAllNewsResponse.NewsData(summary="El dólar Senebi se convierte en la principal cotización libre del mercado cambiario argentino, debido a la regulación del Banco Central y la Comisión Nacional de Valores. El Senebi es un tipo de cambio que no tiene límites al volumen que se puede operar y no cuenta con intervención del BCRA. Esta cotización surge de la negociación entre compradores y vendedores, sin intervención oficial. Los precios obtenidos en Senebi no son necesariamente los más competitivos, pero se busca liquidez. La operación se realiza en el segmento de Negociación Bilateral u OTC, que surge de la compra y venta de bonos.",link="https://www.infobae.com/economia/2023/05/01/volvio-el-dolar-senebi-que-es-cuanto-vale-y-quienes-podran-comprarlo"),
                                        GetAllNewsResponse.NewsData(summary="El dólar Senebi se convierte en la principal cotización libre del mercado cambiario argentino, debido a la regulación del Banco Central y la Comisión Nacional de Valores. El Senebi es un tipo de cambio que no tiene límites al volumen que se puede operar y no cuenta con intervención del BCRA. Esta cotización surge de la negociación entre compradores y vendedores, sin intervención oficial. Los precios obtenidos en Senebi no son necesariamente los más competitivos, pero se busca liquidez. La operación se realiza en el segmento de Negociación Bilateral u OTC, que surge de la compra y venta de bonos.",link="https://www.infobae.com/economia/2023/05/01/volvio-el-dolar-senebi-que-es-cuanto-vale-y-quienes-podran-comprarlo")])

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)