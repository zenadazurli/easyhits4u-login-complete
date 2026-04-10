#!/usr/bin/env python3
# app.py - Login con Browserless BQL + acquisizione cookie completi + server HTTP per download

import requests
import json
import time
import os
import pickle
import threading
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

# ==================== CHIAVI VALIDE ====================
VALID_KEYS = [
    "2UFyHOdxsID23VMa0518a22c6b683ea3c11c1bdca148d5381",
    "2UIAf0U41Twctlr77ecbfa2545692634758496b2eb88a170c",
    "2UIAhSj6AMSpgLM5400cb96e68c36236805887d583fa1c1a8",
    "2UIAkQ4DGbDLMB06db1a95369b032405097bcfe53b9b8d444",
    "2UIAoK9f3FItlml3f95c43bb78d2b15d3e274da5c52fcb5cd",
    "2UIArIu84xpGFuV1b4e825a86352e4bec7b54db59df943bf0",
    "2UIAsvzIYtc0o6Pa719bbb072a635a0140cee8591aec0e617",
    "2UIAzLYxMfMvBTTf24fef2bee78bd26ccc8e423b6dbd9d72c",
    "2UIB0BADWlWBhpUd9b3113aae7aec11928693179b8e97adf7",
    "2UIB8rlEnDrj6Cv44d507f520ec52fa50046e7a70c30df6c6",
    "2UIB9J2tCnemabr9e97eff9685066c2072e18a52cfa283aa9",
    "2UIBB3QQ3H39YFu7d4fd1c778669ef19c8db22610905f23bb",
    "2UIBC8fgRMkg9wZ41fe0fe622994483be7093f33c02e53835",
    "2UIBGwfAlxxB6ni8919255b5bc976ec9ff72e0e7ee7f020de",
    "2UIBHpFuiMsVdXx3403174d9c61f08000e61d09260287e390",
    "2UIBJUl1ne3E92ya0949e27d64225c71a87e1d01458304c98",
    "2UIBKJ1ZL4HeXTTef781aa5c7c90ff94cc7d8e04545cf5ff9",
    "2UIBMTvCwvbW8zyeb1a2c2fc6d628643d2fc7837706f662d4",
    "2UIBOuJaRF5cBah589a83ba07a2bf4b4ae1e0bede889db139",
    "2UIBQDGaiPhyK5cc7d8d10689c2376b516809e26a4331bbe7",
    "2UIBRMkIfmmc5wU462f920ea771e4b0e8c29a96509179becd",
    "2UIBTMXwg0OXKdLdb313c233f7b40884382642b1336a75475",
    "2UIBUw762KYlNYe436d56b56b785ae327aea06af5c57b0856",
    "2UIBWGd7CenkAZP4e84a28fc45390849c04ec824c6b70c4aa",
    "2UIBX2qFOoT6UfQf0dca472d23a39ee0d2cc679711254df6e",
    "2UIBZ6iew6q5MjY587ca12d2ba6a8a7dec2887c680e0a295d",
    "2UIBalRcxjMmhLraa054e3a3fcc66019fa02e4756d40a97ca",
    "2UIBcJf0KJwjIJCc6aa92098f4b4d9677b277fa08bddaa52f",
    "2UIBdWa0VtcPa7l291b4497fca8ed7ad26b5c4d5927f54c52",
    "2UIBfg3C0DBareT4b3bc7b9de04934615085d885e0037c6a9",
    "2UIBg9igA9Adum65d15c87a1ebdbdd8462f2b769b9e6d0534",
    "2UIBiv7UFTo86PL7733f37e8662dc5ac1e44fbbfa69938c47",
    "2UIBjq41So7iISXc9b6488e29439c45ac81ec6655413598b7",
    "2UIBlZtTVvSSd9Mef4e7f74c7dadf262e366cf0d52a9278e1",
    "2UIBmotaoPEgiLGb4d8ff65588ad03856bca142e29d10f9d7",
    "2UIBoXymrMnL6rB7c0bf5d89b1d24423cf95f989c717a93da",
    "2UIBqLMCQct1MEc93871eac596a18158adf155055ea891b82",
    "2UIBsC5kqg908ss2b15a06dfd516f5477e644f4970239c2f3",
    "2UIBtryD9TY1rfLf40876aea895c6b19cfccd6d0423bb1a5a",
    "2UIBvZWEqIfKMABdb7ad2379d49b5fdb791668c5b8ae2872c",
    "2UIBwI8LlOkgnR2401030dc085c656433e9d9967c05cb8500",
    "2UIBzkNUiIo3aqf0fcbbefa77c3d721bcc90d6ea330d21b4b",
    "2UIC0txEnUKbs2e2011d4dbfcaccbf586e7cfd303ee25846c",
    "2UIC2RQTla00fnx09c8e8e078bda0be2ee065f87912fcf3ec",
    "2UIC3HmfnANB85ua2fafaa2b7d15fcddfaf43257ea8207a86",
    "2UIC5oOQStd9GOdd78704a1c13ede87f1ad076b3a3c5c014a",
    "2UIC6fQE3KZWxxF95f4c1b1514c6dd3d62ba0670368dbbdf0",
    "2UIC8HXKajhflGK4f6a4fc65b90703c46867dc5868233557d",
    "2UIC9N5NnxkvkiXc269dcbc7d2611f06b19dd6ac170a0e6a4",
    "2UICByRoMWLCFQP85171e81920c71c994e70f565ea94a5af9",
    "2UICCligGnceGaqb0567585836c440c4d21449a570494dfa6",
    "2UICEY4jAqkhpY0f3ecd736fb3d2b1df0f72a5ee544acf341",
    "2UICFz5KhinMtoGa87a2e4a5e156bb3e991297a8f794509c0",
    "2UICIQvD2zirSr161b5959fe434bec1ebe8e5ba0c62a03892",
    "2UICJ88uL7vxQXI13806d1cc2aab512c879ea4b47488aff01",
    "2UICLD7cUOCd06oe31be2d953915e565572bfc9990c96074b",
    "2UICM5P6tkSm3Qv2adc61218a5a7d6ea2f680320cd4db32ea",
    "2UICOGF3whhFISb5a4d943b2f658a0948de3321458f644f73",
    "2UICPYnut7CE37off5de03b2042b14aae1e1c8916eec85f6a",
    "2UICRMpGaWJQKP954bdcecee3ff7068055ac6c06af038c9e1",
]

BROWSERLESS_URL = "https://production-sfo.browserless.io/chrome/bql"

# CREDENZIALI
EASYHITS_EMAIL = "sandrominori50+giorgiofaggiolini@gmail.com"
EASYHITS_PASSWORD = "DDnmVV45!!"
REFERER_URL = "https://www.easyhits4u.com/?ref=nicolacaporale"

# Directory di output
OUTPUT_DIR = "/tmp/easyhits4u"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==================== SERVER HTTP PER DOWNLOAD COOKIE ====================
PORT = int(os.environ.get("PORT", 10000))
server_running = False

class CookieHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/cookies':
            try:
                latest_path = os.path.join(OUTPUT_DIR, "cookies_latest.txt")
                if os.path.exists(latest_path):
                    with open(latest_path, "r") as f:
                        cookie_string = f.read()
                    self.send_response(200)
                    self.send_header("Content-Type", "text/plain")
                    self.end_headers()
                    self.wfile.write(cookie_string.encode())
                else:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(b"Cookie file not found yet")
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        pass  # silenzia i log del server

def start_http_server():
    global server_running
    try:
        server = HTTPServer(('0.0.0.0', PORT), CookieHandler)
        server_running = True
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 🌐 Server HTTP avviato sulla porta {PORT} - GET /cookies per scaricare la stringa cookie")
        server.serve_forever()
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Errore avvio server: {e}")

# Avvia il server in un thread separato (non blocca il resto)
threading.Thread(target=start_http_server, daemon=True).start()

# Attendi che il server sia pronto (opzionale)
time.sleep(1)

# ==================== FUNZIONI ====================
def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

def get_cf_token(api_key):
    query = """
    mutation {
      goto(url: "https://www.easyhits4u.com/logon/", waitUntil: networkIdle, timeout: 60000) {
        status
      }
      solve(type: cloudflare, timeout: 60000) {
        solved
        token
        time
      }
    }
    """
    url = f"{BROWSERLESS_URL}?token={api_key}"
    try:
        start = time.time()
        response = requests.post(url, json={"query": query}, headers={"Content-Type": "application/json"}, timeout=120)
        if response.status_code != 200:
            return None
        data = response.json()
        if "errors" in data:
            return None
        solve_info = data.get("data", {}).get("solve", {})
        if solve_info.get("solved"):
            token = solve_info.get("token")
            log(f"   ✅ Token ({time.time()-start:.1f}s)")
            return token
        return None
    except Exception as e:
        log(f"   ❌ Errore token: {e}")
        return None

def build_cookie_string(cookies_dict):
    return '; '.join([f"{k}={v}" for k, v in cookies_dict.items()])

def login_and_get_complete_cookies(api_key):
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Firefox/148.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    # 1. GET homepage
    log("   🌐 GET homepage...")
    try:
        home = session.get("https://www.easyhits4u.com/", headers=headers, verify=False, timeout=15)
        log(f"      Homepage status: {home.status_code}")
        time.sleep(1)
    except Exception as e:
        log(f"      ❌ Errore homepage: {e}")
        return None, None, None
    
    # 2. Token
    token = get_cf_token(api_key)
    if not token:
        return None, None, None   # CORRETTO: 3 valori
    
    # 3. POST login
    login_headers = headers.copy()
    login_headers['Content-Type'] = 'application/x-www-form-urlencoded'
    login_headers['Referer'] = REFERER_URL
    data = {
        'manual': '1',
        'fb_id': '',
        'fb_token': '',
        'google_code': '',
        'username': EASYHITS_EMAIL,
        'password': EASYHITS_PASSWORD,
        'cf-turnstile-response': token,
    }
    try:
        login_resp = session.post("https://www.easyhits4u.com/logon/", data=data, headers=login_headers, allow_redirects=True, timeout=30)
        log(f"      Login POST status: {login_resp.status_code}")
        time.sleep(1)
    except Exception as e:
        log(f"      ❌ Errore POST login: {e}")
        return None, None, None
    
    # 4. GET /member/
    log("   🌐 GET /member/...")
    try:
        member = session.get("https://www.easyhits4u.com/member/", headers=headers, verify=False, timeout=15)
        log(f"      Member status: {member.status_code}")
        time.sleep(1)
    except Exception as e:
        log(f"      ❌ Errore member: {e}")
        return None, None, None
    
    # 5. GET /surf/
    log("   🌐 GET /surf/...")
    try:
        surf = session.get("https://www.easyhits4u.com/surf/", headers=headers, verify=False, timeout=15)
        log(f"      Surf page status: {surf.status_code}")
        time.sleep(1)
    except Exception as e:
        log(f"      ❌ Errore surf: {e}")
        return None, None, None
    
    # 6. GET referer (opzionale)
    log("   🌐 GET referer...")
    try:
        ref = session.get(REFERER_URL, headers=headers, verify=False, timeout=15)
        log(f"      Referer status: {ref.status_code}")
    except Exception as e:
        log(f"      ⚠️ Errore referer (non bloccante): {e}")
    
    cookies_dict = session.cookies.get_dict()
    cookie_string = build_cookie_string(cookies_dict)
    log(f"   🍪 Cookie ottenuti: {list(cookies_dict.keys())}")
    
    if 'user_id' in cookies_dict and 'sesids' in cookies_dict:
        log(f"   ✅ Login completo! user_id={cookies_dict['user_id']}, sesids={cookies_dict['sesids']}")
        return cookies_dict, cookie_string, session
    else:
        log(f"   ❌ Cookie essenziali mancanti: user_id={cookies_dict.get('user_id')}, sesids={cookies_dict.get('sesids')}")
        return None, None, None

def save_cookies(cookies_dict, cookie_string, session):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # JSON
    json_path = os.path.join(OUTPUT_DIR, f"cookies_{timestamp}.json")
    with open(json_path, "w") as f:
        json.dump(cookies_dict, f, indent=2)
    log(f"   💾 Cookie JSON: {json_path}")
    
    # Stringa TXT
    txt_path = os.path.join(OUTPUT_DIR, f"cookie_string_{timestamp}.txt")
    with open(txt_path, "w") as f:
        f.write(cookie_string)
    log(f"   💾 Cookie stringa: {txt_path}")
    
    # Ultimo (sovrascrive)
    latest_path = os.path.join(OUTPUT_DIR, "cookies_latest.txt")
    with open(latest_path, "w") as f:
        f.write(cookie_string)
    log(f"   💾 Ultimo cookie: {latest_path}")
    
    # Sessione pickle
    session_path = os.path.join(OUTPUT_DIR, f"session_{timestamp}.pkl")
    with open(session_path, "wb") as f:
        pickle.dump(session, f)
    log(f"   💾 Sessione pickle: {session_path}")
    
    latest_session = os.path.join(OUTPUT_DIR, "session_latest.pkl")
    with open(latest_session, "wb") as f:
        pickle.dump(session, f)

def main():
    log("=" * 50)
    log("🚀 LOGIN BROWSERLESS BQL + ACQUISIZIONE COOKIE COMPLETI")
    log("=" * 50)
    
    for api_key in VALID_KEYS:
        log(f"🔑 Tentativo con chiave: {api_key[:10]}...")
        cookies_dict, cookie_string, session = login_and_get_complete_cookies(api_key)
        if cookies_dict:
            log("🎉 Login e navigazione riusciti! Salvo cookie...")
            save_cookies(cookies_dict, cookie_string, session)
            log("✅ Fatto. Cookie salvati in /tmp/easyhits4u/")
            log(f"   🌐 Per scaricare l'ultima stringa cookie, usa: curl http://localhost:{PORT}/cookies")
            log("   ⚠️ Il servizio rimane in esecuzione per servire il file. Premi Ctrl+C per fermarlo.")
            # Mantieni il processo vivo per servire il file
            while True:
                time.sleep(60)
        else:
            log(f"   ❌ Tentativo fallito con questa chiave")
    
    log("❌ Login fallito con tutte le chiavi. Server rimane attivo per eventuali richieste.")
    while True:
        time.sleep(60)

if __name__ == "__main__":
    main()
