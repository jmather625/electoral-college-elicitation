import threading

LOCK = threading.Lock()

# store session info on everyone
SESSION_DATA = dict()
MAX_ID = 0


def create_new_session() -> int:
    global MAX_ID
    LOCK.acquire()
    new_id = MAX_ID
    MAX_ID += 1
    LOCK.release()
    return new_id


def get_session_data(sid: int):
    LOCK.acquire()
    if sid not in SESSION_DATA:
        LOCK.release()
        return None
    v = SESSION_DATA[sid]
    LOCK.release()
    return v


def insert_session_data(sid: int, data):
    LOCK.acquire()
    SESSION_DATA[sid] = data
    LOCK.release()


def end_session(sid: int):
    LOCK.acquire()
    if sid in SESSION_DATA:
        del SESSION_DATA[sid]
