import jwt
import typer
import asyncio
import subprocess
from fastapi import FastAPI,Header,Depends,HTTPException,Request
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from models.dbconnect import asyncengine,async_main,droptables
from models.dbmodels import TestingDataTypes,TestingTableModel,TestingTablePostModel
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from json import  dumps as jsondumps,JSONDecoder
from passlib.hash import pbkdf2_sha512
from datetime import datetime,timedelta
from curd.sqlcurd import SQLAlchemyCURD
from models.config import settings

capp = typer.Typer()
sqlcurd= SQLAlchemyCURD()

def create_dev_app():
    app=FastAPI(title="Development CURD Generator App")
    ##########################################################
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
    async def get_current_user(token: str = Depends(oauth2_scheme)):
        user= jwt.decode(token,settings.SECRET_KEY,algorithms="HS256")
        user=user["data"]
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user=jsondumps(user)    
        user=JSONDecoder().decode(user)
        return user
    async def get_current_active_user(current_user=Depends(get_current_user)):
        if current_user: 
            return current_user["roles"]
        return ["none"]
    ##########################################################
    ##########################################################
    sqlcurd.init_app(app,asyncengine)
    sqlcurd.set_current_user(get_current_active_user)
    origins = [ "*"]
    app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
            )
    modlist=[[TestingDataTypes,TestingTableModel,TestingTablePostModel]]  
    sqlcurd.add_curd(modlist)
    sqlcurd.include_apirouter(prefix="/")
    @app.get("/")
    def index(x_app_key: Optional[str] = Header(None) ,x_refresh_key: Optional[str] =Header(None)):
        return {"Message":"You should make your own index page"}
    @app.post("/token")
    def auth_sample(request : Request, login_data : OAuth2PasswordRequestForm =Depends()):
        try:                              
            data={
                "roles":["superuser"],
                "password" : pbkdf2_sha512.using(rounds=25000,salt_size=80).hash("password")
            }
            if  pbkdf2_sha512.verify(login_data.password,data["password"]):
                exp=datetime.utcnow()+timedelta(hours=4)
                exp2=datetime.utcnow()+timedelta(hours=5)
                key=settings.SECRET_KEY 
                del data["password"]              
                token=jwt.encode({'data':data,'exp':exp},key,algorithm="HS256")
                reftoken=jwt.encode({'data':data,'exp':exp2},key,algorithm="HS256")
                return {"access_token": token,"refresh_token":reftoken, "token_type": "bearer"}
            else:
                raise HTTPException(status_code=400, detail="Incorrect username or password")
        except Exception as e:
                print(e)
                raise HTTPException(status_code=500, detail="Message: Something Unexpected Happended") 
    return app

app=create_dev_app()

@capp.command()
def upgrade():
    """creates  base models based on their methadata"""
    asyncio.run(async_main())
    
@capp.command()
def test():
    """runs the tests for the app in tests folder
    """
    subprocess.run(["pytest", "tests","--asyncio-mode=strict"])
@capp.command()
def run():
    """runns using uvicorn server
    """
    subprocess.run(["uvicorn", "main:app", "--host" ,"0.0.0.0","--port","9000","--reload"])
    
@capp.command()
def rung():
    """starts gunicorn server of the app with uvicorn works bound  to 0.0.0.0:9000 with one worker
    """
    subprocess.run(["gunicorn", "main:app", "-k" ,"uvicorn.workers.UvicornWorker","-b" ,"0.0.0.0:9000","--reload","-w","1"]) 
@capp.command()
def drop():
    """drops all tables created from provided database"""
    asyncio.run(droptables())

if __name__ == "__main__":
    capp()