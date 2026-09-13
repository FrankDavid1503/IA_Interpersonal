# Modelo Entidad-Relación — NEXO

```text
+-------------------+       +-----------------------+
|       users       | 1---1 |   user_preferences    |
+-------------------+       +-----------------------+
| id (PK)           |       | id (PK)               |
| name              |       | user_id (FK)          |
| email             |       | communication_style   |
| password_hash     |       | directness_level      |
| created_at        |       | preferred_resp_length |
+-------------------+       +-----------------------+
          |
          | 1---N
          v
+-------------------+       +-----------------------+
|    situations     | 1---N |     safety_events     |
+-------------------+       +-----------------------+
| id (PK)           |       | id (PK)               |
| user_id (FK)      |       | situation_id (FK)     |
| input_text        |       | risk_level            |
| relationship_type |       | category              |
| objective         |       | action_taken          |
+-------------------+       +-----------------------+
          |
          | 1---N
          v
+-------------------+
|     analyses      |
+-------------------+
| id (PK)           |
| situation_id (FK) |
| context_summary   |
| detected_emotion  |
| sensitivity_level |
| risk_level        |
| recommendation    |
| suggested_response|
| model_name        |
+-------------------+
     |         |
 1---N         1---N
     v         v
+--------------------+   +--------------------+
|  analysis_emotions |   |  recommendations   |
+--------------------+   +--------------------+
| id (PK)            |   | id (PK)            |
| analysis_id (FK)   |   | analysis_id (FK)   |
| emotion            |   | title              |
| confidence         |   | description        |
|                    |   | benefit / risk     |
+--------------------+   +--------------------+
```
