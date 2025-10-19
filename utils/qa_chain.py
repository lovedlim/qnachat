"""
질의응답(QA) 체인 모듈 - RAG 파이프라인 구현
"""
from typing import Dict, List
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate


class QAChain:
    """RAG 기반 질의응답 체인 클래스"""
    
    # 프롬프트 템플릿 정의
    PROMPT_TEMPLATE = """당신은 '방송 3법' 전문가입니다. 제공된 문서를 바탕으로 사용자의 질문에 정확하고 상세하게 답변해주세요.

답변 시 다음 규칙을 따르세요:
1. 제공된 문서의 내용을 기반으로만 답변하세요.
2. 답변이 문서에 없는 경우, "제공된 문서에서 해당 정보를 찾을 수 없습니다"라고 명확히 말씀해주세요.
3. 가능한 한 구체적이고 상세하게 답변하세요.
4. 법률 조항이나 중요한 내용은 정확하게 인용하세요.
5. 답변은 한국어로 작성하세요.

참고 문서:
{context}

질문: {question}

답변:"""

    def __init__(self, retriever, openai_api_key: str, model_name: str = "gpt-3.5-turbo"):
        """
        Args:
            retriever: 문서 검색을 위한 retriever 객체
            openai_api_key: OpenAI API 키
            model_name: 사용할 OpenAI 모델명
        """
        self.retriever = retriever
        self.openai_api_key = openai_api_key
        self.model_name = model_name
        self.qa_chain = None
        self._setup_chain()
    
    def _setup_chain(self):
        """QA 체인을 설정합니다."""
        # 프롬프트 설정
        prompt = PromptTemplate(
            template=self.PROMPT_TEMPLATE,
            input_variables=["context", "question"]
        )
        
        # LLM 설정
        llm = ChatOpenAI(
            model_name=self.model_name,
            temperature=0,  # 정확한 답변을 위해 temperature를 낮게 설정
            openai_api_key=self.openai_api_key
        )
        
        # RetrievalQA 체인 생성
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=self.retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt}
        )
    
    def ask(self, question: str) -> Dict:
        """
        질문에 대한 답변을 생성합니다.
        
        Args:
            question: 사용자 질문
            
        Returns:
            답변과 출처 문서를 포함한 딕셔너리
            {
                "answer": str,
                "source_documents": List[Document]
            }
        """
        if not question or question.strip() == "":
            return {
                "answer": "질문을 입력해주세요.",
                "source_documents": []
            }
        
        try:
            result = self.qa_chain({"query": question})
            return {
                "answer": result["result"],
                "source_documents": result["source_documents"]
            }
        except Exception as e:
            return {
                "answer": f"답변 생성 중 오류가 발생했습니다: {str(e)}",
                "source_documents": []
            }
    
    def format_sources(self, source_documents: List) -> str:
        """
        출처 문서를 읽기 쉬운 형식으로 포맷팅합니다.
        
        Args:
            source_documents: 출처 문서 리스트
            
        Returns:
            포맷팅된 출처 문자열
        """
        if not source_documents:
            return "출처 정보가 없습니다."
        
        sources = []
        for i, doc in enumerate(source_documents, 1):
            metadata = doc.metadata
            source = metadata.get('source', '알 수 없음')
            page = metadata.get('page', '알 수 없음')
            
            # 파일명만 추출 (전체 경로가 아닌)
            import os
            filename = os.path.basename(source)
            
            sources.append(f"**[{i}] {filename}** (페이지: {page})")
        
        return "\n".join(sources)
    
    def ask_with_formatted_sources(self, question: str) -> Dict:
        """
        질문에 대한 답변과 포맷팅된 출처를 함께 반환합니다.
        
        Args:
            question: 사용자 질문
            
        Returns:
            답변과 포맷팅된 출처를 포함한 딕셔너리
        """
        result = self.ask(question)
        formatted_sources = self.format_sources(result["source_documents"])
        
        return {
            "answer": result["answer"],
            "sources": formatted_sources,
            "source_documents": result["source_documents"]
        }

