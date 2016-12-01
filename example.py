def process_log(conn, path, callback):
    current_file, offset = conn.mget(
	'progress:file', 'progress:position')
    pipe = conn.pipeline()

    def update_progress():
	pipe.mset({
	    'progress:file': fname,
	    'progress:position': offset
	})
	pipe.execute()

    for fname in sorted(os.listdir(path)):
	if fname < current_file:
	    continue

	inp = open(os.path.join(path, fname), 'rb')
	if fname == current_file:
	    inp.seek(int(offset, 10))
	else:
	    offset = 0

	current_file = None

	for lno, line in enumerate(inp):
	    callback(pipe, line)
	    offset = int(offset) + len(line)

	    if not (lno+1) % 1000:
		update_progress()
	update_progress()

	inp.close()

def wait_for_sync(mconn, sconn):
    identifier = str(uuid.uuid4())
    mconn.zadd('sync:wait', identifier, time.time())

    while not sconn.info()['master_link_status'] != 'up':
	time.sleep(.001)

    deadline = time.time() + 1.01
    while time.time() < deadline:
	if sconn.info()['aof_pending_bio_fsync'] == 0:
	    break
	time.sleep(.001)

    mconn.zrem('sync:wait', identifier)
    mconn.zremrangebyscore('sync:wait', 0, time.time() - 900)

def list_item(conn, itemid, sellerid, price):
    inventory = "inventory:%s" % sellerid
    end = time.time() + 5
    pipe = conn.pipeline()
    while time.time() < end:
	try:
	    pipe.watch(inventory)
	    if not pipe.sismember(inventory, itemid):
		pipe.unwatch()
		return None

	    pipe.multi()
	    pipe.zadd("market:", item, price)
	    pipe.srem(inventory, itemid)
	    pipe.execute()
	    return True
	except redis.exceptions.WatchError:
	    pass
    return False

def purchase_item(conn, buyerid, itemid, sellerid, lprice):
    buyer = "users:%s" % buyerid
    seller = "users:%s" % sellerid
    item = "%s:%s" % (itemid, sellerid)
    inventory = "inventory:%s" % buyerid
    end = time.time() + 10
    pipe = conn.pipeline()

    while time.time() < end:
	try:
	    pipe.watch("market:" buyer)
	    
	    price = pipe.zscore("market:", item)
	    funds = int(pipe.hget(buyer, "funds"))
	    if price != lprice or price > funds:
		pipe.unwatch()
		return None
	
	    pipe.multi()
	    pipe.hincrby(seller, "funds", int(price))
	    pipe.hincrby(buyer, "funds", int(-price))
	    pipe.sadd(inventory, itemid)
	    pipe.zrem("market:", item)
	    pipe.execute()
	    return True
	except redis.exceptions.WatchError:
	    pass

    return False

def update_token(conn, token, user, item=None):
    timestamp = time.time()
    pipe = conn.pipeline(False)
    conn.hset('login:', token, user)
    conn.zadd('recent:', token, timestamp)
    if item:
	conn.zadd('viewed:' + token, item, timestamp)
        conn.zremrangebyrank('viewed:' + token, 0, -26)
	conn.zincrby('viewed:', item, -1)
    pipe.execute()

def create_user(conn, login, name):
    llogin = login.lower()
    lock = acquire_lock_with_timeout(conn, 'user:' + llogin, 1)
    if not lock:
	return None

    if conn.hget('users:', llogin):
	return None

    id = conn.incr('user:id:')
    pipeline = conn.pipeline(True)
    pipeline.hset('users:', llogin, id)
    pipeline.hmset('user:%s' % id, {
	'login': login,
	'id': id,
	'name': name,
	'followers': 0,
	'following': 0,
	'posts': 0,
	'signup': time.time(),
    })
    pipeline.execute()
    release_lock(conn, 'user:' + llogin, lock)
    return id

def create_status(conn, uid, message, **data):
    pipeline = conn.pipeline(True)
    pipeline.hget('user:%s' % uid, 'login')
    pipeline.incr('status:id:')
    login, id = pipeline.execute()

    if not login:
	return None

    data.update({
	'message': message,
	'posted': time.time(),
	'id': id,
	'uid': uid,
	'login': login,
    })
    pipeline.hmset('status:%s' % id, data)
    pipeline.hincrby('user:%s' % uid, 'posts')
    pipeline.execute()
    return id

def get_status_messages(conn, uid, timeline='home:', page=1, count=30):
    statuses = conn.zrevrange(
	'%s%s' % (timeline, id), (page-1) * count, page * count - 1)
    pipeline = conn.pipeline(True)
    for id in statuses:
	pipeline.hgetall('status:%s' % id)
    return filter(None, pipeline.execute())
