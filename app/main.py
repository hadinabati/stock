from fastapi import FastAPI
from router import grade



app = FastAPI()

app.include_router(router=grade.router , prefix='/grade' ,tags=['grade'] )



