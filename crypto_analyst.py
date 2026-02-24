import os
import time
import datetime
import sys
import subprocess
import traceback
import random
import warnings

# ==========================================
# 警告メッセージの抑制
# ==========================================
warnings.simplefilter('ignore')
os.environ['GRPC_VERBOSITY'] = 'ERROR'
os.environ['GLOG_minloglevel'] = '2'

# ==========================================
# Windows文字化け対策
# ==========================================
if os.name == 'nt':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

# ==========================================
# 設定: パス設定 & ログ機能
# ==========================================
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

# ==========================================
# 自動インストール・ライブラリ読み込み
# ==========================================
def install_libraries():
    required_libs = ["google-generativeai", "requests", "feedparser", "tweepy", "schedule", "python-dotenv", "beautifulsoup4"]
    for lib in required_libs:
        try:
            m = "google.generativeai" if lib == "google-generativeai" else "dotenv" if lib == "python-dotenv" else "bs4" if lib == "beautifulsoup4" else lib
            __import__(m)
        except ImportError:
            log(f"Installing {lib}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])

try:
    import requests, feedparser, tweepy, schedule, google.generativeai as genai
    from dotenv import load_dotenv
    from bs4 import BeautifulSoup
except ImportError:
    install_libraries()
    import requests, feedparser, tweepy, schedule, google.generativeai as genai
    from dotenv import load_dotenv
    from bs4 import BeautifulSoup

# .envファイルの読み込み
if os.path.exists(ENV_FILE):
    if load_dotenv(ENV_FILE):
        log(f"✅ 設定ファイル '{os.path.basename(ENV_FILE)}' を読み込みました。")
    else:
        log(f"❌ 設定ファイル '{os.path.basename(ENV_FILE)}' の解析に失敗しました。")
else:
    log(f"⚠️ 設定ファイル '{os.path.basename(ENV_FILE)}' が見つかりません。")

# ==========================================
# APIキーの取得と検証
# ==========================================
X_API_KEY = os.getenv("X_API_KEY")
X_API_SECRET = os.getenv("X_API_SECRET")
X_ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
X_ACCESS_SECRET = os.getenv("X_ACCESS_SECRET")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def check_keys():
    keys = {
        "X_API_KEY": X_API_KEY,
        "X_API_SECRET": X_API_SECRET,
        "X_ACCESS_TOKEN": X_ACCESS_TOKEN,
        "X_ACCESS_SECRET": X_ACCESS_SECRET,
        "GEMINI_API_KEY": GEMINI_API_KEY
    }
    missing = [name for name, val in keys.items() if not val]
    if missing:
        log(f"❌ 以下のAPIキーが読み込めていません: {', '.join(missing)}")
        return False
    return True

# ==========================================
# 情報収集ロジック
# ==========================================
RSS_URLS = [
    "https://cryptopanic.com/news/rss/", 
    "https://news.google.com/rss/search?q=Cryptocurrency+OR+Bitcoin+OR+Ethereum&hl=en-US&gl=US&ceid=US:en",
    "https://news.google.com/rss/search?q=仮想通貨+OR+暗号資産+OR+ビットコイン&hl=ja&gl=JP&ceid=JP:ja",
    "https://jp.investing.com/rss/news_14.rss"
]

def get_crypto_prices():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": "bitcoin,ethereum,ripple,solana,binancecoin,dogecoin,fetch-ai,uniswap", "vs_currencies": "jpy", "include_24hr_change": "true"}
    try:
        data = requests.get(url, params=params, timeout=10).json()
        text = "【価格データ】\n"
        for c, s in [("bitcoin","BTC"), ("ethereum","ETH"), ("ripple","XRP"), ("solana","SOL"), ("dogecoin","DOGE"), ("fetch-ai","FET")]:
            if c in data: text += f"{s}: {data[c]['jpy']}円 ({data[c]['jpy_24h_change']:.1f}%)\n"
        return text
    except: return "価格データ取得失敗"

def get_market_vibe_news():
    headlines = []
    shuffled_urls = RSS_URLS.copy()
    random.shuffle(shuffled_urls)
    for url in shuffled_urls:
        if len(headlines) >= 50: break
        try:
            feed = feedparser.parse(requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10).text)
            for entry in feed.entries[:10]:
                summary = BeautifulSoup(getattr(entry, 'summary', ''), "html.parser").get_text()[:80].replace('\n', ' ')
                headlines.append(f"・{entry.title} ({summary})")
        except: pass
    return "【マーケットニュース】\n" + "\n".join(headlines)

def load_prompt():
    if not os.path.exists(PROMPT_FILE):
        log(f"❌ エラー: '{os.path.basename(PROMPT_FILE)}' が見つかりません。")
        return None
    try:
        with open(PROMPT_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            return content if content else None
    except: return None

def generate_analysis_tweet(prices, news):
    if not GEMINI_API_KEY: return None
    genai.configure(api_key=GEMINI_API_KEY)
    
    prompt_template = load_prompt()
    if not prompt_template:
        log("⚠️ プロンプトが読み込めないため、生成を中止します。")
        return None

    # 最新モデル 3.1-pro-preview を使用
    models_to_try = ['gemini-3.1-pro-preview', 'gemini-3-flash-preview']

    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            prompt = prompt_template.replace("{prices}", prices).replace("{news}", news)
            response = model.generate_content(prompt, generation_config={"temperature": 0.85})
            text = response.text.strip()
            if len(text) > 140: text = text[:137] + "..."
            log(f"✨ 使用モデル: {model_name}")
            return text
        except Exception as e:
            time.sleep(2); continue
    return None

def job():
    log("分析を開始します...")
    if not check_keys(): return
    p, n = get_crypto_prices(), get_market_vibe_news()
    tweet_text = generate_analysis_tweet(p, n)
    if tweet_text:
        log(f"--- ツイート ---\n{tweet_text}")
        try:
            # ★ここが原因でした！名札（引数名）を省略せずに正確に渡すように修正しました。
            client = tweepy.Client(
                consumer_key=X_API_KEY, 
                consumer_secret=X_API_SECRET, 
                access_token=X_ACCESS_TOKEN, 
                access_token_secret=X_ACCESS_SECRET
            )
            client.create_tweet(text=tweet_text)
            log("✅ 投稿成功！")
        except Exception as e: log(f"❌ 投稿エラー: {e}")
    else: log("分析をスキップしました。")

if __name__ == "__main__":
    try:
        log("=== AI Crypto Analyst Bot (Windows v6.6 Fix-Auth) Started ===")
        check_keys()
        schedule.every().day.at("01:45").do(job)
        schedule.every().day.at("07:45").do(job)
        schedule.every().day.at("11:45").do(job)
        schedule.every().day.at("17:45").do(job)
        schedule.every().day.at("21:45").do(job)
        job() # 初回実行
        while True:
            schedule.run_pending()
            time.sleep(60)
    except Exception as e:
        log(f"致命的エラー: {e}")
        input("Press Enter to exit...")