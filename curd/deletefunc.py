###################################################################################
#imports
###################################################################################
from . import *
###################################################################################

def delete_res(sqlmod : Base,role_authorization : Callable, get_session : AsyncSession=None,current_user : Callable=None)->Callable:
          """DELETE response CURD response funciton Generator 

               Args:
                    sqlmod (Base): This is SQLalchemy Base model Object. 
                          Expects users to define "tableroute" property method. The method is used to return string which is used as "path"
                          by "FastAPI APIRouter".
           
                    role_authorization (Callable): a callable function that returns true or false, based on resource administration logic provided
                    
                    item_uuid (Optional[uuid.uuid4], required): uses uuid to fetch and remove object form database.Defaults to None.
                    
                    current_user (Callable, optional):Oauth2 schem authorization callabled function.returns list of available roles to the current user.
									Defaults to None.
                    get_session (AsyncSession, required ):The curd generator assumes the session passed on as argument is asynchronous. Defaults to None.


               Returns:
                    Callable: returns async return function which serves a route at the  provided table route method.
          """
          current_sql_model=sqlmod
          get_session=get_session
          async def delete_response(request : Request,item_uuid : uuid.UUID,current_user :List[str]=Depends(current_user), session : AsyncSession=Depends(get_session),):            
               if role_authorization(current_user,current_sql_model.write_roles()):     
                    if item_uuid == 'all':
                         try:
                              await session.execute(delete(current_sql_model))
                              await session.commit()
                              return {"Message" :"Sucessfully Deleted Rows"}
                         except Exception as e:
                              await session.rollback()
                              return {"Message":f"Failled to Sucessfully Delete Rows {e}",
                                   "Error" : f"{e}"}
                         finally:
                              await session.close()
                    else:
                         try:
                              await session.execute(delete(current_sql_model).where(current_sql_model.uuid == item_uuid))
                              await session.commit()
                              return {"Message" :"Sucessfully Deleted object"}
                         except Exception as e:
                              await session.rollback()
                              return {"Message":"Failled to Sucessfully object ","Error" : f"{e}"}
                         finally:
                              await session.close()
               return {"Message" :"Do not have required privileges to access this resource"}
          model_name=current_sql_model.tableroute()          
          delete_response.__name__=f"{model_name}_delete_one_or_all_response"       
          return delete_response