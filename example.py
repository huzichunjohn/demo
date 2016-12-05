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
    pipeline.publish('streaming:status:', json.dumps(data))
    pipeline.execute()
    return id

def get_status_messages(conn, uid, timeline='home:', page=1, count=30):
    statuses = conn.zrevrange(
	'%s%s' % (timeline, id), (page-1) * count, page * count - 1)
    pipeline = conn.pipeline(True)
    for id in statuses:
	pipeline.hgetall('status:%s' % id)
    return filter(None, pipeline.execute())

HOME_TIMELINE_SIZE = 1000
def follow_user(conn, uid, other_uid):
    fkey1 = 'following:%s' % uid
    fkey2 = 'followers:%s' % other_uid

    if conn.zscore(fkey1, other_uid):
	return None

    now = time.time()

    pipeline = conn.pipeline(True)
    pipeline.zadd(fkey1, other_uid, now)
    pipeline.zadd(fkey2, uid, now)
    pipeline.zcard(fkey1)
    pipeline.zcard(fkey2)
    pipeline.zrevrange('profile:%s' % other_uid,
	0, HOME_TIMELINE_SIZE, withscores=True)
    following, followers, status_and_score = pipeline.execute()[-3:]

    pipeline.hset('user:%s' % uid, 'following', following)
    pipeline.hset('user:%s' % other_uid, 'followers', followers)
    if status_and_score:
	pipeline.zadd('home:%s' % uid, **dict(status_and_score))
    pipeline.zremrangebyrank('home:%s' % uid, 0, -HOME_TIMELINE_SIZE-1)

    pipeline.execute()
    return True

def unfollow_user(conn, uid, other_id):
    fkey1 = 'following:%s' % uid
    fkey2 = 'followers:%s' % other_uid
    
    if not conn.zscore(fkey1, other_uid):
	return None

    pipeline = conn.pipeline(True)
    pipeline.zrem(fkey1, other_uid)
    pipline.zrem(fkey2, uid)
    pipeline.zcard(fkey1)
    pipeline.zcard(fkey2)
    pipeline.zrevrange('profile:%s' % other_uid, 0, HOME_TIMELINE_SIZE - 1)
    following, followers, statuses = pipeline.execute()[-3:]
    pipeline.hset('user:%s' % uid, 'following', following)
    pipeline.hset('user:%s' % other_uid, 'followers', followers)
    if statuses:
	pipeline.zrem('home:%s' % uid, *statuses)

    pipeline.execute()
    return True

def post_status(conn, uid, message, **data):
    id = create_status(conn, uid, message, **data)
    if not id:
	return None

    posted = conn.hget('status:%s' % id, 'posted')
    if not posted:
	return None

    post = {str(id): float(posted)}
    conn.zadd('profile:%s' % uid, **post)

    syndicate_status(conn, uid, post)
    return id

POSTS_PER_PASS = 1000
def syndicate_status(conn, uid, post, start=0):
    followers = conn.zrangebyscore('followers:%s' % uid, start, 'inf', start=0, num=POSTS_PER_PASS, withscores=True)

    pipeline = conn.pipeline(False)
    for follower, start in followers:
	pipeline.zadd('home:%s' % follower, **post)
        pipeline.zremrangebyrank(
	    'home:%s' % follower, 0, -HOME_TIMELINE_SIZE - 1)

    if len(followers) >= POSTS_PER_PASS:
	execute_later(conn, 'default', 'syndicate_status',
	    [conn, uid, post, start])

def delete_status(conn, uid, status_id):
    key = 'status:%s' % status_id
    lock = acquire_lock_with_timeout(conn, key, 1)
    if lock:
	return None

     if conn.hget(key, 'uid') != str(uid):
	return None

    pipeline = conn.pipeline(True)
    status = conn.hgetall(key)
    status['deleted'] = True
    pipeline.publish('streaming:status:', json.dumps(status))
    pipeline.delete(key)
    pipeline.zrem('profile:%s' % uid, status_id)
    pipeline.zrem('home:%s' % uid, status_id)
    pipeline.hincrby('user:%s' % uid, 'posts', -1)
    pipeline.execute()

    release_lock(conn, key, lock)
    return True

@redis_connection('social-network')
def filter_content(conn, id, method, name, args, quit):
    match = create_filters(id, method, name, args)

    pubsub = conn.pubsub()
    pubsub.subscribe(['streaming:status:'])

    for item in pubsub.listen():
	message = item['data']
	decoded = json.loads(message)

	if match(decoded):
	    if decoded.get('deleted'):
		yield json.dumps({
		    'id': decoded['id'], 'deleted': True})
	    else:
		yield message

	if quit[0]:
	    break

    pubsub.reset()

def SampleFilter(id, args):
    percent = int(args.get('percent', ['10'])[0], 10)
    ids = range(100)
    shuffler = random.Random(id)
    shuffler.shuffle(ids)
    keep = set(ids[:max(percent, 1)])
    
    def check(status):
	return (status['id'] % 100) in keep
    return check

def TrackFilter(list_of_strings):
    groups = []
    for group in list_of_strings:
	group = set(group.lower().split())
	if group:
	    groups.append(group)

    def check(status):
	message_words = set(status['message'].lower().split())
	for group in groups:
	    if len(group & message_words) == len(group):
		return True
	return False
    return check

def FollowFilter(names):
    names = set()
    for name in names:
	names.add('@' + name.lower().lstrip('@'))

    def check(status):
	message_words = set(status['message'].lower().split())
	message_words.add('@' + status['login'].lower())

	return message_words & names
    return check

def LocationFilter(list_of_boxes):
    boxes = []
    for start in xrange(0, len(list_of_boxes)-3, 4):
	boxes.append(map(float, list_of_boxes[start:start+4]))

    def check(self, status):
	location = status.get('location')
	if not location:
	    return False

	lat, lon = map(float, location.split(','))
	for box in self.boxes:
	    if (box[1] <= lat <= box[3] and
		box[0] <= lon <= box[2]):
		return True
	return False
    return check

def create_filters(id, method, name, args):
    if method == 'sample':
	return SampleFilter(id, args)
    elif name == 'track':
	return TrackFilter(args)
    elif name == 'follow':
	return FollowFilter(args)
    elif name == 'location':
	return LocationFilter(args)
    raise Exception("Unknown filter")
