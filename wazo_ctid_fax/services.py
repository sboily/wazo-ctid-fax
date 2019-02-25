# -*- coding: utf-8 -*-
# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import os
import logging


class FaxService(object):

    def __init__(self, amid):
        self.amid = amid

    def list_faxes(self):
        sessions = self.amid.action('faxsessions')
        channels = self._get_channels_linkedid()
        s = []
        for session in sessions:
            if session.get('Event') == 'FAXSessionsEntry':
                s.append(self._fax_session(session, channels))
        return s

    def get_fax(self, fax_session):
        result = self.amid.action('faxsession', {'SessionNumber': fax_session})
        for session in result:
            if session.get('Event') == 'FAXSession':
                return self._fax(session)
        return {}

    def cancel_fax(self, fax_session):
        channel = self._find_channel(fax_session)
        self.amid.action('hangup', {'Channel': channel})

    def send_fax(self, fax_path, fax_data):
        send = self.amid.action('originate', {'Channel': 'Local/%s@%s' % (fax_data.get('fax_extension'), fax_data.get('fax_context')),
                                              'CallerID': fax_data.get('fax_caller_id'),
                                              'Variable': 'XIVO_USERID=%s' % fax_data.get('fax_user_id'),
                                              'Variable': 'XIVO_FAX_PATH=%s' % fax_path,
                                              'Context': 'txfax',
                                              'Exten': 's',
                                              'Async': 'true',
                                              'Priority': '1'})
        print(send)
        return {}

    def get_faxes_stats(self):
        stats = self.amid.action('faxstats')
        for stat in stats:
            if stat.get('Event') == 'FAXStats':
                return self._fax_stats(stat)
        return {}

    def save_fax_file(self, path, content):
        with os.fdopen(os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o660), 'wb') as fobj:
            return fobj.write(content)

    def _find_channel(self, fax_session):
        sessions = self.amid.action('faxsessions')
        for session in sessions:
            if session.get('Event') == 'FAXSessionsEntry':
                if session.get('SessionNumber') == fax_session:
                    return session.get('Channel')
        return None

    def _get_channels_linkedid(self):
        channels = self.amid.action('coreshowchannels')
        c = {}
        for channel in channels:
            if channel.get('Event') == 'CoreShowChannel':
                chan = channel.get('Channel')
                linkedid = channel.get('Linkedid')
                c.update({chan: linkedid})
        return c

    def _fax_session(self, session, channels):
        return {
            'session': session.get('SessionNumber'),
            'files': session.get('Files'),
            'operation': session.get('Operation'),
            'session_type': session.get('SessionType'),
            'state': session.get('State'),
            'technology': session.get('Technology'),
            'channel': session.get('Channel'),
            'call_id': channels.get(session.get('Channel'))
        }

    def _fax(self, session):
        return {
            'session': session.get('SessionNumber'),
            'file_name': session.get('FileName'),
            'operation': session.get('Operation'),
            'image_resolution': session.get('ImageResolution'),
            'data_rate': session.get('DataRate'),
            'pages_transmitted': session.get('PagesTransmitted'),
            'state': session.get('State'),
            'error_correction_mode': session.get('ErrorCorrectionMode'),
            'total_bad_lines': session.get('TotalBadLines'),
            'page_number': session.get('PageNumber'),
            'pages_received': session.get('PagesReceived'),
        }

    def _fax_stats(self, stat):
        return {
            "current_sessions": stat.get('CurrentSessions'),
            "completed_faxes": stat.get('CompletedFAXes'),
            "reserved_sessions": stat.get('ReservedSessions'),
            "failed_faxes": stat.get('FailedFAXes'),
            "transmit_attempts": stat.get('TransmitAttempts'),
            "receive_attempts": stat.get('ReceiveAttempts')
        }
