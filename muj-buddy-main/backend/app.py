from flask import Flask, jsonify
from flask_cors import CORS
from backend.config import Config
from backend.modules import db
import os

# For FAISS + Embeddings
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# ------------------------------------------------------
# App Factory Function
# ------------------------------------------------------
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    db.init_app(app)

    # Initialize FAISS Vector Store (if it exists)
    embeddings = HuggingFaceEmbeddings(model_name=Config.EMBEDDING_MODEL)

    if os.path.exists(Config.VECTOR_STORE_PATH):
        try:
            vector_store = FAISS.load_local(
                Config.VECTOR_STORE_PATH,
                embeddings,
                allow_dangerous_deserialization=True
            )
            print("✅ FAISS index loaded successfully.")
        except Exception as e:
            print(f"⚠️ Error loading FAISS index: {e}")
            vector_store = None
    else:
        print("ℹ️ No FAISS index found yet. Run create_faiss_index.py first.")
        vector_store = None

    # ------------------------------------------------------
    # Routes
    # ------------------------------------------------------
    @app.route('/')
    def home():
        return jsonify({"message": "MUJ Buddy API running"})

    @app.route('/health')
    def health_check():
        """Simple health check route"""
        return jsonify({
            "database_connected": db.engine.url.database,
            "vector_store_loaded": vector_store is not None
        })

    return app


# ------------------------------------------------------
# Run the app
# ------------------------------------------------------
if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="127.0.0.1", port=5000)
