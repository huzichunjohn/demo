# memcached

~~~~ .sh
telnet localhost 11211
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
stats items
STAT items:1:number 1
STAT items:1:age 296
STAT items:1:evicted 0
STAT items:1:evicted_nonzero 0
STAT items:1:evicted_time 0
STAT items:1:outofmemory 0
STAT items:1:tailrepairs 0
STAT items:1:reclaimed 0
STAT items:1:expired_unfetched 0
STAT items:1:evicted_unfetched 0
END
stats cachedump 1 0
ITEM :1:mydemo [11 b; 1467887190 s]
END
get :1:mydemo
END
quit
Connection closed by foreign host.
~~~~
