import requests
import re
import time
import random
import os

# ---- HELPER FUNCTIONS ----
def extract_post_id(post_url):
    match = re.search(r'/posts/(\d+)', post_url)
    if match:
        return match.group(1)
    return None

def comment_on_post(post_id, message, token):
    url = f"https://graph.facebook.com/v19.0/{post_id}/comments"
    payload = {
        'message': message,
        'access_token': token
    }
    try:
        res = requests.post(url, data=payload)
        return res.status_code == 200, res.json()
    except Exception as e:
        return False, str(e)

def safe_load(file):
    try:
        with open(file, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"⚠️ File not found: {file}")
        return []

def safe_load_single(file):
    try:
        with open(file, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"⚠️ File not found: {file}")
        return ""

# ---- LOAD DATA ----
tokens = safe_load("token.txt")
comments = safe_load("comments.txt")
haters = safe_load("hatersname.txt")
post_url = safe_load_single("postlink.txt")
interval = int(safe_load_single("time.txt") or 60)

post_id = extract_post_id(post_url)

if not post_id:
    print("❌ Invalid post link. Exiting.")
    exit()

print("🚀 Starting Facebook Auto Comment Bot...\n")

# ---- MAIN LOOP ----
while True:
    if not tokens or not comments:
        print("⚠️ Tokens or comments missing. Exiting.")
        break

    token = random.choice(tokens)
    comment = random.choice(comments)

    if "{hater}" in comment and haters:
        comment = comment.replace("{hater}", random.choice(haters))

    print(f"➡️ Trying comment: {comment}")

    success, response = comment_on_post(post_id, comment, token)

    if success:
        print(f"✅ Commented: {comment}")
    else:
        print(f"❌ Failed: {response}")

    print(f"⏱ Waiting {interval} seconds...\n")
    time.sleep(interval)
