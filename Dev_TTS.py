# -*- coding: utf-8 -*-
'''
Code By: Vũ Tuyển
Designed by: BootstrapMade
GitHub VBot: https://github.com/marion001/VBot_Offline.git
Facebook Group: https://www.facebook.com/groups/1148385343358824
Facebook: https://www.facebook.com/TWFyaW9uMDAx
'''

"""
Phần xử lý dữ liệu các bạn sẽ tự code và xử lý theo ý, sở thích và tùy biến của bạn
Tôi sẽ cung cấp các tài liệu và ví dụ đủ để các bạn xây dựng và phát triển thỏa mãn mày mò, học hỏi
Các dữ liệu và tài nguyên khác có thể tham khảo ở file: Dev_Customization.py
"""

# Thư Viện VBot: Lib
import os
import re
from unidecode import unidecode
from google.cloud import texttospeech

# Giả lập thư viện Lib
class Lib:
    directory_tts = "/home/pi/VBot_Offline/TTS_Audio/"

    @staticmethod
    def tts_string(text_input):
        """
        Chuyển văn bản thành tên file hợp lệ.
        Chuyển tiếng Việt có dấu sang không dấu, thay khoảng trắng và ký tự đặc biệt bằng gạch nối,
        loại bỏ ký tự không hợp lệ, giới hạn độ dài.
        """
        if not text_input or not isinstance(text_input, str):
            return "default"
        # Chuyển tiếng Việt có dấu sang không dấu và chuyển thành chữ thường
        cleaned = unidecode(text_input).lower()
        # Thay khoảng trắng, dấu phẩy, và ký tự đặc biệt bằng gạch nối
        cleaned = re.sub(r'[\s,.!?;:/\\]+', '-', cleaned)
        # Loại bỏ ký tự không phải chữ cái, số, hoặc gạch nối
        cleaned = re.sub(r'[^a-z0-9-]', '', cleaned)
        # Loại bỏ nhiều gạch nối liên tiếp
        cleaned = re.sub(r'-+', '-', cleaned)
        # Loại bỏ gạch nối ở đầu hoặc cuối
        cleaned = cleaned.strip('-')
        # Giới hạn độ dài tên file
        max_length = 50
        cleaned = cleaned[:max_length]
        # Nếu rỗng sau khi xử lý, trả về tên mặc định
        return cleaned if cleaned else "default"

    @staticmethod
    def show_log(message, color=None):
        """
        Giả lập hàm show_log. Thay bằng triển khai thực tế nếu có.
        """
        print(message)  # Thay bằng Lib.show_log thực tế nếu có

"""
hàm dev_tts cần được giữ nguyên,
Mọi tùy biến và xử lý dữ liệu các bạn dev sẽ code bên trong hàm này
"""
def dev_tts(text_input):
    # Lib.show_log(f"[DEV TTS] Dữ liệu truyền vào để chuyển đổi là: {text_input}", color=Lib.Color.GREEN)
    Lib.show_log(f"[DEV TTS] Dữ liệu truyền vào để chuyển đổi là: {text_input}")

    # Đường Dẫn Path Lưu File TTS (Giữ Nguyên dòng output_file_path này)
    output_file_path = Lib.directory_tts+"/"+Lib.tts_string(text_input)+".mp3"

    # Đường dẫn đến file JSON xác thực
    duong_dan_json = "/home/pi/VBot_Offline/sttgoogle.json"

    try:
        # Thiết lập biến môi trường GOOGLE_APPLICATION_CREDENTIALS
        if not os.path.exists(duong_dan_json):
            # Lib.show_log(f"[DEV TTS] Lỗi: File JSON xác thực không tồn tại tại: {duong_dan_json}", color=Lib.Color.RED)
            Lib.show_log(f"[DEV TTS] Lỗi: File JSON xác thực không tồn tại tại: {duong_dan_json}")
            return None
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = duong_dan_json
        # Lib.show_log(f"[DEV TTS] Đã thiết lập biến môi trường GOOGLE_APPLICATION_CREDENTIALS trỏ đến {duong_dan_json}", color=Lib.Color.YELLOW)
        Lib.show_log(f"[DEV TTS] Đã thiết lập biến môi trường GOOGLE_APPLICATION_CREDENTIALS trỏ đến {duong_dan_json}")

        # Tạo thư mục đầu ra nếu chưa tồn tại
        os.makedirs(Lib.directory_tts, exist_ok=True)

        # Khởi tạo client Text-to-Speech
        client = texttospeech.TextToSpeechClient()

        # Thiết lập văn bản đầu vào
        dau_vao = texttospeech.SynthesisInput(text=text_input)

        # Cấu hình tham số giọng nói
        giong = texttospeech.VoiceSelectionParams(
            language_code="vi-VN",  # Mã ngôn ngữ cho tiếng Việt
            name="vi-VN-Standard-A",  # Giọng tiếng Việt chuẩn
        )

        # Cấu hình định dạng đầu ra âm thanh
        cau_hinh_am_thanh = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,  # Định dạng MP3
            speaking_rate=0.9,                             # Tốc độ nói (tương tự Zalo SPEED_TTS)
            pitch=0.0,                                     # Cao độ bình thường
            volume_gain_db=0.0                             # Âm lượng bình thường
        )

        # Thực hiện yêu cầu chuyển văn bản thành giọng nói
        phan_hoi = client.synthesize_speech(
            input=dau_vao, voice=giong, audio_config=cau_hinh_am_thanh
        )

        # Lưu âm thanh vào file
        with open(output_file_path, 'wb') as audio_file:
            audio_file.write(phan_hoi.audio_content)
        # Lib.show_log(f"[DEV TTS] File được tải xuống thành công tại: {output_file_path}", color=Lib.Color.GREEN)
        Lib.show_log(f"[DEV TTS] File được tải xuống thành công tại: {output_file_path}")

        # Trả dữ liệu về cho chương trình phát TTS (đường dẫn path)
        return output_file_path

    except Exception as e:
        # Lib.show_log(f"[DEV TTS] Lỗi khi xử lý âm thanh: {e}", color=Lib.Color.RED)
        Lib.show_log(f"[DEV TTS] Lỗi khi xử lý âm thanh: {e}")
        # Trả về None nếu lỗi
        return None

if __name__ == "__main__":
    # Văn bản mẫu để kiểm tra
    van_ban_mau = "Xin chào, đây là bài kiểm tra API chuyển văn bản thành giọng nói"
    dev_tts(van_ban_mau)