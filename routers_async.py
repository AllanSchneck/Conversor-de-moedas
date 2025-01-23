from fastapi import APIRouter, Path, Query
from converter_async import async_converter
from asyncio import gather
from schemas import ConverterInput,ConverterOutput

router_async = APIRouter(prefix='/converter')

#quando todas as suas rotas tem o mesmo prefixo você pode utilizar desta maneira para economizar dedo kkk
#isso significa que todas as nossa rotas dentro do router vão começar com /converter

@router_async.get('/async/{from_currency}')
async def async_converter_router(
    from_currency : str = Path(max_length=3,regex='^[A-Z]{3}$'),
    to_currencies : str = Query(max_length=50,regex='^[A-Z]{3}(,[A-Z]{3})*$'),
    price: float = Query(gt=0)
):
    to_currencies = to_currencies.split(',')
    corroutines = []
    for currency in to_currencies:
        # lembrando quando eu não uso await a função em si não é executada ele apenas me retorna uma corrotina apenas
        # me retorna um instância da tarefa que irá ser executada
        # então não usaremos V aqui o await por conta que perderiamos toda a performance de corrotinas trabalharem
        # de forma concorrente
        coro =  async_converter(
            from_currency=from_currency,
            to_currency=currency,
            price=price
        )
        corroutines.append(coro)
        # percebe que agora nós conseguimos colocar em uma lista todas as corrotinas que precisam ser executadar?
        # e como que eu faço para adicionar elas em um EVENT LOOP para performar essas tasks? 
        # e executar todas as corrotinas juntas
        # para isso vamos usar o gather
    result = await gather(*corroutines)
    return result
    #esse parametro desintegra a lista e passa cada uma das corrotinas como parametro dento da função do gather
    # e agora sim colocamos await para as função retornarem o dado de fato
    



@router_async.get('/async/v2/{from_currency}', response_model=ConverterOutput) # este converterOutput como response_model
# não muda absolutamente nada no nosso código porém sim na documentação em no status code 200 que indicara que esperamos 
# uma lista de dicionario com o sucesso do request e uma mensagem
async def converter(
    body: ConverterInput,
    from_currency : str = Path(max_length=3,regex='^[A-Z]{3}$')
):
    to_currencies = body.to_currencies
    price = body.price
    coroutines = []
    for currency in to_currencies:
        coro =  async_converter(
            from_currency=from_currency,
            to_currency=currency,
            price=price
        )
        coroutines.append(coro)
    result = await gather(*coroutines)
    return ConverterOutput(
        message="sucess",
        data= result
    )
