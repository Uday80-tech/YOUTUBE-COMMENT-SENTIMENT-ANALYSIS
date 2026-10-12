from pydantic import BaseModel, Field, field_validator,HttpUrl ,computed_field
from typing import Annotated 
from urllib.parse import urlparse ,parse_qs

class Input_URL(BaseModel):
    url : Annotated[ HttpUrl,Field(..., description = "the url of the youtube video") ]

    @field_validator("url")
    def validate_url(cls ,value) ->HttpUrl:

        parsed = urlparse(str(value))

        if parsed.hostname != "www.youtube.com":
            raise ValueError("PLEASE ENTER YOUTUBE VIDEO LINK")
        
        if parsed.path != "/watch":
            raise ValueError("PLEASE ENTER A YOUTUBE WATCH URL")

        video_id = parse_qs(parsed.query).get("v", [None])[0]

        if not video_id:
            raise ValueError("YouTube video ID is missing from URL")
        return value
       


    @computed_field
    @property
    def video_id(self) -> str:
        parse = urlparse(str(self.url))
        id = parse_qs(parse.query).get("v",[None])[0]
        return id

    
