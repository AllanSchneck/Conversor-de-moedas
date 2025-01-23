import requests
from os import getenv
from fastapi import HTTPException

API_KEY = getenv('ALPHAVANTAGE_APIKEY')

def sync_converter(from_currency:str,to_currency:str,price:float):
    url  = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={from_currency}&to_currency={to_currency}&apikey={API_KEY}"
    try: 
        response = requests.get(url=url)
    except Exception as error:
        raise HTTPException(status_code=400,detail=error)
    data = response.json()

    if "Realtime Currency Exchange Rate" not in data:
        raise HTTPException(status_code=400,detail=f"Realtime Currency Exchange Rate not in response {data}")
    #percebe que na nossa exceção estamos lançando ela com os dados que a Api deve nos retorna e porque?
    # se eu não importar os dados na exceção eu não saberei que dados ela está me retornando oq é meio óbvio porém
    # não tão óbvio em ambiente de trabalho por que você não terá acesso a API_KEY diretamente
    # e desta forma você sabera se de fato é um erro de input, lógica ou uma negação da própria Api Terceira
    exchange_rate = float(data['Realtime Currency Exchange Rate']['5. Exchange Rate'])
    # me retorna a cotação do dicionario requisitado

    return price * exchange_rate