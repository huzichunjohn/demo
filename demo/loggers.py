import logging
import datetime

class SyslogHandler(logging.Handler):
    def emit(self, record):
        try:
            from blog.models import Syslog
            log = Syslog(level=record.levelname, message=record.msg, timestamp=datetime.datetime.now())
            log.save()
        except:
            raise 
