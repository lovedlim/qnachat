# 방송 3법 QnA 봇

방송 3법 관련 PDF 문서를 기반으로 질의응답을 제공하는 AI 챗봇입니다.

## 기능
- PDF 문서 기반 질의응답 (RAG)
- Streamlit 웹 인터페이스
- OpenAI GPT 모델 활용
- 출처 표시 기능

## 설치 방법

1. 필요한 패키지 설치:
```bash
pip install -r requirements.txt
```

2. `.env` 파일에 OpenAI API 키 설정:
```
OPENAI_API_KEY=your-api-key-here
```

3. PDF 문서를 `data` 폴더에 저장

## 실행 방법

```bash
streamlit run app.py
```

## 기술 스택
- **프레임워크**: Streamlit
- **LLM**: OpenAI GPT
- **RAG 프레임워크**: LangChain
- **벡터 데이터베이스**: ChromaDB
- **문서 처리**: PyPDF

