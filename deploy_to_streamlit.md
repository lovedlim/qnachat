# Streamlit Cloud 배포 빠른 가이드

## 🚀 5분 안에 배포하기

### 1️⃣ GitHub 저장소 생성
1. https://github.com/new 접속
2. Repository name: `vibe_qna5` 입력
3. Public 선택
4. "Create repository" 클릭

### 2️⃣ 코드 업로드
PowerShell 또는 명령 프롬프트에서:

```powershell
# 현재 프로젝트 폴더에서 실행

# Git 초기화
git init

# 모든 파일 추가
git add .

# 커밋
git commit -m "Initial commit"

# 원격 저장소 연결 (YOUR-USERNAME을 본인 GitHub 계정으로 변경!)
git remote add origin https://github.com/YOUR-USERNAME/vibe_qna5.git

# 업로드
git branch -M main
git push -u origin main
```

**중요**: `YOUR-USERNAME`을 본인의 GitHub 사용자명으로 바꾸세요!

예시:
```powershell
git remote add origin https://github.com/danmu/vibe_qna5.git
```

### 3️⃣ Streamlit Cloud 배포
1. https://streamlit.io/cloud 접속
2. "Sign in with GitHub" 클릭
3. "New app" 클릭
4. 저장소 선택:
   - **Repository**: `YOUR-USERNAME/vibe_qna5`
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. "Advanced settings" 클릭
6. "Secrets" 탭에 다음 내용 복사-붙여넣기:

```toml
OPENAI_API_KEY = "your-openai-api-key-here"
```

7. "Deploy!" 클릭
8. 완료! (2-3분 소요)

### 4️⃣ 배포 완료
- URL 형태: `https://vibe-qna5.streamlit.app`
- 이 URL을 공유하면 누구나 접속 가능합니다

---

## 🔧 문제 해결

### Git이 설치되어 있지 않은 경우
https://git-scm.com/download/win 에서 Git 다운로드 및 설치

### "Git is not recognized" 오류
Git 설치 후 PowerShell/명령 프롬프트를 재시작하세요

### 업로드 중 인증 오류
1. GitHub 웹사이트에서 로그인 확인
2. Personal Access Token 생성:
   - GitHub → Settings → Developer settings → Personal access tokens
   - "Generate new token" → repo 권한 선택
   - 생성된 토큰을 비밀번호 대신 사용

### PDF 파일이 너무 큰 경우
GitHub는 100MB 이상 파일 업로드 불가
- 해결 1: PDF 파일 압축
- 해결 2: Git LFS 사용
- 해결 3: 배포 후 직접 업로드

---

## 📌 주의사항

### 보안
- ✅ `.gitignore`가 `.streamlit/secrets.toml`을 포함하고 있는지 확인
- ✅ API 키가 코드에 하드코딩되어 있지 않은지 확인
- ✅ GitHub에 API 키가 노출되지 않았는지 확인

### FAISS 인덱스
`faiss_index/` 폴더를 Git에 포함하면:
- ✅ 장점: 배포 후 즉시 사용 가능 (인덱스 생성 시간 절약)
- ❌ 단점: 저장소 크기 증가

현재 `.gitignore`에서 주석 처리되어 있음 (포함됨)

---

## 🔄 업데이트 방법

코드를 수정한 후:

```powershell
git add .
git commit -m "업데이트 내용"
git push
```

Streamlit Cloud가 자동으로 새 버전을 배포합니다!

---

## 💰 비용

### Streamlit Cloud
- **무료**: 1개 앱, Public 저장소
- **충분한 리소스**: 대부분의 경우 무료 플랜으로 충분

### OpenAI API
- 질문 1회당 약 $0.01~0.05
- 월 100회 질문 시 약 $1~5

---

## 📞 추가 지원

- Streamlit 문서: https://docs.streamlit.io
- Streamlit 커뮤니티: https://discuss.streamlit.io

