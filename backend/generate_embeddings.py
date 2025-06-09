import psycopg2
from sentence_transformers import SentenceTransformer
import numpy as np

# Load pre-trained embedding model
model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="mydatabase",
    user="postgres",
    password="Admin1234",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Fetch SOWs without embeddings
cursor.execute("SELECT id, content FROM sow_data WHERE embedding IS NULL;")
rows = cursor.fetchall()

# Generate embeddings and update database
for row in rows:
    sow_id, content = row
    embedding_array = model.encode(content)
    print(f"Embedding shape: {len(embedding_array)}")

    # Store embeddings as a vector
    cursor.execute(
        "UPDATE sow_data SET embedding = %s WHERE id = %s",
        (embedding_array.tolist(), sow_id)
    )
    print(f"✅ Embedding stored for SOW ID: {sow_id}")

# Commit changes
conn.commit()
cursor.close()
conn.close()
print("🎉 All embeddings stored successfully!")
