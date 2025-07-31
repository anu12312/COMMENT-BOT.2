import requests
import re
import time
import random

# ---- HELPER FUNCTIONS ----
def get_numeric_post_id(post_url, token):
    try:
        print("🔍 Extracting numeric post ID using token...")
        res = requests.get(f"https://graph.facebook.com/?id={post_url}&access_token={token}")
        data = res.json()
        # Optional: print(data) for debug
        return data["og_object"]["id"]
    except Exception as e:
        print(f"❌ Error extracting post ID: {e}")
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

def load_file_lines(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except:
        print(f"⚠️ File missing: {filename}")
        return []

def load_single_line(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read().strip()
    except:
        print(f"⚠️ File missing: {filename}")
        return ""

# ---- LOAD FILES ----
tokens = load_file_lines("token.txt")
comments = load_file_lines("comments.txt")
haters = load_file_lines("hatersname.txt")
post_url = load_single_line("postlink.txt")
interval = int(load_single_line("time.txt") or 60)

if not tokens:
    print("❌ No tokens found. Exiting.")
    exit()

# ---- EXTRACT POST ID USING TOKEN ----
post_id = get_numeric_post_id(post_url, tokens[0])

if not post_id:
    print("❌ Failed to extract post ID. Check your post URL or token.")
    exit()

print(f"✅ Post ID Extracted: {post_id}")
print("🚀 Auto Comment Bot Started...\n")

# ---- MAIN LOOP ----
while True:
    if not tokens or not comments:
        print("⚠️ Tokens or comments missing. Exiting.")
        break

    token = random.choice(tokens)
    comment = random.choice(comments)

    if "{hater}" in comment and haters:
        comment = comment.replace("{hater}", random.choice(haters))

    print(f"➡️ Commenting: {comment}")

    success, response = comment_on_post(post_id, comment, token)

    if success:
        print(f"✅ Success: Comment posted!")
    else:
        print(f"❌ Failed: {response}")

    print(f"⏳ Waiting {interval} seconds...\n")
    time.sleep(interval)
