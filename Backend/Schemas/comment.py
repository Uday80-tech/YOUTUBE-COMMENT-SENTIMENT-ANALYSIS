from pydantic import BaseModel, Field, field_validator,HttpUrl ,computed_field
from typing import Annotated ,Literal

class commentsentiment(BaseModel):
    comment : Annotated[str ,Field(...,description="comment of the youtube video")]
    sentiment : Annotated[Literal["positive" , "negative" ,"neutral"] , Field(..., description="the sentiment of the respected youtube comment")]

class VideoInfo(BaseModel):
    title: Annotated[str, Field(..., description="YouTube video title")]
    channel_name: Annotated[str, Field(..., description="YouTube channel name")]
    upload_date: Annotated[str, Field(..., description="Video publication date")]

class response(BaseModel):
    result : Annotated[list[commentsentiment] ,Field(...,description="the response")]
    video_info: Annotated[VideoInfo,Field(..., description="YouTube video metadata")]
    

