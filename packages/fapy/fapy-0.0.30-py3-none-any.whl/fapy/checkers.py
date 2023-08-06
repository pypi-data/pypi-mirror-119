from re import I as _I, findall as _findall
import sys as _sys
from threading import Event, Lock, Thread
from types import GeneratorType as _GenType

from fapy.net import http_connection, http_request
from fapy.utils import fmt_bytes, is_binary, random_lower_str


class Checker(Thread):
    """Base class for checkers"""
    _print_lock = Lock()
    _gen_lock = Lock()
    _running_event = Event()
    _results = []
    _gen: _GenType

    def check(self, _):
        self.set_running(False)
        raise NotImplementedError('%s::check()' % self.__class__.__name__)

    def filter(self, result):
        return bool(result)

    def output(self, ip, result):
        print(ip)

        if is_binary(result):
            text = '<binary data> %s' % fmt_bytes(len(result))
        else:
            text = result.decode(errors='ignore')

        # not redirected
        if _sys.stdout.isatty():
            print(text, end='\n---\n')
        # redirected
        else:
            # duplicate ip, print data on screen
            _sys.stderr.write('%s\n%s\n---\n' % (ip, text))
            _sys.stderr.flush()

    def run(self):
        while self._running_event.is_set():
            with self._gen_lock:
                try:
                    ip = next(self._gen)
                except StopIteration:
                    break

            result = self.check(ip)

            if self.filter(result):
                with self._print_lock:
                    self.output(ip, result)

    @classmethod
    def set_generator(cls, gen):
        cls._gen = gen

    @classmethod
    def set_running(cls, state):
        if state:
            cls._running_event.set()
        else:
            cls._running_event.clear()


class PathChecker(Checker):
    path = ''
    port = 80
    ssl = False
    timeout = 2
    inc_re = ''
    exc_re = ''

    def check(self, ip):
        _path = self.random_path()
        _c = http_connection(ip, self.port, self.ssl, timeout=self.timeout)

        # check for SPA
        code, _ = http_request(_c, _path)

        if 200 <= code < 300 or code == 999:
            return b''

        # check target path
        code, body = http_request(_c, self.path)

        if not 200 <= code < 300:
            return b''

        if self.exc_re:
            text = body.decode(errors='ignore')
            if _findall(self.exc_re, text, _I):
                return b''

        if self.inc_re:
            text = body.decode(errors='ignore')
            if not _findall(self.inc_re, text, _I):
                return b''

        return body

    @staticmethod
    def random_path(min_len=8, max_len=12):
        """Get random path. Mainly used to determine 
        single page applications (SPA) or honeypots"""
        return '/%s' % random_lower_str(min_len, max_len)
