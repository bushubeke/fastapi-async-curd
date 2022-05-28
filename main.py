
from fastapi import FastAPI,Header
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from curd.curd import sqlalchemycurd
from models.dbconnect import asyncengine
# from .models.dbconnect import async_session,engine
from models.dbmodels import TestingDataTypes,TestingTableModel


# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sqlcurd=sqlalchemycurd()
def create_dev_app():
    app=FastAPI()
    sqlcurd.init_app(app,asyncengine)
    
    origins = [ "*"]
    app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
            )
    modlist=[[TestingDataTypes,TestingTableModel]]
    
    #modlist=[[Role,RoleModel]]
    sqlcurd.add_curd(modlist)
    #sqlcurd.add_curd(Role,RoleModel)
    
    
    
    @app.get("/")
    def index(x_app_key: Optional[str] = Header(None) ,x_refresh_key: Optional[str] =Header(None)):
        return {"Message":"You should make your own index page"}
    
    return app
# subprocess.run(["gunicorn", "manage:app", "-k" ,"uvicorn.workers.UvicornWorker","-b" ,"0.0.0.0:9000","--reload","-w","1"]) 
# gunicorn main:app -k uvicorn.workers.UvicornWorker -b 0.0.0.0:9000 --reload -w 1
# https://packaging.python.org/en/latest/tutorials/packaging-projects/
app=create_dev_app()