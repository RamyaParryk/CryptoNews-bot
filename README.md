<div align="right">
<strong>日本語</strong> | <a href="README_en.md">English</a>
</div>

<h1>AI Crypto Analyst Bot (Market-Vibe Edition) 📈🤖</h1>

仮想通貨の価格データと世界中から集めた大量のニュースストリームをスキャンし、Google Gemini AI (最新の 3.1 Pro Preview) が市場全体の「空気感（センチメント）」を分析して X (旧Twitter) に自動投稿するPython製ボットです。

Windows (デスクトップ) と Linux (Umbrelサーバー等) の両方に対応し、キャラクター設定や口調を外部ファイルから自由に変更可能です。

<h2>✨ 特徴</h2>

<ul>
<li><b>AIによる市況俯瞰分析:</b> 単一のニュースを解説するのではなく、<b>Gemini 3.1 Pro</b> が大量の情報から「いま市場はどういう空気か？（強気、警戒、資金循環など）」を読み取り、独自の相場観を語ります。</li>
<li><b>超・広域情報収集:</b> CryptoPanic, Google News (日英広域), Investing.com 等のアグリゲーターを使用し、一度に最大50件のニュース見出しをAIに流し込みます。</li>
<li><b>プロンプト外部化:</b> キャラクター設定やAIへの指示内容を <code>prompt.txt</code> に切り出し。Botを再起動させることなく、テキストファイルを編集するだけでいつでも口調や分析スタンスを変更できます。</li>
<li><b>プライバシー重視:</b> APIキーは <code>X-GoogleAPI.env</code>、独自の指示内容は <code>prompt.txt</code> に保存。コード内に機密情報やノウハウを残さず、安全に GitHub へ公開できます。</li>
</ul>

<h2>⚙️ 事前準備 (APIキーの取得)</h2>

このBotを動かすには、以下の2つのAPIキーが必要です。

<ol>
<li><b>X (Twitter) API Keys</b> (Free TierでOK)
<ul>
<li>取得先: <a href="https://developer.x.com/en/portal/dashboard">X Developer Portal</a></li>
<li>必要な権限: <b>Read and Write</b> (設定変更後、必ずトークンをRegenerateしてください)</li>
</ul>
</li>
<li><b>Google Gemini API Key</b> (無料枠でOK)
<ul>
<li>取得先: <a href="https://aistudio.google.com/app/apikey">Google AI Studio</a></li>
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

Google Gemini Settings

GEMINI_API_KEY=あなたのGEMINI_API_KEY</code></pre>

<b>② 指示内容設定:</b> <code>prompt.txt</code>
AIへの指示（口調、キャラクター、分析のルール）を記述します。
※ <code>{prices}</code> と <code>{news}</code> はプログラムがデータを挿入する目印なので<b>必ず含めてください</b>。

<pre><code>あなたは経験豊富で知的な若い女性の専業クリプトトレーダーです。
以下の「現在の価格データ」と「世界中から集めた大量のニュース見出し」をスキャンし、今の仮想通貨市場全体の【空気感（センチメント）】を読み取ってください。

【価格データ】
{prices}

【市場のニュースストリーム】
{news}

【あなたの思考・出力プロセス（厳守）】
特定の1つのニュースだけを解説する「ニュースキャスター」にならないでください。
大量の情報から市場の全体的な【市況感・バイブス】を読み取ってください。
その読み取った相場観を元に、プロのトレーダーとして、あなたのフォロワーに向けた【自由な相場ツイート】を作成してください。

【出力形式】
120文字以内で簡潔に（ハッシュタグ込み140文字未満）。
一人称は「私」、語尾は「〜わ」「〜わね」等、上品かつ知的な女性の口調。
関連するハッシュタグを最後に付ける。</code></pre>

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

ライブラリのインストール

pip install google-generativeai requests feedparser tweepy schedule python-dotenv beautifulsoup4

実行 (ログは analyst_bot.log に保存されます)

nohup python3 crypto_analyst_linux.py > /dev/null 2>&1 &</code></pre>

<ul>
<li><b>UTC自動補正機能:</b> サーバーが世界標準時(UTC)の場合、自動的に日本時間(JST)のスケジュールに合わせて調整します。</li>
</ul>

<h2>🕒 更新履歴 (Changelog)</h2>

<ul>
<li><b>v6.6</b>: X APIの認証方法を修正（引数の明示化）。Windows/Linux両環境での安定稼働を確認。</li>
<li><b>v6.0 - v6.4</b>: 「市況俯瞰・自由詠唱版」へ大幅アップデート。特定のニュースサイト依存を廃止し、アグリゲーターによる超・広域情報収集に変更。プロンプトを <code>prompt.txt</code> に外部化。使用AIモデルを <b>Gemini 3.1 Pro Preview</b> にアップデート。</li>
<li><b>v4.x以前</b>: 特定のニュースサイトから記事をピックアップして要約する従来型のロジック。</li>
</ul>

<h2>⚠️ 免責事項</h2>

このBotによる投資助言や分析結果によって生じた損失について、開発者は一切の責任を負いません。投資は自己責任で行ってください。