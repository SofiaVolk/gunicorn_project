from marshmallow import Schema, fields
from marshmallow import validate, utils, class_registry
from marshmallow.utils import is_collection, missing as missing
from marshmallow.compat import basestring, Mapping as _Mapping, iteritems
from marshmallow.exceptions import (
    ValidationError
)


class HhDomainSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(allow_none=True)

def valid(data):
    try:
        id = fields.Int(dump_only=True)
        name = fields.Str(allow_none=True)
    except ValidationError as err:
        return err
    return 0


class Curency(Schema):
    def valid(self):
        try:
            id = fields.Int(dump_only=True)
            name = fields.Str(allow_none=True)
        except ValidationError as err:
            return err
        return 0


class HhSubdomainSchema(Schema):
    id = fields.Int(dump_only=True)
    id_domain = fields.Nested(HhDomainSchema, many=True)
    name = fields.Str(allow_none=True)

#
# class HhShelduleSchema(Schema):
#     id = fields.Int(dump_only=True)
#     name = fields.Str(allow_none=True)


class StationSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(allow_none=True)


class HhCompanySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(allow_none=True)
    contact = fields.Str(allow_none=True)


class HhVacancySchema(Schema):
    id = fields.Int(dump_only=True)
    id_company = fields.Nested(HhCompanySchema, many=True)
   # id_scheldule = fields.Nested(HhShelduleSchema, many=True)
    salary = fields.Float(allow_none=True)
    id_subdomain = fields.Nested(HhSubdomainSchema, many=True)
    id_station = fields.Nested(StationSchema, many=True)


class CianSchema(Schema):
    id = fields.Int(dump_only=True)
    count_rooms = fields.Int(allow_none=True)
    id_station = fields.Nested(StationSchema, many=True, allow_none=True)
    price = fields.Float(allow_none=True)
    floor = fields.Int(allow_none=True)
    square = fields.Float(allow_none=True)
    price_sq = fields.Float(allow_none=True)


class HhVacancyUserSchema(Schema):
    #id = fields.Int(dump_only=True)
    id_company = fields.Str(allow_none=True)
   # id_scheldule = fields.Nested(HhShelduleSchema, many=True)
    salary = fields.Float(allow_none=True)
    id_subdomain = fields.Str(allow_none=True)
    id_station = fields.Str(allow_none=True)


class CianUserSchema(Schema):
    #id = fields.Int(dump_only=True)
    count_rooms = fields.Int(allow_none=True)
    id_station = fields.Str(allow_none=True)
    price = fields.Float(allow_none=True)
    floor = fields.Int(allow_none=True)
    square = fields.Float(allow_none=True)
    price_sq = fields.Float(allow_none=True)

