import os


def run_uvicorn():
    command = "uvicorn routes.fastapi_server:app --reload --host 0.0.0.0 --port 591"
    os.system(command)


if __name__ == "__main__":
    run_uvicorn()
