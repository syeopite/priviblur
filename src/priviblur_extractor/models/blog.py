from typing import NamedTuple


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


class BrokenBlog(NamedTuple):
    name: str
    avatar: list[dict]

    def to_json_serialisable(self):
        return self._asdict()

    @classmethod
    def from_json(cls, json):
        return cls(**json)


class Blog(NamedTuple):
    name: str
    # [{"width": 512, "height": 512, url: "..."}, {"width": ...}...]
    avatar: list[dict]
    title: str
    url: str
    is_adult: bool

    description_npf: list[dict]
    uuid: str
    theme: BlogTheme
    is_paywall_on: bool

    # If blog is deactivated or not
    active: bool = False

    def to_json_serialisable(self):
        json_serializable = self._asdict()

        if json_serializable["theme"]:
            json_serializable["theme"] = json_serializable["theme"].to_json_serialisable()

        return json_serializable

    @classmethod
    def from_json(cls, json):
        import orjson
        x = orjson.dumps(json)

        with open('test.json', "wb") as f:
            f.write(x)
        json["theme"] = BlogTheme.from_json(json["theme"])
        return cls(**json)

