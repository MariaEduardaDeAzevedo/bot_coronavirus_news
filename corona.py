import tweepy
from urllib.request import Request, urlopen
from datetime import datetime
from time import sleep
import requests
import json

#COVID-19 API
def get_data():
    url = "https://coronavirus-monitor.p.rapidapi.com/coronavirus/cases_by_country.php"

    headers = {
    'x-rapidapi-host': "coronavirus-monitor.p.rapidapi.com",
    'x-rapidapi-key': "8d56b929a4msh4e243a8667ce102p106a6cjsn10327daff739"
    }

    response = requests.request("GET", url, headers=headers)

    data = dict()
    
    for e in response.text.split("},"):
        if "brazil" in e.lower():
            data = json.loads(e + "}")
        
    return data

#Busca de palavras chave
def has(tweet):
    if "covid-19" in tweet.text.lower():
        return True
    elif "coronavírus" in tweet.text.lower():
        return True
    elif "pandemia" in tweet.text.lower():
        return True
    elif "epidemia" in tweet.text.lower():
        return True
    elif "quarentena" in tweet.text.lower():
        return True
    return False

#Retweeta posts contendo as palavras chave
def retweet(profile, api):
    for i in range(0, 11):
        try:
            if has(profile[i]) and str(profile[i].id):
                api.retweet(profile[i].id)
                print("rt em {profile[i].text} - id {profile[i].id}".format(profile[i].text, profile[i].id))
        except:
            print("já retweetado")

#Acessa os dados da API e formata o post do relatório de atualização
def tweet():
    data = get_data()
    confirm = data["cases"]
    death = data["deaths"]
    recovered = data["total_recovered"]
    new = data["new_cases"]
    qnt_1m = data["total_cases_per_1m_population"]
    text = """Coronavírus no Brasil
    
Total de casos: {}
Total de mortes: {}
Total de recuperações: {}
Novos casos confirmados hoje: {}
Casos por 1 milhão de habitantes: {}

Fonte: https://bit.ly/2UdkXLk""".format(confirm, death, recovered, new, qnt_1m)

    return text

#Atualização dos posts
def att(api):

    #Canais de notícia
    folha_sp = api.user_timeline(screen_name="folha")
    estadao = api.user_timeline(screen_name="Estadao")
    bbc_brasil = api.user_timeline(screen_name="bbcbrasil")
    uol = api.user_timeline(screen_name="UOLNoticias")
    min_saude = api.user_timeline(screen_name="minsaude")
    oms_br = api.user_timeline(screen_name="OPASOMSBrasil")

    #Retweets
    retweet(folha_sp, api)
    retweet(estadao, api)
    retweet(bbc_brasil, api)
    retweet(uol, api)
    retweet(min_saude, api)
    retweet(oms_br, api)

#Autenticação
#inserir as chaves dadas na sua conta de desenvolvedor abaixo, elas irão
#te dar o acesso direto à API do Twitter
auth = tweepy.OAuthHandler("consumer_key", "consumer_secret")
auth.set_access_token("key", "secret")

#Twitter API
api = tweepy.API(auth)

#Primeiro relatório postado
try:
    api.update_status(tweet())
    print("novo relatório postado", datetime.now())
except:
    print("relatório duplicado ou erro na API")
while True:
    #Post de Relatório
    try:
        api.update_status(tweet())
        print("novo relatório postado", datetime.now())
    except tweepy.TweepError:
        print("relatório duplicado ou erro na API")

    print("pausa", datetime.now())
    #Pausa na execução
    sleep(180)
    print("retorno", datetime.now())

    #Atualização da timeline
    att(api)
