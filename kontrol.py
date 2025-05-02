import redis

r = redis.Redis(
    host="redis-13967.c300.eu-central-1-1.ec2.redns.redis-cloud.com",
    port=13967,
    username="default",
    password="he7hSzA089lnCwBFRv4B62EY0S9rmOP2",
    decode_responses=True
)

keys = r.keys('*')

if not keys:
    print("🎉 Tertemiz! Redis veritabanında hiç veri yok.")
else:
    print("📦 Hâlâ şu key'ler var:")
    for key in keys:
        print(f" - {key}")
