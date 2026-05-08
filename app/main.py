import uvicorn
from fastapi import FastAPI
from routes.task_route import route as task_route
from routes.auth_route import route as auth_route


app = FastAPI()
app.include_router(task_route)
app.include_router(auth_route)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
