import librosa
import numpy as np
from pathlib import Path
from tqdm import tqdm
from pydub import AudioSegment

# === CONFIGURACIÓN ===
input_folder = Path(r"C:\Users\Daniel\Downloads\audiopruebas\Pia")  # carpeta con MP3
output_folder = input_folder / "recortes"
output_folder.mkdir(exist_ok=True)

SEGMENT_DURATION = 30  # segundos de cada recorte

# === FUNCIONES ===
def get_most_significant_segment(y, sr, duration=SEGMENT_DURATION):
    """Devuelve el inicio del segmento más significativo según energía en frecuencias 200-8000 Hz."""
    total_duration = librosa.get_duration(y=y, sr=sr)
    
    # Espectrograma
    S = np.abs(librosa.stft(y, n_fft=2048, hop_length=512))
    freqs = librosa.fft_frequencies(sr=sr, n_fft=2048)
    
    # Rango relevante: 200 Hz a 8000 Hz
    mask = (freqs >= 200) & (freqs <= 8000)
    S_focus = S[mask, :]
    
    # Energía promedio por frame
    energy_per_frame = S_focus.mean(axis=0)
    times = librosa.frames_to_time(np.arange(len(energy_per_frame)), sr=sr, hop_length=512)
    
    # Buscar segmento de mayor energía
    best_start = 0
    max_energy = 0
    for i in range(len(times)):
        start_time = times[i]
        end_time = start_time + duration
        if end_time > total_duration:
            break
        mask = (times >= start_time) & (times < end_time)
        segment_energy = energy_per_frame[mask].mean()
        if segment_energy > max_energy:
            max_energy = segment_energy
            best_start = start_time
    return best_start

# === PROCESO PRINCIPAL ===
mp3_files = list(input_folder.glob("*.mp3"))

if not mp3_files:
    print("No se encontraron archivos MP3 en la carpeta.")
else:
    for audio_file in tqdm(mp3_files):
        print(f"\nProcesando {audio_file.name}...")
        y, sr = librosa.load(audio_file, sr=None)
        
        # Obtener inicio del segmento más significativo
        best_start = get_most_significant_segment(y, sr)
        start_sample = int(best_start * sr)
        end_sample = int((best_start + SEGMENT_DURATION) * sr)
        y_clip = y[start_sample:end_sample]
        
        # Convertir float32 [-1,1] a int16 [-32768,32767]
        y_int16 = np.int16(y_clip * 32767)
        
        # Convertir a AudioSegment para exportar como MP3
        clip = AudioSegment(
            y_int16.tobytes(),
            frame_rate=sr,
            sample_width=y_int16.dtype.itemsize,
            channels=1
        )
        
        output_path = output_folder / f"{audio_file.stem}_clip.mp3"
        clip.export(output_path, format="mp3")
        
        print(f" → Segmento: {best_start:.1f}s - {best_start + SEGMENT_DURATION:.1f}s")
        print(f" → Guardado en: {output_path}")

print("\n Todos los audios procesados.")
