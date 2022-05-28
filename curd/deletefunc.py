###################################################################################
#imports
###################################################################################
from . import *
###################################################################################





def delete_res(sqlmod : Base,item_uuid:Optional[uuid.uuid4]=None, get_session : AsyncSession=None):
          current_sql_model=sqlmod

          get_session=get_session
          async def delete_response(request : Request,item_uuid, session : AsyncSession=Depends(get_session)):
             
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
                    
                         await session.execute(delete(current_sql_model).where(current_sql_model.uid == item_uuid))
                         await session.commit()
                         return {"Message" :"Sucessfully Deleted object"}
                    except Exception as e:
                         await session.rollback()
                         return {"Message":"Failled to Sucessfully object ","Error" : f"{e}"}
     
                    finally:
                         await session.close()
                                   
          model_name=current_sql_model.tableroute()          
          delete_response.__name__=f"{model_name}_delete_one_or_all_response"       
          return delete_response