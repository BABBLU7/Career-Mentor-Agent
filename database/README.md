# MongoDB Dataset

- Database: `career_mentor`
- Collection: `pathways` (15 documents, one per career pathway)
- File: `pathways.json` (JSON array, `_id` equals the pathway `id`)

Document fields: `_id`, `id`, `name`, `short_name`, `icon`, `description`,
`interests[]`, `subjects[]`, `strengths[]`, `work_styles[]`, `careers[]`,
`routes[]`, `skills[]`, `watch_out`.

## Option 1: mongoimport

```
mongoimport --uri "mongodb://127.0.0.1:27017/career_mentor" --collection pathways --jsonArray --drop --file database/pathways.json
```

## Option 2: Python seed script

```
pip install pymongo
python database/seed_mongodb.py
```

## Running the backend

The Flask backend reads pathways from MongoDB when it is reachable, and falls
back to the built-in list in `backend/career_engine.py` otherwise.

```
cd backend
pip install -r requirements.txt
python app.py
```

Set `MONGO_URI` / `MONGO_DB` to point at a different server (for example
MongoDB Atlas).
