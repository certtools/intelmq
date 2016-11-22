# -*- coding: utf-8 -*-
"""
TODO: accept multiple attachment names
"""
import re

import imbox


class Mail():
    '''
    Additional information: https://github.com/martinrusev/imbox
    '''

    def __init__(self, host, user, password, ssl):
        self.host = host
        self.user = user
        self.password = password
        self.ssl = ssl
        self.connect()

    def connect(self):
        self.connection = imbox.Imbox(self.host, self.user, self.password,
                                      self.ssl)

    def disconnect(self):
        self.connection.logout()

    def reconnect(self):
        # try:
        self.disconnect()
        # except
        self.connection = imbox.Imbox(
            self.host, self.user, self.password, self.ssl)

    def get(self, folder, unread, sent_from, sent_to, subject):
        messages_folder = self.connection.messages(folder=folder,
                                                   unread=unread,
                                                   sent_from=sent_from,
                                                   sent_to=sent_to)

        for uid, message in messages_folder:
            if subject and re.search(subject, message.subject):
                continue

            return uid, message
        return None, None

    def mark_seen(self, uid):
        self.connection.mark_seen(uid)
