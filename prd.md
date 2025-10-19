## 방송 3법 QnA 봇 (Vibe Coding/Streamlit) PRD

### 1\. 개요 (Introduction)

본 프로젝트는 **'방송 3법'** 관련 질의응답을 목적으로 하는 QnA 봇을 개발하는 것입니다. 사용자가 'data' 폴더 내에 저장된 **PDF 문서**를 기반으로 질문하면, 봇이 **정확하고 신뢰성 있는 답변**을 제공합니다. 개발 환경은 \*\*바이브 코딩(Vibe Coding)\*\*을 사용하며, **Streamlit**을 활용하여 사용자 친화적인 웹 인터페이스를 구축하고, 답변 생성 기능은 **OpenAI API**를 이용한 LLM(Large Language Model)으로 구현합니다.

\<hr\>

### 2\. 목표 (Goals)

| ID | 목표 설명 | 측정 지표 |
| :--- | :--- | :--- |
| G1 | 'data' 폴더의 PDF 문서 내용에 근거한 **정확한 답변** 제공 | 답변 정확도 90% 이상 |
| G2 | 사용자 친화적이고 **쉬운 사용성**을 가진 웹 인터페이스 구현 | 사용자 피드백 만족도 (5점 만점에 4점 이상) |
| G3 | **안정적인 LLM 기능** 구현 및 API 키 보안 관리 | API 호출 성공률 99% 이상, 환경 변수(`.env`)를 통한 키 관리 |

\<hr\>

### 3\. 주요 기능 (Core Features)

| ID | 기능명 | 설명 | 비고 |
| :--- | :--- | :--- | :--- |
| F1 | **문서 로딩 및 인덱싱** | 'data' 폴더 내의 PDF 문서를 읽어와 LLM이 활용 가능한 형태로 전처리하고 인덱싱합니다. | RAG (Retrieval-Augmented Generation) 기반 |
| F2 | **질문 입력 인터페이스** | 사용자가 질문을 입력할 수 있는 텍스트 입력창을 Streamlit에 구현합니다. | - |
| F3 | **답변 생성 (LLM)** | 사용자의 질문과 인덱싱된 문서를 기반으로 **OpenAI LLM**을 호출하여 답변을 생성합니다. | API 호출 |
| F4 | **답변 출력** | LLM이 생성한 답변을 사용자에게 명확하고 읽기 쉽게 Streamlit 화면에 표시합니다. | - |
| F5 | **출처 표시 (선택)** | 답변이 근거한 문서 내의 페이지 번호 또는 섹션을 함께 제공하여 신뢰도를 높입니다. | (Optional) |
| F6 | **API 키 보안 관리** | OpenAI API 키는 소스코드에 직접 노출하지 않고, \*\*환경 변수(.env 파일 또는 Streamlit Secrets)\*\*를 통해 안전하게 관리합니다. | **필수 구현** |

\<hr\>

### 4\. 기술 스택 (Technical Stack)

| 구분 | 기술/도구 | 용도 |
| :--- | :--- | :--- |
| 개발 환경 | **Vibe Coding** | 주요 개발 및 테스트 환경 |
| 프론트엔드/배포 | **Streamlit** | 웹 인터페이스 및 손쉬운 배포 |
| LLM | **OpenAI API (GPT-3.5-turbo)** | 질의응답 및 답변 생성 기능 |
| LLM 프레임워크 | **LangChain** | PDF 로딩, 분할, 임베딩, 벡터 저장소 구성 등 RAG 파이프라인 구축 |
| 벡터 데이터베이스 | **FAISS** | 문서 임베딩 저장 및 유사도 검색 (ChromaDB 대신 사용) |
| 문서 처리 | **PyPDF** | PDF 파일 로딩 및 파싱 |
| 데이터 저장 | **'data' 폴더** | 방송 3법 관련 PDF 문서 저장소 |
| 보안 | **Streamlit Secrets** | OpenAI API 키 등 민감 정보 관리 |

\<hr\>

### 5\. 배포 및 운영 (Deployment & Operations)

  * **배포 플랫폼:** Streamlit Cloud 또는 기타 웹 호스팅 환경을 고려합니다.
  * **API 비용 관리:** OpenAI API 사용량을 모니터링하여 예상 비용 범위 내에서 운영되도록 관리합니다.
  * **유지보수:** 방송 3법 내용 변경 시 'data' 폴더의 PDF 문서만 교체하면 봇이 자동으로 새로운 내용을 반영할 수 있도록 모듈화하여 개발합니다.

\<hr\>

### 6\. 개발 단계 (Development Phases)

1.  **환경 설정:** Vibe Coding 환경 구성, 필요한 라이브러리(Streamlit, LangChain 등) 설치, `.env` 파일을 통한 API 키 설정.
2.  **데이터 준비:** PDF 문서 로딩, 분할(Chunking), 임베딩 및 벡터 데이터베이스 구축 (F1).
3.  **LLM 통합:** 질문-답변 파이프라인 (RAG) 구현 및 테스트 (F3).
4.  **인터페이스 개발:** Streamlit을 활용한 사용자 입력/출력 화면 구현 (F2, F4).
5.  **테스트 및 검증:** 다양한 질문 시나리오를 통한 답변의 정확도 및 안정성 검증.
6.  **배포 준비:** Streamlit 배포 환경 설정 및 키 보안 설정(F6) 최종 점검.


---

### 7\. 개발 시 주의사항 (Development Notes)

#### 핵심 포인트

1. **벡터 데이터베이스:** ChromaDB 대신 **FAISS** 사용 (설치 간편)
2. **필수 패키지:** `tiktoken` 반드시 설치 필요
3. **Windows 호환:** 이모지/특수문자 대신 일반 텍스트 사용 (`[OK]`, `[오류]` 등)
4. **API 키 보안:** `.streamlit/secrets.toml`에 저장, Git에 커밋 금지

#### 상세 기술 노트 (개발자용)

<details>
<summary>Windows 인코딩 문제 해결</summary>

- Windows에서 유니코드 문자(✓, ✗, 🔄) 사용 시 `cp949 codec` 오류 발생
- 해결: `[OK]`, `[오류]`, `[안내]` 등 일반 텍스트로 대체
</details>

<details>
<summary>올바른 Import 구문</summary>

```python
# 최신 LangChain 버전
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
```
</details>

<details>
<summary>Streamlit UI 팁</summary>

- HTML 박스는 하나의 `st.markdown()` 호출로 통합
- 예시 질문 버튼은 `st.session_state` 활용
</details>

---

### 8\. OpenAI API 키

API 키는 `.streamlit/secrets.toml` 파일에 저장되어 있습니다. (Git에 커밋되지 않음)