import secrets

from drf_spectacular.openapi import AutoSchema as DefaultAutoSchema


class AutoSchema(DefaultAutoSchema):
    def _get_serializer_name(self, serializer, direction):
        name = super()._get_serializer_name(serializer, direction)
        return f'{secrets.token_hex(3)}.{name}'
