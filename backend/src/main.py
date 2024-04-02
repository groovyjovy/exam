import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

def main():
    uvicorn.run("project_name.main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main()
