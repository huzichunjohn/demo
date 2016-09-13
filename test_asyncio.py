import asyncio
import time
import concurrent

@asyncio.coroutine
def clock():
    while True:
        print("Current time from asynchronous code: {}".format(int(time.time())))
        yield from asyncio.sleep(1)

def blocking():
    while True:
        print("Current time from blocking code: {}".format(int(time.time())))
        time.sleep(1)
        raise Exception("Test")

def main():
    loop = asyncio.get_event_loop()
    block = loop.run_in_executor(None, blocking)
    async = asyncio.async(clock())
    loop.run_until_complete(asyncio.wait([block, async], return_when=concurrent.futures.FIRST_COMPLETED))
    print(block.exception())

if __name__ == "__main__":
    main()
