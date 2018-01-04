# Since https://github.com/isislovecruft/python-gnupg/issues/49 is not fully solved, you may want to use these class instead of gnupg.GPG class in order to mitigate the encoding issue (I.E. when using email.mime.MIMEMultipart).
#
# Example of use:
# gpg = GPGSafe(use_agent=False, homedir="~/.gnupg/") (instead of gpg = gnupg.GPG(...))
# gpg.sign(text)

import codecs
from functools import wraps

import gnupg


class GPGSafe:
    def __init__(self, *args, **kwargs):
        self._default_strict_func = codecs.lookup_error('strict')
        self._gpg = gnupg.GPG(*args, **kwargs)
        self._gpg_strict_func = codecs.lookup_error('strict')
        self._gpgoff()

    def _gpgon(self):
        codecs.register_error('strict', self._gpg_strict_func)

    def _gpgoff(self):
        codecs.register_error('strict', self._default_strict_func)

    def __getattr__(self, f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            self._gpgon()
            r = getattr(self._gpg, f)(*args, **kwargs)
            self._gpgoff()
            return r

        return wrapper
