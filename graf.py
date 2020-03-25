import matplotlib.pyplot as plt
import datetime
import requests
import json

#Gera um gráfico automático partindo das informações acessadas na API
def generate_graf():
    url = "https://coronavirus-monitor.p.rapidapi.com/coronavirus/cases_by_particular_country.php"

    querystring = {"country":"Brazil"}

    headers = {
        'x-rapidapi-host': "coronavirus-monitor.p.rapidapi.com",
        'x-rapidapi-key': "8d56b929a4msh4e243a8667ce102p106a6cjsn10327daff739"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    data = json.loads(response.text)["stat_by_country"]

    time = list()
    values = list()
    today = str(datetime.date.today())
    cases = 0
    month = str(datetime.date.today()).split("-")[1]
    print(month)
    for d in data:
        if month == d["record_date"].split()[0].split("-")[1]:
            day = int(d["record_date"].split()[0].split("-")[2])
            hour = float(d["record_date"].split()[1].split(":")[0])/24
            minute = float(d["record_date"].split()[1].split(":")[1])/1440
            time.append(day + hour + minute)
            value = d["total_cases"]
            if len(value) >= 4:
                values.append(int("".join(value.split(","))))
                cases = int("".join(value.split(",")))
            else:
                values.append(int(value))
                cases = int(value)

    plt.plot(time, values)
    plt.title("Número de casos confirmados no mês {} de 2020".format(month))
    plt.ylabel("Número de casos confirmados")
    plt.xlabel("Dias do mês {}".format(month))
    plt.savefig("graf.png", format="png")
    
    return "graf.png"
