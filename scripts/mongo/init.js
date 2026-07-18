db = db.getSiblingDB("alv_mongo"); // Creating database alv_mongo

db.createCollection("messages"); // Creating entity messages

db.messages.createIndex({
  chat_id: 1,
  message_id: 1
}, { unique: true }) // Indexing notes for fast

db.messages.createIndex({
  chat_id: 1,
  created_at: -1
}) // Indexing notes to find by date

// Example of containig default data

/*
  "_id": uniq id AUTO GENERATED
  "chat_id": 123, FOREIGN KEY for  postgres
  "message_id": 777,
  "type": "audio",

  "vector": [...],
  "text": ....,

  "has_document": false,
  "has_audio": true,
  "has_photo": false,
  "has_video": false,

  "created_at": "2026-03-19T12:00:00Z"
*/
