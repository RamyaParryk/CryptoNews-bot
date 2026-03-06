<div align="right">
<a href="README.md">日本語</a> | <strong>English</strong>
</div>

<h1>AI Crypto Analyst Bot (Trend Deep-Dive Edition) 📈🤖</h1>

A Python-based bot powered by Google Gemini AI (the latest <b>3.1 Pro Preview</b>) that scans trending cryptocurrency search data and hot news streams with community sentiment (votes). Instead of generic market summaries, it dives deep into specific hot topics (like meme coins or viral news) and automatically posts sharp, insightful tweets to X (formerly Twitter).

Compatible with both Windows (Desktop) and Linux (Umbrel servers, etc.). Character settings and tone can be freely customized via an external text file.

<h2>✨ Features</h2>

<ul>
<li><b>AI Single-Topic Deep Dive:</b> Bypasses boring, weather-report-style market summaries. <b>Gemini 3.1 Pro</b> focuses on specific trends ("Why is this obscure coin trending?" or "What's the hidden motive behind this news?") to share professional and unique trading insights.</li>
<li><b>Sentiment & Trend Detection:</b> Combines CryptoPanic API (v2) for community vote data (Bullish/Important) and CoinGecko API for real-time global "Trending Searches," ensuring the AI is always fed the freshest narratives.</li>
<li><b>Robust Error Handling (Auto-Retry):</b> Equipped with a resilient logic that prevents crashes and automatically retries after a few minutes when encountering X API server overloads (e.g., 503 Service Unavailable).</li>
<li><b>Privacy & Prompt Externalization:</b> Character personas and AI instructions are safely isolated in <code>prompt.txt</code>, and API keys in <code>X-GoogleAPI.env</code>. You can safely publish your code to GitHub without leaking sensitive data or your secret trading prompts.</li>
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
Define the AI's instructions, tone, and persona here.
Note: The variable <code>{market_data}</code> is a required placeholder where the script injects data.

<pre><code>You are an experienced and intelligent young female full-time crypto trader.
Scan the "Latest Market Data (trending coins, prices, hot news with community votes)" below and pick 【ONE highly interesting specific topic (coin or news)】.

【Latest Market Data】
{market_data}

【Your Thought/Output Process】
Absolutely DO NOT provide a generic "weather report" summary of the whole market.
Focus on just ONE theme from the data and deploy a 【sharp, unique perspective】 as a pro trader (e.g., "Why is this catching on right now?").
Based on your insight, create a 【free-form market tweet】 for your followers.

【Output Format】
Keep it concise within 120 characters (under 140 including hashtags).
Use an elegant, intelligent, and confident female tone.
Add relevant hashtags (like the ticker of the chosen coin) at the end.</code></pre>

<hr>

<h2>💻 How to Run on Windows</h2>

Open Command Prompt (cmd) or PowerShell and run:

<pre><code>python crypto_analyst.py</code></pre>

<ul>
<li>Necessary libraries will be installed automatically on the first run.</li>
<li>The bot will automatically post daily at <b>01:45, 07:45, 11:45, 17:45, 21:45</b> as long as the terminal is open.</li>
</ul>

<hr>

<h2>🐧 How to Run on Linux (Ubuntu/Docker)</h2>

Instructions for background execution on a server.

<pre><code># Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install libraries
pip install google-generativeai requests tweepy schedule python-dotenv beautifulsoup4

# Run in background (Logs are saved to analyst_bot.log)
nohup python3 crypto_analyst_linux.py > /dev/null 2>&1 &</code></pre>

<ul>
<li><b>UTC Auto-Correction:</b> Automatically adjusts posting times to JST schedules if the server timezone is UTC.</li>
</ul>

<h2>🕒 Changelog</h2>

<ul>
<li><b>v7.0</b>: Evolved to "Trend Deep-Dive Edition". Integrated CryptoPanic API (v2) and CoinGecko API to fetch community votes and trending coins. Implemented an auto-retry feature for X API 503 errors. Unified prompt data variable to <code>{market_data}</code>.</li>
<li><b>v6.6</b>: Fixed X API authentication parameters. Confirmed stable operation on both Windows and Linux environments.</li>
<li><b>v6.0 - v6.4</b>: Major update to the "Market-Vibe Edition." Externalized AI instructions to <code>prompt.txt</code>.</li>
</ul>

<h2>⚠️ Disclaimer</h2>

The developer assumes no responsibility for any financial losses incurred from the investment insights generated by this bot. Please invest at your own risk.