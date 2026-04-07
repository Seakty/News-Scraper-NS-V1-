# 📰 News Scraper v1.0

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/FastAPI-0.100+-green.svg" alt="FastAPI">
  <img src="https://img.shields.io/badge/Streamlit-1.25+-red.svg" alt="Streamlit">
  <img src="https://img.shields.io/badge/OpenAI-GPT--4o--mini-orange.svg" alt="OpenAI">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
</div>

## 📋 Overview

**News Scraper** is an AI-powered web application that analyzes news articles in real-time. Simply paste any article URL, and get instant insights including:

- 🤖 **AI-Generated Summary** (concise, 2-3 sentences)
- 🔍 **Key Topics & Keywords** extraction
- 😊 **Sentiment Analysis** with confidence scores
- 🖼️ **Main Article Image** detection
- 📊 **Beautiful Visual Dashboard**

Built with modern Python stack featuring FastAPI backend and Streamlit frontend for a seamless user experience.

## ✨ Features

- **🔗 URL Scraping**: Extracts clean text content from any news article
- **🧠 AI Analysis**: Powered by OpenAI GPT-4o-mini for intelligent summarization
- **🎯 Keyword Extraction**: Identifies 3-5 key topics automatically
- **📈 Sentiment Scoring**: Rates articles from 0-100 with positive/negative/neutral classification
- **💾 History Tracking**: Saves all analyses to CSV for future reference
- **🎨 Modern UI**: Newspaper-inspired design with responsive layout
- **⚡ Fast Processing**: Optimized for quick article analysis

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "News Scraper/News Scraper v1.0"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the root directory by copying `.env.example`:
   ```bash
   cp .env.example .env
   ```
   
   Then edit `.env` and add your OpenAI API key:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

### Running the Application

#### Option 1: Full Application (Recommended)

1. **Start the FastAPI backend**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Start the Streamlit frontend** (in a new terminal)
   ```bash
   streamlit run frontend/ui.py
   ```

3. **Open your browser** to `http://localhost:8501`

#### Option 2: Backend Only (API Mode)

```bash
uvicorn app.main:app --reload
```

Access the API documentation at `http://localhost:8000/docs`

## 📖 Usage

### Web Interface

1. Paste any news article URL in the input field
2. Click "🔍 Analyze Article"
3. View the comprehensive analysis including:
   - Article title and main image
   - AI-generated summary
   - Sentiment analysis with visual score bar
   - Extracted keywords as tags

### API Usage

Send a POST request to `/api/process`:

```bash
curl -X POST "http://localhost:8000/api/process" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://example.com/news-article"}'
```

**Response Format:**
```json
{
  "title": "Article Title",
  "summary": "AI-generated summary in 2-3 sentences...",
  "keywords": ["keyword1", "keyword2", "keyword3"],
  "sentiment": "positive",
  "sentiment_score": 85,
  "full_text_preview": "First 200 characters of article...",
  "url": "https://example.com/news-article",
  "main_image": "https://example.com/image.jpg"
}
```

## 🏗️ Architecture

```
News Scraper v1.0/
├── app/
│   ├── main.py              # FastAPI application & routes
│   └── services/
│       ├── scraper.py       # Web scraping logic
│       └── ai_handler.py    # OpenAI integration
├── frontend/
│   └── ui.py                # Streamlit user interface
├── data/
│   └── news_history.csv     # Analysis history
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

### Core Components

- **🕷️ Scraper Service**: Uses BeautifulSoup to extract clean text and images
- **🤖 AI Handler**: OpenAI GPT-4o-mini for natural language processing
- **🌐 FastAPI Backend**: RESTful API with automatic documentation
- **🎨 Streamlit Frontend**: Interactive web interface with custom CSS

## 🛠️ Technologies Used

- **Backend**: FastAPI, Uvicorn
- **Frontend**: Streamlit, HTML/CSS
- **AI/ML**: OpenAI GPT-4o-mini
- **Web Scraping**: BeautifulSoup4, Requests
- **Data Processing**: Python Standard Library
- **Environment**: python-dotenv

## 📊 Data Storage

All article analyses are automatically saved to `news_history.csv` with the following fields:
- Date & Time
- Article Title
- Sentiment Classification
- Sentiment Score (0-100)
- Source URL

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for providing powerful AI models
- FastAPI and Streamlit communities for excellent frameworks
- BeautifulSoup for reliable web scraping

---

<div align="center">
  <p>Made with ❤️ for AI-powered news analysis</p>
  <p>
    <a href="#overview">Overview</a> •
    <a href="#features">Features</a> •
    <a href="#quick-start">Quick Start</a> •
    <a href="#usage">Usage</a> •
    <a href="#architecture">Architecture</a>
  </p>
</div>