import streamlit as st
import random
import pandas as pd

from redis_ekle import kelime_ekle
from redis_sil import kelime_sil
from redis_listele import tum_kelimeleri_getir

st.set_page_config(page_title="İngilizce-Türkçe Sözlük", layout="centered")

st.markdown("""
    <style>
    body { background-color: #f5f5f5; }
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #333333;
        transition: all 0.3s ease-in-out;
    }
    h1, h2, h3 { color: #222222; }
    .stButton>button {
        background: linear-gradient(to right, #4a90e2, #6fb1fc);
        color: white;
        border: none;
        padding: 0.6em 1.2em;
        border-radius: 10px;
        transition: background 0.3s ease-in-out;
    }
    .stButton>button:hover {
        background: linear-gradient(to right, #357ABD, #5794e0);
    }
    input, textarea, .stTextInput>div>div>input {
        background-color: white;
        border: 1px solid #ccc;
        border-radius: 8px;
        padding: 0.5em;
        transition: border 0.3s ease-in-out;
    }
    input:focus, textarea:focus {
        border: 1px solid #4a90e2;
    }
    .stDataFrame {
        border-radius: 10px;
        background-color: #ffffff;
    }
    .css-1d391kg { color: #222222; }
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

sayfa = st.sidebar.selectbox("\ud83d\udcc1 Sayfa Se\u00e7iniz", ["\ud83c\udfe0 Ana Sayfa", "\ud83d\udcd6 S\u00f6zl\u00fck", "\ud83c\udfaf Quiz Modu", "\ud83d\udcde S\u00f6zl\u00fck Listesi"])

if sayfa == "\ud83c\udfe0 Ana Sayfa":
    st.markdown("## \ud83d\udfdd\ufe0f \u0130ngilizce-T\u00fcrk\u00e7e S\u00f6zl\u00fck")
    st.markdown("Bu site ile kelime arayabilir, yeni kelime ekleyebilir veya Quiz modunda kendinizi test edebilirsiniz.")

elif sayfa == "\ud83d\udcd6 S\u00f6zl\u00fck":
    st.subheader("\ud83d\udd0d Kelime Ara")
    kelime = st.text_input("Kelime giriniz:", key="arama_kelimesi")

    sozluk = tum_kelimeleri_getir()

    if st.button("Ara"):
        aranan = kelime.strip().lower()

        eslesen_kayit = None
        for k, v in sozluk.items():
            if k.lower() == aranan:
                eslesen_kayit = (k, v)
                break

        if eslesen_kayit:
            kelime_adı, bilgi = eslesen_kayit
            anlam = bilgi.get("anlam", "-")
            es = bilgi.get("es_anlamlar", "")
            st.markdown(f"""
            <div style='background-color:#f0f2f6;padding:15px;border-radius:10px;margin-bottom:10px;'>
                <h4>\ud83c\udf24\ufe0f <b>{kelime_adı.capitalize()}</b></h4>
                <p>\ud83d\udccc <b>Anlamı:</b> {anlam}</p>
                <p>\ud83d\udd70 <b>E\u015f Anlamlılar:</b> {es or 'Yok'}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Kelime bulunamadı.")

    st.subheader("\u270d\ufe0f Yeni Kelime Ekle")
    yeni_kelime = st.text_input("Yeni Kelime:", key="ekle_kelime")
    yeni_anlam = st.text_input("Anlamı:", key="ekle_anlam")
    es_anlamlilar = st.text_input("Bu Kelimenin E\u015f Anlamlıları:", key="ekle_es")

    if st.button("Ekle"):
        if yeni_kelime and yeni_anlam:
            es_anlam_listesi = [w.strip() for w in es_anlamlilar.split(",") if w.strip()]
            kelime_ekle(yeni_kelime, yeni_anlam, es_anlam_listesi)
            st.success(f"\u2705 '{yeni_kelime.capitalize()}' eklenmi\u015ftir.")
        else:
            st.error("L\u00fctfen hem kelimeyi hem anlamını girin.")

    st.subheader("\ud83d\uddd1\ufe0f Kelime Sil")
    sil_kelime = st.text_input("Silinecek Kelime:", key="sil_kelime")
    if st.button("Sil"):
        sonuc = kelime_sil(sil_kelime)
        if sonuc == 1:
            st.warning(f"\u274c '{sil_kelime.capitalize()}' silinmi\u015ftir.")
        else:
            st.error("Kelime bulunamadı.")

elif sayfa == "\ud83c\udfaf Quiz Modu":
    st.subheader("\ud83e\uddea Quiz Modu")
    sozluk = tum_kelimeleri_getir()
    ters_sozluk = {v['anlam']: k for k, v in sozluk.items() if 'anlam' in v}

    if "quiz_kelime" not in st.session_state:
        st.session_state.quiz_kelime = ""
        st.session_state.quiz_cevap = ""
        st.session_state.soru_tipi = ""
        st.session_state.sec_option = ""

    def yeni_soru():
        if not sozluk:
            return

        if random.choice([True, False]):
            st.session_state.soru_tipi = "ing-tr"
            st.session_state.quiz_kelime, bilgi = random.choice(list(sozluk.items()))
            st.session_state.quiz_cevap = bilgi['anlam']
            secenekler = random.sample([v['anlam'] for v in sozluk.values() if 'anlam' in v], min(4, len(sozluk)))
        else:
            st.session_state.soru_tipi = "tr-ing"
            anlam, kelime = random.choice(list(ters_sozluk.items()))
            st.session_state.quiz_kelime = anlam
            st.session_state.quiz_cevap = kelime
            secenekler = random.sample(list(ters_sozluk.values()), min(4, len(ters_sozluk)))

        if st.session_state.quiz_cevap not in secenekler:
            secenekler[random.randint(0, len(secenekler)-1)] = st.session_state.quiz_cevap

        random.shuffle(secenekler)
        st.session_state.sec_options = secenekler

    if st.button("\ud83d\udd04 Yeni Soru"):
        yeni_soru()

    if st.session_state.quiz_kelime:
        st.markdown(f"**\u2753 {st.session_state.quiz_kelime} ne anlama gelir?**")
        for secenek in st.session_state.sec_options:
            if st.button(secenek):
                if secenek == st.session_state.quiz_cevap:
                    st.success("\u2705 Do\u011fru!")
                else:
                    st.error(f"\u274c Yanlış! Doğru cevap: {st.session_state.quiz_cevap}")
                st.session_state.quiz_kelime = ""

elif sayfa == "\ud83d\udcde S\u00f6zl\u00fck Listesi":
    st.header("\ud83d\udcd8 T\u00fcm S\u00f6zl\u00fck Kartları")
    sozluk = tum_kelimeleri_getir()

    if sozluk:
        for kelime, bilgi in sozluk.items():
            st.markdown(f"""
            <div style="background-color:#ffffff;padding:15px;border-radius:10px;margin-bottom:10px;box-shadow:2px 2px 5px rgba(0,0,0,0.05);">
                <h4>\ud83c\udf24\ufe0f <b>{bilgi.get('orijinal', kelime).capitalize()}</b></h4>
                <p><b>\ud83d\udccc Anlamı:</b> {bilgi.get('anlam', '-')}</p>
                <p><b>\ud83d\udd70 E\u015f Anlamlılar:</b> {bilgi.get('es_anlamlar', 'Yok')}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Henüz sözlükte kayıtlı kelime yok.")