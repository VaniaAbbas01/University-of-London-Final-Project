import librosa
import numpy as np
import parselmouth
from parselmouth.praat import call

class AudioAnalyser:
    def __init__(self, audio_file):
        self.audio_file = audio_file
        self.analysis_results = {}

    def extractFeatures(self):
        """Extract Audio Features such as pitch, jitter"""
        # Load file with librosa
        y, sr = librosa.load(self.audio_file)
        duration_sec = librosa.get_duration(y=y, sr=sr)

        if duration_sec == 0:
            raise ValueError("Audio file is empty or corrupted")

        # Librosa features
        # Pitch (F0)
        f0, voiced_flag, voiced_probs = librosa.pyin(y, fmin=75, fmax=500)
        avg_pitch = np.nanmean(f0)
        pitch_var = np.nanstd(f0)

        # Loudness
        rms = librosa.feature.rms(y=y)
        avg_loudness_db = float(librosa.amplitude_to_db(rms).mean())

        # Speaking rate proxy
        voiced_frames = len(f0[~np.isnan(f0)])
        speech_rate = voiced_frames / duration_sec

        # Silence detection (pause ratio)
        intervals = librosa.effects.split(y, top_db=30)
        total_silence = duration_sec - sum([(e - s)/sr for s, e in intervals])
        pause_ratio = total_silence / duration_sec

        # Parselmouth features
        sound = parselmouth.Sound(self.audio_file)

        pitch = sound.to_pitch()
        intensity = sound.to_intensity()

        point_process = call(sound, "To PointProcess (periodic, cc)", 75, 500)

        # Fixed: Added all required parameters
        jitter = call(point_process, "Get jitter (local)", 0.0001, 0.02, 1.3, 1.6, 1.3)
        shimmer = call([sound, point_process], "Get shimmer (local)", 0.0001, 0.02, 1.3, 1.6, 1.3, 1.6)

        hnr = call(sound, "To Harmonicity (cc)", 0.01, 75, 0.1, 1.0)
        hnr_mean = call(hnr, "Get mean", 0, 0)

        # Extract time series data for visualization
        pitch_series = self.extractPitchTimeSeries(pitch)
        intensity_series = self.extractIntensityTimeSeries(intensity)

        # Collect features
        features = {
            # Librosa
            "avg_pitch": avg_pitch,
            "pitch_var": pitch_var,
            "avg_loudness_db": avg_loudness_db,
            "speech_rate": speech_rate,
            "pause_ratio": pause_ratio,
            # Parselmouth
            "jitter": jitter,
            "shimmer": shimmer,
            "hnr": hnr_mean
        }

        self.analysis_results = {
            "features": features,
            "feedback": self.interpretFeatures(features),
            "pitch_series": pitch_series,
            "intensity_series": intensity_series
        }

        return self.analysis_results

    def extractPitchTimeSeries(self, pitch):
        """Extract pitch values over time for visualization"""
        try:
            times = pitch.xs()
            values = [pitch.get_value_at_time(t) for t in times]
            
            # Filter out undefined values and create time-value pairs
            time_series = []
            for i, (time, value) in enumerate(zip(times, values)):
                if not np.isnan(value) and value > 0:  # Valid pitch values
                    time_series.append({"time": float(time), "value": float(value)})
            
            return time_series
        except Exception as e:
            print(f"Error extracting pitch time series: {e}")
            return []

    def extractIntensityTimeSeries(self, intensity):
        """Extract intensity values over time for visualization"""
        try:
            times = intensity.xs()
            values = [intensity.get_value_at_time(t) for t in times]
            
            # Create time-value pairs
            time_series = []
            for time, value in zip(times, values):
                if not np.isnan(value):  # Valid intensity values
                    time_series.append({"time": float(time), "value": float(value)})
            
            return time_series
        except Exception as e:
            print(f"Error extracting intensity time series: {e}")
            return []

    def interpretFeatures(self, f):
        """Interpret the Features and provide feedback"""
        feedback = {}

        # Pitch
        if f["pitch_var"] < 20:
            feedback["pitch"] = "Your speech sounds monotone, try adding more pitch variation."
        elif f["avg_pitch"] < 100:
            feedback["pitch"] = "Your pitch is low, project more energy."
        elif f["avg_pitch"] > 250:
            feedback["pitch"] = "Your pitch is high, relax and bring it down."
        else:
            feedback["pitch"] = "Your pitch is in a healthy range."

        # Loudness
        if f["avg_loudness_db"] < -30:
            feedback["loudness"] = "Your voice is too soft, speak louder."
        elif f["avg_loudness_db"] > -15:
            feedback["loudness"] = "Your voice is quite loud, soften a little."
        else:
            feedback["loudness"] = "Good volume control."

        # Speech rate
        if f["speech_rate"] > 5:
            feedback["rate"] = "You're speaking too fast, try slowing down."
        elif f["speech_rate"] < 2:
            feedback["rate"] = "You're speaking quite slowly, try picking up the pace."
        else:
            feedback["rate"] = "Your pace is natural."

        # Pauses
        if f["pause_ratio"] > 0.4:
            feedback["pauses"] = "You pause a lot, try smoother delivery."
        elif f["pause_ratio"] < 0.05:
            feedback["pauses"] = "Almost no pauses — try adding short breaks for clarity."
        else:
            feedback["pauses"] = "Good use of pauses."

        # Voice quality
        if f["jitter"] > 0.02:
            feedback["jitter"] = "Your pitch stability is low, may indicate nervousness."
        if f["shimmer"] > 0.04:
            feedback["shimmer"] = "Noticeable amplitude variation — relax and breathe steadily."
        if f["hnr"] < 10:
            feedback["hnr"] = "Your voice sounds breathy — try clearer articulation."
        else:
            feedback["hnr"] = "Your voice clarity is good."

        return feedback