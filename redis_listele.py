from redis_baglanti import redis_baglan

def tum_kelimeleri_getir():
    r = redis_baglan()
    kelimeler = {}

    for key in r.keys('*'):
        if r.type(key) != 'hash':
            continue

        veri = r.hgetall(key)
        anlam = veri.get('anlam', '-')
        es_anlam = veri.get('es_anlamlar', '')
        orijinal = veri.get('orijinal', key)
        
        # Sözlükte anahtar olarak key (küçük harfli kelime) kullanılmalı
        kelimeler[key] = {
            "orijinal": orijinal,  # Orijinal kelimeyi de veri içinde tut
            "anlam": anlam,
            "es_anlamlar": es_anlam
        }

    # Alfabetik sıralama (küçük har