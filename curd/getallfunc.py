###################################################################################
#imports
###################################################################################
from . import *
###################################################################################



def get_all(sqlmod : Base,get_session : AsyncSession=None):
         current_sql_model=sqlmod
         
         get_session=get_session
         async def get_all_response(request:Request,session : AsyncSession=Depends(get_session)):
              try:
               #  print('###1')
                cur_model= await session.execute(select(current_sql_model))
                cur_model=cur_model.scalars().all()
                
               #  print('###2')
                return cur_model
              except Exception as e:
                print(e)
                await session.rollback()
                return {"Message": "some Error Occured"}
              finally:
                await session.close()
         model_name=current_sql_model.tableroute()          
         get_all_response.__name__=f"{model_name}_get_all_response"       
         return get_all_response