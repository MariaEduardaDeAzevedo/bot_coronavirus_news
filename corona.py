import tweepy
from urllib.request import Request, urlopen
from datetime import datetime
from time import sleep
import requests
import json
from graf import generate_graf

#Acessa a API de dados sobre a doença
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
        
    return (data, url)


#Verifica se um post tem as palavras chaves procuradas
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

#Retweeta um post que contém as palavras chave
def retweet(profile, api):
    for i in range(0, 11):
        try:
            if has(profile[i]) and str(profile[i].id):
                api.retweet(profile[i].id)
                print("rt em {profile[i].text} - id {profile[i].id}".format(profile[i].text, profile[i].id))
        except:
            print("já retweetado")


#Formata o post de relatório
def tweet():
    data = get_data()[0]
    confirm = data["cases"]
    death = data["deaths"]
    recovered = data["total_recovered"]
    new = data["new_cases"]
    qnt_1m = data["total_cases_per_1m_population"]
    hour = 21 + datetime.now().hour if datetime.now().hour < 3 else datetime.now().hour - 3
    text = """Coronavírus no Brasil:
    

Total de casos: {}
Total de mortes: {}
Total de recuperações: {}
Novos casos confirmados hoje: {}
Casos por 1 milhão de habitantes: {}

Fonte: {} """.format(confirm, death, recovered, new, qnt_1m, get_data()[1])

    return text

#Atualiza a timeline
def att(api):

    #News
    folha_sp = api.user_timeline(screen_name="folha")
    estadao = api.user_timeline(screen_name="Estadao")
    bbc_brasil = api.user_timeline(screen_name="bbcbrasil")
    uol = api.user_timeline(screen_name="UOLNoticias")
    min_saude = api.user_timeline(screen_name="minsaude")
    oms_br = api.user_timeline(screen_name="OPASOMSBrasil")


    retweet(folha_sp, api)
    retweet(estadao, api)
    retweet(bbc_brasil, api)
    retweet(uol, api)
    retweet(min_saude, api)
    retweet(oms_br, api)

#Autenticação
auth = tweepy.OAuthHandler("consumer_key", "consumer_secret")
auth.set_access_token("key", "secret")

#API
api = tweepy.API(auth)
last_status = tweet()
#Primeiro relatório
try:
    api.update_with_media(generate_graf(), new_status)
except:
    print("ocorreu um erro")
while True:

    try:
        print(last_status)
        new_status = tweet()
        print(new_status)
        if last_status != new_status:
            api.update_with_media(generate_graf(), new_status)
            last_status = new_status
            print("novo relatório postado", datetime.now())
    except:
        print("ocorreu um erro")

    print("pausa", datetime.now())
    #Pausa na execução
    sleep(180)
    #Retorno da execução
    print("retorno", datetime.now())
    
    #Atualização da timeline
    att(api)
