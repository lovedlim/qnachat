"""
방송 3법 QnA 봇 - Streamlit 애플리케이션
"""
import streamlit as st
import os
from utils import DocumentProcessor, QAChain


# 페이지 설정
st.set_page_config(
    page_title="방송 3법 QnA 봇",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .question-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .answer-box {
        background-color: #e8f4f8;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        border-left: 4px solid #1f77b4;
    }
    .source-box {
        background-color: #f9f9f9;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        font-size: 0.9rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """세션 상태 초기화"""
    if 'initialized' not in st.session_state:
        st.session_state.initialized = False
        st.session_state.qa_chain = None
        st.session_state.chat_history = []
        st.session_state.current_question = ""


def get_api_key():
    """API 키를 가져옵니다 (Streamlit secrets 우선, 환경변수 대체)"""
    try:
        # Streamlit secrets에서 가져오기
        return st.secrets["OPENAI_API_KEY"]
    except:
        # 환경변수에서 가져오기
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            st.error("[오류] OpenAI API 키가 설정되지 않았습니다. .streamlit/secrets.toml 파일에 API 키를 설정하거나 환경변수를 설정해주세요.")
            st.stop()
        return api_key


def setup_qa_system():
    """QA 시스템 초기화"""
    with st.spinner("시스템을 초기화하는 중입니다..."):
        try:
            # API 키 가져오기
            api_key = get_api_key()
            
            # 문서 처리기 생성
            doc_processor = DocumentProcessor()
            
            # 문서 처리 (벡터 DB 생성 또는 로드)
            doc_processor.process_documents(api_key, force_reload=False)
            
            # Retriever 가져오기
            retriever = doc_processor.get_retriever(search_kwargs={"k": 4})
            
            # QA Chain 생성
            qa_chain = QAChain(
                retriever=retriever,
                openai_api_key=api_key,
                model_name="gpt-3.5-turbo"
            )
            
            return qa_chain
            
        except FileNotFoundError as e:
            st.error(f"[오류] {str(e)}")
            st.info("[안내] data 폴더에 방송 3법 관련 PDF 문서를 추가해주세요.")
            st.stop()
        except Exception as e:
            st.error(f"[오류] 시스템 초기화 중 오류가 발생했습니다: {str(e)}")
            st.stop()


def main():
    """메인 애플리케이션"""
    # 세션 상태 초기화
    initialize_session_state()
    
    # 헤더
    st.markdown('<div class="main-header">방송 3법 QnA 봇</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # 사이드바
    with st.sidebar:
        st.header("설정")
        
        # 시스템 초기화 버튼
        if st.button("시스템 초기화", help="시스템을 다시 초기화합니다"):
            st.session_state.initialized = False
            st.session_state.qa_chain = None
            st.rerun()
        
        # 대화 기록 초기화 버튼
        if st.button("대화 기록 삭제", help="현재까지의 대화 기록을 삭제합니다"):
            st.session_state.chat_history = []
            st.success("대화 기록이 삭제되었습니다!")
        
        st.markdown("---")
        
        # 정보
        st.header("정보")
        st.markdown("""
        **방송 3법 QnA 봇**은 방송 3법 관련 
        PDF 문서를 기반으로 질문에 답변합니다.
        
        **기능:**
        - PDF 문서 기반 질의응답
        - 문서 출처 표시
        - OpenAI GPT 활용
        
        **사용 방법:**
        1. 아래 입력창에 질문 입력
        2. '질문하기' 버튼 클릭
        3. AI의 답변 확인
        """)
        
        st.markdown("---")
        st.caption("Powered by OpenAI GPT & LangChain")
    
    # QA 시스템 초기화
    if not st.session_state.initialized:
        st.session_state.qa_chain = setup_qa_system()
        st.session_state.initialized = True
        st.success("[완료] 시스템이 준비되었습니다!")
    
    # 메인 영역
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("질문하기")
        
        # 예시 질문 버튼들
        st.markdown("**예시 질문을 클릭해보세요:**")
        col_q1, col_q2, col_q3 = st.columns(3)
        
        example_questions = [
            "주요내용은 뭐야?",
            "방송문화진흥회의 역할은?",
            "한국교육방송공사의 목적은?"
        ]
        
        # 예시 질문 버튼 처리
        with col_q1:
            if st.button(example_questions[0], use_container_width=True):
                st.session_state.current_question = example_questions[0]
        with col_q2:
            if st.button(example_questions[1], use_container_width=True):
                st.session_state.current_question = example_questions[1]
        with col_q3:
            if st.button(example_questions[2], use_container_width=True):
                st.session_state.current_question = example_questions[2]
        
        st.markdown("---")
        
        # 질문 입력
        question = st.text_area(
            "또는 직접 질문을 입력하세요:",
            value=st.session_state.current_question,
            height=100,
            placeholder="예: 방송 3법의 주요 내용은 무엇인가요?",
            key="question_input"
        )
        
        # 입력창의 값이 변경되면 세션 상태 업데이트
        if question != st.session_state.current_question:
            st.session_state.current_question = question
        
        # 질문 버튼
        ask_button = st.button("질문하기", type="primary")
        
        # 질문 처리
        if ask_button and st.session_state.current_question:
            with st.spinner("답변을 생성하는 중입니다..."):
                # QA Chain으로 답변 생성
                result = st.session_state.qa_chain.ask_with_formatted_sources(st.session_state.current_question)
                
                # 대화 기록에 추가
                st.session_state.chat_history.append({
                    "question": st.session_state.current_question,
                    "answer": result["answer"],
                    "sources": result["sources"]
                })
                
                # 질문 초기화
                st.session_state.current_question = ""
                st.rerun()
        
        elif ask_button and not st.session_state.current_question:
            st.warning("[안내] 질문을 입력해주세요.")
    
    with col2:
        st.header("통계")
        st.metric("총 질문 수", len(st.session_state.chat_history))
        
        # data 폴더의 PDF 파일 수 표시
        if os.path.exists("data"):
            pdf_count = len([f for f in os.listdir("data") if f.endswith('.pdf')])
            st.metric("등록된 문서 수", pdf_count)
    
    # 대화 기록 표시
    if st.session_state.chat_history:
        st.markdown("---")
        st.header("대화 기록")
        
        # 최신 대화부터 표시
        for i, chat in enumerate(reversed(st.session_state.chat_history), 1):
            with st.expander(f"질문 {len(st.session_state.chat_history) - i + 1}: {chat['question'][:50]}...", expanded=(i == 1)):
                # 질문
                st.markdown(f'''
                <div class="question-box">
                    <strong>[질문]</strong> {chat['question']}
                </div>
                ''', unsafe_allow_html=True)
                
                # 답변
                answer_text = chat['answer'].replace('\n', '<br>')
                st.markdown(f'''
                <div class="answer-box">
                    <strong>[답변]</strong><br><br>{answer_text}
                </div>
                ''', unsafe_allow_html=True)
                
                # 출처
                if chat['sources']:
                    sources_text = chat['sources'].replace('\n', '<br>')
                    st.markdown(f'''
                    <div class="source-box">
                        <strong>[출처]</strong><br><br>{sources_text}
                    </div>
                    ''', unsafe_allow_html=True)
    
    else:
        st.info("[안내] 위의 입력창에 질문을 입력하고 '질문하기' 버튼을 눌러 시작하세요!")


if __name__ == "__main__":
    main()

