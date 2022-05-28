from . import * 


#################################################
# Recurssively change all dataclass to dictionary
###################################################

def dataclass_to_dic(pydantic_model):
    
    data=dict(pydantic_model)
    for key, value in data.items():
    # If value satisfies the condition, then store it in new_dict
            if is_dataclass(value):
                data[key] = asdict(value)
                dataclass_to_dic(data[key])
                
    return data