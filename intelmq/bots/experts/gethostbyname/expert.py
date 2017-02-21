# -*- coding: utf-8 -*-
"""
These are all possible gaierrors according to the source:
http://www.castaglia.org/proftpd/doc/devel-guide/src/lib/glibc-gai_strerror.c.html
# define EAI_BADFLAGS     -1    /* Invalid value for `ai_flags' field.  */
# define EAI_NONAME       -2    /* NAME or SERVICE is unknown.  */
# define EAI_AGAIN        -3    /* Temporary failure in name resolution.  */
# define EAI_FAIL         -4    /* Non-recoverable failure in name res.  */
# define EAI_NODATA       -5    /* No address associated with NAME.  */
# define EAI_FAMILY       -6    /* `ai_family' not supported.  */
# define EAI_SOCKTYPE     -7    /* `ai_socktype' not supported.  */
# define EAI_SERVICE      -8    /* SERVICE not supported for `ai_socktype'.  */
# define EAI_ADDRFAMILY   -9    /* Address family for NAME not supported.  */
# define EAI_MEMORY       -10   /* Memory allocation failure.  */
# define EAI_SYSTEM       -11   /* System error returned in `errno'.  */

We treat some of them as valid (ie record does not exist) and other as temporary or
permanent failure (default).
"""
import socket

from intelmq.lib.bot import Bot


class GethostbynameExpertBot(Bot):

    def process(self):
        event = self.receive_message()

        for key in ["source.", "destination."]:
            key_fqdn = key + "fqdn"
            key_ip = key + "ip"
            if key_fqdn not in event:
                continue
            if key_ip in event:
                continue
            try:
                ip = socket.gethostbyname(event.get(key_fqdn))
            except socket.gaierror as exc:
                print(repr(exc.args))
                if exc.args[0] in [-2, -4, -5, -8, -11]:
                    pass
                else:
                    raise
            else:
                event.add(key_ip, ip, raise_failure=False)

        self.send_message(event)
        self.acknowledge_message()


BOT = GethostbynameExpertBot
