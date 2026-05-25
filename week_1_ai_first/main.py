from fastapi import FastAPI

# 1. Create an instance of FastAPI
app = FastAPI()


# 2. Define a "path operation" (route)
@app.post("/workouts")
def create_workout():
    # 3. Return a dictionary (automatically converted to JSON)
    return {"message": "POST: Welcome to my workouts!"}


@app.get("/workouts")
def list_workout():
    return {"message": "GET: Welcome to my workouts!"}


# GET    /events/{id}
@app.get("/workouts/{id}")
def get_workout(id: int):
    return {"message": f"GET: Welcome to workout: {id}!"}


# PUT    /workouts/{id}
@app.put("/workouts/{id}")
def update_workout(id: int):
    return {"message": f"PUT: Welcome to workout: {id}!"}


# DELETE /workouts/{id}
@app.delete("/workouts/{id}")
def delete_workout(id: int):
    return {"message": f"DELETE: Welcome to workout: {id}!"}
