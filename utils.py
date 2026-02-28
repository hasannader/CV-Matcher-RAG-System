"""
Utility functions for CV Matcher RAG System.
Includes PDF extraction, name validation, and file handling.
"""
import os
import re
import PyPDF2
from typing import Optional
from config import (
    CV_SECTION_HEADERS, CV_RELATED_WORDS, 
    MIN_NAME_WORD_LENGTH, MAX_NAME_WORD_LENGTH, MAX_NAME_WORDS,
    UPLOADS_DIR
)

# Keywords and patterns for irrelevant questions
IRRELEVANT_KEYWORDS = [
    'joke', 'funny', 'laugh', 'humor', 'humour',
    'cook', 'recipe', 'food', 'dish', 'meal', 'restaurant',
    'weather', 'temperature', 'forecast',
    'movie', 'film', 'show', 'series', 'netflix',
    'game', 'gaming', 'play',
    'song', 'music', 'singer', 'band',
    'sport', 'football', 'basketball', 'soccer',
    'love', 'dating', 'relationship', 'marry',
    'story', 'tale', 'narrative',
    'riddle', 'puzzle',
    'poem', 'poetry',
    'color', 'colour', 'favorite', 'favourite',
    'animal', 'pet', 'dog', 'cat',
]

PROMPT_INJECTION_PATTERNS = [
    r'ignore\s+(all\s+)?(previous|prior|above)',
    r'disregard\s+(all\s+)?(previous|prior|instructions)',
    r'forget\s+(all\s+)?(previous|prior|instructions)',
    r'new\s+instructions?',
    r'system\s+(prompt|message|instruction)',
    r'act\s+as\s+(if|a|an)',
    r'pretend\s+(to\s+be|you\s+are)',
    r'you\s+are\s+now',
    r'from\s+now\s+on',
    r'override',
    r'bypass',
]


def is_question_irrelevant(question: str) -> bool:
    """
    Check if a question is irrelevant to CV analysis and job matching.
    Detects jokes, unrelated topics, and prompt injection attempts.
    
    Args:
        question: User's question text
        
    Returns:
        True if question is irrelevant, False if it might be relevant
    """
    if not question or len(question.strip()) < 3:
        return True
    
    question_lower = question.lower()
    
    # Check for prompt injection attempts
    for pattern in PROMPT_INJECTION_PATTERNS:
        if re.search(pattern, question_lower):
            return True
    
    # Check for irrelevant keywords
    for keyword in IRRELEVANT_KEYWORDS:
        if keyword in question_lower:
            return True
    
    # Check if question contains CV/job-related terms (allowlist approach)
    cv_related_terms = [
        'candidate', 'cv', 'resume', 'skill', 'experience', 'qualification',
        'job', 'position', 'role', 'work', 'project', 'education',
        'degree', 'certification', 'training', 'language', 'technical',
        'programming', 'developer', 'engineer', 'manager', 'analyst',
        'design', 'development', 'team', 'leadership', 'professional',
        'employment', 'background', 'expertise', 'knowledge', 'proficient',
        'years', 'senior', 'junior', 'expert', 'familiar'
    ]
    
    # If question is very short and doesn't contain CV-related terms, likely irrelevant
    if len(question.split()) <= 5:
        has_cv_term = any(term in question_lower for term in cv_related_terms)
        if not has_cv_term:
            # Check if it's a general HR-related question (like "who are you")
            general_questions = ['who are you', 'what do you do', 'what is your', 'how can you help']
            is_general = any(gq in question_lower for gq in general_questions)
            if not is_general:
                return True
    
    return False


def extract_pdf_text(file_path: str) -> str:
    """
    Extract text from a PDF file.
    
    Args:
        file_path: Path to the PDF file
        
    Returns:
        Extracted text from all pages
        
    Raises:
        FileNotFoundError: If PDF file doesn't exist
        Exception: If there's an error extracting text
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"PDF file not found: {file_path}")
    
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
    except Exception as e:
        raise Exception(f"Error extracting text from {os.path.basename(file_path)}: {str(e)}")


def is_valid_name(text: str) -> bool:
    """
    Validate if the extracted text is likely a person's name and not a section header.
    
    Args:
        text: Text to validate
        
    Returns:
        True if it appears to be a valid name, False otherwise
    """
    # Check if text matches common section headers (case-insensitive)
    text_lower = text.lower().strip()
    if text_lower in CV_SECTION_HEADERS:
        return False
    
    # Check if any section header is contained in the text
    if any(header in text_lower for header in CV_SECTION_HEADERS):
        return False
    
    # Names shouldn't be all uppercase (usually section headers are)
    if text.isupper() and len(text.split()) > 2:
        return False
    
    # Names should have reasonable length (not too long)
    words = text.split()
    if len(words) > MAX_NAME_WORDS:
        return False
    
    # Each word should be a reasonable length for a name
    if not all(MIN_NAME_WORD_LENGTH <= len(word) <= MAX_NAME_WORD_LENGTH for word in words):
        return False
    
    return True


def extract_candidate_name(text: str, file_name: str) -> str:
    """
    Try to extract the candidate name from the CV text.
    Returns only the first two names.
    Falls back to the file name if extraction fails.
    
    Args:
        text: CV text content
        file_name: Original filename
        
    Returns:
        Extracted candidate name (first two words)
    """
    # Try to find name patterns in the first 500 characters
    lines = text[:500].split('\n')
    for line in lines[:5]:  # Check first 5 lines
        line = line.strip()
        # Look for lines that might be names (2-4 words, capitalized, no special chars)
        if line and len(line.split()) >= 2 and len(line.split()) <= 4:
            if all(word[0].isupper() if word else False for word in line.split()):
                if not any(char in line for char in ['@', ':', '|', '•', '/']):
                    # Validate it's actually a name and not a section header
                    if is_valid_name(line):
                        # Return only first two names
                        words = line.split()
                        return ' '.join(words[:2])
    
    # Fallback to filename without extension
    fallback_name = os.path.splitext(file_name)[0].replace('_', ' ').replace('-', ' ')
    
    # Remove common CV-related words (case-insensitive)
    words = fallback_name.split()
    
    # Filter out CV-related words
    filtered_words = [word for word in words if word.lower() not in CV_RELATED_WORDS]
    
    # If no words left after filtering, use original words
    if not filtered_words:
        filtered_words = words
    
    # Take first two words and capitalize properly
    name_words = filtered_words[:2]
    candidate_name = ' '.join(word.capitalize() for word in name_words)
    
    return candidate_name if candidate_name else fallback_name.title()


def save_uploaded_file(uploaded_file, uploads_dir: Optional[str] = None) -> str:
    """
    Save an uploaded file and return its path.
    
    Args:
        uploaded_file: Streamlit uploaded file object
        uploads_dir: Directory to save uploads (defaults to UPLOADS_DIR from config)
        
    Returns:
        Path to the saved file
        
    Raises:
        FileNotFoundError: If file creation fails
        Exception: For other file saving errors
    """
    # Use configured uploads directory if not specified
    if uploads_dir is None:
        uploads_dir = os.path.join(os.getcwd(), UPLOADS_DIR)
    
    # Create uploads directory if it doesn't exist
    os.makedirs(uploads_dir, exist_ok=True)
    
    # Sanitize filename to remove problematic characters
    safe_filename = "".join(c for c in uploaded_file.name if c.isalnum() or c in (' ', '.', '_', '-'))
    safe_filename = safe_filename.replace(' ', '_')
    file_path = os.path.join(uploads_dir, safe_filename)
    
    try:
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Verify the file was created
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Failed to create file: {file_path}")
            
        return file_path
    except Exception as e:
        raise Exception(f"Error saving file {uploaded_file.name}: {str(e)}")


def check_file_exists(uploaded_file, uploads_dir: Optional[str] = None) -> tuple[bool, str]:
    """
    Check if an uploaded file already exists in the uploads directory.
    
    Args:
        uploaded_file: Streamlit uploaded file object
        uploads_dir: Directory to check (defaults to UPLOADS_DIR from config)
        
    Returns:
        Tuple of (exists: bool, file_path: str)
    """
    # Use configured uploads directory if not specified
    if uploads_dir is None:
        uploads_dir = os.path.join(os.getcwd(), UPLOADS_DIR)
    
    # Sanitize filename (same logic as save_uploaded_file)
    safe_filename = "".join(c for c in uploaded_file.name if c.isalnum() or c in (' ', '.', '_', '-'))
    safe_filename = safe_filename.replace(' ', '_')
    file_path = os.path.join(uploads_dir, safe_filename)
    
    return os.path.exists(file_path), file_path


def format_docs(docs) -> str:
    """
    Format documents for context in the RAG chain.
    
    Args:
        docs: List of document objects
        
    Returns:
        Formatted string of document contents
    """
    return "\n\n".join(doc.page_content for doc in docs)


def clear_uploads(uploads_dir: Optional[str] = None) -> int:
    """
    Clear all files from the uploads directory.
    
    Args:
        uploads_dir: Directory containing uploads (defaults to UPLOADS_DIR from config)
        
    Returns:
        Number of files deleted
        
    Raises:
        Exception: If there's an error deleting files
    """
    # Use configured uploads directory if not specified
    if uploads_dir is None:
        uploads_dir = os.path.join(os.getcwd(), UPLOADS_DIR)
    
    # Check if directory exists
    if not os.path.exists(uploads_dir):
        return 0
    
    deleted_count = 0
    
    try:
        # Get all files in the directory
        files = [f for f in os.listdir(uploads_dir) if os.path.isfile(os.path.join(uploads_dir, f))]
        
        # Delete each file
        for filename in files:
            file_path = os.path.join(uploads_dir, filename)
            try:
                os.remove(file_path)
                deleted_count += 1
            except Exception as e:
                print(f"Warning: Could not delete {filename}: {str(e)}")
        
        return deleted_count
    except Exception as e:
        raise Exception(f"Error clearing uploads directory: {str(e)}")

