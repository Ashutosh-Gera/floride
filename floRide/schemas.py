from pydantic import BaseModel

#This file is to store all the pydantic schemas that we make
#This is a pydantic model i.e a class that inherits from BaseModel and 
# we use it to define the data types of the attributes of the class

class Blog(BaseModel):
    title : str
    body : str