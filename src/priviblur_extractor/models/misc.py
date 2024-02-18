from typing import Optional, NamedTuple, Tuple


class ReblogAttribution(NamedTuple):
    """Object representing reblog author information from individual posts"""
    post_id: str
    post_url: str
    blog_name: str
    blog_title: str

    def to_json_serialisable(self):
        return self._asdict()

    @classmethod
    def from_json(cls, json):
        return cls(**json)


class HeaderInfo(NamedTuple):
    header_image: str
    focused_header_image: str
    scaled_header_image: str

    def to_json_serialisable(self):
        return self._asdict()

    @classmethod
    def from_json(cls, json):
        return cls(**json)


class BlogTheme(NamedTuple):
    avatar_shape: str
    background_color: str
    body_font: str
    header_info : HeaderInfo

    def to_json_serialisable(self):
        json_serializable = self._asdict()
        json_serializable["header_info"] = self.header_info.to_json_serialisable()

        return json_serializable

    @classmethod
    def from_json(cls, json):
        json["header_info"] = HeaderInfo.from_json(json["header_info"])
        return cls(**json)
