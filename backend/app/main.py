from fastapi import FastAPI

app = FastAPI(
    title="Task Manager",
    version = "1.0.0"
)

@app.get('/')
def home_page():
    return {'App': 'Task Manager',
            'Version':'1.0.0'}

@app.get('/health')
def health_check():
    return {
    "status": "healthy",
    "application": "AI-Enhanced Task Manager"
}