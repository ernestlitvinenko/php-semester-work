import typing
import json


class ToDictMixin:
    def to_json(self) -> typing.Any:
        pass

    def to_dict(self):
        return json.loads(self.to_json())
