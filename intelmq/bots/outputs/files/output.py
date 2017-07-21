# -*- coding: utf-8 -*-
import io
import socket
import time
import errno
import os
from os import path

from intelmq.lib.bot import Bot
from intelmq.lib.exceptions import ConfigurationError


class FilesOutputBot(Bot):

    def init(self):
        self.tmp = self._ensure_path(self.parameters.tmp)
        self.dir = self._ensure_path(self.parameters.dir)
        if os.stat(self.tmp).st_dev != os.stat(self.dir).st_dev:    # pragma: no cover (hard to test)
            raise ConfigurationError(
                "bot setup",
                "tmp and dir must reside on the same filesystem")
        self.hostname = socket.gethostname()
        self.pid = os.getpid()

    def _ensure_path(self, p):
        try:
            os.mkdir(p)
        except OSError:
            if not path.isdir(p):
                raise
        return p

    def _get_new_name(self, fd=None):
        """ Creates unique filename (Maildir inspired) """
        (inode, device) = os.fstat(fd)[1:3] if fd else (0, 0)
        return "%s.%d.%f.%d.%d%s" % (
            self.hostname, self.pid, time.time(), device, inode, self.parameters.suffix)

    def create_unique_file(self):
        """ Safely creates machine-wide uniquely named file in tmp dir. """

        # Note that we don't use tempfile module because we need unique filename
        # over _two_ dirs - so we simply incorporate dev/inode num into filename.

        # First find and open name unique within tmp
        tmpname = None
        while not tmpname:
            tmpname = self._get_new_name()
            try:
                fd = os.open(path.join(self.tmp, tmpname), os.O_CREAT | os.O_RDWR | os.O_EXCL)
            except OSError as e:    # pragma: no cover (random, hard to test)
                if e.errno != errno.EEXIST:
                    raise   # other errors than duplicates should get noticed
                tmpname = None
        # Now we know the device/inode, rename to raise uniqueness within the whole filesystem
        newname = self._get_new_name(fd)
        os.rename(path.join(self.tmp, tmpname), path.join(self.tmp, newname))
        nf = io.open(fd, "w", encoding="utf-8")
        return nf, newname

    def process(self):
        event = self.receive_message()
        if self.parameters.single_key:
            event_data = str(event.get(self.parameters.single_key))
        else:
            event_data = event.to_json(hierarchical=self.parameters.hierarchical_output)
        # Create file in tmp dir
        f, name = self.create_unique_file()
        f.write(event_data)
        f.close()
        # Rename atomically into the final dir
        os.rename(path.join(self.tmp, name), path.join(self.dir, name))
        self.acknowledge_message()


BOT = FilesOutputBot
