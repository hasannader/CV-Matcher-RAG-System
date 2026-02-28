"""
RAG System implementation for CV Matcher.
Contains the main CVMatcherRAG class.
"""
import os
from typing import List, Dict
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from config import (
    GOOGLE_API_KEY, EMBEDDING_MODEL, LLM_MODEL, LLM_TEMPERATURE,
    CHUNK_SIZE, CHUNK_OVERLAP, RETRIEVER_K, HR_ANALYSIS_PROMPT
)
from utils import extract_pdf_text, extract_candidate_name, format_docs


class CVMatcherRAG:
    """
    RAG system for matching candidates to job requirements based on their CVs.
    """
    
    def __init__(self, file_paths: List[str], chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP):
        """
        Initialize the CV Matcher RAG system.
        
        Args:
            file_paths: List of paths to CV PDF files
            chunk_size: Size of text chunks for embedding
            overlap: Overlap between chunks
        """
        self.cv_files = file_paths
        self.candidate_names = []
        self.docs = []
        
        # Process each CV separately to maintain candidate identity
        for file_path in file_paths:
            text = extract_pdf_text(file_path)
            candidate_name = extract_candidate_name(text, os.path.basename(file_path))
            self.candidate_names.append(candidate_name)
            
            # Split the text into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=overlap
            )
            docs = text_splitter.create_documents([text])
            
            # Add metadata to each chunk
            for doc in docs:
                doc.metadata = {
                    "source": file_path,
                    "candidate_name": candidate_name
                }
            
            self.docs.extend(docs)
        
        # Create embeddings and vector store
        embeddings = GoogleGenerativeAIEmbeddings(
            model=EMBEDDING_MODEL,
            google_api_key=GOOGLE_API_KEY
        )
        
        vector_store = FAISS.from_documents(self.docs, embeddings)
        self.retriever = vector_store.as_retriever(
            search_kwargs={"k": RETRIEVER_K}
        )
        
        # Initialize the LLM
        self.llm = ChatGoogleGenerativeAI(
            model=LLM_MODEL,
            google_api_key=GOOGLE_API_KEY,
            temperature=LLM_TEMPERATURE
        )
        
        # Create prompt and chain
        prompt = ChatPromptTemplate.from_template(HR_ANALYSIS_PROMPT)
        
        # Create the RAG chain
        self.chain = (
            {"context": self.retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )
    
    def get_total_chunks(self) -> int:
        """
        Return the total number of chunks in the vector database.
        
        Returns:
            Number of document chunks
        """
        return len(self.docs)
    
    def get_candidates(self) -> List[str]:
        """
        Return the list of candidate names.
        
        Returns:
            List of candidate names
        """
        return self.candidate_names
    
    def find_matching_candidates(self, job_requirements: str) -> Dict:
        """
        Find candidates that match the job requirements.
        
        Args:
            job_requirements: Description of job requirements, skills, or question
            
        Returns:
            Dictionary containing:
                - analysis: AI-generated analysis
                - candidate_evidence: Evidence by candidate
                - ranked_candidates: Candidates ranked by relevance
                - all_candidates: All candidate names
        """
        # Get the AI analysis
        analysis = self.chain.invoke(job_requirements)
        
        # Retrieve relevant chunks to provide additional evidence
        relevant_docs = self.retriever.invoke(job_requirements)
        
        # Group evidence by candidate
        candidate_evidence = {}
        candidate_chunk_count = {}
        
        for doc in relevant_docs:
            candidate = doc.metadata.get('candidate_name', 'Unknown')
            
            if candidate not in candidate_evidence:
                candidate_evidence[candidate] = []
                candidate_chunk_count[candidate] = 0
            
            candidate_evidence[candidate].append(doc.page_content)
            candidate_chunk_count[candidate] += 1
        
        # Rank candidates by number of relevant chunks (simple relevance metric)
        ranked_candidates = sorted(
            candidate_chunk_count.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return {
            'analysis': analysis,
            'candidate_evidence': candidate_evidence,
            'ranked_candidates': ranked_candidates,
            'all_candidates': self.candidate_names
        }
