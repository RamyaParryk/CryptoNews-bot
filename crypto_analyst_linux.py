#!/usr/bin/env python3
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
# 設定: パス設定 & ログ機能
# ==========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "analyst_bot.log")
ENV_FILE = os.path.join(BASE_DIR, "X-GoogleAPI.env")
PROMPT_FILE = os.path.join(BASE_DIR, "prompt.txt")

def log(message):
    """ログをコンソールとファイルに出力"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"[{timestamp}] {message}"
    print(msg, flush=True) # Docker logs用にflush
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
CRYPTOPANIC_API_KEY = os.getenv("CRYPTOPANIC_API_KEY")
COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")

def check_keys():
    keys = {
        "X_API_KEY": X_API_KEY,
        "X_API_SECRET": X_API_SECRET,
        "X_ACCESS_TOKEN": X_ACCESS_TOKEN,
        "X_ACCESS_SECRET": X_ACCESS_SECRET,
        "GEMINI_API_KEY": GEMINI_API_KEY,
        "CRYPTOPANIC_API_KEY": CRYPTOPANIC_API_KEY
    }
    missing = [name for name, val in keys.items() if not val]
    if missing:
        log(f"❌ 以下のAPIキーが読み込めていません: {', '.join(missing)}")
        return False
    return True

# ==========================================
# 情報収集ロジック
# ==========================================

def get_trending_coins():
    """CoinGeckoから「今検索されているトレンド銘柄」を取得（APIキー対応）"""
    url = "https://api.coingecko.com/api/v3/search/trending"
    
    # デモ版APIキーをヘッダーにセットする（Demoプランの仕様: x-cg-demo-api-key）
    headers = {"accept": "application/json"}
    if COINGECKO_API_KEY:
        headers["x-cg-demo-api-key"] = COINGECKO_API_KEY

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # エラーなら例外を出す
        data = response.json()
        
        trending = []
        for item in data.get("coins", [])[:3]:
            coin = item["item"]
            trending.append(f"{coin['name']} ({coin['symbol']})")
            
        return "【現在のトレンド銘柄】\n" + ", ".join(trending) + "\n\n"
    except Exception as e:
        log(f"⚠️ トレンド銘柄取得エラー: {e}")
        return ""

def get_crypto_prices():
    """CoinGeckoから主要銘柄の現在価格・変動率を取得（APIキー対応）"""
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin,ethereum,solana", 
        "vs_currencies": "jpy", 
        "include_24hr_change": "true"
    }
    
    headers = {"accept": "application/json"}
    if COINGECKO_API_KEY:
        headers["x-cg-demo-api-key"] = COINGECKO_API_KEY

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10).json()
        text = "【主要銘柄の価格データ】\n"
        for c, s in [("bitcoin","BTC"), ("ethereum","ETH"), ("solana","SOL")]:
            if c in data: 
                text += f"{s}: {data[c]['jpy']:,.0f}円 ({data[c]['jpy_24h_change']:.1f}%)\n"
        return text + "\n"
    except Exception as e:
        log(f"⚠️ 価格取得エラー: {e}")
        return "価格データ取得失敗\n\n"

def get_trending_news():
    """
    【新機能】CryptoPanicの公式API (v2) から最新の注目ニュースを取得します。
    以前のRSS(GoogleNews等)を廃止し、これ一本に絞ることで仮想通貨特有の熱量(Vote)を拾います。
    """
    if not CRYPTOPANIC_API_KEY:
        return "ニュースデータなし (APIキー未設定)\n"

    url = "https://cryptopanic.com/api/developer/v2/posts/"
    params = {
        "auth_token": CRYPTOPANIC_API_KEY,
        "public": "true",
        "regions": "en",        # 情報が早い英語圏をターゲット
        "filter": "hot",        # 注目度が高い（Hot）ニュース
        "kind": "news"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status() 
        data = response.json()
        
        headlines = []
        # AIが処理しやすいよう上位5件に絞り、ユーザーの熱量（Vote数）を付与する
        for item in data.get("results", [])[:5]:
            title = item.get("title", "No Title")
            votes = item.get("votes", {})
            positive = votes.get("positive", 0)
            important = votes.get("important", 0)
            headlines.append(f"・{title} (強気: {positive}票, 重要: {important}票)")
            
        return "【注目の最新ホットニュース】\n" + "\n".join(headlines)

    except Exception as e:
        log(f"⚠️ ニュース取得エラー: {e}")
        return f"ニュースの取得に失敗: {e}"

def load_prompt():
    if not os.path.exists(PROMPT_FILE):
        log(f"❌ エラー: '{os.path.basename(PROMPT_FILE)}' が見つかりません。")
        return None
    try:
        with open(PROMPT_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            return content if content else None
    except: return None

def generate_analysis_tweet(market_data):
    """Geminiを使ってツイート本文を生成する"""
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
            # プロンプトの置換対象を一つにまとめる
            prompt = prompt_template.replace("{market_data}", market_data)
            response = model.generate_content(prompt, generation_config={"temperature": 0.85})
            text = response.text.strip()
            if len(text) > 140:
                 log("⚠️ 文字数調整を行います")
                 text = text[:137] + "..."
            log(f"✨ 使用モデル: {model_name}")
            return text
        except Exception as e:
            time.sleep(2); continue
    return None

def job():
    log("分析を開始します...")
    if not check_keys(): return
    
    # 3つの情報を1つのテキスト(market_data)にまとめる
    market_data = get_trending_coins() + get_crypto_prices() + get_trending_news()
    
    tweet_text = generate_analysis_tweet(market_data)
    
    if tweet_text:
        log(f"--- ツイート ---\n{tweet_text}")
        
        # ==========================================
        # Xへの投稿（503エラー対策の自動リトライ機能付き）
        # ==========================================
        MAX_RETRIES = 3  # 最大3回まで再チャレンジ
        
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                client = tweepy.Client(
                    consumer_key=X_API_KEY, 
                    consumer_secret=X_API_SECRET, 
                    access_token=X_ACCESS_TOKEN, 
                    access_token_secret=X_ACCESS_SECRET
                )
                client.create_tweet(text=tweet_text)
                log("✅ 投稿成功！")
                break # 成功したらループを抜ける
                
            except Exception as e:
                error_msg = str(e)
                # 503エラー（サーバー混雑）などの場合
                if "503" in error_msg or "Service Unavailable" in error_msg:
                    if attempt < MAX_RETRIES:
                        wait_time = 30 * attempt  # 1回目は30秒、2回目は60秒待機
                        log(f"⚠️ Xサーバー混雑(503)。{wait_time}秒後にリトライします ({attempt}/{MAX_RETRIES})...")
                        time.sleep(wait_time)
                    else:
                        log(f"❌ {MAX_RETRIES}回リトライしましたが、投稿できませんでした: {e}")
                else:
                    # その他の致命的なエラーはすぐに諦める
                    log(f"❌ 投稿エラー: {e}")
                    break
    else: 
        log("分析をスキップしました。")

def main():
    log("=== AI Crypto Analyst Bot (v7.0 with CryptoPanic & Retry) Started ===")
    check_keys()
    now = datetime.datetime.now()
    is_utc = abs((now - datetime.datetime.utcnow()).total_seconds()) < 60
    
    # Linux環境のUTC判定によるスケジュール補正
    if is_utc:
        schedule.every().day.at("16:45").do(job)
        schedule.every().day.at("22:45").do(job)
        schedule.every().day.at("02:45").do(job)
        schedule.every().day.at("08:45").do(job)
        schedule.every().day.at("12:45").do(job)
    else:
        schedule.every().day.at("01:45").do(job)
        schedule.every().day.at("07:45").do(job)
        schedule.every().day.at("11:45").do(job)
        schedule.every().day.at("17:45").do(job)
        schedule.every().day.at("21:45").do(job)

    job() # 初回実行
    log("スケジュール待機中...")
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)
        except KeyboardInterrupt:
            break
        except Exception as e:
            log(f"メインループエラー: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()