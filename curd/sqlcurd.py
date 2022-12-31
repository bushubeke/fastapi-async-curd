####################################################################################
# imports
#####################################################################################
from pkg_resources import require
from . import *
from .getallfunc import get_all
from .getfunc import get_one
from .deletefunc import delete_res
from .postfunc import post_one
from .putfunc import put_one
from .getadvanced import get_advanced
from .util import role_authorization
######################################################################################

class SQLAlchemyCURD:
    
    def __init__(self, app : FastAPI = None, session : AsyncSession=None ,engine : create_async_engine= None):
        """FastAPI CURD Generotor Object for SQLalchemy Declarative Base Models

        Args:
            app (FastAPI, optional): FastAPI application Object. Defaults to None.
            session (AsyncSession, optional): Asynchronous SQLalchemy sessionmaker. Defaults to None.
            engine (create_async_engine, optional): Asynchronous SQLalchemy engine maker. Defaults to None.
        """
        self.combmodels : List[List[Base,BaseModel,BaseModel]] = []
        self.app : FastAPI = None
        self.session : sessionmaker = None
        self.curdroute=APIRouter()
        self.engine: create_async_engine=None
        self.current_user : Callable=None
        if self.app is not None and self.engine is not None:
            self.init_app(app,session,engine)
     
    def  init_app(self, app : FastAPI = None,engine : create_async_engine= None)->None:
        """_summary_

        Args:
            app (FastAPI, optional): FastAPI application Object. Defaults to None.
            engine (create_async_engine, optional): Asynchronous SQLalchemy engine maker. Defaults to None.
        """
        if app is not None and engine is not None:
            self.app = app
            self.engine=engine
            self.session = sessionmaker(engine, expire_on_commit=False,class_=AsyncSession)
    
    def set_current_user(self,current : List[str])->None:
        """_summary_

        Args:
            current (List[str]): fetchs Oauth2 callable object.
        """
        self.current_user=current
    
    async def get_session(self,) -> AsyncSession:
          """"returns session to be used by the sqlalchemycurd object"""
          async with self.session() as session:
               yield session
    
    def add_curd(self, modlist,role_auth:Callable=role_authorization)->None:
        """Adding List of SQLalchemy and Pydantic validation model objects

        Args:
            modlist (List[List[Base,BaseModel,BaseModel]): List of sqlalchemy and pydantic models to be utilized for 
            role_auth (Callable, optional): function that takes two sets of lists and returns boolean value. Defaults to role_authorization function .
        """
        if modlist  is not None :
            self.combmodels=modlist     
        self.create_routes(role_auth)
         
    def create_routes(self,role_auth)-> None:
        xroute=self.curdroute 
        for x in self.combmodels:
            xroute.add_api_route(f"/{x[0].tableroute()}/all", get_all(x[0],get_session=self.get_session,role_authorization=role_auth,current_user=self.current_user),methods=["GET"])
            xroute.add_api_route(f"/{x[0].tableroute()}/{{item_uuid}}/",get_one(sqlmod=x[0],get_session=self.get_session,role_authorization=role_auth,current_user=self.current_user),response_model=x[1],methods=["GET"])
            xroute.add_api_route(f"/{x[0].tableroute()}",post_one(x[0],x[2],get_session=self.get_session,role_authorization=role_auth,current_user=self.current_user), methods=["POST"])
            xroute.add_api_route(f"/{x[0].tableroute()}/{{item_uuid}}/",put_one(x[0],x[1],get_session=self.get_session,role_authorization=role_auth,current_user=self.current_user), methods=["PUT"])
            xroute.add_api_route(f"/{x[0].tableroute()}/{{item_uuid}}/",delete_res(x[0],get_session=self.get_session,role_authorization=role_auth,current_user=self.current_user), methods=["DELETE"])
    

    def create_get_route(self,route_path :str ,raw_query:str ,funcname : str,required_roles : List[str]=["superuser"],role_auth:Callable=role_authorization,response_mod : BaseModel= None):
        """Creating Heavely Modified get Route

        Args:
            route_path (str): path to create the get route on
            raw_query (str): raw sql query to execute
            funcname (str): name of the callable callback function
            required_roles (List[str], optional):list of required roles to have access on the created route. Defaults to ["superuser"].
            role_auth (Callable, optional):a callable function that takes two lists available roles, and provided required roles. Defaults to role_authorization.
            response_mod (BaseModel, optional): pydantic basemodel to parse response with. Defaults to None.
        """
        xroute=self.curdroute
        xroute.add_api_route(f"/{route_path}", get_advanced(raw_query=raw_query,funcname=funcname,role_authorization=role_auth,current_user=self.current_user,required_roles=required_roles,get_session=self.get_session),response_model=response_mod,methods=["GET"])
    
    def include_apirouter(self,prefix:str="/")->None:
        """Mouting sqlalchemycurd Object API router

        Args:
            prefix (str, optional): url path to be used when mouting the genrated apirouter routes Defaults to "/".
        """
        if prefix !=  "/":
            self.app.include_router(self.curdroute,prefix=prefix)
        else:
            self.app.include_router(self.curdroute)