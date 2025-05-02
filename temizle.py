import redis

r = redis.Redis(
    host="redis-13967.c300.eu-central-1-1.ec2.redns.redis-cloud.com",
    port=13967,
    username="default",
    password="he7hSzA089lnCwBFRv4B62EY0S9rmOP2",
    decode_responses=True
)

tum_keyler = r.keys('*')

if not tum_keyler:
    print("✅ Redis zaten temiz.")
else:
    for key in tum_keyler:
        r.delete(key)
        print(f"🗑️ Silindi: {key}")

    print(f"\n✅ Toplam {len(tum_keyler)} anahtar başarıyla silindi.")
