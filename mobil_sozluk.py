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

sayfa = st.sidebar.selectbox("📁 Sayfa Seçiniz", ["🏠 Ana Sayfa", "📖 Sözlük", "🎯 Quiz Modu", "📞 Sözlük Listesi"])

if sayfa == "🏠 Ana Sayfa":
    st.markdown("## 🗭 İngilizce-Türkçe Sözlük")
    st.markdown("Bu site ile kelime arayabilir, yeni kelime ekleyebilir veya Quiz modunda kendinizi test edebilirsiniz.")

elif sayfa == "📖 Sözlük":
    st.subheader("🔍 Kelime Ara")
    kelime = st.text_input("Kelime giriniz:", key="arama_kelimesi")
    sozluk = tum_kelimeleri_getir()

    if st.button("Ara"):
        giris = kelime.strip().lower()
        bilgi = sozluk.get(giris)

        if not bilgi:
            st.error("Kelime bulunamadı.")
        else:
            st.markdown(f"""
            <div style='background-color:#f0f2f6;padding:15px;border-radius:10px;margin-bottom:10px;'>
                <h4>🔤 <b>{bilgi.get('orijinal', giris).capitalize()}</b></h4>
                <p><b>📌 Anlamı:</b> {bilgi.get('anlam', '-')}</p>
                <p><b>🝰 Eş Anlamlılar:</b> {bilgi.get('es_anlamlar') or 'Yok'}</p>
            </div>
            """, unsafe_allow_html=True)

    st.subheader("✍️ Yeni Kelime Ekle")
    yeni_kelime = st.text_input("Yeni Kelime:", key="ekle_kelime")
    yeni_anlam = st.text_input("Anlamı:", key="ekle_anlam")
    es_anlamlilar = st.text_input("Bu Kelimenin Eş Anlamlıları:", key="ekle_es")

    if st.button("Ekle"):
        if yeni_kelime and yeni_anlam:
            es_anlam_listesi = [w.strip() for w in es_anlamlilar.split(",") if w.strip()]
            kelime_ekle(yeni_kelime, yeni_anlam, es_anlam_listesi)
            st.success(f"✅ '{yeni_kelime.capitalize()}' eklenmiştir.")
        else:
            st.error("Lütfen hem kelimeyi hem anlamını girin.")

    st.subheader("🗑️ Kelime Sil")
    sil_kelime = st.text_input("Silinecek Kelime:", key="sil_kelime")
    if st.button("Sil"):
        sonuc = kelime_sil(sil_kelime)
        if sonuc == 1:
            st.warning(f"❌ '{sil_kelime.capitalize()}' silinmiştir.")
        else:
            st.error("Kelime bulunamadı.")

elif sayfa == "🎯 Quiz Modu":
    st.subheader("🧪 Quiz Modu")
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

    if st.button("🔄 Yeni Soru"):
        yeni_soru()

    if st.session_state.quiz_kelime:
        st.markdown(f"**❓ {st.session_state.quiz_kelime} ne anlama gelir?**")
        for secenek in st.session_state.sec_options:
            if st.button(secenek):
                if secenek == st.session_state.quiz_cevap:
                    st.success("✅ Doğru!")
                else:
                    st.error(f"❌ Yanlış! Doğru cevap: {st.session_state.quiz_cevap}")
                st.session_state.quiz_kelime = ""

elif sayfa == "📞 Sözlük Listesi":
    st.header("📘 Tüm Sözlük Kartları")
    sozluk = tum_kelimeleri_getir()

    if sozluk:
        for kelime, bilgi in sozluk.items():
            st.markdown(f"""
            <div style="background-color:#ffffff;padding:15px;border-radius:10px;margin-bottom:10px;box-shadow:2px 2px 5px rgba(0,0,0,0.05);">
                <h4>🔤 <b>{bilgi.get('orijinal', kelime).capitalize()}</b></h4>
                <p><b>📌 Anlamı:</b> {bilgi.get('anlam', '-')}</p>
                <p><b>🝰 Eş Anlamlılar:</b> {bilgi.get('es_anlamlar', 'Yok')}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Henüz sözlükte kayıtlı kelime yok.")
