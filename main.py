import os
import asyncio
import random
import time
import re
from flask import Flask
from threading import Thread
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from colorama import Fore, Style, init

init(autoreset=True)

# --- CẤU HÌNH TỪ RENDER (BẮT BUỘC PHẢI CÓ SESSION) ---
API_ID = int(os.environ.get('API_ID', 0))
API_HASH = os.environ.get('API_HASH')
SESSION_STRING = os.environ.get('SESSION_STRING')

# Danh sách Game Bot cần chăm sóc
TARGETS = ["@BlumCryptoBot", "@major", "@notcoin_bot", "@hotwallet_bot", "@xkucoinbot", "@catsgang_bot"]

# Các từ khóa để nhận diện nút bấm kiếm tiền
KEYWORDS = ["claim", "farm", "start", "daily", "check", "harvest", "nhận", "đào"]

# --- WEB SERVER GIỮ SỐNG ---
app = Flask(__name__)
@app.route('/')
def home(): return "⛏️ MINER V26 AUTO-TASK IS RUNNING!"
def run_web(): app.run(host='0.0.0.0', port=10000)
def keep_alive(): Thread(target=run_web).start()

if not SESSION_STRING:
    print("❌ LỖI: Chưa có SESSION_STRING! Vui lòng nạp vào Render Environment.")
    exit()

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

# --- HÀM TỰ ĐỘNG BẤM NÚT (AUTO CLICKER) ---
@client.on(events.NewMessage(chats=TARGETS))
async def handler(event):
    try:
        # Nếu tin nhắn có nút bấm
        if event.message.buttons:
            print(f"{Fore.CYAN}👀 Phát hiện nút bấm từ {event.chat.username}...")
            for row in event.message.buttons:
                for btn in row:
                    # Kiểm tra xem nút có chứa từ khóa kiếm tiền không
                    txt = btn.text.lower()
                    if any(k in txt for k in KEYWORDS):
                        print(f"{Fore.GREEN}👉 ĐANG BẤM NÚT: '{btn.text}'")
                        await btn.click()
                        await asyncio.sleep(random.randint(2, 5))
    except Exception as e:
        print(f"⚠️ Lỗi bấm nút: {e}")

# --- CHU TRÌNH TUẦN TRA (PATROL) ---
async def patrol():
    print(f"{Fore.YELLOW}⚡ ĐANG KẾT NỐI VỆ TINH...{Style.RESET_ALL}")
    await client.start()
    print(f"{Fore.GREEN}✅ ĐĂNG NHẬP THÀNH CÔNG! CHẾ ĐỘ: AUTO-TASK{Style.RESET_ALL}")
    
    while True:
        print(f"\n🔄 {Fore.MAGENTA}BẮT ĐẦU VÒNG ĐI SĂN ({time.strftime('%H:%M')})...{Style.RESET_ALL}")
        
        for bot in TARGETS:
            try:
                print(f"🔨 Gõ cửa: {bot}")
                await client.send_message(bot, "/start")
                
                # Đợi bot phản hồi và để sự kiện (event handler) tự bấm nút
                await asyncio.sleep(random.randint(10, 20))
                
            except Exception as e:
                print(f"❌ Lỗi tại {bot}: {e}")

        print(f"{Fore.BLUE}💤 Xong 1 vòng. Ngủ 4 tiếng hồi sức...{Style.RESET_ALL}")
        await asyncio.sleep(14400) # 4 tiếng chạy 1 lần

if __name__ == '__main__':
    keep_alive()
    client.loop.run_until_complete(patrol())
