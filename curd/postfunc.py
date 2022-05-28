
###################################################################################
#imports
###################################################################################
from . import *
from .util import dataclass_to_dic
###################################################################################









def post_one(sqlmod : Base, pyMod : BaseModel, get_session : AsyncSession=None ):
              current_sql_model=sqlmod
              curmod=pyMod
              
              
              get_session=get_session
              async def post_response(request : Request,mod : curmod,session : AsyncSession=Depends(get_session)):
                   
                   data=dict(mod)
                   data=dataclass_to_dic(data)             
                   try:
                        
                        db_model_value=current_sql_model(**data)
                    #     print(db_model_value.password)
                    #     print("4 \n")
                        session.add(db_model_value)
                        await session.commit()
                        return {"Message":"insert has been sucessful"}                   
                        
                   except Exception as e :
                         print(e)
                         return {"Message":"Something is Wrong",
                                 "Error":{e}}
                         await session.rollback()
                         
                        
                   finally: 
                         
                         await session.close()
                         
                   
                   
              model_name=current_sql_model.tableroute()          
              post_response.__name__=f"{model_name}_post_response"  
              return post_response