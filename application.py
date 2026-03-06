    
from flask import Flask, jsonify
from sqlalchemy import text
from FlaskWebProject.db import engine
import sys
sys.path.append("..")
import config

app = Flask(__name__)

@app.route('/')
def home():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))  
            return f"✅ DB connected successfully, query result: {result.scalar()}"
    except Exception as e:
        return f"❌ DB connection failed: {e}"

@app.route('/users')
def users():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM users")) 
            rows = result.fetchall()
            users_list = [dict(row._mapping) for row in rows]
            return jsonify(users_list)
    except Exception as e:
        return jsonify({"error": str(e)})
'''
if __name__ == "__main__":
    app.run(debug=True)'''
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)