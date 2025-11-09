from flask import Blueprint, request, jsonify
from backend.modules import Professor, db
from backend.config import Config
import os

# LangChain + FAISS Imports
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

bp = Blueprint("professors", __name__, url_prefix="/api")

# ------------------------------------------------------
# Load FAISS Store when routes are registered
# ------------------------------------------------------
embeddings = HuggingFaceEmbeddings(model_name=Config.EMBEDDING_MODEL)

if os.path.exists(Config.VECTOR_STORE_PATH):
    try:
        vector_store = FAISS.load_local(
            Config.VECTOR_STORE_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )
        print("✅ FAISS index loaded successfully in professors.py")
    except Exception as e:
        print(f"⚠️ Error loading FAISS index in professors.py: {e}")
        vector_store = None
else:
    print("ℹ️ No FAISS index found yet. Run create_faiss_index.py first.")
    vector_store = None


# ------------------------------------------------------
# ROUTES
# ------------------------------------------------------

@bp.route("/professors", methods=["GET"])
def all_professors():
    """Return all professors from the database."""
    profs = Professor.query.all()
    return jsonify([p.to_dict() for p in profs]), 200


@bp.route("/professor/search", methods=["GET"])
def search_professor():
    """
    Semantic search using FAISS.
    If FAISS not available, fallback to name-based SQL search.
    """
    query = request.args.get("q", "")
    if not query:
        return jsonify({"error": "Query parameter 'q' is required"}), 400

    # ✅ If FAISS is ready → use embeddings for semantic search
    if vector_store:
        try:
            results = vector_store.similarity_search(query, k=2)
            matches = []
            for res in results:
                matches.append({
                    "professor_text": res.page_content,
                    "score": res.metadata.get("score", None)
                })
            return jsonify({
                "query": query,
                "matches": matches
            }), 200
        except Exception as e:
            print("FAISS Search Error:", e)

    # ⚠️ Fallback to normal database search
    prof = Professor.query.filter(Professor.name.ilike(f"%{query}%")).first()
    if not prof:
        return jsonify({"error": "Professor not found"}), 404

    return jsonify(prof.to_dict()), 200
