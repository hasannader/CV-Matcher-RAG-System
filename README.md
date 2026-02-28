# 🎯 CV Matcher RAG System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![LangChain](https://img.shields.io/badge/LangChain-0.3+-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**An intelligent AI-powered recruitment assistant that analyzes CVs using RAG (Retrieval-Augmented Generation) to find the perfect candidates for your job requirements.**

[Features](#-features) • [Quick Start](#-quick-start) • [Demo](#-demo) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Demo](#-demo)
- [Technology Stack](#-technology-stack)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Usage](#-usage)
- [Configuration](#-configuration)
- [Project Structure](#-project-structure)
- [Examples](#-examples)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgements](#-acknowledgements)

---

## 🌐 Overview

CV Matcher RAG System is a modern recruitment tool that leverages advanced AI technologies to streamline the candidate screening process. By combining retrieval-augmented generation with semantic search, it provides HR professionals with evidence-based candidate recommendations, significantly reducing time spent on manual CV screening.

### Why CV Matcher RAG?

- **⚡ Save Time**: Analyze multiple CVs in seconds instead of hours
- **🎯 Precision Matching**: AI-powered semantic understanding of job requirements
- **📊 Evidence-Based**: Every recommendation comes with supporting evidence from CVs
- **🔒 Privacy-Focused**: All processing happens locally, your data stays with you
- **🚀 Easy to Use**: Clean, intuitive interface designed for HR professionals

---

## ✨ Features

### Core Capabilities

- **🔄 Batch Processing**: Analyze 2-5 CVs simultaneously
- **🤖 AI-Powered Analysis**: Uses Google Gemini for intelligent candidate evaluation
- **🔍 Semantic Search**: FAISS-based vector search for relevant skill matching
- **📝 Evidence Extraction**: Provides exact quotes from CVs supporting each match
- **📊 Candidate Ranking**: Ranks candidates by relevance with match scores
- **🛡️ Security Features**: 
  - Prompt injection detection
  - Irrelevant query filtering
  - Duplicate CV detection
  - Content validation

### User Interface

- **📤 Drag-and-Drop Upload**: Easy CV upload with duplicate detection
- **💬 Natural Language Queries**: Ask questions in plain English
- **📋 Detailed Results**: Expandable sections showing evidence from CVs
- **🗑️ File Management**: Clear uploaded CVs with one click
- **💾 Persistent Storage**: CVs remain saved between sessions

---

## 🎥 Demo

### Sample Query and Response

**Query**: "Find candidates with Python and machine learning experience"

**Response**:
```
Matching Candidates:

1. Sarah Johnson - High Match
   Skills: Python, R, Machine Learning, Deep Learning
   Evidence: "5+ years experience in Python development with focus on 
   ML algorithms including TensorFlow and PyTorch..."

2. John Smith - Medium Match
   Skills: Python, AWS, Basic ML
   Evidence: "Proficient in Python for backend development and familiar 
   with scikit-learn for basic machine learning tasks..."
```

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **LLM** | Google Gemini 2.5 Flash | Natural language understanding and generation |
| **Embeddings** | Gemini Embedding 001 | Converting text to vector representations |
| **Vector Store** | FAISS | Efficient similarity search |
| **Framework** | LangChain 0.3+ | RAG pipeline orchestration |
| **Frontend** | Streamlit | Interactive web interface |
| **PDF Processing** | PyPDF2 | Text extraction from CVs |
| **Environment** | Python 3.8+ | Core runtime |

---

## 🏗️ Architecture

### System Design

```
┌─────────────────┐
│   Streamlit UI  │
└────────┬────────┘
         │
    ┌────▼────┐
    │  app.py │ (Main UI Logic)
    └────┬────┘
         │
    ┌────▼──────────┐
    │  rag_system   │ (CVMatcherRAG Class)
    └────┬──────────┘
         │
    ┌────▼────┬──────────┬────────┐
    │ FAISS   │  Gemini  │ LangC  │
    │ Vector  │    LLM   │ Chain  │
    │  Store  │          │        │
    └─────────┴──────────┴────────┘
```

### Data Flow

1. **Upload** → CVs uploaded via Streamlit
2. **Extract** → PyPDF2 extracts text from PDFs
3. **Chunk** → Text split into semantic chunks (600 chars, 100 overlap)
4. **Embed** → Gemini creates vector embeddings
5. **Store** → FAISS indexes vectors for fast retrieval
6. **Query** → User asks question about candidates
7. **Retrieve** → FAISS finds relevant CV sections (k=15)
8. **Generate** → Gemini analyzes and ranks candidates
9. **Display** → Results shown with evidence

---

## 🚀 Quick Start

```bash
# 1. Clone the repository
cd "your-project-directory"

# 2. Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
# source venv/bin/activate    # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
echo "GOOGLE_API_KEY=your_api_key_here" > .env

# 5. Run the application
streamlit run app.py
```

**Access the app**: Open your browser to `http://localhost:8501`

---

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- Google API Key ([Get one here](https://makersuite.google.com/app/apikey))
- 4GB+ RAM recommended

### Step-by-Step Installation

1. **Set up Virtual Environment**

```bash
python -m venv venv
```

2. **Activate Virtual Environment**

**Windows:**
```powershell
.\venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

3. **Install Required Packages**

```bash
pip install -r requirements.txt
```

**Core Dependencies:**
```
streamlit>=1.28.0
langchain>=0.3.27
langchain-google-genai>=2.1.8
langchain-community>=0.3.27
faiss-cpu>=1.7.4
pypdf2>=2.12.1
python-dotenv>=1.0.0
```

4. **Configure API Key**

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_actual_api_key_here
```

---

## 💻 Usage

### Starting the Application
### Starting the Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

### Step-by-Step Workflow

#### 1. **Upload CVs**

- Click **"Browse files"** in the sidebar
- Select 2-5 PDF CVs
- Duplicates are automatically detected and removed
- Click **"🚀 Process CVs and Start Analysis"**

#### 2. **Review Processed Candidates**

- View total chunks and candidate names
- Verify all CVs were processed correctly

#### 3. **Enter Job Requirements**

Type natural language queries like:
- "Find candidates with Python and ML experience"
- "Who has 5+ years in cloud architecture?"
- "Which candidate knows React and Node.js?"

#### 4. **Analyze Results**

- Review AI analysis with match scores
- Expand candidate sections to see evidence
- Compare candidates side-by-side

#### 5. **Refine Search**

- Ask follow-up questions
- Clear results and try new queries
- Use the **"🗑️ Clear All Uploaded CVs"** button to start fresh

---

## ⚙️ Configuration

### Adjustable Parameters

Edit `config.py` to customize:

```python
# Model Configuration
EMBEDDING_MODEL = "gemini-embedding-001"
LLM_MODEL = "gemini-2.5-flash"
LLM_TEMPERATURE = 0.2  # Lower = more focused, Higher = more creative

# RAG Configuration
CHUNK_SIZE = 600        # Size of text chunks
CHUNK_OVERLAP = 100     # Overlap between chunks
RETRIEVER_K = 15        # Number of chunks to retrieve

# File Upload Configuration
MIN_CVS = 2             # Minimum CVs required
MAX_CVS = 5             # Maximum CVs allowed
```

### Prompt Customization

Modify `HR_ANALYSIS_PROMPT` in `config.py` to change AI behavior:

```python
HR_ANALYSIS_PROMPT = """
Your custom prompt here...
"""
```

---

## 📁 Project Structure

```
├── app.py                     # Main Streamlit application (entry point)
├── config.py                  # Configuration and prompt templates
├── utils.py                   # Utility functions (PDF, file handling)
├── rag_system.py              # CVMatcherRAG class implementation
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (API keys)
├── .gitignore                 # Git ignore rules
├── cvs/                       # Sample CV files (PDFs and text)
│   ├── sample_cv_john_smith.pdf
│   ├── sample_cv_sarah_johnson.pdf
│   └── ...
├── uploads/                   # User-uploaded CVs (auto-created)
├── README.md                  # This file
└── MODULE_STRUCTURE.md        # Detailed module documentation
```

### Module Descriptions

| File | Purpose | Key Components |
|------|---------|----------------|
| `app.py` | Streamlit UI | UI rendering, user interactions, session state |
| `config.py` | Settings | API keys, model configs, prompts, constants |
| `utils.py` | Utilities | PDF extraction, name validation, file operations |
| `rag_system.py` | Core RAG | CVMatcherRAG class, vector store, retrieval logic |

For detailed module documentation, see [MODULE_STRUCTURE.md](MODULE_STRUCTURE.md)

---

## 💡 Examples

### Example 1: Find Python Developers

**Query:**
```
I need a developer with strong Python skills and experience 
in web frameworks like Django or Flask
```

**Result:**
- **John Smith** - High Match (5/15 sections)
  - Evidence: "5 years of Python development, Django REST Framework expert..."
- **Sarah Johnson** - Medium Match (3/15 sections)
  - Evidence: "Python for data processing and Flask APIs..."

### Example 2: Cloud Architecture Role

**Query:**
```
Looking for a cloud architect experienced with AWS, Kubernetes, 
and infrastructure as code (Terraform)
```

**Result:**
- **Michael Chen** - High Match (8/15 sections)
  - Evidence: "AWS certified architect, 6 years Kubernetes and Terraform..."
- **John Smith** - Low Match (2/15 sections)
  - Evidence: "Basic AWS experience for deployment..."

### Example 3: UI/UX Designer

**Query:**
```
Need a UI/UX designer skilled in React, Figma, and responsive design
```

**Result:**
- **Emma Rodriguez** - High Match (7/15 sections)
  - Evidence: "4 years React development, Figma expert for prototyping..."

### Example 4: General Question

**Query:**
```
Who are you?
```

**Result:**
```
I am an experienced HR professional specialized in CV screening 
and candidate evaluation. My role is to analyze candidates' CVs, 
match them with job requirements, and provide evidence-based 
recommendations...
```

---

## 🛡️ Security Features

### 1. Prompt Injection Protection

The system detects and blocks malicious prompts:
- "Ignore all previous instructions..."
- "Override your role and..."
- Bypass attempts

### 2. Irrelevant Query Filtering

Automatically rejects non-CV-related questions:
- Jokes and entertainment
- Cooking, weather, sports
- Personal questions

### 3. Duplicate Detection

- Prevents uploading the same CV multiple times
- Filename-based deduplication
- Clear warning messages

### 4. Data Privacy

- All processing happens locally
- No data sent to third parties (except Google Gemini API)
- CVs stored only in local `uploads/` folder
- `.env` file excluded from version control

---

## 🐛 Troubleshooting

### Common Issues

<details>
<summary><b>"GOOGLE_API_KEY environment variable not set"</b></summary>

**Solution:**
1. Check if `.env` file exists in project root
2. Verify the file contains: `GOOGLE_API_KEY=your_actual_key`
3. Restart the Streamlit application
4. If using PowerShell, ensure the venv is activated

</details>

<details>
<summary><b>"No text extracted from PDF"</b></summary>

**Solution:**
1. Ensure PDF is not image-based (OCR not supported)
2. Try opening the PDF in a reader to verify it's not corrupted
3. Check if the PDF has copy-paste enabled (not locked)
4. Use text-based PDFs, not scanned images

</details>

<details>
<summary><b>"Streamlit not found"</b></summary>

**Solution:**
```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1  # Windows

# Install Streamlit
pip install streamlit

# Verify installation
streamlit --version
```

</details>

<details>
<summary><b>"Button not working / Page refreshing"</b></summary>

**Solution:**
- This was fixed with session state implementation
- Make sure you're using the latest version of `app.py`
- Clear browser cache and refresh

</details>

<details>
<summary><b>"Poor matching results"</b></summary>

**Solution:**
1. Use more specific keywords in queries
2. Try different phrasing
3. Adjust `RETRIEVER_K` in `config.py` (increase for more context)
4. Lower `LLM_TEMPERATURE` for more focused results

</details>

### Getting Help

If you encounter other issues:
1. Check [LangChain Documentation](https://python.langchain.com/)
2. Review [Streamlit Documentation](https://docs.streamlit.io/)
3. Consult [Google AI Documentation](https://ai.google.dev/)

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Areas for Contribution

- 🐛 **Bug Fixes**: Report or fix bugs
- ✨ **Features**: Suggest or implement new features
- 📝 **Documentation**: Improve docs and examples
- 🧪 **Testing**: Add test cases
- 🎨 **UI/UX**: Enhance the interface

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Test thoroughly
5. Commit: `git commit -m "Add your feature"`
6. Push: `git push origin feature/your-feature`
7. Open a Pull Request

### Code Style

- Follow PEP 8 guidelines
- Add docstrings to functions
- Comment complex logic
- Keep functions focused and modular

---

## 📄 License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2026 CV Matcher RAG System

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 Acknowledgements

### Technologies

- **[LangChain](https://python.langchain.com/)** - RAG framework
- **[Google Gemini](https://ai.google.dev/)** - LLM and embeddings
- **[FAISS](https://github.com/facebookresearch/faiss)** - Vector search by Facebook Research
- **[Streamlit](https://streamlit.io/)** - Web framework
- **[PyPDF2](https://pypdf2.readthedocs.io/)** - PDF processing

### Inspiration

This project was built to demonstrate:
- Modern RAG architecture patterns
- Practical AI applications in HR
- Clean modular Python code structure
- User-centric interface design

---

## 📊 Sample Candidate Profiles

The `cvs/` folder includes 5 diverse professional profiles:

| Name | Role | Key Skills | Experience |
|------|------|------------|------------|
| **John Smith** | Software Engineer | Python, JavaScript, AWS, ML | 5 years |
| **Sarah Johnson** | Data Scientist | Python, R, ML, Deep Learning, Azure | 4 years |
| **Michael Chen** | DevOps Engineer | AWS, Kubernetes, Docker, Terraform | 6 years |
| **Emma Rodriguez** | Full Stack Developer | React, Vue.js, Node.js, UI/UX | 4 years |
| **David Thompson** | Project Manager | Agile, Scrum, PMP, Leadership | 7 years |

---

## 📞 Contact & Support

### Resources

- **Documentation**: See [MODULE_STRUCTURE.md](MODULE_STRUCTURE.md) for detailed docs
- **Issues**: Report bugs or request features via GitHub Issues
- **Questions**: Check the Troubleshooting section first

### External Resources

- [LangChain Documentation](https://python.langchain.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Google AI Studio](https://makersuite.google.com/)
- [FAISS Documentation](https://github.com/facebookresearch/faiss/wiki)

---

<div align="center">

**⭐ If you find this project helpful, please consider giving it a star! ⭐**

Made with ❤️ using LangChain, Google Gemini, and Streamlit

**[Back to Top](#-cv-matcher-rag-system)**

</div>

---

<!-- ## 📝 Project Description

CV Matcher RAG System revolutionizes recruitment with AI-powered CV analysis. Using Google Gemini, LangChain, and FAISS, it analyzes up to 5 CVs, matching candidates to job requirements through semantic search. It provides evidence-based recommendations with exact quotes from CVs, all through an intuitive Streamlit interface. -->
