import redis

if __name__ == "__main__":
    conn = redis.Redis(host='moneteam-1.csse.rose-hulman.edu', port=6379);
    conn.set("hi","byebye")
