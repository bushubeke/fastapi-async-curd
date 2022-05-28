###################################################################################
#imports
###################################################################################
from . import *
###################################################################################

def get_one(sqlmod : Base,item_uuid:Optional[uuid.uuid4]=None, get_session : AsyncSession=None):
         current_sql_model=sqlmod
         
         get_session=get_session
         async def get_one_response(request:Request,item_uuid,session : AsyncSession=Depends(get_session)):
              
               try:
                 curr_model=await session.execute(select(current_sql_model).filter_by(id=int(item_uuid)))
                 curr_model=curr_model.scalars().first()
               
                 return curr_model
               except Exception as e:
                 print(e)
                 return {"Message":"Some Error Occured"}
                 
               finally:
                 await session.close()
                   
         model_name=current_sql_model.tableroute()          
         get_one_response.__name__=f"{model_name}_get_one_response"        
                
         return get_one_response