####################################################################################
# imports
#####################################################################################
from . import *
from .getallfunc import get_all
from .getfunc import get_one
from .deletefunc import delete_res
from .postfunc import post_one
from .putfunc import put_one
from .getadvanced import get_advanced

######################################################################################

class sqlalchemycurd:
    #
    def __init__(self, app : FastAPI = None, session : AsyncSession=None ,engine : create_async_engine= None):
        self.combmodels : List[List[Base,BaseModel]] = []
        self.app : FastAPI = None
        self.session : sessionmaker = None
        self.curdroute=APIRouter()
        self.engine: create_async_engine=None
        if self.app is not None and self.engine is not None:
            self.init_app(app,session,engine)
    # inistializing init app 
    def  init_app(self, app : FastAPI = None,engine : create_async_engine= None):
        if app is not None and engine is not None:
            self.app = app
            self.engine=engine
            self.session = sessionmaker(engine, expire_on_commit=False,class_=AsyncSession)
            
    # Dependency
    async def get_session(self,) -> AsyncSession:

          async with self.session() as session:
               yield session
    
    def add_curd(self, modlist):
        #    specroute=self.curdroute
         if modlist  is not None :
              self.combmodels=modlist 
              #print(self.combmodels) 
         self.create_routes()
         
    def create_routes(self,)-> None:
        xroute=self.curdroute
       
        for x in self.combmodels:
            xroute.add_api_route(f"/{x[0].tableroute()}/all", get_all(x[0],get_session=self.get_session),methods=["GET"])
            xroute.add_api_route(f"/{x[0].tableroute()}/{{item_uuid}}",get_one(x[0],get_session=self.get_session),response_model=x[1],methods=["GET"])
            xroute.add_api_route(f"/{x[0].tableroute()}",post_one(x[0],x[1],get_session=self.get_session), methods=["POST"])
            xroute.add_api_route(f"/{x[0].tableroute()}/{{item_uuid}}",put_one(x[0],x[1],get_session=self.get_session), methods=["PUT"])
            xroute.add_api_route(f"/{x[0].tableroute()}/{{item_uuid}}",delete_res(x[0],get_session=self.get_session), methods=["DELETE"])
 
        self.app.include_router(xroute)
    def create_get_route(self,route_path,raw_query:str ,funcname : str,response_mod : BaseModel= None):
        xroute=self.curdroute
        xroute.add_api_route(f"/{route_path}", get_advanced(raw_query=raw_query,funcname=funcname,response_mod=response_mod,get_session=self.get_session),methods=["GET"])
        