###################################################################################
#imports
###################################################################################
from . import *
from .util import dataclass_to_dic
###################################################################################

def put_one(sqlmod : Base, pyMod : BaseModel,role_authorization : Callable,current_user:Callable=None, get_session : AsyncSession=None):
     """PUT response CURD response funciton Generator 

      Args:
            sqlmod (Base): This is SQLalchemy Base model Object. 
						Expects users to define "tableroute" property method. The method is used to return string which is used as "path"
						by "FastAPI APIRouter".
            pyMod (BaseModel): pydantic BaseModel object used to validate post requst data parametersl. 
            
            get_session (AsyncSession, required ):The curd generator assumes the session passed on as argument is asynchronous. Defaults to None.
            
            role_authorization (Callable): A funciton that takes two lists of role as arguments and returns boolean, if true path will be processed
            
            current_user (Callable, optional):Oauth2 schem authorization callabled function.returns list of available roles to the current user.
                                                      Defaults to None.
            get_session (AsyncSession, optional): asynchronous SQLalchemy session to be used to process the returned route. Defaults to None.
          
            
        

      Returns:
          Callable:returns asynchronous callback function to be mapped using fastapi aprouter defined path handling function
     """
     current_sql_model=sqlmod
     curmod=pyMod           
     get_session=get_session
     async def put_response(request : Request,item_uuid:uuid.UUID ,mod:curmod,current_user : List[str]=Depends(current_user), session : AsyncSession=Depends(get_session)):
          if role_authorization(current_user,current_sql_model.write_roles()):     
               data=dict(mod)
               data=dataclass_to_dic(data)
               try:
                    await session.execute(update(current_sql_model).where(current_sql_model.uuid==item_uuid).values(**data))
                    await session.commit()
                    return { f"Message" : f"sucessfully updated object "}
               except Exception as e:
                    print(e)
                    await session.rollback()
                    return { f"Message" : f"failed to sucessfully update object "}
               finally:
                    await session.close()
          return {"Message":"Do not have required privileges to access this resource"}
     model_name=current_sql_model.tableroute()          
     put_response.__name__=f"{model_name}_put_response"      
     return put_response 