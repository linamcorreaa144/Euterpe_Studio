
# =====================================================
# 🎙️ EUTERPE STUDIO – Creador de artistas generativos
# =====================================================
import streamlit as st
import json
import librosa
import librosa.display
import matplotlib.pyplot as plt
from pydub import AudioSegment
from io import BytesIO
import numpy as np

# ---- Animación y logo ----
import os
import streamlit as st

# 🎨 Estilo CSS para animación
st.markdown("""
    <style>
    .fade-in {
        animation: fadeIn 2s ease-in-out;
        opacity: 0;
        animation-fill-mode: forwards;
    }
    @keyframes fadeIn {
        from {opacity: 0;}
        to {opacity: 1;}
    }
    </style>
""", unsafe_allow_html=True)

# 📁 Ruta absoluta del logo
logo_path = r"C:\Users\Maria Alejandra\Desktop\Euterpe_AI_Logo.png"

# 🧭 Distribución en columnas
col1, col2 = st.columns([1, 4])

with col1:
    if os.path.exists(logo_path):
        st.image(
            logo_path, 
            width=140, 
            caption="Euterpe Studio", 
            output_format="auto"
        )
    else:
        st.warning("⚠️ No se encontró el logo de Euterpe. Verifica la ruta del archivo o su nombre.")

with col2:
    st.markdown(
        """
        <div class="fade-in">
            <h1 style='font-size:2.5em; margin-bottom:0;'>🎼 Euterpe AI Studio</h1>
            <p style='font-size:1.2em; color:gray;'>Tu asistente creativo musical impulsado por IA</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# =====================================================
# 🎨 Cabecera y diseño general
# =====================================================


st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/3/3e/Muse_Euterpe_Louvre_Ma436_n2.jpg", use_column_width=True)
st.sidebar.markdown("""
**Euterpe** fue la musa griega de la música y la poesía lírica.  
Aquí, inspira la creación de artistas digitales que interpretan canciones con identidad propia.
""")

st.markdown("---")


# =====================================================
# 📚 Diccionario de ayuda
# =====================================================
HELP_DICT = {
    "gesture_style": {
        "title": "Gestos característicos",
        "desc": "Describe los movimientos escénicos más comunes del artista: manos, postura, dirección de la mirada, ritmo corporal.",
        "example": "mano al rostro, brazo extendido, inclinación lenta"
    },
    "vocal_tone": {
        "title": "Tono vocal",
        "desc": "Define la textura emocional y técnica de la voz: suave, ronca, vibrante, quebrada, teatral, susurrada.",
        "example": "voz cálida al inicio, vibrato profundo, se quiebra al final"
    },
    "emotion_palette": {
        "title": "Paleta emocional",
        "desc": "Lista de emociones que predominan en la interpretación o la canción. Ayuda a definir la expresividad del artista.",
        "example": "melancolía, deseo, culpa, redención"
    },
    "color_theme": {
        "title": "Paleta de color escénica",
        "desc": "Colores dominantes del escenario, vestuario o atmósfera visual. Sirve como referencia estética para Gemmy o Grok.",
        "example": "rojo intenso, negro, ámbar dorado, gris humo"
    }
}



# =====================================================
# 🧩 Tabs principales
# =====================================================
tab1, tab2, tab3 = st.tabs(["🧠 Perfil del artista", "🎵 Cargar canción", "🕺 Sincronización de gestos"])


# =====================================================
# TAB 1 – PERFIL DEL ARTISTA (VERSIÓN FLUIDA)
# =====================================================
with tab1:
    st.header("🧠 Crear o editar perfil de artista")

    # Form principal
    with st.form("artist_form"):
        st.subheader("🪪 Identidad básica")
        artist_id = st.text_input(
            "ID único del artista",
            help="Este ID actúa como semilla. Guárdalo para futuros proyectos del mismo personaje."
        )
        name = st.text_input("Nombre artístico")
        age = st.number_input("Edad (numérica)", min_value=0, value=25)

        st.subheader("🎨 Apariencia")
        hair = st.text_input("Cabello")
        eyes = st.text_input("Ojos")
        skin = st.text_input("Piel")
        body_type = st.text_input("Tipo de cuerpo")
        outfit = st.text_input("Vestimenta o estilo")

        st.subheader("🎭 Perfil escénico")
        # Gestos con ayuda contextual
        st.markdown("#### Gestos característicos")
        with st.expander("📘 Ayuda para 'Gestos'"):
            st.markdown(f"**{HELP_DICT['gesture_style']['title']}**")
            st.write(HELP_DICT['gesture_style']['desc'])
            st.caption("Ejemplo: " + HELP_DICT['gesture_style']['example'])
            st.info("💡 Ejemplo extendido:\n`mirada al horizonte, mano al pecho, paso atrás lento, brazo extendido hacia el público`")
        gesture_style = st.text_input(
            "Gestos (separados por coma)",
            placeholder=HELP_DICT["gesture_style"]["example"],
            help="Usa el panel de ayuda arriba para inspiración."
        )
        if st.form_submit_button("🎲 Insertar ejemplo de gestos", key="gestos"):
            gesture_style = HELP_DICT["gesture_style"]["example"]
            st.info("🎬 Ejemplo insertado automáticamente.")

        # Tono vocal
        st.markdown("#### Tono vocal")
        with st.expander("📘 Ayuda para 'Tono vocal'"):
            st.markdown(f"**{HELP_DICT['vocal_tone']['title']}**")
            st.write(HELP_DICT['vocal_tone']['desc'])
            st.caption("Ejemplo: " + HELP_DICT['vocal_tone']['example'])
        vocal_tone = st.text_input("Tono vocal / estilo", placeholder=HELP_DICT["vocal_tone"]["example"])

        # Energía
        performance_energy = st.select_slider("Nivel de energía escénica", options=["Baja", "Media", "Alta"], value="Media")

        st.subheader("🎵 Perfil de la canción")
        title = st.text_input("Título de la canción")
        theme = st.text_area("Tema / narrativa", help="Describe la historia o emoción principal de la canción.")

        # Paleta emocional
        st.markdown("#### Paleta emocional")
        with st.expander("📘 Ayuda para 'Emociones'"):
            st.markdown(f"**{HELP_DICT['emotion_palette']['title']}**")
            st.write(HELP_DICT['emotion_palette']['desc'])
            st.caption("Ejemplo: " + HELP_DICT['emotion_palette']['example'])
        emotion_palette = st.text_input("Emociones (separadas por coma)", placeholder=HELP_DICT["emotion_palette"]["example"])

        tempo = st.text_input("Tempo o ritmo (ej: Lento, Moderado, Rápido)")

        # Paleta de color
        st.markdown("#### Paleta de color escénica")
        with st.expander("📘 Ayuda para 'Colores'"):
            st.markdown(f"**{HELP_DICT['color_theme']['title']}**")
            st.write(HELP_DICT['color_theme']['desc'])
            st.caption("Ejemplo: " + HELP_DICT['color_theme']['example'])
        color_theme = st.text_input("Colores (separados por coma)", placeholder=HELP_DICT["color_theme"]["example"])

        st.subheader("🖼️ Visuales y avatar")
        portrait = st.text_input("Ruta de imagen o avatar (opcional)")
        lighting = st.text_input("Iluminación escénica")
        camera_style = st.text_input("Estilo de cámara o encuadre visual")

        # Botón principal de guardar perfil
        submitted = st.form_submit_button("💾 Guardar perfil de artista")
        if submitted:
            artist_profile = {
                "artist_id": artist_id,
                "name": name,
                "age": age,
                "appearance": {
                    "hair": hair,
                    "eyes": eyes,
                    "skin": skin,
                    "body_type": body_type,
                    "outfit": outfit
                },
                "stage_persona": {
                    "gesture_style": gesture_style,
                    "vocal_tone": vocal_tone,
                    "performance_energy": performance_energy
                },
                "song_profile": {
                    "title": title,
                    "theme": theme,
                    "emotion_palette": [e.strip() for e in emotion_palette.split(",") if e.strip()],
                    "tempo": tempo,
                    "color_theme": [c.strip() for c in color_theme.split(",") if c.strip()]
                },
                "visual_assets": {
                    "portrait": portrait,
                    "lighting": lighting,
                    "camera_style": camera_style
                }
            }
            json_name = f"{artist_id or name}.json"
            with open(json_name, "w", encoding="utf-8") as f:
                json.dump(artist_profile, f, ensure_ascii=False, indent=2)
            st.success(f"✅ Perfil guardado como {json_name}")
            st.json(artist_profile)

# =====================================================
# TAB 2 – CARGAR CANCIÓN
# =====================================================
with tab2:
    st.header("🎵 Cargar canción o voz")

    with st.form("audio_form"):
        audio_file = st.file_uploader("Sube un archivo de audio (.mp3 o .wav)", type=["mp3", "wav"])
        submitted_audio = st.form_submit_button("🎧 Procesar audio")

        if submitted_audio and audio_file:
            try:
                # Convertir a WAV para análisis
                audio = AudioSegment.from_file(audio_file)
                wav_io = BytesIO()
                audio.export(wav_io, format="wav")
                wav_io.seek(0)

                y, sr = librosa.load(wav_io, sr=None)
                tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
                times = librosa.frames_to_time(beats, sr=sr)

                st.audio(audio_file)
                st.write(f"🎚️ Tempo estimado: **{tempo:.2f} BPM** – Beats detectados: {len(beats)}")

                fig, ax = plt.subplots(figsize=(10, 3))
                librosa.display.waveshow(y, sr=sr, alpha=0.7)
                ax.vlines(times, -1, 1, color="r", linestyle="--")
                st.pyplot(fig)

                st.session_state["beats_times"] = times.tolist()
                st.success("✅ Audio procesado correctamente.")
            except Exception as e:
                st.error(f"❌ Error al procesar el audio: {e}")

import time  # ⚠️ necesario para time.sleep()

# =====================================================
# TAB 3 – Sincronización avanzada de gestos + Lipsy
# =====================================================
with tab3:
    st.header("🕺 Sincronización avanzada: Gestos + Labios 💋")

    uploaded_json = st.file_uploader("Sube modelo de gestos y fonemas (.json)", type=["json"])
    start_preview = st.button("▶️ Reproducir preview avanzado")

    gesture_emojis = {
        "mano al pecho": "🤚",
        "brazo extendido": "🖐️",
        "paso atrás": "👣",
        "mirada al horizonte": "👀",
        "default": "💃"
    }
    lipsy_map = {"A": "👄", "E": "🫦", "I": "👅", "O": "🫨", "U": "💋", "default": "👄"}

    gestures = ["default"]
    phonemes = ["A","E","I","O","U"]

    if uploaded_json:
        modelo = json.load(uploaded_json)
        gestures = modelo.get("gestures", ["default"])
        phonemes = modelo.get("phonemes", ["A","E","I","O","U"])

    if "beats_times" in st.session_state and uploaded_json and start_preview:
        times = st.session_state["beats_times"]
        preview_placeholder = st.empty()

        for i in range(len(times)):
            # Elegir gesto y fonema
            gesture = gestures[i % len(gestures)].strip()
            phoneme = phonemes[i % len(phonemes)].strip()

            # Mostrar en dos columnas para claridad
            col_g, col_l = st.columns(2)
            with col_g:
                preview_placeholder.markdown(f"🕒 **{times[i]:.2f}s** → {gesture_emojis.get(gesture,'💃')} **{gesture}**")
            with col_l:
                preview_placeholder.markdown(f"💋 **{phoneme}** {lipsy_map.get(phoneme.upper(),'👄')}")

            # Duración hasta el siguiente beat
            if i < len(times)-1:
                duration = times[i+1] - times[i]
            else:
                duration = 0.5  # último beat, mostrar un poquito
            time.sleep(duration)
        
        preview_placeholder.markdown("✅ Preview avanzado finalizado 🎶✨💋")



# =====================================================
# PIE DE PÁGINA
# =====================================================
st.markdown("---")
st.caption("✨ Euterpe Studio v1.2 — Integración creativa de IA, música y performance digital. Hecho con ❤️ por Ekatte & Ian")
