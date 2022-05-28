###################################################################################
#imports
###################################################################################
from . import *
from .util import dataclass_to_dic
###################################################################################





def put_one(sqlmod : Base, pyMod : BaseModel,item_uuid:Optional[uuid.uuid4]=None, get_session : AsyncSession=None):
          
          current_sql_model=sqlmod
          curmod=pyMod
                     
          get_session=get_session
          async def put_response(request : Request,item_uuid,mod : curmod, session : AsyncSession=Depends(get_session)):
             
               
               data=dict(mod)
               data=dataclass_to_dic(data)
               try:
                    
                    await session.execute(update(current_sql_model).where(current_sql_model.id==int(item_uuid)).values(**data))
                    # print("####3")
                    await session.commit()
                    return { f"Message" : f"sucessfully updated object "}
               except Exception as e:
                    print(e)
                    await session.rollback()
                    return { f"Message" : f"failed to sucessfully update object "}
               finally:
                    await session.close()
          model_name=current_sql_model.tableroute()          
          put_response.__name__=f"{model_name}_put_response"      
          return put_response 