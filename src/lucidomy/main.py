from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Lucidomy is running!"}