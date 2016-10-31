class DBTask(celery.Task):
    abstract = True
    _db = None

    @property
    def db(self):
        if self._db is None:
            self._db = Database.connect()
        return self._db

    def after_failure(self, *args, **kwargs):
        send_email('The task failed!')

@app.task(base=DBTask)
def get_data(table_name):
    return get_data.db.table(table_name).all()

@app.task(soft_time_limit=3600)
def run_job(job_id):
    try:
        job = AbusiveJob(job_id)
        job.build()
        job.run()
    except celery.exceptions.SoftTimeLimitExceeded:
        raise celery.task.current.retry()
    except celery.exceptions.MaxRetriesExceededError:
        send_email('AbusiveJob failed')

@contextlib.contextmanager
def semaphore(self):
    semaphore = None
    if self.dms_code and not self.called_directly:
        semaphore = client.Semaphore(self.dms.code,
                                     max_leases=3)
        if not semaphore.acquire(blocking=False):
            raise celery.task.current.retry()

    try:
        yield
    finally:
        if semaphore:
            semaphore.release()

def _get_node(self, args, kwargs):
    mutex_keys = getattr(self, 'mutex_keys', ())
    lock_node = '/mutex/celery/{}'.format(self.name)
    items = inspect.getcallargs(self.run, *args, **kwargs)
    for value in (items[x] for x in mutex_keys if
                  items.get(x))
        lock_node += value
    return lock_node

@contextlib.contextmanager
def mutex(self, args, kwargs):
    client = None
    success = False
    lock_node = self._get_node(args, kwargs)
    if not client.exists(lock_node):
        success = True
    if success:
        client.create(lock_node, makepath=True)
        yield True
    else:
        yield False

class MutexTask(celery.Task):
    abstract = True

    @contextlib.contextmanager
    def mutex(self, args, kwargs, delete=False):
        pass

    def apply_async(self, args=None, kwargs=None, **options):
        with self.mutex(args, kwargs) as mutex_acquired:
            if mutex_acquired:
                return super(MutexTask, 
                             self).apply_async(args, kwargs,
                                               **options)

    def after_return(self, *args, **kwargs):
        lock_node = self._get_node(args, kwargs)
        if client.exists(lock_node):
            client.delete(lock_node)
