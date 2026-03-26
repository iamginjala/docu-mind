FROM python:3.12-slim

WORKDIR /docu-mind

COPY frontend/requirements.txt .
RUN pip install -r requirements.txt

COPY frontend/ ./frontend/

EXPOSE 8501

CMD ["streamlit", "run", "frontend/streamlit_app.py", "--server.address", "0.0.0.0", "--server.port", "8501"]