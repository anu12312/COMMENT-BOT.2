import requests
import time
import os
import threading
from platform import system
import http.server
import socketserver

# ──────────────────────────────────────────────────────────
# ✅ 1. Simple uptime server (Render-compatible)
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write("✅ Facebook Comment Bot Running...".encode('utf-8'))

def execute_server():
    PORT = 4000
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"[🌐] Server running at http://localhost:{PORT}")
        httpd.serve_forever()

# ──────────────────────────────────────────────────────────
# ✅ 2. Utility functions
def clear_console():
    os.system('cls' if system() == 'Windows' else 'clear')

def line():
    print('\033[37m' + '•' + '─' * 57 + '•')

def extract_post_id(link):
    import re
    match = re.search(r'/posts/(\d+)', link) or re.search(r'story_fbid=(\d+)', link)
    return match.group(1) if match else link.strip()

def get_name(token):
    try:
        data = requests.get(f'https://graph.facebook.com/v17.0/me?access_token={token}').json()
        return data.get('name', 'Unknown')
    except:
        return "Error"

# ──────────────────────────────────────────────────────────
# ✅ 3. Main comment posting loop
def post_comments():
    # Load config files
    with open('token.txt', 'r') as f:
        tokens = [t.strip() for t in f.readlines()]
    with open('postlink.txt', 'r') as f:
        raw_post = f.read().strip()
        post_id = extract_post_id(raw_post)
    with open('comments.txt', 'r') as f:
        comments = [c.strip() for c in f.readlines()]
    with open('hatersname.txt', 'r') as f:
        prefix = f.read().strip()
    with open('time.txt', 'r') as f:
        delay = int(f.read().strip())

    clear_console()
    line()
    print(f"[📌] Target Post ID: {post_id}")
    print(f"[🔁] Delay Between Comments: {delay}s")
    print(f"[💬] Total Comments: {len(comments)} | Tokens: {len(tokens)}")
    line()

    headers = {
        'User-Agent': 'Mozilla/5.0',
        'referer': 'www.google.com'
    }

    while True:
        try:
            for i, comment in enumerate(comments):
                token = tokens[i % len(tokens)]
                full_comment = f"{prefix} {comment}"
                url = f"https://graph.facebook.com/{post_id}/comments"
                data = {'access_token': token, 'message': full_comment}
                response = requests.post(url, json=data, headers=headers)
                current_time = time.strftime("%Y-%m-%d %I:%M:%S %p")

                if response.ok:
                    print(f"[✅] Comment {i+1}: {full_comment}")
                else:
                    print(f"[❌] Failed {i+1}: {full_comment}")
                print(f"  - Time: {current_time}")
                line()
                time.sleep(delay)
            print("\n[🔁] All comments sent. Restarting...\n")
        except Exception as e:
            print(f"[⚠️] Error: {e}")
            line()

# ──────────────────────────────────────────────────────────
# ✅ 4. Entry Point
def main():
    threading.Thread(target=execute_server).start()
    post_comments()

if __name__ == '__main__':
    main()
