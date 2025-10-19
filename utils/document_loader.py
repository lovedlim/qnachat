"""
PDF 문서 로딩 및 벡터 데이터베이스 구축 모듈
"""
import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
import pickle


class DocumentProcessor:
    """PDF 문서를 처리하고 벡터 데이터베이스를 구축하는 클래스"""
    
    def __init__(self, data_folder: str = "data", persist_directory: str = "faiss_index"):
        """
        Args:
            data_folder: PDF 파일들이 저장된 폴더 경로
            persist_directory: 벡터 데이터베이스 저장 경로
        """
        self.data_folder = data_folder
        self.persist_directory = persist_directory
        self.embeddings = None
        self.vectorstore = None
        
    def load_documents(self) -> List[Document]:
        """
        data 폴더에서 모든 PDF 문서를 로드합니다.
        
        Returns:
            로드된 문서 리스트
        """
        if not os.path.exists(self.data_folder):
            raise FileNotFoundError(f"'{self.data_folder}' 폴더를 찾을 수 없습니다.")
        
        # PDF 파일이 있는지 확인
        pdf_files = [f for f in os.listdir(self.data_folder) if f.endswith('.pdf')]
        if not pdf_files:
            raise FileNotFoundError(f"'{self.data_folder}' 폴더에 PDF 파일이 없습니다.")
        
        # DirectoryLoader를 사용하여 모든 PDF 로드
        loader = DirectoryLoader(
            self.data_folder,
            glob="**/*.pdf",
            loader_cls=PyPDFLoader,
            show_progress=True
        )
        
        documents = loader.load()
        print(f"[OK] {len(documents)}개의 페이지를 로드했습니다.")
        return documents
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        문서를 작은 청크로 분할합니다.
        
        Args:
            documents: 원본 문서 리스트
            
        Returns:
            분할된 문서 청크 리스트
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        chunks = text_splitter.split_documents(documents)
        print(f"[OK] {len(chunks)}개의 청크로 분할했습니다.")
        return chunks
    
    def create_vectorstore(self, chunks: List[Document], openai_api_key: str):
        """
        문서 청크로부터 벡터 데이터베이스를 생성합니다.
        
        Args:
            chunks: 분할된 문서 청크
            openai_api_key: OpenAI API 키
        """
        self.embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        
        # FAISS 벡터스토어 생성
        self.vectorstore = FAISS.from_documents(
            documents=chunks,
            embedding=self.embeddings
        )
        
        # 디스크에 저장
        if not os.path.exists(self.persist_directory):
            os.makedirs(self.persist_directory)
        
        self.vectorstore.save_local(self.persist_directory)
        print(f"[OK] 벡터 데이터베이스를 '{self.persist_directory}'에 저장했습니다.")
    
    def load_vectorstore(self, openai_api_key: str):
        """
        저장된 벡터 데이터베이스를 로드합니다.
        
        Args:
            openai_api_key: OpenAI API 키
        """
        self.embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        
        self.vectorstore = FAISS.load_local(
            self.persist_directory,
            self.embeddings,
            allow_dangerous_deserialization=True
        )
        print(f"[OK] 벡터 데이터베이스를 '{self.persist_directory}'에서 로드했습니다.")
    
    def process_documents(self, openai_api_key: str, force_reload: bool = False):
        """
        전체 문서 처리 파이프라인을 실행합니다.
        
        Args:
            openai_api_key: OpenAI API 키
            force_reload: True일 경우 기존 벡터 DB를 무시하고 새로 생성
        """
        # 이미 벡터스토어가 있고 force_reload가 False면 기존 것 사용
        if not force_reload and os.path.exists(self.persist_directory):
            print("기존 벡터 데이터베이스를 사용합니다.")
            self.load_vectorstore(openai_api_key)
            return
        
        print("새로운 벡터 데이터베이스를 생성합니다...")
        
        # 문서 로드
        documents = self.load_documents()
        
        # 문서 분할
        chunks = self.split_documents(documents)
        
        # 벡터 데이터베이스 생성
        self.create_vectorstore(chunks, openai_api_key)
    
    def get_retriever(self, search_kwargs: dict = None):
        """
        벡터스토어에서 retriever를 가져옵니다.
        
        Args:
            search_kwargs: 검색 파라미터 (예: {"k": 4})
            
        Returns:
            Retriever 객체
        """
        if self.vectorstore is None:
            raise ValueError("벡터스토어가 초기화되지 않았습니다. process_documents()를 먼저 실행하세요.")
        
        if search_kwargs is None:
            search_kwargs = {"k": 4}
        
        return self.vectorstore.as_retriever(search_kwargs=search_kwargs)

