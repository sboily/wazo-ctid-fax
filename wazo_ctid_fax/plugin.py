# -*- coding: utf-8 -*-
# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from xivo_amid_client import Client as AmidClient
from xivo_auth_client import Client as AuthClient

from .resources import (
    FaxListResource,
    FaxStatsResource,
    FaxSessionResource,
    )
from .services import FaxService
from .bus_consume import FaxBusEventHandler


class Plugin(object):

    def load(self, dependencies):
        api = dependencies['api']
        bus_publisher = dependencies['bus_publisher']
        config = dependencies['config']
        token_changed_subscribe = dependencies['token_changed_subscribe']
        bus_consumer = dependencies['bus_consumer']
        bus_publisher = dependencies['bus_publisher']

        amid_client = AmidClient(**config['amid'])

        token_changed_subscribe(amid_client.set_token)

        fax_service = FaxService(amid_client)

        fax_bus_event_handler = FaxBusEventHandler(bus_publisher)
        fax_bus_event_handler.subscribe(bus_consumer)

        api.add_resource(FaxListResource, '/fax', resource_class_args=[fax_service])
        api.add_resource(FaxStatsResource, '/fax/stats', resource_class_args=[fax_service])
        api.add_resource(FaxSessionResource, '/fax/<fax_session>', resource_class_args=[fax_service])
