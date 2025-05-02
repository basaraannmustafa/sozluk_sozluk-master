# redis_listele.py
from redis_baglanti import redis_baglan

def tum_kelimeleri_getir():
    r = redis_baglan()
    kelimeler = {}

    for key in r.keys("*"):
        if r.type(key) != b'hash':
            continue

        veri = r.hgetall(key)
        anlam = veri.get("anlam", "")
        es_anlam = veri.get("es_anlamlar", "")
        orijinal = veri.get("orijinal", key)

        # normalize edilmiş key ile saklıyoruz
        kelimeler[key.lower()] = {
            "anlam": anlam,
            "es_anlamlar": es_anlam,
            "orijinal": orijinal
        }

    return dict(sorted(kelimeler.items()))
