from typing import NamedTuple, Optional


class Signpost(NamedTuple):
    title: str
    description: Optional[str] = None

    def to_json_serialisable(self):
        return {"title": self.title, "description": self.description}

    @classmethod
    def from_json(cls, json):
        return cls(**json)
