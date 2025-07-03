from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"Out": "Root comms validated"}

@app.get("/dataframes/mythic/{name}")
def mythic():
    
