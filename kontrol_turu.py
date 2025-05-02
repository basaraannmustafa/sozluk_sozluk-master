import redis

r = redis.Redis(
    host="redis-13967.c300.eu-central-1-1.ec2.redns.redis-cloud.com",
    port=13967,
    username="default",
    password="he7hSzA089lnCwBFRv4B62EY0S9rmOP2",
    decode_responses=True
)

tum_keyler = r.keys('*')

for key in tum_keyler:
    veri_tipi = r.type(key)
    print(f"🔎 {key} ➜ {veri_tipi}")
