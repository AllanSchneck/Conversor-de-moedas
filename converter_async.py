
import aiohttp # é como se fosse uma versão assincrona do requests
from os import getenv
from fastapi import HTTPException

API_KEY = getenv('ALPHAVANTAGE_APIKEY')

async def async_converter(from_currency:str,to_currency:str,price:float):
    url  = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={from_currency}&to_currency={to_currency}&apikey={API_KEY}"
    try: 
        async with aiohttp.ClientSession() as session:
        # iremos pegar uma sessão do nosso aiohttp
            # e dentro da sessão iremos fazer a chamada http
            async with session.get(url=url) as reponse:
            #desta forma que eu consigo fazer uma request assincrona usando aiohttp
            # iremos pegar está resposta como response
                data = await reponse.json()
                # por que usamos await já aqui? 
                # porque aqui eu quero receber esse valor do retorno dessa função em dado não somente a corrotina 
                # por isso o await que serve para receber este valor que vai ser retornado no json
    except Exception as error:
        raise HTTPException(status_code=400,detail=error)

    if "Realtime Currency Exchange Rate" not in data:
        raise HTTPException(status_code=400,detail=f"Realtime Currency Exchange Rate not in response {data}")
    exchange_rate = float(data['Realtime Currency Exchange Rate']['5. Exchange Rate'])

    return {to_currency : price * exchange_rate}
# feito isso está pronto nossa vesão assincrona da biblioteca