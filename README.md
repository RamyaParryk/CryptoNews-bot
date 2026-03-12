<div align="right">
<strong>日本語</strong> | <a href="README_en.md">English</a>
</div>

<h1>AI Crypto Analyst Bot (Macro & Memory Edition) 📈🤖</h1>

仮想通貨のトレンドやニュースだけでなく、日米の株式市場やマクロ経済の動向もスキャンし、Google Gemini AI (最新の 3.1 Pro Preview) がプロの専業投資家として X (旧Twitter) に自動投稿するPython製ボットです。

Windows (デスクトップ) と Linux (サーバー) 用の専用実行ファイルを用意しており、キャラクター設定や口調を外部ファイルから自由に変更可能です。

<h2>✨ 特徴 (V8 アップデート)</h2>

<ul>
<li><b>マクロ経済・株式ニュースの統合:</b> Yahoo!ニュース（経済カテゴリ）のRSSを自動取得。暗号資産の枠を超え、株式市場のリスクオフや金利動向がクリプトに与える影響まで俯瞰して語ります。</li>
<li><b>過去の記憶（話題の重複回避）:</b> 自身の直近のツイート履歴をログファイルから読み込み、同じ話題や切り口を連続して呟かないように自動調整する「記憶力」を持たせました。</li>
<li><b>5つの動的アプローチ:</b> 単調な相場解説を脱却。AIがその日のデータに合わせて「株からの波及」「過熱感のファクトチェック」「辛口銘柄レビュー」「大衆への冷や水」「今日はノートレ（何もしない）宣言」の5つから最適な態度を自動で選択します。</li>
<li><b>堅牢なエラー対策:</b> X API特有のサーバー混雑エラー（503 Service Unavailable等）に対して、プログラムをクラッシュさせずに数分待機して自動リトライする粘り強いロジックを搭載。</li>
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
<li>取得先: <a href="https://www.coingecko.com/ja/api/pricing">仮想通貨データAPI プラン</a></li>
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
AIへの指示（口調、キャラクター、5つのアプローチ）を記述します。
※ <code>{market_data}</code>（最新データ）と <code>{last_tweet}</code>（前回の発言）は、プログラムがデータを挿入する目印なので<b>必ず含めてください</b>。

<pre><code>あなたは経験豊富で知的な、若い女性の専業投資家（クリプト・株）です。
以下の「最新データ（株・経済のニュース、仮想通貨のトレンドとニュース）」を読み込み、そこから一番気になる1つのトピックを選んでください。

【最新データ】
{market_data}

【直近のあなたの発言（記憶）】
{last_tweet}

【あなたの思考・出力プロセス（厳守）】
1. 直近の発言（{last_tweet}）と「同じ話題」や「同じ切り口」は【絶対に避けて】ください。
2. 以下の「5つのアプローチ」から、データと今の気分に一番合うものを【1つだけ】選び、呟きを作成してください。

アプローチ1：【株・マクロ経済からの波及】
日米の株式市場や金利のニュースを取り上げ、そのマクロの動きが仮想通貨の資金循環にどう影響するかをプロ目線で語る。

アプローチ2：【噂・過熱感のファクトチェック】
企業提携の噂や政治絡みの草コインを取り上げ、「公式発表じゃないわよ」「便乗よ」と、事実に基づき過熱感をバッサリ斬る。

アプローチ3：【銘柄レビュー・辛口要約】
トレンド入りしたトークンに対し、フォロワーからの質問に答える体（てい）で、その技術や実態（無名ならギャンブルと斬る）を辛口で要約する。

アプローチ4：【FOMO（大衆の熱狂）への冷や水】
強気ニュースでTLが沸いている時、あえて斜め上の目線から「事実売りが始まるわ」「靴磨きの少年が増えたわね」と大衆を突き放す。

アプローチ5：【ノートレ（何もしない）宣言】
データを見ても「今日はどれもノイズね。優位性がないから手を出さないわ」と判断し、チャートを閉じてお茶を飲むような日常感を見せる。

【出力形式】
120文字以内で簡潔に（ハッシュタグ込み140文字未満）。
一人称は「私」、語尾は「〜わ」「〜わね」等、上品かつ知的な女性の口調。
関連するハッシュタグを最後に付ける。</code></pre>

<hr>

<h2>💻 Windows (デスクトップ) での実行方法</h2>

Windows特有の文字化けエラーを防止した専用ファイル <code>crypto_analyst_x86.py</code> を使用します。
コマンドプロンプト(cmd) または PowerShell を開いて実行してください。

<pre><code># 今すぐ1回だけテスト投稿（手動実行）したい場合
python -c "from crypto_analyst_x86 import job; job()"

# スケジュール通りに継続稼働させる場合
python crypto_analyst_x86.py</code></pre>

<hr>

<h2>🐧 Linux (Ubuntu等のサーバー環境) での実行方法</h2>

<code>crypto_analyst_linux.py</code> を使用します。隔離されたPython仮想環境 (venv) を使って、バックグラウンドで24時間安全に稼働させます。

<pre><code># 1. 仮想環境の作成と有効化
python3 -m venv venv
source venv/bin/activate

# 2. ライブラリのインストール
pip install google-generativeai requests tweepy schedule python-dotenv beautifulsoup4

# 3. テスト実行（今すぐ1回だけ動かす）
python3 -c "from crypto_analyst_linux import job; job()"

# 4. 本番稼働 (PCを閉じても裏側で24時間動かし続ける)
nohup python3 crypto_analyst_linux.py &

# ログの確認方法
tail -f analyst_bot.log

# Botを停止させる方法
pkill -f crypto_analyst_linux.py</code></pre>

<h2>🕒 更新履歴 (Changelog)</h2>

<ul>
<li><b>v8.0</b>: 「Macro & Memory Edition」へ進化。Yahoo!ニュース(経済)からのマクロ指標取得を追加。自身の直近のツイート履歴を読み込んで話題の重複を防ぐ「記憶力」を実装。プロンプトを5つの動的アプローチに拡張。</li>
<li><b>v7.0</b>: CryptoPanic API(v2)とCoinGecko APIを導入。X APIの503エラーに対する自動リトライ機能を実装。</li>
<li><b>v6.6</b>: X APIの認証方法を修正。</li>
</ul>

<h2>⚠️ 免責事項</h2>

このBotによる投資助言や分析結果によって生じた損失について、開発者は一切の責任を負いません。投資は自己責任で行ってください。