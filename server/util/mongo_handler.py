import datetime as dt
import logging
import threading

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import OperationFailure
from pymongo.errors import ServerSelectionTimeoutError

"""
Example format of generated bson document:
{
    'thread': -1216977216,
    'threadName': 'MainThread',
    'level': 'ERROR',
    'timestamp': datetime.datetime(2016, 8, 16, 15, 20, 24, 794341),
    'message': 'test message',
    'module': 'test_module',
    'fileName': '/var/projects/python/log4mongo-python/tests/test_handlers.py',
    'lineNumber': 38,
    'method': 'test_emit_exception',
    'loggerName':  'testLogger',
    'exception': {
        'stackTrace': 'Traceback (most recent call last):
                       File "/var/projects/python/log4mongo-python/tests/\
                           test_handlers.py", line 36, in test_emit_exception
                       raise Exception(\'exc1\')
                       Exception: exc1',
        'message': 'exc1',
        'code': 0
    }
}
"""
_connection = None


class MongoFormatter(logging.Formatter):

    DEFAULT_PROPERTIES = logging.LogRecord(
        '', '', '', '', '', '', '', '').__dict__.keys()

    def format(self, record):
        """Formats LogRecord into python dictionary."""
        # Standard document
        document = {
            'timestamp': dt.datetime.utcnow(),
            'level': record.levelname,
            'thread': record.thread,
            'threadName': record.threadName,
            'message': record.getMessage(),
            'loggerName': record.name,
            'fileName': record.pathname,
            'module': record.module,
            'method': record.funcName,
            'lineNumber': record.lineno
        }
        # Standard document decorated with exception info
        if record.exc_info is not None:
            document.update({
                'exception': {
                    'message': str(record.exc_info[1]),
                    'code': 0,
                    'stackTrace': self.formatException(record.exc_info)
                }
            })
        # Standard document decorated with extra contextual information
        if len(self.DEFAULT_PROPERTIES) != len(record.__dict__):
            contextual_extra = set(record.__dict__).difference(
                set(self.DEFAULT_PROPERTIES))
            if contextual_extra:
                for key in contextual_extra:
                    document[key] = record.__dict__[key]
        return document


class MongoHandler(logging.Handler):

    def __init__(self, level=logging.NOTSET, host='localhost', port=27017,
                 database_name='logs', collection='logs',
                 username=None, password=None, authentication_db='admin',
                 fail_silently=False, formatter=None, capped=False,
                 capped_max=1000, capped_size=1000000, reuse=True, **kwargs):
        """
        Setting up mongo handler, initializing mongo database connection via
        pymongo.
        If reuse is set to false every handler will have it's own MongoClient.
        This could hammer down your MongoDB instance, but you can still use
        this option.
        The default is True. As such a program with multiple handlers
        that log to mongodb will have those handlers share a single connection
        to MongoDB.
        """
        logging.Handler.__init__(self, level)
        self.host = host
        self.port = port
        self.database_name = database_name
        self.collection_name = collection
        self.username = username
        self.password = password
        self.authentication_database_name = authentication_db
        self.fail_silently = fail_silently
        self.connection = None
        self.db = None
        self.collection = None
        self.authenticated = False
        self.formatter = formatter or MongoFormatter()
        self.capped = capped
        self.capped_max = capped_max
        self.capped_size = capped_size
        self.reuse = reuse
        self._connect(**kwargs)

    def _connect(self, **kwargs):
        """Connecting to mongo database."""
        global _connection
        if self.reuse and _connection:
            self.connection = _connection
        else:
            if self.username is not None and self.password is not None:
                self.connection = MongoClient(host=self.host, port=self.port, username=self.username,
                                            password=self.password, **kwargs)

            else:
                self.connection = MongoClient(host=self.host, port=self.port,
                                            **kwargs)
            try:
                self.connection.is_primary
            except ServerSelectionTimeoutError:
                if self.fail_silently:
                    return
                raise
            _connection = self.connection

        self.db = self.connection[self.database_name]

        if self.capped:
            #
            # We don't want to override the capped collection
            # (and it throws an error anyway)
            try:
                self.collection = Collection(self.db, self.collection_name,
                                             capped=True, max=self.capped_max,
                                             size=self.capped_size)
            except OperationFailure:
                # Capped collection exists, so get it.
                self.collection = self.db[self.collection_name]
        else:
            self.collection = self.db[self.collection_name]

    def close(self):
        """
        closing mongo database connection.
        """
        if self.connection is not None:
            self.connection.close()

    def emit(self, record):
        """Inserting new logging record to mongo database."""
        if self.collection is not None:
            try:
                self.collection.insert_one(self.format(record))
            except Exception:
                if not self.fail_silently:
                    self.handleError(record)

    def __exit__(self, type, value, traceback):
        self.close()


class BufferedMongoHandler(MongoHandler):

    def __init__(self, level=logging.NOTSET, host='localhost', port=27017,
                 database_name='logs', collection='logs',
                 username=None, password=None, authentication_db='admin',
                 fail_silently=False, formatter=None, capped=False,
                 capped_max=1000, capped_size=1000000, reuse=True,
                 buffer_size=100, buffer_periodical_flush_timing=5.0,
                 buffer_early_flush_level=logging.CRITICAL, **kwargs):
        """
        Setting up buffered mongo handler, initializing mongo database connection via
        pymongo.
        This subclass aims to provide buffering mechanism to avoid hammering the database server and
        write-locking the database too often (even if mongo is performant in that matter).
        If buffer_periodical_flush_timer is set to None or 0, no periodical flush of the buffer will be done.
        It means that buffered messages might be stuck here for a while until the buffer full or
        a critical message is sent (both causing flush).
        If buffer_periodical_flush_timer is set to numeric value, a thread with timer will be launched
        to call the buffer flush periodically.
        """

        MongoHandler.__init__(self, level=level, host=host, port=port, database_name=database_name, collection=collection,
                              username=username, password=password, authentication_db=authentication_db,
                              fail_silently=fail_silently, formatter=formatter, capped=capped, capped_max=capped_max,
                              capped_size=capped_size, reuse=reuse, **kwargs)
        self.buffer = []
        self.buffer_size = buffer_size
        self.buffer_periodical_flush_timing = buffer_periodical_flush_timing
        self.buffer_early_flush_level = buffer_early_flush_level
        self.last_record = None #kept for handling the error on flush
        self.buffer_timer_thread = None

        self.buffer_lock = threading.RLock()

        self._timer_stopper = None

        # setup periodical flush
        if self.buffer_periodical_flush_timing:

            # clean exit event
            import atexit
            atexit.register(self.destroy)

            # call at interval function
            def call_repeatedly(interval, func, *args):
                stopped = threading.Event()

                # actual thread function
                def loop():
                    while not stopped.wait(interval):  # the first call is in `interval` secs
                        func(*args)

                timer_thread = threading.Thread(target=loop)
                timer_thread.daemon = True
                timer_thread.start()
                return stopped.set, timer_thread

            # launch thread
            self._timer_stopper, self.buffer_timer_thread = call_repeatedly(self.buffer_periodical_flush_timing, self.flush_to_mongo)

    def emit(self, record):
        """Inserting new logging record to buffer and flush if necessary."""

        with self.buffer_lock:
            self.last_record = record
            self.buffer.append(self.format(record))

        if len(self.buffer) >= self.buffer_size or record.levelno >= self.buffer_early_flush_level:
            self.flush_to_mongo()

    def flush_to_mongo(self):
        """Flush all records to mongo database."""
        if self.collection is not None and len(self.buffer) > 0:
            with self.buffer_lock:
                try:
                    self.collection.insert_many(self.buffer)
                    self.empty_buffer()
                except Exception:
                    if not self.fail_silently:
                        self.handleError(self.last_record) #handling the error on flush

    def empty_buffer(self):
        """Empty the buffer list."""
        del self.buffer
        self.buffer = []

    def destroy(self):
        """Clean quit logging. Flush buffer. Stop the periodical thread if needed."""
        if self._timer_stopper:
            self._timer_stopper()
        self.flush_to_mongo()
        self.close()

"""
capped=True 控制 MongoDB 使用固定集合
MongoDB 固定集合（Capped Collections）是性能出色且有着固定大小的集合，对于大小固定，我们可以想象其就像一个环形队列，当集合空间用完后，
再插入的元素就会覆盖最初始的头部的元素！
capped_size 是整个集合空间大小，单位为【字节】
capped_max 是集合文档个数上线，单位是【个】
如果空间大小到达上限，则插入下一个文档时，会覆盖第一个文档；如果文档个数到达上限，同样插入下一个文档时，会覆盖第一个文档。
两个参数上限判断取的是【与】的逻辑。

   'mongo': {
            'class': 'util.mongo_handler.MongoHandler',
            'host': "mongodb://localhost:27017/",  # 通过uri方式配置
            'database_name': 'mongo_logs',
            'collection': 'logs',
            'level': 'INFO',
            'capped' : True,
            'capped_max' : 100000, 
            'capped_size' : 100000000
        },
"""
