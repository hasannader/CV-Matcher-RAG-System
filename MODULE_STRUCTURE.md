# CV Matcher RAG System - Modular Architecture

## 📁 Project Structure

The codebase has been refactored into a modular architecture for better maintainability and scalability:

```
session 7/
├── app.py                      # Main Streamlit application (entry point)
├── config.py                   # Configuration, constants, and prompt templates
├── utils.py                    # Utility functions (PDF, name extraction, file handling)
├── rag_system.py               # CVMatcherRAG class implementation
├── cv_matcher_rag.py          # Original monolithic version (kept for reference)
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (API keys)
├── .gitignore                  # Git ignore rules
├── cvs/                        # Sample CV files (PDFs and text)
├── uploads/                    # Directory for uploaded CVs
└── README.md                   # This file
```

## 🏗️ Module Details

### 1. `app.py` - Main Application
**Purpose**: Streamlit web interface and user interactions

**Key Functions**:
- `setup_page()` - Configure Streamlit page
- `render_header()` - Display application header
- `render_sidebar()` - File uploader and examples
- `validate_uploads()` - Validate uploaded files
- `process_cvs()` - Process and save CVs
- `display_results()` - Show analysis results
- `main()` - Application entry point

**Usage**:
```bash
streamlit run app.py
```

### 2. `config.py` - Configuration & Prompts
**Purpose**: Central configuration management and prompt templates

**Contains**:
- API keys and environment setup
- Model configurations (Gemini models, temperature)
- RAG settings (chunk size, overlap, retriever k)
- File upload constraints (min/max CVs, file types)
- CV section headers for name validation
- Streamlit page configuration
- **LLM prompt templates** (HR_ANALYSIS_PROMPT)
- **Response markers** (GENERAL_QUESTION_MARKER, CV_ANALYSIS_MARKER)

**Key Variables**:
```python
GOOGLE_API_KEY = "your-api-key"
EMBEDDING_MODEL = "gemini-embedding-001"
LLM_MODEL = "gemini-2.5-flash"
CHUNK_SIZE = 600
MIN_CVS = 2
MAX_CVS = 5
HR_ANALYSIS_PROMPT = "..."  # Full HR analysis prompt with question classification
```

### 3. `utils.py` - Utility Functions
**Purpose**: Reusable helper functions

**Functions**:
- `extract_pdf_text(file_path)` - Extract text from PDF
- `is_valid_name(text)` - Validate if text is a name
- `extract_candidate_name(text, file_name)` - Extract candidate name
- `save_uploaded_file(uploaded_file)` - Save uploaded files
- `format_docs(docs)` - Format documents for RAG chain

**Example**:
```python
from utils import extract_pdf_text, extract_candidate_name

text = extract_pdf_text("resume.pdf")
name = extract_candidate_name(text, "resume.pdf")
```

### 4. `rag_system.py` - RAG Implementation
**Purpose**: Core RAG system logic

**Class**: `CVMatcherRAG`

**Methods**:
- `__init__(file_paths, chunk_size, overlap)` - Initialize RAG system
- `get_total_chunks()` - Return number of chunks
- `get_candidates()` - Return candidate names
- `find_matching_candidates(job_requirements)` - Find matching candidates

**Example**:
```python
from rag_system import CVMatcherRAG

rag = CVMatcherRAG(["cv1.pdf", "cv2.pdf"])
results = rag.find_matching_candidates("Python developer with ML experience")
```

## 🚀 Running the Application

### Option 1: Run the Modular Version (Recommended)
```bash
streamlit run app.py
```

### Option 2: Run the Original Monolithic Version
```bash
streamlit run cv_matcher_rag.py
```

Both versions have the same functionality. The modular version is better for:
- **Maintenance**: Easy to update specific components
- **Testing**: Each module can be tested independently
- **Scalability**: Can add new features without cluttering code
- **Reusability**: Functions can be imported in other projects

## 📦 Installation

1. **Activate virtual environment**:
   ```bash
   .\venv\Scripts\Activate.ps1
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   - Ensure `.env` file exists with your `GOOGLE_API_KEY`

4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

## 🎯 Benefits of Modular Architecture

### 1. **Separation of Concerns**
- Configuration separate from logic
- UI separate from business logic
- Utilities separate from core functionality

### 2. **Easier Testing**
```python
# Test utilities independently
from utils import is_valid_name
assert is_valid_name("John Smith") == True
assert is_valid_name("PROFESSIONAL SUMMARY") == False
```

### 3. **Better Maintainability**
- Update prompts without touching RAG logic
- Modify UI without affecting processing
- Change configuration without code changes

### 4. **Reusability**
```python
# Import RAG system in other projects
from rag_system import CVMatcherRAG
from utils import extract_pdf_text
```

### 5. **Cleaner Code**
- Each file has a single responsibility
- Functions are focused and testable
- Easier to understand and navigate

## 🔧 Customization

### Change Model Settings
Edit `config.py`:
```python
LLM_MODEL = "gemini-pro"  # Change model
LLM_TEMPERATURE = 0.5      # Adjust creativity
CHUNK_SIZE = 800           # Larger chunks
```

### Modify Prompts
Edit `config.py`:
```python
HR_ANALYSIS_PROMPT = """Your custom prompt here..."""
```

### Add New Utilities
Add to `utils.py`:
```python
def new_utility_function():
    """Your new utility"""
    pass
```

### Extend RAG Functionality
Add methods to `CVMatcherRAG` class in `rag_system.py`:
```python
class CVMatcherRAG:
    def new_analysis_method(self):
        """New analysis feature"""
        pass
```

## 📚 Import Examples

### From Another Script
```python
# Import configuration
from config import GOOGLE_API_KEY, CHUNK_SIZE

# Import utilities
from utils import extract_pdf_text, save_uploaded_file

# Import RAG system
from rag_system import CVMatcherRAG

# Create RAG instance
rag = CVMatcherRAG(["resume1.pdf", "resume2.pdf"])
```

### Run as Module
```python
# In a Jupyter notebook or Python script
import sys
sys.path.append("path/to/session 7")

from rag_system import CVMatcherRAG
from utils import extract_candidate_name
```

## 🧪 Testing

You can now test individual components:

```python
# Test name extraction
from utils import extract_candidate_name, is_valid_name

assert is_valid_name("Jane Doe") == True
assert is_valid_name("WORK EXPERIENCE") == False

# Test with sample data
name = extract_candidate_name("JOHN SMITH\nSoftware Engineer...", "test.pdf")
print(name)  # Should print "John Smith"
```

## 🔄 Migration Path

If you prefer the original single-file version:
- `cv_matcher_rag.py` is kept for backward compatibility
- Both versions are functionally identical
- New features will be added to the modular version

## 📝 Future Enhancements

The modular structure makes it easy to add:
- Automated testing suite
- API endpoints (FastAPI)
- Database integration
- Caching layer
- Logging system
- Multiple language support

## 🤝 Contributing

When adding new features:
1. Identify the appropriate module
2. Add new functions/classes to that module
3. Update imports in dependent modules
4. Document your changes

---

**Built with ❤️ using LangChain, Google Gemini, and Streamlit**
