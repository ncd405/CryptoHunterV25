import os
import asyncio
import random
import time
from flask import Flask
from threading import Thread
from telethon import TelegramClient
from telethon.sessions import StringSession
from colorama import Fore, Style, init

init(autoreset=True)

# --- CẤU HÌNH TỪ RENDER ---
API_ID = int(os.environ.get('API_ID', 0))
API_HASH = os.environ.get('API_HASH')
SESSION_STRING = os.environ.get('SESSION_STRING')

# --- DANH SÁCH MỎ VÀNG (GAME) ---
TARGET_BOTS = [
    "@BlumCryptoBot",      # Blum
    "@major",              # Major
    "@notcoin_bot",        # Notcoin
    "@hotwallet_bot",      # HOT Wallet
    "@xkucoinbot",         # KuCoin
    "@tapswap_bot",        # TapSwap
    "@hamster_kombat_bot", # Hamster
    "@catsgang_bot"        # Cats
]

# --- WEB SERVER GIỮ MẠNG SỐNG ---
app = Flask(__name__)
@app.route('/')
def home(): return "💎 CRYPTO HUNTER V25 IS MINING!"
def run_web(): app.run(host='0.0.0.0', port=10000)
def keep_alive(): Thread(target=run_web).start()

# --- LOGIC ĐÀO COIN ---
async def miner():
    print(f"{Fore.YELLOW}⚡ ĐANG KẾT NỐI VỆ TINH...{Style.RESET_ALL}")
    
    if not SESSION_STRING:
        print("❌ LỖI: Chưa nạp SESSION_STRING trên Render!")
        return

    try:
        async with TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH) as client:
            print(f"{Fore.GREEN}✅ ĐĂNG NHẬP THÀNH CÔNG! BẮT ĐẦU ĐI SĂN...{Style.RESET_ALL}")
            
            while True:
                print(f"\n🔄 {Fore.CYAN}BẮT ĐẦU VÒNG QUÉT ({time.strftime('%H:%M:%S')})...{Style.RESET_ALL}")
                
                for bot in TARGET_BOTS:
                    try:
                        print(f"👉 Đang gõ cửa: {bot}")
                        # Gửi lệnh /start để kích hoạt/thu hoạch
                        await client.send_message(bot, "/start")
                        
                        # Nghỉ ngẫu nhiên 15-30s để né ban
                        wait = random.randint(15, 30)
                        await asyncio.sleep(wait)
                        
                    except Exception as e:
                        print(f"{Fore.RED}❌ Lỗi tại {bot}: {e}{Style.RESET_ALL}")
                        await asyncio.sleep(5)

                # Tính toán thời gian nghỉ (1 đến 8 tiếng tùy chiến thuật)
                # Ở đây để 8 tiếng (28800s) là an toàn nhất cho Blum/Major
                print(f"\n{Fore.BLUE}💤 XONG 1 VÒNG! NGỦ 8 TIẾNG HỒI MANA...{Style.RESET_ALL}")
                await asyncio.sleep(28800)

    except Exception as e:
        print(f"💀 Lỗi Fatal: {e}")

if __name__ == '__main__':
    keep_alive() # Bật tim nhân tạo
    loop = asyncio.get_event_loop()
    loop.run_until_complete(miner())
