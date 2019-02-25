# -*- coding: utf-8 -*-
# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from marshmallow import (
    fields,
    Schema,
)
from marshmallow.validate import Length


class FaxListSchema(Schema):
    session = fields.Str(validate=Length(min=1))

    class Meta:
        strict = True


class FaxSessionSchema(Schema):
    session = fields.Integer()
    files = fields.Str()
    operation = fields.Str()
    session_type = fields.Str()
    state = fields.Str()
    technology = fields.Str()
    call_id = fields.Str()

    class Meta:
        strict = True

class FaxQueryParametersSchema(Schema):
    fax_extension = fields.Str()
    fax_context = fields.Str()
    fax_number = fields.Str()
    fax_user_id = fields.Str()


fax_list_schema = FaxListSchema()
fax_session_schema = FaxSessionSchema()
fax_query_parameters_schema = FaxQueryParametersSchema()
