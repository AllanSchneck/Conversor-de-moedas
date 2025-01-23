from fastapi import FastAPI
from routers import router
from routers_async import router_async
app = FastAPI()

app.include_router(router=router)
app.include_router(router=router_async) # boa prática




@app.get('/hello-world') # prática ruim
def hello_word():
  return 'Hello world'
