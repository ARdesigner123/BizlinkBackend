import os
from flask import Flask, jsonify
from flask_cors import CORS
from supabase import create_client, Client

app = Flask(__name__)
# Enable CORS so your GitHub Pages frontend is allowed to request data from this Render backend
CORS(app) 

# Grab secret keys from Render Environment Variables
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Initialize Supabase Client ONLY on the backend
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/api/container/<container_id>', methods=['GET'])
def get_container_data(container_id):
    try:
        # Query the 'data' table in Supabase
        response = supabase.table('data').select('*').eq('container_id', container_id).execute()
        
        # Send the data back to the frontend as JSON
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Health check route for Render
@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "Backend is running!"}), 200

if __name__ == '__main__':
    # Render assigns a dynamic port, so we use os.environ.get('PORT')
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)