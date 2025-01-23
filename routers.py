from fastapi import APIRouter, Path, Query
from converter import sync_converter
from schemas import ConverterInput,ConverterOutput

router = APIRouter(prefix='/converter')

@router.get('/{from_currency}')
def converter(
    from_currency : str = Path(max_length=3,regex='^[A-Z]{3}$'),
    to_currencies : str = Query(max_length=50,regex='^[A-Z]{3}(,[A-Z]{3})*$'),
    price: float = Query(gt=0)
):
    to_currencies = to_currencies.split(',')
    result = []
    for currency in to_currencies:
        response =  sync_converter(
            from_currency=from_currency,
            to_currency=currency,
            price=price
        )
        #percebe que estou lidando com o to_currency na rota e não na função
        # desta forma nós reduzimos problemas e dores de cabeça
        result.append(response)
    return result
# desta maneira estamos usando o split para separar cada palavra da lista por virgula



#Welcome to Alpha Vantage! 
# Your API key is: H8W6VSU98UHBX2MQ. 
# Please record this API key at a safe place for future data access.




@router.get('/v2/{from_currency}')
def converter(
    body: ConverterInput,
    from_currency : str = Path(max_length=3,regex='^[A-Z]{3}$')
):
    to_currencies = body.to_currencies
    price = body.price
    result = []
    for currency in to_currencies:
        response =  sync_converter(
            from_currency=from_currency,
            to_currency=currency,
            price=price
        )
        result.append(response)
    return result