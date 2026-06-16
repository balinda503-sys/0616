import sys
import asyncio
import os  # <--- 1. 記得引入 os 模組
import discord
from discord.ext import commands

# Windows 專用事件循環補丁
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# 核心全域資料庫狀態機
game = {
    "is_active": False,      
    "players": [],           
    "words": {},             
    "identities": {},        
    "undercover_id": None,   
    "voted_users": {}        
}

@bot.event
async def on_ready():
    print(f'🤖 遊戲主機已成功對接連線：{bot.user.name}')

@bot.command(name="報名")
async def sign_up(ctx):
    if game["is_active"]:
        await ctx.send("⚠️ 遊戲已經在進行中，請等下一局！")
        return

    if ctx.author in game["players"]:
        await ctx.send(f"❓ {ctx.author.mention} 你已經報名過了，請勿重複註冊！")
        return

    game["players"].append(ctx.author)
    await ctx.send(f"✅ {ctx.author.mention} 報名成功！目前房間總人數：{len(game['players'])} 人")

# ========================================================
# 2. 關鍵修正：在程式最下方加入啟動代碼
# ========================================================
if __name__ == "__main__":
    # 從環境變數中讀取名為 DISCORD_TOKEN 的值
    TOKEN = os.getenv("DISCORD_TOKEN")
    
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("❌ 錯誤：找不到 DISCORD_TOKEN 環境變數，請在 Render 的 Environment 設定它！")
