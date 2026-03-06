<div align="right">
<strong>日本語</strong> | <a href="README_en.md">English</a>
</div>

<h1>AI Crypto Analyst Bot (Trend Deep-Dive Edition) 📈🤖</h1>

仮想通貨のトレンド検索データと熱量（Vote）付きのホットニュースをスキャンし、Google Gemini AI (最新の 3.1 Pro Preview) が「いま一番面白い特定のトピック（ミームコインや注目ニュース等）」を深掘りして X (旧Twitter) に自動投稿するPython製ボットです。

Windows (デスクトップ) と Linux (Umbrelサーバー等) の両方に対応し、キャラクター設定や口調を外部ファイルから自由に変更可能です。

<h2>✨ 特徴</h2>

<ul>
<li><b>AIによる一点突破の深掘り分析:</b> 市場全体の無難な要約（天気予報）ではなく、<b>Gemini 3.1 Pro</b> が「なぜ今この草コインが検索されているのか」「このニュースの裏にある思惑は何か」など、特定の話題にフォーカスして鋭い私見を語ります。</li>
<li><b>熱量とトレンドの感知:</b> CryptoPanic API (v2) によるユーザーの投票数（強気/重要）データと、CoinGecko API による世界中の「検索急増トレンド銘柄」を組み合わせ、常に鮮度の高い話題をAIに供給します。</li>
<li><b>堅牢なエラー対策:</b> X API特有のサーバー混雑エラー（503 Service Unavailable等）に対して、プログラムをクラッシュさせずに数分待機して自動リトライする粘り強いロジックを搭載。</li>
<li><b>プロンプト外部化とプライバシー:</b> キャラクター設定やAIへの指示内容は <code>prompt.txt</code> に、APIキーは <code>X-GoogleAPI.env</code> に完全分離。機密情報や独自のプロンプト（ノウハウ）を漏らすことなく、安全に GitHub へ公開できます。</li>
</ul>

<h2>⚙️ 事前準備 (APIキーの取得)</h2>

このBotを動かすには、以下の4つのAPIキーが必要です。

<ol>
<li><b>X (Twitter) API Keys</b> (無料のPay-Per-Use枠でOK)
<ul>
<li>取得先: <a href="https://console.x.com/">X Developer Console</a></li>
<li>必要な権限: <b>Read and Write</b> (設定変更後、必ずトークンをRegenerateしてください)</li>
</ul>
</li>
<li><b>Google Gemini API Key</b> (無料枠でOK)
<ul>
<li>取得先: <a href="https://aistudio.google.com/app/apikey">Google AI Studio</a></li>
</ul>
</li>
<li><b>CryptoPanic API Key</b> (auth_token)
<ul>
<li>取得先: <a href="https://cryptopanic.com/developers/api/">CryptoPanic Developer API</a></li>
</ul>
</li>
<li><b>CoinGecko API Key</b> (無料のDemoプラン)
<ul>
<li>取得先: <a href="https://www.coingecko.com/ja/api/pricing">CoinGecko Developer Console</a></li>
</ul>
</li>
</ol>

<h2>🚀 インストールと設定</h2>

<h3>1. リポジトリのクローン</h3>

<pre><code>git clone https://github.com/あなたのユーザー名/リポジトリ名.git
cd リポジトリ名</code></pre>

<h3>2. 設定ファイルの作成 (必須)</h3>

フォルダ内に以下の2つのファイルを作成してください。

<b>① APIキー設定:</b> <code>X-GoogleAPI.env</code>

<pre><code># X (Twitter) Settings
X_API_KEY=あなたのAPI_KEY
X_API_SECRET=あなたのAPI_SECRET
X_ACCESS_TOKEN=あなたのACCESS_TOKEN
X_ACCESS_SECRET=あなたのACCESS_SECRET

# Google Gemini Settings
GEMINI_API_KEY=あなたのGEMINI_API_KEY

# Data Source APIs
CRYPTOPANIC_API_KEY=あなたのCRYPTOPANIC_AUTH_TOKEN
COINGECKO_API_KEY=あなたのCOINGECKO_DEMO_API_KEY</code></pre>

<b>② 指示内容設定:</b> <code>prompt.txt</code>
AIへの指示（口調、キャラクター、分析のルール）を記述します。
※ <code>{market_data}</code> はプログラムが統合データを挿入する目印なので<b>必ず含めてください</b>。

<pre><code>あなたは経験豊富で知的な若い女性の専業クリプトトレーダーです。
以下の「最新の市場データ（検索トレンド銘柄、価格、コミュニティの熱量付きホットニュース）」を読み込み、そこから【今一番面白そうな特定の1つのトピック（銘柄やニュース）】をピックアップしてください。

【最新の市場データ】
{market_data}

【あなたの思考・出力プロセス（厳守）】
市場全体の無難な要約（天気予報）は絶対にしないでください。
データの中から1つのテーマだけに焦点を絞り、「なぜ今これがウケているのか」など、プロのトレーダーとしての【鋭い私見・独自の考察】を展開してください。
その考察を元に、フォロワーに向けた【自由な相場ツイート】を作成してください。

【出力形式】
120文字以内で簡潔に（ハッシュタグ込み140文字未満）。
一人称は「私」、語尾は「〜わ」「〜わね」等、上品かつ知的な女性の口調。
関連するハッシュタグ（選んだ銘柄のティッカーなど）を最後に付ける。</code></pre>

<hr>

<h2>💻 Windowsでの実行方法</h2>

コマンドプロンプト(cmd) または PowerShell を開いて実行します。

<pre><code>python crypto_analyst.py</code></pre>

<ul>
<li>初回起動時に必要なライブラリが自動的にインストールされます。</li>
<li>黒い画面が開いている間、毎日 <b>01:45, 07:45, 11:45, 17:45, 21:45</b> に自動投稿します。</li>
</ul>

<hr>

<h2>🐧 Linux (Ubuntu/Docker等) での実行方法</h2>

バックグラウンド実行する場合の手順です。

<pre><code># 仮想環境の作成と有効化
python3 -m venv venv
source venv/bin/activate

# ライブラリのインストール
pip install google-generativeai requests tweepy schedule python-dotenv beautifulsoup4

# 実行 (ログは analyst_bot.log に保存されます)
nohup python3 crypto_analyst_linux.py > /dev/null 2>&1 &</code></pre>

<ul>
<li><b>UTC自動補正機能:</b> サーバーが世界標準時(UTC)の場合、自動的に日本時間(JST)のスケジュールに合わせて調整します。</li>
</ul>

<h2>🕒 更新履歴 (Changelog)</h2>

<ul>
<li><b>v7.0</b>: 「Trend Deep-Dive Edition」へ進化。CryptoPanic公式API(v2)とCoinGecko APIを導入し、投票熱量とトレンド銘柄の取得に対応。X APIの503エラーに対する自動リトライ機能を実装。プロンプトのデータ変数を <code>{market_data}</code> に統合。</li>
<li><b>v6.6</b>: X APIの認証方法を修正（引数の明示化）。Windows/Linux両環境での安定稼働を確認。</li>
<li><b>v6.0 - v6.4</b>: 「市況俯瞰・自由詠唱版」へのアップデート。プロンプトを <code>prompt.txt</code> に外部化。</li>
</ul>

<h2>⚠️ 免責事項</h2>

このBotによる投資助言や分析結果によって生じた損失について、開発者は一切の責任を負いません。投資は自己責任で行ってください。