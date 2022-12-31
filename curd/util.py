from . import * 

#################################################
# Recursively change all dataclass to dictionary
#################################################

def dataclass_to_dic(pydantic_model)->dict:
    """Recursively changing to dictionary

    Args:
        pydantic_model (BaseModel): Takes pydantic Data Model as argument

    Returns:
        dict: returns dictionary object,by Recursively changing dataclass and basemodel objects to dictionary elements
    """
    data=dict(pydantic_model)
    for key, value in data.items():
        if is_dataclass(value):
            data[key] = asdict(value)
            dataclass_to_dic(data[key])                    
        elif isinstance(value,list):
            amended_list=[]
            for x in value:
                
                if is_dataclass(value):
                    amended_list.append(dataclass_to_dic(asdict(x))) 
                elif isinstance(x,BaseModel):
                    amended_list.append(dataclass_to_dic(dict(x)))
                else:
                    amended_list.append(x)
            data[key]=amended_list               
    return data

##########################################################
# Changing uuid type found in pydantic model objecs to str 
##########################################################
def uuid_to_str(pydantic_model)->dict:
    data=dict(pydantic_model)
    for key, value in data.items():
        if isinstance(value,uuid.UUID):
              data[key] = str(value)  
    return data

######################################################################
# Checks if available roles are found in required roles to grant acess 
######################################################################
def role_authorization(available_roles : List[str],required_roles:List[str])->bool:
    if len([x for x in available_roles if x in required_roles]) >0:
        return True
    return False