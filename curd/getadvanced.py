###################################################################################
#imports
###################################################################################
from . import *
###################################################################################

def get_advanced(raw_query:str ,funcname:str,role_authorization : Callable,current_user :Callable=None,required_roles:List[str]=["none"], get_session : AsyncSession=None)->Callable:
         get_session=get_session
         async def get_advanced_response(request:Request,current_user:List[str]=Depends(current_user),session : AsyncSession=Depends(get_session)):
              if role_authorization(current_user,required_roles):  
                try:
                  curr_model=await session.execute(raw_query)
                  curr_model=curr_model.scalars().all()
                
                  return curr_model
                except Exception as e:
                  print(e)
                  return {"Message":"Some Error Occured"}
                  
                finally:
                  await session.close()
              return {"Message" :"Do not have required privileges to access this resource"}
         get_advanced_response.__name__=f"{funcname}_advanced_get_response"        
         return get_advanced_response