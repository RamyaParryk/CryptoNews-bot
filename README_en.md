<div align="right">
<a href="README.md">日本語</a> | <strong>English</strong>
</div>

<h1>AI Crypto Analyst Bot (Market-Vibe Edition) 📈🤖</h1>

A Python-based bot that scans cryptocurrency price data and massive news streams gathered from around the world. Powered by Google Gemini AI (the latest <b>3.1 Pro Preview</b>), it analyzes the overall "market sentiment/vibe" and automatically posts its insights to X (formerly Twitter).

Compatible with both Windows (Desktop) and Linux (Umbrel servers, etc.). Character settings and tone can be freely customized via an external text file.

<h2>✨ Features</h2>

<ul>
<li><b>Macro Market Sentiment Analysis:</b> Instead of simply summarizing single news articles, <b>Gemini 3.1 Pro</b> reads a massive amount of headlines to grasp the overall "vibe" of the market (e.g., bullish, cautious, sector rotation) and shares professional trading insights.</li>
<li><b>Ultra-Wide Data Collection:</b> Uses aggregators like CryptoPanic, Google News (Broad search), and Investing.com to feed up to 50 news headlines to the AI at once.</li>
<li><b>Externalized Prompts:</b> Character personas and AI instructions are separated into <code>prompt.txt</code>. You can change the bot's tone or analysis stance simply by editing this text file, without needing to restart the bot.</li>
<li><b>Privacy Focused:</b> API keys are stored in <code>X-GoogleAPI.env</code> and custom instructions in <code>prompt.txt</code>. You can safely publish your code to GitHub without leaking sensitive information or your secret trading prompts.</li>
</ul>

<h2>⚙️ Prerequisites (Get API Keys)</h2>

To run this bot, you need the following two API keys:

<ol>
<li><b>X (Twitter) API Keys</b> (Free Tier is OK)
<ul>
<li>Get from: <a href="https://developer.x.com/en/portal/dashboard">X Developer Portal</a></li>
<li>Required Permissions: <b>Read and Write</b> (If you change permissions, don't forget to regenerate your Access Token!)</li>
</ul>
</li>
<li><b>Google Gemini API Key</b> (Free Tier is OK)
<ul>
<li>Get from: <a href="https://aistudio.google.com/app/apikey">Google AI Studio</a></li>
</ul>
</li>
</ol>

<h2>🚀 Installation and Setup</h2>

<h3>1. Clone the Repository</h3>

<pre><code>git clone https://www.google.com/search?q=https://github.com/YourUsername/repository-name.git
cd repository-name</code></pre>

<h3>2. Create Configuration Files (Required)</h3>

Create the following two files inside your folder.

<b>① API Key Config:</b> <code>X-GoogleAPI.env</code>

<pre><code># X (Twitter) Settings
X_API_KEY=YOUR_API_KEY
X_API_SECRET=YOUR_API_SECRET
X_ACCESS_TOKEN=YOUR_ACCESS_TOKEN
X_ACCESS_SECRET=YOUR_ACCESS_SECRET

Google Gemini Settings

GEMINI_API_KEY=YOUR_GEMINI_API_KEY</code></pre>

<b>② AI Prompt Config:</b> <code>prompt.txt</code>
Define the AI's instructions, tone, and persona here.
Note: The variables <code>{prices}</code> and <code>{news}</code> are required placeholders where the script injects data.

<pre><code>You are an experienced and intelligent young female full-time crypto trader.
Scan the "Current Price Data" and the "Massive News Stream" below to read the overall 【sentiment/vibe】 of the cryptocurrency market.

【Price Data】
{prices}

【Market News Stream】
{news}

【Your Thought/Output Process】
Do not act like a "newscaster" who just summarizes one specific news item.
Read the overall market vibe from the massive amount of information.
Based on that, create a 【free-form market tweet】 for your followers as a pro trader.

【Output Format】
Keep it concise within 120 characters (under 140 including hashtags).
Use an elegant, intelligent, and slightly confident female tone.
Add relevant hashtags at the end.</code></pre>

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

Install libraries

pip install google-generativeai requests feedparser tweepy schedule python-dotenv beautifulsoup4

Run in background (Logs are saved to analyst_bot.log)

nohup python3 crypto_analyst_linux.py > /dev/null 2>&1 &</code></pre>

<ul>
<li><b>UTC Auto-Correction:</b> Automatically adjusts posting times to JST schedules if the server timezone is UTC.</li>
</ul>

<h2>🕒 Changelog</h2>

<ul>
<li><b>v6.6</b>: Fixed X API authentication parameters. Confirmed stable operation on both Windows and Linux environments.</li>
<li><b>v6.0 - v6.4</b>: Major update to the "Market-Vibe Edition." Shifted from single-news summarization to ultra-wide aggregator data collection. Externalized AI instructions to <code>prompt.txt</code>. Upgraded AI model to <b>Gemini 3.1 Pro Preview</b>.</li>
<li><b>v4.x and below</b>: Legacy logic that picked and summarized specific news articles.</li>
</ul>

<h2>⚠️ Disclaimer</h2>

The developer assumes no responsibility for any financial losses incurred from the investment insights generated by this bot. Please invest at your own risk.