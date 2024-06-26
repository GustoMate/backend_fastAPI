# backend_fastAPI

- 설치
`pip install "fastapi[all]"`
`pip install python-dotenv`
`pip install -r requirements.txt`

- 준비
root 파일에 .env 생성 (openai key 유출 조심!)

- 실행
터미널에서 `uvicorn main:app --reload`를 실행
http://127.0.0.1:8000/docs 에서 API 문서 확인 가능


파일구조:
```
.
├── GustomateApp
│   ├── database
│   │   ├── database.py
│   │   └── models.py
│   ├── dependency
│   │   └── dependencies.py
│   └── signup
│       ├── CRUD.py
│       ├── router.py
│       └── schema.py
├── README.md
├── config.py
├── create_Gustomate_Database.sql
├── main.py
└── requirements.txt

```