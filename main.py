import customtkinter as ctk
import sounddevice as sd
import numpy as np
from scipy import signal
import threading

class YahyaVoiceChanger(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Pencere Ayarları
        self.title("Yahya Yapımı - Voice Changer Pro")
        self.geometry("500x600")
        ctk.set_appearance_mode("dark")

        # Değişkenler
        self.is_running = False
        self.pitch_shift = 1.0  # 1.0 normal, 0.5 kalın, 1.5 ince
        self.sample_rate = 44100
        self.buffer_size = 1024
        self.stream = None

        # --- ARAYÜZ ---
        self.label_head = ctk.CTkLabel(self, text="YAHYA SES DEĞİŞTİRİCİ", font=("Impact", 30), text_color="#FF8C00")
        self.label_head.pack(pady=20)

        # Pitch Kontrol
        self.label_pitch = ctk.CTkLabel(self, text=f"Ses Tonu (Pitch): {self.pitch_shift}")
        self.label_pitch.pack()
        
        self.slider_pitch = ctk.CTkSlider(self, from_=0.5, to=2.0, command=self.update_pitch)
        self.slider_pitch.set(self.pitch_shift)
        self.slider_pitch.pack(pady=10, padx=30, fill="x")

        self.info_text = ctk.CTkLabel(self, text="0.5: Canavar/Kalın | 1.0: Normal | 1.5+: Çocuk/İnce", font=("Arial", 10))
        self.info_text.pack()

        # Başlat/Durdur Butonu
        self.btn_toggle = ctk.CTkButton(self, text="SES DEĞİŞTİRMEYİ BAŞLAT", font=("Arial", 14, "bold"),
                                        fg_color="green", hover_color="#006400", command=self.toggle_voice)
        self.btn_toggle.pack(pady=40, padx=50, fill="x")

        # Durum Bilgisi
        self.st_label = ctk.CTkLabel(self, text="DURUM: KAPALI", text_color="red", font=("Arial", 12, "bold"))
        self.st_label.pack()

        ctk.CTkLabel(self, text="Not: Discord'da kullanmak için VB-Cable gereklidir.", text_color="gray", font=("Arial", 10)).pack(side="bottom", pady=10)

    def update_pitch(self, val):
        self.pitch_shift = round(float(val), 2)
        self.label_pitch.configure(text=f"Ses Tonu (Pitch): {self.pitch_shift}")

    def audio_callback(self, indata, outdata, frames, time, status):
        """Sesi anlık olarak işleyen fonksiyon"""
        if self.is_running:
            # Sesi işle (Basic Pitch Shift)
            # Not: Gerçek zamanlı pitch shift için basit bir resampling kullanıyoruz
            indices = np.round(np.arange(0, len(indata), self.pitch_shift))
            indices = indices[indices < len(indata)].astype(int)
            
            resampled_data = indata[indices]
            
            # Veriyi orijinal boyuta getir (Padding veya Truncate)
            if len(resampled_data) < frames:
                resampled_data = np.pad(resampled_data, ((0, frames - len(resampled_data)), (0, 0)), mode='constant')
            else:
                resampled_data = resampled_data[:frames]
                
            outdata[:] = resampled_data
        else:
            outdata[:] = indata

    def toggle_voice(self):
        if not self.is_running:
            self.is_running = True
            self.btn_toggle.configure(text="SESİ DURDUR", fg_color="red", hover_color="#8B0000")
            self.st_label.configure(text="DURUM: AKTİF (SES İŞLENİYOR)", text_color="green")
            
            # Ses akışını başlat
            self.stream = sd.Stream(callback=self.audio_callback, channels=1, samplerate=self.sample_rate, blocksize=self.buffer_size)
            self.stream.start()
        else:
            self.is_running = False
            self.btn_toggle.configure(text="SES DEĞİŞTİRMEYİ BAŞLAT", fg_color="green", hover_color="#006400")
            self.st_label.configure(text="DURUM: KAPALI", text_color="red")
            if self.stream:
                self.stream.stop()
                self.stream.close()

if __name__ == "__main__":
    app = YahyaVoiceChanger()
    app.mainloop()
      
