#!/usr/bin/env python3
import os
import time
import datetime
import sys
import subprocess
import traceback
import random
import warnings
import xml.etree.ElementTree as ET

warnings.simplefilter('ignore')
os.environ['GRPC_VERBOSITY'] = 'ERROR'
os.environ['GLOG_minloglevel'] = '2'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "analyst_bot.log")
ENV_FILE = os.path.join(BASE_DIR, "X-GoogleAPI.env")
PROMPT_FILE = os.path.join(BASE_DIR, "prompt.txt")

def log(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"[{timestamp}] {message}"
    print(msg, flush=True) 
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(msg + "\n")
            f.flush()
            os.fsync(f.fileno())
    except:
        pass

def install_libraries():
    required_libs = ["google-generativeai", "requests", "tweepy", "schedule", "python-dotenv", "beautifulsoup4"]
    for lib in required_libs:
        try:
            m = "google.generativeai" if lib == "google-generativeai" else "dotenv" if lib == "python-dotenv" else "bs4" if lib == "beautifulsoup4" else lib
            __import__(m)
        except ImportError:
            log(f"Installing {lib}...")
            try: subprocess.check_call([sys.executable, "-m", "pip", "install", lib])
            except Exception as e: log(f"Failed to install {lib}: {e}")

try:
    import requests, tweepy, schedule, google.generativeai as genai
    from dotenv import load_dotenv
    from bs4 import BeautifulSoup
except ImportError:
    install_libraries()
    import requests, tweepy, schedule, google.generativeai as genai
    from dotenv import load_dotenv
    from bs4 import BeautifulSoup

if os.path.exists(ENV_FILE): load_dotenv(ENV_FILE)

X_API_KEY = os.getenv("X_API_KEY")
X_API_SECRET = os.getenv("X_API_SECRET")
X_ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
X_ACCESS_SECRET = os.getenv("X_ACCESS_SECRET")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CRYPTOPANIC_API_KEY = os.getenv("CRYPTOPANIC_API_KEY")
COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")

def check_keys():
    keys = {"X_API_KEY": X_API_KEY, "X_API_SECRET": X_API_SECRET, "X_ACCESS_TOKEN": X_ACCESS_TOKEN, "X_ACCESS_SECRET": X_ACCESS_SECRET, "GEMINI_API_KEY": GEMINI_API_KEY}
    missing = [name for name, val in keys.items() if not val]
    if missing:
        log(f"❌ 以下のAPIキーが読み込めていません: {', '.join(missing)}")
        return False
    return True

def get_macro_news():
    url = "https://news.yahoo.co.jp/rss/categories/business.xml"
    try:
        res = requests.get(url, timeout=10)
        root = ET.fromstring(res.text)
        headlines = []
        for item in root.findall('.//item')[:4]:
            headlines.append(f"・{item.find('title').text}")
        return "【マクロ経済・株式ニュース】\n" + "\n".join(headlines) + "\n\n"
    except Exception as e:
        log(f"⚠️ マクロニュース取得エラー: {e}")
        return ""

def get_trending_coins():
    url = "https://api.coingecko.com/api/v3/search/trending"
    headers = {"accept": "application/json"}
    if COINGECKO_API_KEY: headers["x-cg-demo-api-key"] = COINGECKO_API_KEY
    try:
        data = requests.get(url, headers=headers, timeout=10).json()
        trending = [f"{item['item']['name']} ({item['item']['symbol']})" for item in data.get("coins", [])[:3]]
        return "【現在の仮想通貨トレンド銘柄】\n" + ", ".join(trending) + "\n\n"
    except: return ""

def get_crypto_prices():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": "bitcoin,ethereum,solana", "vs_currencies": "jpy", "include_24hr_change": "true"}
    headers = {"accept": "application/json"}
    if COINGECKO_API_KEY: headers["x-cg-demo-api-key"] = COINGECKO_API_KEY
    try:
        data = requests.get(url, headers=headers, params=params, timeout=10).json()
        text = "【主要銘柄の価格データ】\n"
        for c, s in [("bitcoin","BTC"), ("ethereum","ETH"), ("solana","SOL")]:
            if c in data: text += f"{s}: {data[c]['jpy']:,.0f}円 ({data[c]['jpy_24h_change']:.1f}%)\n"
        return text + "\n"
    except: return ""

def get_trending_news():
    if not CRYPTOPANIC_API_KEY: return "ニュースデータなし (APIキー未設定)\n"
    url = "https://cryptopanic.com/api/developer/v2/posts/"
    params = {"auth_token": CRYPTOPANIC_API_KEY, "public": "true", "regions": "en", "filter": "hot", "kind": "news"}
    try:
        data = requests.get(url, params=params, timeout=10).json()
        headlines = []
        for item in data.get("results", [])[:5]:
            headlines.append(f"・{item.get('title')} (強気: {item.get('votes', {}).get('positive', 0)}票)")
        return "【注目の仮想通貨ニュース】\n" + "\n".join(headlines)
    except: return ""

# 過去50回分を取得する
def get_recent_tweets(limit=50):
    if not os.path.exists(LOG_FILE): return "まだ過去のツイートはありません。"
    tweets = []
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for i in range(len(lines)-1, -1, -1):
            if "--- ツイート ---" in lines[i] and i + 1 < len(lines):
                tweet = lines[i+1].strip()
                if tweet not in tweets:
                    tweets.append(tweet)
                if len(tweets) >= limit:
                    break
    except: pass
    if not tweets: return "取得に失敗しました。"
    return "\n".join([f"・{t}" for t in tweets])

def load_prompt():
    if not os.path.exists(PROMPT_FILE): return None
    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        return f.read().strip()

def generate_analysis_tweet(market_data, recent_tweets):
    if not GEMINI_API_KEY: return None
    genai.configure(api_key=GEMINI_API_KEY)
    prompt_template = load_prompt()
    if not prompt_template: return None

    models_to_try = ['gemini-3.1-pro-preview', 'gemini-3-flash-preview']
    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            prompt = prompt_template.replace("{market_data}", market_data).replace("{recent_tweets}", recent_tweets)
            response = model.generate_content(prompt, generation_config={"temperature": 0.85})
            text = response.text.strip()
            log(f"✨ 使用モデル: {model_name} (生成文字数: {len(text)})")
            if len(text) > 140: text = text[:137] + "..."
            return text
        except Exception as e: time.sleep(2); continue
    return None

def job():
    log("分析を開始します...")
    if not check_keys(): return
    
    market_data = get_macro_news() + get_trending_coins() + get_crypto_prices() + get_trending_news()
    recent_tweets = get_recent_tweets()
    
    log_preview = recent_tweets.replace('\n', ' ')
    log(f"🧠 直近50回の発言を記憶しました: {log_preview[:30]}...")
    
    tweet_text = generate_analysis_tweet(market_data, recent_tweets)
    
    if tweet_text:
        log(f"--- ツイート ---\n{tweet_text}")
        for attempt in range(1, 4):
            try:
                client = tweepy.Client(consumer_key=X_API_KEY, consumer_secret=X_API_SECRET, access_token=X_ACCESS_TOKEN, access_token_secret=X_ACCESS_SECRET)
                client.create_tweet(text=tweet_text)
                log("✅ 投稿成功！")
                break 
            except Exception as e:
                error_msg = str(e)
                if "503" in error_msg or "Service Unavailable" in error_msg:
                    if attempt < 3:
                        time.sleep(30 * attempt)
                else:
                    log(f"❌ 投稿エラー: {e}")
                    break
    else: log("分析をスキップしました。")

def main():
    log("=== AI Crypto Analyst Bot (Macro & Memory V8.2) Started ===")
    if abs((datetime.datetime.now() - datetime.datetime.utcnow()).total_seconds()) < 60:
        for t in ["16:45", "22:45", "02:45", "08:45", "12:45"]: schedule.every().day.at(t).do(job)
    else:
        for t in ["01:45", "07:45", "11:45", "17:45", "21:45"]: schedule.every().day.at(t).do(job)

    job() 
    log("スケジュール待機中...")
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()