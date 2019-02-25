# -*- coding: utf-8 -*-
# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import logging

from xivo_bus.resources.common.event import ArbitraryEvent


logger = logging.getLogger(__name__)


class FaxBusEventHandler(object):

    def __init__(self, bus_publisher):
        self.bus_publisher = bus_publisher

    def subscribe(self, bus_consumer):
        bus_consumer.on_ami_event('ReceiveFAX', self._receive_fax)
        bus_consumer.on_ami_event('SendFAX', self._send_fax)
        bus_consumer.on_ami_event('FAXStatus', self._fax_status)
        #bus_consumer.on_ami_event('FaxProgress', self._fax_progress) # from UserEvent in dialplan

    def _receive_fax(self, event):
        bus_event = ArbitraryEvent(
            name='receive_fax',
            body=event,
            required_acl='events.fax'
        )
        bus_event.routing_key = 'fax.receive_fax'
        self.bus_publisher.publish(bus_event)

    def _send_fax(self, event):
        bus_event = ArbitraryEvent(
            name='send_fax',
            body=event,
            required_acl='events.fax'
        )
        bus_event.routing_key = 'fax.send_fax'
        self.bus_publisher.publish(bus_event)

    def _fax_status(self, event):
        bus_event = ArbitraryEvent(
            name='fax_status',
            body=event,
            required_acl='events.fax'
        )
        bus_event.routing_key = 'fax.fax_status'
        self.bus_publisher.publish(bus_event)

    def _fax_progress(self, event):
        bus_event = ArbitraryEvent(
            name='fax_progress',
            body=event,
            required_acl='events.fax'
        )
        bus_event.routing_key = 'fax.fax_progress'
        self.bus_publisher.publish(bus_event)
