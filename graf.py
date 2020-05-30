import matplotlib.pyplot as plt
import datetime
import requests
import json
import os

#Gera um gráfico automático partindo das informações acessadas na API
def generate_graf_new_cases():
    url = "https://coronavirus-monitor.p.rapidapi.com/coronavirus/cases_by_particular_country.php"

    querystring = {"country":"Brazil"}

    headers = {
        'x-rapidapi-host': "coronavirus-monitor.p.rapidapi.com",
        'x-rapidapi-key': "chave de acesso aqui"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    data = json.loads(response.text)['stat_by_country']
    values = list()
    days = list()

    month = str(datetime.date.today()).split("-")[1]
    days_data = dict()
    for d in data:
        if month == d['record_date'].split()[0].split("-")[1]:
            day = int(d['record_date'].split()[0].split("-")[2])
            value = d['new_cases']
            if len(value) >= 4:
                value = int("".join(value.split(",")))
            elif value == "":
                value = 0
            else:
                value = int(value)

            if day in days:
                days_data[day].append(value)
            else:
                days_data[day] = [value]

    for key in days_data.keys():
        values.append(max(days_data[key]))
        days.append(key)

    plt.scatter(days, values)
    plt.plot(days, values, color="blue", label = "Número de casos confirmados por dia")
    
def generate_graf_total_cases():
    url = "https://coronavirus-monitor.p.rapidapi.com/coronavirus/cases_by_particular_country.php"

    querystring = {"country":"Brazil"}

    headers = {
        'x-rapidapi-host': "coronavirus-monitor.p.rapidapi.com",
        'x-rapidapi-key': "chave de acesso aqui"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    data = json.loads(response.text)['stat_by_country']

    time = list()
    values = list()

    month = str(datetime.date.today()).split("-")[1]
    for d in data:
        if month == d['record_date'].split()[0].split('-')[1]:
            day = int(d['record_date'].split()[0].split('-')[2])
            hour = float(d["record_date"].split()[1].split(":")[0])/24
            minute = float(d["record_date"].split()[1].split(":")[1])/1440
            time.append(day + hour + minute)
            value = d["total_cases"]
            if len(value) >= 4:
                values.append(int("".join(value.split(","))))
            elif value == "":
                values.append(0)
            else:
                values.append(int(value))


    plt.plot(time, values, color="orange", label="Número de casos totais")

def generate_graf_new_deaths():
    url = "https://coronavirus-monitor.p.rapidapi.com/coronavirus/cases_by_particular_country.php"

    querystring = {"country":"Brazil"}

    headers = {
        'x-rapidapi-host': "coronavirus-monitor.p.rapidapi.com",
        'x-rapidapi-key': "chave de acesso aqui"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    data = json.loads(response.text)['stat_by_country']

    values = list()
    days = list()

    month = str(datetime.date.today()).split("-")[1]
    days_data = dict()
    for d in data:
        if month == d['record_date'].split()[0].split('-')[1]:
            day = int(d['record_date'].split()[0].split('-')[2])
            value = d["new_deaths"]
            if len(value) >= 4:
                value = int("".join(value.split(",")))
            elif value == "":
                value = 0
            else:
                value = int(value)

            if day in days:
                days_data[day].append(value)
            else:
                days_data[day] = [value]

    for key in days_data.keys():
        values.append(max(days_data[key]))
        days.append(key)
    
    plt.scatter(days, values)
    plt.plot(days, values, color="red", label="Número de mortes confirmadas por dia")

def generate_graf_total_deaths():
    url = "https://coronavirus-monitor.p.rapidapi.com/coronavirus/cases_by_particular_country.php"

    querystring = {"country":"Brazil"}

    headers = {
        'x-rapidapi-host': "coronavirus-monitor.p.rapidapi.com",
        'x-rapidapi-key': "chave de acesso aqui"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    data = json.loads(response.text)['stat_by_country']

    time = list()
    values = list()

    month = str(datetime.date.today()).split("-")[1]
    for d in data:
        if month == d['record_date'].split()[0].split('-')[1]:
            day = int(d['record_date'].split()[0].split('-')[2])
            hour = float(d["record_date"].split()[1].split(":")[0])/24
            minute = float(d["record_date"].split()[1].split(":")[1])/1440
            time.append(day + hour + minute)
            value = d["total_deaths"]
            if len(value) >= 4:
                values.append(int("".join(value.split(","))))
            elif value == "":
                values.append(0)
            else:
                values.append(int(value))
    
    plt.plot(time, values, color="black", label="Número de mortes totais")

def generate_graf():
    plt.clf()
    plt.cla()
    month = str(datetime.date.today()).split("-")[1]
    generate_graf_new_cases()
    generate_graf_new_deaths()
    generate_graf_total_cases()
    generate_graf_total_deaths()
    plt.xlabel("Dias do mês {}".format(month))
    plt.ylabel("Número de casos")
    plt.savefig("graf.png")

    return "graf.png"
