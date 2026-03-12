<div align="right">
<a href="README.md">日本語</a> | <strong>English</strong>
</div>

<h1>AI Crypto Analyst Bot (Macro & Memory Edition) 📈🤖</h1>

A Python-based bot powered by Google Gemini AI (the latest <b>3.1 Pro Preview</b>). It scans not only trending cryptocurrency data and hot news but also US/Japan stock markets and macro-economy trends. It automatically posts sharp, insightful tweets to X (formerly Twitter) acting as a professional full-time investor.

It includes dedicated execution files for both Windows (Desktop) and Linux (Servers). Character settings and tone can be freely customized via an external text file.

<h2>✨ Features (V8 Update)</h2>

<ul>
<li><b>Macro Economy & Stock News Integration:</b> Automatically fetches RSS feeds from Yahoo Finance. The AI observes the crypto market from a broader macro perspective, analyzing how stock market risk-off scenarios or interest rate changes affect crypto liquidity.</li>
<li><b>Memory (Topic Repetition Avoidance):</b> The bot reads its own most recent tweet from the log file, ensuring it never repeats the same topic or analytical angle twice in a row.</li>
<li><b>5 Dynamic AI Approaches:</b> Bypasses boring market summaries. The AI automatically selects one of five distinct attitudes based on the daily data: Macro analysis, Rumor fact-checking, Harsh token reviews, Cooling down FOMO, or Declaring a "No-Trade" day.</li>
<li><b>Robust Error Handling (Auto-Retry):</b> Equipped with a resilient logic that prevents crashes and automatically retries after a few minutes when encountering X API server overloads (e.g., 503 Service Unavailable).</li>
</ul>

<h2>⚙️ Prerequisites (Get API Keys)</h2>

To run this bot, you need the following four API keys:

<ol>
<li><b>X (Twitter) API Keys</b> (Free Pay-Per-Use Tier is OK)
<ul>
<li>Get from: <a href="https://console.x.com/">X Developer Console</a></li>
<li>Required Permissions: <b>Read and Write</b> (If you change permissions, don't forget to regenerate your Access Token!)</li>
</ul>
</li>
<li><b>Google Gemini API Key</b> (Free Tier is OK)
<ul>
<li>Get from: <a href="https://aistudio.google.com/app/apikey">Google AI Studio</a></li>
</ul>
</li>
<li><b>CryptoPanic API Key</b> (auth_token)
<ul>
<li>Get from: <a href="https://cryptopanic.com/developers/api/">CryptoPanic Developer API</a></li>
</ul>
</li>
<li><b>CoinGecko API Key</b> (Free Demo Plan)
<ul>
<li>Get from: <a href="https://www.coingecko.com/ja/api/pricing">Crypto Data API Plans</a></li>
</ul>
</li>
</ol>

<h2>🚀 Installation and Setup</h2>

<h3>1. Clone the Repository</h3>

<pre><code>git clone https://github.com/YourUsername/repository-name.git
cd repository-name</code></pre>

<h3>2. Create Configuration Files (Required)</h3>

Create the following two files inside your folder.

<b>① API Key Config:</b> <code>X-GoogleAPI.env</code>

<pre><code># X (Twitter) Settings
X_API_KEY=YOUR_API_KEY
X_API_SECRET=YOUR_API_SECRET
X_ACCESS_TOKEN=YOUR_ACCESS_TOKEN
X_ACCESS_SECRET=YOUR_ACCESS_SECRET

# Google Gemini Settings
GEMINI_API_KEY=YOUR_GEMINI_API_KEY

# Data Source APIs
CRYPTOPANIC_API_KEY=YOUR_CRYPTOPANIC_AUTH_TOKEN
COINGECKO_API_KEY=YOUR_COINGECKO_DEMO_API_KEY</code></pre>

<b>② AI Prompt Config:</b> <code>prompt.txt</code>
Define the AI's instructions, tone, and the 5 approaches here.
Note: The variables <code>{market_data}</code> and <code>{last_tweet}</code> are required placeholders where the script injects data.

<pre><code>You are an experienced and intelligent young female full-time investor (crypto & stocks).
Read the "Latest Data (stock/macro news, crypto trends)" below and pick ONE most interesting topic.

【Latest Data】
{market_data}

【Your Recent Tweet (Memory)】
{last_tweet}

【Your Thought/Output Process (Strict)】
1. Absolutely AVOID talking about the same topic or using the same angle as your {last_tweet}.
2. Choose exactly ONE of the following "5 Approaches" that best fits the data and your current mood, and draft your tweet.

Approach 1: [Macro & Stocks] Analyze how recent US/Japan stock market or interest rate movements will affect crypto liquidity.
Approach 2: [Fact-Check] Cool down the hype around a trending rumor or political meme coin by pointing out the lack of official sources.
Approach 3: [Harsh Token Review] Answer an imaginary follower's question about a trending token. Summarize its tech/reality harshly (or dismiss it as a gamble if unknown).
Approach 4: [Cooling FOMO] When the timeline is overly bullish, take a contrarian view. Warn about "sell-the-fact" scenarios or "shoeshine boy" signals.
Approach 5: [No-Trade Declaration] If the data is just noise with no edge, declare that you won't trade today and are just closing the charts to drink tea.

【Output Format】
Keep it concise within 120 characters (under 140 including hashtags).
Use an elegant, confident, and slightly sarcastic female tone (using "I").
Add relevant hashtags at the end.</code></pre>

<hr>

<h2>💻 How to Run on Windows (Desktop)</h2>

Use <code>crypto_analyst_x86.py</code>, which includes fixes for Windows-specific encoding errors.
Open Command Prompt (cmd) or PowerShell and run:

<pre><code># To test a single post immediately:
python -c "from crypto_analyst_x86 import job; job()"

# To run continuously on a schedule:
python crypto_analyst_x86.py</code></pre>

<hr>

<h2>🐧 How to Run on Linux (Ubuntu/Servers)</h2>

Use <code>crypto_analyst_linux.py</code>. We recommend running it in a Python virtual environment (venv) in the background.

<pre><code># 1. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install libraries
pip install google-generativeai requests tweepy schedule python-dotenv beautifulsoup4

# 3. Test execution (run once)
python3 -c "from crypto_analyst_linux import job; job()"

# 4. Run in background (keeps running even if you close SSH)
nohup python3 crypto_analyst_linux.py &

# To check live logs
tail -f analyst_bot.log

# To stop the bot
pkill -f crypto_analyst_linux.py</code></pre>

<h2>🕒 Changelog</h2>

<ul>
<li><b>v8.0</b>: Evolved to "Macro & Memory Edition". Added macro-economy RSS integration (Yahoo Finance). Implemented "Memory" to read recent tweets from logs to avoid topic repetition. Expanded prompt to 5 dynamic approaches.</li>
<li><b>v7.0</b>: Integrated CryptoPanic API (v2) and CoinGecko API. Implemented auto-retry for X API 503 errors.</li>
<li><b>v6.6</b>: Fixed X API authentication parameters.</li>
</ul>

<h2>⚠️ Disclaimer</h2>

The developer assumes no responsibility for any financial losses incurred from the investment insights generated by this bot. Please invest at your own risk.