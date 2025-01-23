import re
from pydantic import BaseModel, Field,validator
from typing import List
# e como conseguimos trabalhar no nivel de tipagem aqui?
# para isso usaremos a biblioteca typing que é uma biblioteca nativa de python
# para dizer o tipo que esperamos dessa varíavel será lista colocamos entre colchetes o tipo primitivo
# fica semelhante a declarar uma lista em orientação a objetos ou arrays justamente por que estamos lidando com orientação a objetos

class ConverterInput(BaseModel):
    price: float = Field(gt=0)
    to_currencies: List[str]

    @validator('to_currencies')
    # validando atributo to_currencies
    def validate_to_currencies(cls, value):
        # para cada moeda estamos testando o currency por padrão se não der match com o padrão
        # ele lançara um erro com o currency junto
        for currency in value:
            if not re.match('^[A-Z]{3}$',currency):
                raise ValueError(f'Invalid Currency {currency}')
            
        return value
        # sempre precisamos retornar o value caso a validação de certo por conta que se caso
        # faltar o nosso valor ficará nulo depois
             
# perceba que se nós usarmos desta maneira nós iremos perder as validações feitas por rota 
# Então agora ao invés de nós fazermos uma validação de query nós precisamos fazer uma validação de Field 
# porém nós temos um problema como nós vamos validar uma lista?
# como eu posso fazer uma validação mais complexa?
# como vamos validar cada item da lista?
# para isso nós temos o validator do próprio pydantic que é em formato de decorator
# então podemos criar uma função personalizada para validar esta lista 
# esta função precisa ter o parametro de classe por conta disso precisamos inserir o cls
# e precisamos receber o valor que vira do to_currencies
# então basicamente agora podemos fazer a validação que nós quisermos aqui dentro da função
# mas para seguirmos o modelo com regex precisamos importar a biblioteca re de regex do python

#estrutura mais o menos neste modelo de input que precisamos
"""
{
    "price": 12312,
    "to_currencies": ["USD", "EUR"]
}
"""
#OUTPUT COM PYDANTIC
class ConverterOutput(BaseModel):
    message: str
    data :List[dict]

    


#para trabalharmos com output iremos usar este cara aqui como referência untitled-1.json