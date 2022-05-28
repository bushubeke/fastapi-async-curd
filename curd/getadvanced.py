###################################################################################
#imports
###################################################################################
from . import *
###################################################################################

def get_advanced(raw_query:str ,funcname:str,response_mod : BaseModel= None, get_session : AsyncSession=None):
         
         
         get_session=get_session
         async def get_advanced_response(request:Request,response_model=response_mod,session : AsyncSession=Depends(get_session)):
              
               try:
                 curr_model=await session.execute(raw_query)
                 curr_model=curr_model.scalars().all()
               
                 return curr_model
               except Exception as e:
                 print(e)
                 return {"Message":"Some Error Occured"}
                 
               finally:
                 await session.close()
                   
                 
         get_advanced_response.__name__=f"{funcname}_advanced_get_response"        
                
         return get_advanced_response