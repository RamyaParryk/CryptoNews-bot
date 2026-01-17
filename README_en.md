<div align="right">
<a href="README.md">日本語</a> | <strong>English</strong>
</div>

<h1>AI Crypto Analyst Bot 📈🤖</h1>

A Python-based bot that collects cryptocurrency price data and the latest news, analyzes the market using Google Gemini AI (3.0 Pro/Flash Preview), and automatically posts to X (formerly Twitter).

Compatible with both Windows (Desktop) and Linux (Umbrel servers, etc.).

<h2>✨ Features</h2>

<ul>
<li><b>AI Market Analysis:</b> Instead of just listing news, the latest <b>Gemini 3.0 Pro</b> (or Flash) acts as a "young female trader" persona to discuss daily market sentiments.</li>
<li><b>Multi-Source Data Collection:</b> Gathers information from a total of 12 major domestic and international media outlets (CoinPost, CoinTelegraph, Bloomberg, Yahoo Finance, etc.).</li>
<li><b>Price Integration:</b> Fetches prices and fluctuation rates for 11 assets including BTC, ETH, XRP, SOL, BNB, DOGE, FET, UNI, IMX, Gold (XAUT), and XMR from CoinGecko to reflect in the analysis.</li>
<li><b>Variety in Analysis:</b> Prevents repetition by analyzing from 8 different perspectives each time, such as "Macro Economy Focus," "Altcoin Spotlight," "Risk Alert," and "Technical Analysis."</li>
<li><b>Automated Hashtags:</b> Automatically selects appropriate hashtags based on the content of the article.</li>
</ul>

<h2>⚙️ Prerequisites (Get API Keys)</h2>

To run this bot, you need the following two API keys:

<ol>
<li><b>X (Twitter) API Keys</b> (Free Tier is OK)
<ul>
<li>Get from: <a href="https://developer.x.com/en/portal/dashboard">X Developer Portal</a></li>
<li>Required Permissions: <b>Read and Write</b> (Don't forget to change settings!)</li>
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

<h3>2. Create Configuration File (Required)</h3>

For security reasons, API keys are not included in the code.
Create a file named <code>X-GoogleAPI.env</code> inside the folder and enter the following content:

<b>Filename:</b> <code>X-GoogleAPI.env</code>

<pre><code># X (Twitter) Settings
X_API_KEY=YOUR_API_KEY
X_API_SECRET=YOUR_API_SECRET
X_ACCESS_TOKEN=YOUR_ACCESS_TOKEN
X_ACCESS_SECRET=YOUR_ACCESS_SECRET

Google Gemini Settings

GEMINI_API_KEY=YOUR_GEMINI_API_KEY</code></pre>

<hr>

<h2>💻 How to Run on Windows</h2>

Instructions for easily running on a desktop environment.

Open Command Prompt (cmd) or PowerShell.

Navigate to the folder and run the script.

<pre><code>python crypto_analyst.py</code></pre>

<ul>
<li>Necessary libraries (<code>google-generativeai</code>, <code>tweepy</code>, etc.) will be installed automatically on the first run.</li>
<li>Automatic posts will occur daily at <b>01:45, 07:45, 11:45, 17:45, 21:45</b> as long as the black screen is open.</li>
</ul>

<hr>

<h2>🐧 How to Run on Linux (Umbrel)</h2>

Instructions for running in the background on an always-on server like Umbrel.

<h3>1. Create Virtual Environment and Install Libraries</h3>

Use a virtual environment (venv) to keep the Umbrel environment clean.

<pre><code># Create virtual environment
python3 -m venv venv

Activate virtual environment

source venv/bin/activate

Install libraries

pip install google-generativeai requests feedparser tweepy schedule python-dotenv</code></pre>

<h3>2. Start in Background</h3>

Use <code>nohup</code> to keep it running even after disconnecting SSH.

<pre><code># Run (Logs are saved to analyst_bot.log)
nohup python3 crypto_analyst_linux.py > /dev/null 2>&1 &</code></pre>

<ul>
<li><b>UTC Auto-Correction:</b> If the server is on Coordinated Universal Time (UTC), it automatically adjusts to the Japan Standard Time (JST) schedule (01:45, 07:45, 11:45, 17:45, 21:45).</li>
</ul>

<h3>3. Check Status and Stop</h3>

<b>Check Logs:</b>

<pre><code>tail -f analyst_bot.log</code></pre>

<b>Stop Bot:</b>

<pre><code>pkill -f crypto_analyst_linux.py</code></pre>

<h2>📂 File Structure</h2>

<ul>
<li><code>crypto_analyst.py</code>: <b>Windows Version</b> (Includes character encoding fix & auto-install function)</li>
<li><code>crypto_analyst_linux.py</code>: <b>Linux Version</b> (Includes log file output & UTC time correction)</li>
<li><code>X-GoogleAPI.env</code>: API key configuration file (*Not uploaded to GitHub)</li>
</ul>

<h2>🕒 Changelog</h2>

<ul>
<li><b>v4.4</b>: Updated AI model to <b>Gemini 3.0 Pro/Flash Preview</b> for better analysis and expression (removed 2.0 series). Windows version updated to match specs.</li>
<li><b>v4.3</b>: Changed posting frequency to 5 times a day (01:45, 07:45, 11:45, 17:45, 21:45). Removed heartbeat logs.</li>
<li><b>v4.2</b>: Expanded analysis perspectives to 8 patterns (added Technical, Whale Tracking, Sector Analysis).</li>
<li><b>v4.1</b>: Increased monitored assets to 11 (BTC, ETH, XRP, SOL, BNB, DOGE, FET, UNI, IMX, GOLD, XMR).</li>
<li><b>v3.x</b>: Added macro-economic news sources, API key externalization (.env).</li>
<li><b>v2.x</b>: Added Japanese/English news support, UTC time auto-correction.</li>
</ul>

<h2>⚠️ Disclaimer</h2>

The developer assumes no responsibility for any losses caused by investment advice or analysis results from this bot.





Please invest at your own risk.