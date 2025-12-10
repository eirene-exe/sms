from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
# CORS'u açıyoruz ki senin siten bu Replit sunucusuna erişebilsin
CORS(app)

@app.route('/sms-gonder', methods=['POST'])
def proxy_sms():
    try:
        # 1. Senin sitenden gelen veriyi al
        data = request.json
        numara = data.get('target')

        if not numara:
            return jsonify({"error": "Numara girilmedi"}), 400

        # 2. HEDEF SİTEYE GİDECEK İSTEK (Bypass kısmı burası)
        # Replit sunucusu sanki bir tarayıcıymış gibi davranacak
        target_url = "https://erenbaba.pro/api/sms"
        
        payload = {"target": numara}
        
        # Buradaki headerlar hedef sitenin seni engellemesini zorlaştırır
        fake_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Content-Type": "application/json",
            "Referer": "https://erenbaba.pro/",
            "Origin": "https://erenbaba.pro"
        }

        # 3. İsteği Replit üzerinden hedefe gönderiyoruz
        response = requests.post(target_url, json=payload, headers=fake_headers)

        # 4. Sonucu senin sitene geri döndürüyoruz
        return jsonify({
            "durum": "istek_gonderildi",
            "hedef_cevap_kodu": response.status_code,
            "hedef_cevap": response.text
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # 0.0.0.0 ile dış dünyaya açıyoruz
    app.run(host='0.0.0.0', port=8080)  
