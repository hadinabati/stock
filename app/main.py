from fastapi import FastAPI
from router import grade, position, stock , category , persons , roles ,routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=grade.router, prefix='/grade', tags=['grade'])
app.include_router(router=position.router, prefix='/positions', tags=['positions'])
app.include_router(router=category.router, prefix='/category' , tags=['category'])
app.include_router(router=stock.router, prefix='/stock', tags=['stock'])
app.include_router(router=persons.router , prefix='/person' , tags=['person'])
app.include_router(router=roles.router , prefix='/role' , tags=['roles'])
app.include_router(router=routes.router , prefix='/routes' , tags=['routes'])
