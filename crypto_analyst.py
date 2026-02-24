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
# 読み込む設定ファイル名を指定
ENV_FILE = os.path.join(BASE_DIR, "X-GoogleAPI.env")

def log(message):
    """ログをコンソールとファイルに出力"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"[{timestamp}] {message}"
    # コンソールにも即時出力
    print(msg, flush=True)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(msg + "\n")
            # バッファに溜めずに強制的にディスクに書き込む
            f.flush()
            os.fsync(f.fileno())
    except:
        pass

# ==========================================
# 自動インストール機能
# ==========================================
def install_libraries():
    required_libs = ["google-generativeai", "requests", "feedparser", "tweepy", "schedule", "python-dotenv", "beautifulsoup4"]
    for lib in required_libs:
        try:
            if lib == "google-generativeai":
                module_name = "google.generativeai"
            elif lib == "python-dotenv":
                module_name = "dotenv"
            elif lib == "beautifulsoup4":
                module_name = "bs4"
            else:
                module_name = lib
            __import__(module_name)
        except ImportError:
            log(f"Installing {lib}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", lib])
            except Exception as e:
                log(f"Failed to install {lib}: {e}")

# ライブラリ読み込み
try:
    import requests
    import feedparser
    import tweepy
    import schedule
    import google.generativeai as genai
    from dotenv import load_dotenv
    from bs4 import BeautifulSoup
except ImportError:
    log("必要なライブラリが見つかりません。自動インストールを試みます...")
    install_libraries()
    import requests
    import feedparser
    import tweepy
    import schedule
    import google.generativeai as genai
    from dotenv import load_dotenv
    from bs4 import BeautifulSoup

# .envファイルの読み込み
if os.path.exists(ENV_FILE):
    load_dotenv(ENV_FILE)
    log(f"設定ファイル {os.path.basename(ENV_FILE)} を読み込みました。")
else:
    log(f"⚠️ 設定ファイル {os.path.basename(ENV_FILE)} が見つかりません。環境変数から設定を読み込みます。")

# ==========================================
# 設定エリア (環境変数から読み込み)
# ==========================================

# 1. X (Twitter) API Keys
X_API_KEY = os.getenv("X_API_KEY")
X_API_SECRET = os.getenv("X_API_SECRET")
X_ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
X_ACCESS_SECRET = os.getenv("X_ACCESS_SECRET")

# 2. Google Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# キーチェック
if not all([X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_SECRET, GEMINI_API_KEY]):
    log("!!!! 設定エラー !!!!")
    log("APIキーが正しく読み込めませんでした。")
    log(f"同じフォルダに {os.path.basename(ENV_FILE)} ファイルがあるか確認してください。")
    log("内容が正しいか（X_API_KEY=... の形式）も確認してください。")

# ==========================================
# 超・広域ニュースソース（アグリゲーター中心）
# ==========================================
RSS_URLS = [
    # CryptoPanic (世界中の何百ものクリプトニュースメディアを自動集約した最強のフィード)
    "https://cryptopanic.com/news/rss/", 
    
    # Googleニュースの広域検索（アルゴリズムによるトレンドピックアップ）
    "https://news.google.com/rss/search?q=Cryptocurrency+OR+Bitcoin+OR+Ethereum&hl=en-US&gl=US&ceid=US:en", # 英語圏全体
    "https://news.google.com/rss/search?q=仮想通貨+OR+暗号資産+OR+ビットコイン&hl=ja&gl=JP&ceid=JP:ja", # 日本圏全体
    "https://news.google.com/rss/search?q=DeFi+OR+Web3+OR+AI+token&hl=en-US&gl=US&ceid=US:en", # トレンドテーマ
    
    # マクロ経済（全体的な金融の動き）
    "https://jp.investing.com/rss/news_14.rss"
]

IGNORE_KEYWORDS = ["パペット", "フィギュア", "子育て", "芸能", "映画", "グルメ", "占い"]

# ==========================================
# 関数群
# ==========================================

def get_crypto_prices():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": "bitcoin,ethereum,ripple,solana,binancecoin,dogecoin,fetch-ai,uniswap", "vs_currencies": "jpy", "include_24hr_change": "true"}
    try:
        data = requests.get(url, params=params, timeout=10).json()
        text = "【現在価格と24h変動】\n"
        for coin, symbol in [("bitcoin","BTC"), ("ethereum","ETH"), ("ripple","XRP"), ("solana","SOL"), ("dogecoin","DOGE"), ("fetch-ai","FET")]:
            if coin in data: text += f"{symbol}: {data[coin]['jpy']}円 ({data[coin]['jpy_24h_change']:.1f}%)\n"
        return text
    except:
        return "価格取得失敗"

def clean_html(html_text):
    if not html_text: return ""
    soup = BeautifulSoup(html_text, "html.parser")
    return soup.get_text()[:100].replace('\n', ' ')

def get_market_vibe_news():
    """特定サイトではなく、世界中の大量のニュース見出しをかき集める"""
    headlines = []
    shuffled_urls = RSS_URLS.copy()
    random.shuffle(shuffled_urls)

    for url in shuffled_urls:
        if len(headlines) >= 50: break # 最大50件の大量データを取得
        try:
            feed = feedparser.parse(requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10).text)
            count = 0
            for entry in feed.entries:
                if any(kw in entry.title for kw in IGNORE_KEYWORDS): continue
                
                summary = clean_html(getattr(entry, 'summary', getattr(entry, 'description', '')))
                if summary:
                    headlines.append(f"・{entry.title} ({summary})")
                else:
                    headlines.append(f"・{entry.title}")
                
                count += 1
                if count >= 10: break # 1つの広域ソースから最大10件拾う
        except:
            pass
    return "【世界中の最新クリプト・マクロニュース（大量データ）】\n" + "\n".join(headlines)

def generate_analysis_tweet(prices, news):
    """Gemini APIを使って相場全体の空気感を分析したツイートを生成"""
    if not GEMINI_API_KEY:
        log("❌ エラー: GEMINI_API_KEY が読み込めませんでした。")
        return None

    genai.configure(api_key=GEMINI_API_KEY)
    
    models_to_try = ['gemini-3-pro-preview', 'gemini-3-flash-preview']

    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            
            prompt = f"""
あなたは経験豊富で知的な若い女性の専業クリプトトレーダーです。
以下の「現在の価格データ」と「世界中から集めた大量のニュース見出し」をスキャンし、今の仮想通貨市場全体の【空気感（センチメント）】を読み取ってください。

【価格データ】
{prices}

【市場のニュースストリーム】
{news}

【あなたの思考・出力プロセス（厳守）】
1. 特定の1つのニュースだけを解説する「ニュースキャスター」にならないでください。
2. 大量の情報から「今は強気なのか」「様子見ムードなのか」「特定のセクター（AIやミーム等）に資金が流れているのか」「マクロ経済の警戒感があるのか」など、市場の全体的な【市況感・バイブス】を読み取ってください。
3. その読み取った相場観を元に、プロのトレーダーとして、あなたのフォロワーに向けた【自由な相場ツイート】を作成してください。

【出力形式】
- 120文字以内で簡潔に（ハッシュタグ込み140文字未満）。
- 一人称は「私」、語尾は「〜わ」「〜わね」「〜よ」「〜かしら」等、上品かつ知的な女性の口調。
- 絵文字は適度に（3〜4個）。
- 具体的な金融・相場用語（資金循環、ボラティリティ、ドミナンス、底堅い、上値が重い 等）を自然に使う。
- トレード指示（買え、売れ）は出さず、「私はこう見ている」というスタンス。
- 関連するハッシュタグを最後に付ける。
"""
            response = model.generate_content(prompt, generation_config={"temperature": 0.85})
            text = response.text.strip()
            
            if len(text) > 140:
                 log("⚠️ 文字数調整を行います")
                 text = text[:137] + "..."
            
            log(f"✨ 使用モデル: {model_name}")
            return text
            
        except Exception as e:
            time.sleep(2)
            continue

    log("❌ 全てのモデルで生成失敗")
    return None

def job():
    log(f"分析を開始します...")
    
    # APIキーの存在チェック
    if not all([X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_SECRET]):
        log("❌ エラー: X APIキーが読み込めませんでした。処理をスキップします。")
        return

    prices = get_crypto_prices()
    news = get_market_vibe_news() # 広域ニュースを取得
    
    tweet_text = generate_analysis_tweet(prices, news)
    
    if tweet_text:
        log("--- ツイート内容 ---")
        log(tweet_text)
        try:
            client = tweepy.Client(
                consumer_key=X_API_KEY, consumer_secret=X_API_SECRET,
                access_token=X_ACCESS_TOKEN, access_token_secret=X_ACCESS_SECRET
            )
            client.create_tweet(text=tweet_text)
            log("✅ 投稿成功！")
        except Exception as e:
            log(f"❌ 投稿エラー: {e}")
            if hasattr(e, 'response') and e.response is not None:
                log(f"詳細情報: {e.response.text}")
    else:
        log("スキップします。")

if __name__ == "__main__":
    try:
        log("=== AI Crypto Analyst Bot (Windows v6.0 Market-Vibe Edition) Started ===")
        
        # PCの現在時刻を表示
        now = datetime.datetime.now()
        log(f"PCの現在時刻: {now.strftime('%Y-%m-%d %H:%M:%S')}")
        
        schedule.every().day.at("01:45").do(job)
        schedule.every().day.at("07:45").do(job)
        schedule.every().day.at("11:45").do(job)
        schedule.every().day.at("17:45").do(job)
        schedule.every().day.at("21:45").do(job)
        
        # テスト実行（初回のみ）
        log("起動時テストを実行します...")
        job()

        # 次回実行予定を表示
        log("--- 次回実行スケジュール ---")
        for j in schedule.get_jobs():
            log(f"次回実行: {j.next_run.strftime('%Y-%m-%d %H:%M:%S')}")
        log("----------------------------")

        log("スケジュール待機中... (画面を閉じると停止します)")
        while True:
            schedule.run_pending()
            time.sleep(60)
    except Exception as e:
        log(f"エラー発生: {e}")
        log(traceback.format_exc())
        input("Enterキーを押して終了...")