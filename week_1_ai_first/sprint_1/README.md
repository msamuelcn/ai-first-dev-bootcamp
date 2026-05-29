# Workout REST API

## Github Repository
https://github.com/msamuelcn/ai-first-dev-bootcamp/tree/main/week_1_ai_first/sprint_1

## Live Public Deployment
https://gauntletai-vslp.onrender.com/workouts

## Live endpoint list
- `POST /workouts`: Create a new workout.
- `GET /workouts`: List all workouts.
- `GET /workouts/{id}`: Get a workout by ID.
- `PUT /workouts/{id}`: Update a workout by ID.
- `DELETE /workouts/{id}`: Delete a workout by ID.

### Health Check
```bash
curl "https://gauntletai-vslp.onrender.com/health"
```

### API Documentation
- Swagger UI: https://gauntletai-vslp.onrender.com/docs
- ReDoc: https://gauntletai-vslp.onrender.com/redoc


## Example usage
### Create a workout
```bash
curl -X POST "https://gauntletai-vslp.onrender.com/workouts" \
-H "Content-Type: application/json" \
-d '{
  "duration_minutes": 30,
  "distance_km": 5,
  "workout_type": "Community Run",
  "workout_date": "2024-06-01"
}'
```

### List workouts
```bash
curl "https://gauntletai-vslp.onrender.com/workouts"
```

### Get a workout by ID
```bash
curl "https://gauntletai-vslp.onrender.com/workouts/1"
```

### Update a workout
```bash
curl -X PUT "https://gauntletai-vslp.onrender.com/workouts/1" \
-H "Content-Type: application/json" \
-d '{
  "duration_minutes": 35,
  "distance_km": 6,
  "workout_type": "Community Run",
  "workout_date": "2024-06-01"
}'
```

### Delete a workout
```bash
curl -X DELETE "https://gauntletai-vslp.onrender.com/workouts/1"
```



