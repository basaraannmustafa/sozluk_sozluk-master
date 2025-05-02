import redis

r = redis.Redis(
    host="redis-13967.c300.eu-central-1-1.ec2.redns.redis-cloud.com",
    port=13967,
    username="default",
    password="he7hSzA089lnCwBFRv4B62EY0S9rmOP2",
    decode_responses=True
)

print("🔗 Bağlantı başarılı mı?:", r.ping())

print("📦 Kayıtlı tüm key'ler:")
for key in r.keys('*'):
    print("KEY:", key, "| TYPE:", r.type(key))
    if r.type(key) == b'hash':
        print(" →", r.hgetall(key))
    else:
        print(" →", r.get(key))
