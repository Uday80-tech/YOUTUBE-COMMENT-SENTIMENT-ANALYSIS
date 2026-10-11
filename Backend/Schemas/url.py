from pydantic import BaseModel, Field, field_validator,HttpUrl ,computed_field
from typing import Annotated 
from urllib import urlparse ,parse_qs

class Input_URL(BaseModel):
    url : Annotated[ HttpUrl,Field(..., description = "the url of the youtube video") ]

    @field_validator("url")
    def validate_url(cls ,value):
        parse = urlparse(value)
        if parse.hostname != "www.youtube.com":
            raise ValueError("PLEASE ENTER YOUTUBE VIDEO LINK")
       


    @computed_field
    @property
    def video_id(self) -> str:
        parse = urlparse(self.url)
        id = parse_qs(parse.query).get("v",[None])[0]
        if id is None:
            raise ValueError("youtbe video id is missing from url")
        return id

    
