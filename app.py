"""
Streamlit application for CV Matcher RAG System.
Main entry point for the web interface.
"""
import os
import streamlit as st

from config import (
    PAGE_TITLE, PAGE_ICON, LAYOUT, MIN_CVS, MAX_CVS, UPLOADS_DIR,
    GENERAL_QUESTION_MARKER, CV_ANALYSIS_MARKER
)
from utils import save_uploaded_file, clear_uploads, is_question_irrelevant, check_file_exists
from rag_system import CVMatcherRAG


def setup_page():
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon=PAGE_ICON,
        layout=LAYOUT
    )


def render_header():
    """Render the application header."""
    st.title("🎯 CV Matcher - RAG System")
    st.markdown("""
    ### Find the Best Candidates for Your Job Requirements
    Upload up to 5 CVs and ask questions about specific skills, experience, or qualifications.
    The system will identify the best matching candidates with evidence from their CVs.
    """)


def render_sidebar():
    """
    Render the sidebar with file uploader and example questions.
    
    Returns:
        uploaded_files: List of uploaded files
    """
    with st.sidebar:
        st.header("📂 Upload CVs")
        uploaded_files = st.file_uploader(
            "Upload CVs (PDF format)",
            type="pdf",
            accept_multiple_files=True,
            help=f"Upload {MIN_CVS}-{MAX_CVS} CVs in PDF format"
        )
        
        # Clear uploads button
        if st.button("🗑️ Clear All Uploaded CVs", type="secondary", use_container_width=True):
            try:
                deleted_count = clear_uploads()
                # Reset session state
                st.session_state.rag = None
                st.session_state.processed = False
                if deleted_count > 0:
                    st.success(f"✅ Successfully cleared {deleted_count} file(s) from uploads folder")
                    st.rerun()
                else:
                    st.info("ℹ️ No files to clear in uploads folder")
            except Exception as e:
                st.error(f"❌ Error clearing uploads: {str(e)}")
        
        st.markdown("---")
        st.markdown("#### Example Questions:")
        st.markdown("""
        **Job/Skill Related:**
        - Who has experience with Python?
        - Find candidates skilled in machine learning
        - Who has worked with cloud technologies?
        - Which candidate has project management experience?
        - Who knows React and frontend development?
        
        **General Questions:**
        - Who are you?
        - What do you do?
        - How can you help me?
        """)
    
    return uploaded_files


def remove_duplicate_uploads(uploaded_files):
    """
    Remove duplicate files from uploaded files list based on sanitized filename.
    
    Args:
        uploaded_files: List of uploaded files
        
    Returns:
        List of unique uploaded files (keeps first occurrence)
    """
    if not uploaded_files:
        return uploaded_files
    
    seen_filenames = set()
    unique_files = []
    duplicate_names = []
    
    for file in uploaded_files:
        # Sanitize filename (same logic as in utils.py)
        safe_filename = "".join(c for c in file.name if c.isalnum() or c in (' ', '.', '_', '-'))
        safe_filename = safe_filename.replace(' ', '_')
        
        if safe_filename not in seen_filenames:
            seen_filenames.add(safe_filename)
            unique_files.append(file)
        else:
            duplicate_names.append(file.name)
    
    # Show warning if duplicates were detected
    if duplicate_names:
        st.warning(f"⚠️ Removed {len(duplicate_names)} duplicate file(s): {', '.join(duplicate_names)}")
    
    return unique_files


def validate_uploads(uploaded_files):
    """
    Validate the number of uploaded files.
    
    Args:
        uploaded_files: List of uploaded files
        
    Returns:
        True if valid, False otherwise (displays appropriate message)
    """
    if not uploaded_files:
        st.info(f"👈 Please upload {MIN_CVS}-{MAX_CVS} CVs to get started")
        return False
    
    if len(uploaded_files) < MIN_CVS or len(uploaded_files) > MAX_CVS:
        st.warning(f"⚠️ Please upload {MIN_CVS}-{MAX_CVS} CVs. You uploaded {len(uploaded_files)} file(s).")
        return False
    
    return True


def show_uploaded_files(uploaded_files):
    """
    Display the list of uploaded files.
    
    Args:
        uploaded_files: List of uploaded files
    """
    st.success(f"✅ {len(uploaded_files)} CV(s) uploaded successfully!")
    with st.expander("📝 View uploaded files"):
        for i, file in enumerate(uploaded_files, 1):
            st.write(f"{i}. {file.name}")


def process_cvs(uploaded_files):
    """
    Process uploaded CVs and create RAG instance.
    
    Args:
        uploaded_files: List of uploaded files
        
    Returns:
        CVMatcherRAG instance or None if processing fails
    """
    saved_file_paths = []
    skipped_files = []
    new_files = []
    
    try:
        # Check for existing files and save new ones
        for uploaded_file in uploaded_files:
            try:
                # Check if file already exists
                exists, file_path = check_file_exists(uploaded_file)
                
                if exists:
                    # File already exists, skip uploading but include in processing
                    skipped_files.append(uploaded_file.name)
                    saved_file_paths.append(file_path)
                else:
                    # Save new file
                    saved_path = save_uploaded_file(uploaded_file)
                    saved_file_paths.append(saved_path)
                    new_files.append(uploaded_file.name)
            except Exception as e:
                st.error(f"Failed to process {uploaded_file.name}: {str(e)}")
                return None
        
        # Show upload status
        if new_files:
            st.success(f"✅ Uploaded {len(new_files)} new file(s): {', '.join(new_files)}")
        if skipped_files:
            st.info(f"ℹ️ Skipped {len(skipped_files)} existing file(s): {', '.join(skipped_files)}")
        
        # Create RAG instance
        rag = CVMatcherRAG(saved_file_paths)
        return rag
        
    except Exception as e:
        st.error(f"An error occurred while processing CVs: {str(e)}")
        return None


def display_cv_info(rag):
    """
    Display information about processed CVs.
    
    Args:
        rag: CVMatcherRAG instance
    """
    st.success("✅ CVs processed successfully!")
    st.info(f"📁 Saved {len(rag.get_candidates())} CV(s) in: {os.path.join(os.getcwd(), UPLOADS_DIR)}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Chunks", rag.get_total_chunks())
    with col2:
        st.metric("Candidates", len(rag.get_candidates()))
    
    # Display candidate names
    st.markdown("### 👥 Candidates:")
    for i, name in enumerate(rag.get_candidates(), 1):
        st.write(f"{i}. **{name}**")


def handle_query(rag):
    """
    Handle user query and display results.
    
    Args:
        rag: CVMatcherRAG instance
    """
    st.markdown("---")
    st.markdown("### 💬 Ask a Question")
    
    job_query = st.text_area(
        "Enter job requirements, skills, or ask any question:",
        placeholder="Example: I'm looking for a candidate with 3+ years of Python experience, knowledge of machine learning, and experience with cloud platforms like AWS or Azure.\n\nYou can also ask general questions like 'Who are you?' or 'What do you do?'",
        height=100
    )
    
    if st.button("🔍 Analyze & Find Answer", type="primary"):
        if not job_query:
            st.warning("Please enter a job requirement or question.")
        else:
            # Check if question is irrelevant before processing
            if is_question_irrelevant(job_query):
                st.markdown("### 📊 Analysis")
                st.warning("⚠️ No relevant CVs found. This question appears to be unrelated to candidate evaluation or job requirements. Please ask about candidate skills, experience, qualifications, or job-related topics.")
                return
            
            with st.spinner("Analyzing CVs..."):
                results = rag.find_matching_candidates(job_query)
                display_results(results)


def display_results(results):
    """
    Display analysis results.
    
    Args:
        results: Dictionary containing analysis results
    """
    # Check if this is a general question or CV analysis
    analysis_text = results['analysis']
    is_general_question = GENERAL_QUESTION_MARKER in analysis_text
    
    # Clean up the markers from the displayed text
    analysis_text = analysis_text.replace(GENERAL_QUESTION_MARKER, '').replace(CV_ANALYSIS_MARKER, '').strip()
    
    # Display AI Analysis
    st.markdown("### 📊 Analysis")
    st.markdown(analysis_text)
    
    # Only show detailed evidence for relevant CV analysis questions
    if not is_general_question and results['ranked_candidates']:
        display_evidence(results)


def display_evidence(results):
    """
    Display detailed evidence for each candidate.
    
    Args:
        results: Dictionary containing candidate evidence
    """
    st.markdown("---")
    st.markdown("### 📋 Detailed Evidence")
    
    for candidate, count in results['ranked_candidates']:
        with st.expander(f"**{candidate}** - {count} relevant sections found", expanded=True):
            evidence = results['candidate_evidence'][candidate]
            
            st.markdown(f"**Relevance Score:** {count} matching sections")
            st.markdown("**Evidence from CV:**")
            
            # Show top 3 chunks
            for i, chunk in enumerate(evidence[:3], 1):
                with st.container():
                    st.markdown(f"**Section {i}:**")
                    st.info(chunk)
            
            if len(evidence) > 3:
                st.caption(f"... and {len(evidence) - 3} more relevant sections")


def main():
    """Main application function."""
    setup_page()
    render_header()
    
    # Initialize session state for RAG instance
    if 'rag' not in st.session_state:
        st.session_state.rag = None
    if 'processed' not in st.session_state:
        st.session_state.processed = False
    
    # Sidebar with file upload
    uploaded_files = render_sidebar()
    
    # Remove duplicate files from upload list
    uploaded_files = remove_duplicate_uploads(uploaded_files)
    
    # Validate uploads
    if not validate_uploads(uploaded_files):
        st.session_state.rag = None
        st.session_state.processed = False
        return
    
    # Show uploaded files
    show_uploaded_files(uploaded_files)
    
    # Add button to start processing
    st.markdown("---")
    process_button = st.button("🚀 Process CVs and Start Analysis", type="primary", use_container_width=True)
    
    # Process CVs when button is clicked
    if process_button:
        with st.spinner("Processing CVs..."):
            rag = process_cvs(uploaded_files)
            
            if rag is None:
                st.session_state.rag = None
                st.session_state.processed = False
                return
            
            # Store RAG in session state
            st.session_state.rag = rag
            st.session_state.processed = True
    
    # Display CV info and handle queries if already processed
    if st.session_state.processed and st.session_state.rag is not None:
        # Display CV information
        display_cv_info(st.session_state.rag)
        
        # Handle queries
        handle_query(st.session_state.rag)
    elif not process_button:
        st.info("👆 Click the button above to process the uploaded CVs")


if __name__ == '__main__':
    main()
