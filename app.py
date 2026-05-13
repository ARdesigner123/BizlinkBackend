import os
import sys
from datetime import datetime, timezone, timedelta # <-- Added timedelta

# Wrap the imports in a try-catch so we know if a library is failing to load
try:
    from flask import Flask, jsonify
    from flask_cors import CORS
    from supabase import create_client, Client
    print("All libraries imported successfully!")
except Exception as e:
    print(f"CRASH DURING IMPORTS: {e}")
    sys.exit(1)

app = Flask(__name__)
CORS(app) 

# Grab secret keys from Render Environment Variables
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase = None

# Safely initialize Supabase Client
try:
    if SUPABASE_URL and SUPABASE_KEY:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("Supabase client initialized successfully!")
    else:
        print("CRITICAL WARNING: SUPABASE_URL or SUPABASE_KEY is missing from Render Environment Variables!")
except Exception as e:
    print(f"CRASH DURING SUPABASE SETUP: {e}")

@app.route('/api/container/<container_id>', methods=['GET'])
def get_container_data(container_id):
    if not supabase:
        return jsonify({"error": "Server is missing Supabase keys. Please add them in Render."}), 500

    try:
        # 1. Force the timezone to UTC+8 (Singapore/Local Time)
        local_timezone = timezone(timedelta(hours=8))
        current_time = datetime.now(local_timezone).isoformat()

        # 2. Update the database! 
        response = supabase.table('materials') \
            .update({'issuance_time': current_time}) \
            .eq('container_id', container_id) \
            .execute()

        # 3. Send the updated data back
        return jsonify(response.data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def health_check():
    if not supabase:
        return jsonify({"status": "Backend running, but missing Database Keys!"}), 500
    return jsonify({"status": "Backend is running and connected to database!"}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)