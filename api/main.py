from fastapi import FastAPI
from shared.services.hello_service import say_hello_and_publish

app = FastAPI(title="Example FastAPI Service")


@app.get(f"/")
def hello_world(name: str = "hello_world"):
    return say_hello_and_publish(message=name)
