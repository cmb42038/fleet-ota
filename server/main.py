from fastapi import FastAPI

app = FastAPI()


# check if server is up
@app.get("/health")
def health():
    return {"status": "ok"}