###################################################################################
#imports
###################################################################################
from uuid import uuid4
from . import *
###################################################################################

def get_one(sqlmod : Base,role_authorization : Callable,current_user: Callable=None, get_session : AsyncSession=None):
	"""GET response CURD response funciton Generator (retrives single Object)

	Args:
		sqlmod (Base): This is SQLalchemy Base model Object. 
						Expects users to define "tableroute" property method. The method is used to return string which is used as "path"
						by "FastAPI APIRouter".
		
		get_session (AsyncSession, required ):The curd generator assumes the session passed on as argument is asynchronous. Defaults to None.
		
		role_authorization (Callable): A funciton that takes two lists of role as arguments and returns boolean, if true path will be processed
		
		current_user (Callable, optional):Oauth2 schem authorization callabled function.returns list of available roles to the current user.
									Defaults to None.
		
		get_session (AsyncSession, optional): asynchronous SQLalchemy session to be used to process the returned route. Defaults to None.

	Returns:
		Callable:returns asynchronous callback function to be mapped using fastapi aprouter defined path handling function
	"""
	current_sql_model=sqlmod
	get_session=get_session
	async def get_one_response(request:Request,item_uuid :uuid.UUID ,current_user :List[str]=Depends(current_user),session : AsyncSession=Depends(get_session)):
		if role_authorization(current_user,current_sql_model.read_roles()):
			try:
				curr_model=await session.execute(select(current_sql_model).filter_by(uuid = item_uuid))
				curr_model=curr_model.scalars().first()
				print(curr_model)
				return curr_model
			except Exception as e:
				print(e)
				return {"Message":"Some Error Occured"}
			finally:
				await session.close()
		return {"Message":"Do not have required privileges to access this resource"}       
	model_name=current_sql_model.tableroute()          
	get_one_response.__name__=f"{model_name}_get_one_response"        	
	return get_one_response