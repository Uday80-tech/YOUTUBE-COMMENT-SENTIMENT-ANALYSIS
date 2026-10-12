from pydantic import BaseModel, Field, field_validator,HttpUrl ,computed_field
from typing import Annotated ,Literal

class commentsentiment(BaseModel):
    comment : Annotated[str ,Field(...,description="comment of the youtube video")]
    sentiment : Annotated[Literal["positive" , "negative" ,"neutral"] , Field(..., description="the sentiment of the respected youtube comment")]

class response(BaseModel):
    result : Annotated[list[commentsentiment] ,Field(...,description="the response")]
    

