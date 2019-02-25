# -*- coding: utf-8 -*-
# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+


import uuid
from flask import request

from xivo_ctid_ng.auth import required_acl
from xivo_ctid_ng.rest_api import AuthResource

from .schema import (
    fax_list_schema,
    fax_session_schema,
    fax_query_parameters_schema,
)


class FaxListResource(AuthResource):

    def __init__(self, fax_service):
        self._fax_service = fax_service

    @required_acl('ctid-ng.fax.read')
    def get(self):
        fax_list = self._fax_service.list_faxes()

        return {
            'items': fax_session_schema.dump(fax_list, many=True).data
        }, 200

    @required_acl('ctid-ng.fax.create')
    def post(self):
        parameters = fax_query_parameters_schema.load(request.args).data
        path = '/tmp/wazo-fax-{}'.format(str(uuid.uuid4()))
        self._fax_service.save_fax_file(path, request.data)
        result = self._fax_service.send_fax(path, parameters)

        return result, 201


class FaxStatsResource(AuthResource):

    def __init__(self, fax_service):
        self._fax_service = fax_service

    @required_acl('ctid-ng.fax.stats.read')
    def get(self):
        return self._fax_service.get_faxes_stats()


class FaxSessionResource(AuthResource):

    def __init__(self, fax_service):
        self._fax_service = fax_service

    @required_acl('ctid-ng.fax.{fax_session}.read')
    def get(self, fax_session):
        return self._fax_service.get_fax(fax_session)

    @required_acl('ctid-ng.fax.{fax_session}.cancel')
    def delete(self, fax_session):
        result = self._fax_service.cancel_fax(fax_session)

        return '', 204
