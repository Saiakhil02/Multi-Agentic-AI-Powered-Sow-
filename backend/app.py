from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from llm import model
from config import POSTGRESQL_BASE_URL
import uuid
from graph import graph_agentor
from vector_rag import vector_store
from langchain_core.documents import Document

SQLALCHEMY_TRACK_MODIFICATIONS = False

app = Flask(__name__,static_folder='static')
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{POSTGRESQL_BASE_URL}"
db = SQLAlchemy(app)
CORS(app)  # Enable CORS to allow frontend requests

class SOWUserInput(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sow_type = db.Column(db.String(100), nullable=False)
    work_type= db.Column(db.String(100), nullable=False)
    project_objectives = db.Column(db.Text,nullable = False)
    project_scope = db.Column(db.Text,nullable = False)
    detailed_desc = db.Column(db.Text,nullable = False)
    specific_feature = db.Column(db.Text,nullable = False)
    platform_tech = db.Column(db.Text,nullable = False)
    integrations = db.Column(db.Text,nullable = False)
    design_specification = db.Column(db.Text,nullable = False)
    out_of_scope = db.Column(db.Text,nullable = False)
    deliverables = db.Column(db.Text,nullable = False)
    project_timeline = db.Column(db.Text,nullable = False)

@app.route('/generate-sow', methods=['POST'])
def generate_sow():
    try:
        # Get the request data
        data = request.get_json()
        
        # Extract necessary fields (modify based on your form fields)
        sow_type= data.get("sowType", "Unknown")
        work_type = data.get("workType", "Unknown")
        project_objectives = data.get("projectObjectives", "NA")
        project_scope = data.get("projectScope", "NA")
        detailed_desc = data.get("servicesDescription", "NA")
        specific_feature = data.get("specificFeatures", "NA")
        platform_tech = data.get("platformsTechnologies", "NA")
        integrations = data.get("integrations", "NA")
        design_specification = data.get("designSpecifications", "NA")
        out_of_scope = data.get("outOfScope", "NA")
        deliverables = data.get("deliverables", "NA")
        project_timeline = data.get("timeline", "NA")
        

        # Store user's query in database for future use.
        sow_data = SOWUserInput(sow_type=sow_type, 
                                work_type=work_type, 
                                project_objectives=project_objectives,
                                project_scope=project_scope,
                                detailed_desc= detailed_desc,
                                specific_feature=specific_feature,
                                platform_tech=platform_tech,
                                integrations=integrations,
                                design_specification=design_specification,
                                out_of_scope=out_of_scope,
                                deliverables=deliverables,
                                project_timeline=project_timeline)
        db.session.add(sow_data)
        db.session.commit()

        user_query = (
            f"The type of SOW should be {sow_type}.\n"
            f"The type of work is {work_type}.\n"
            f"Objectives of project are {project_objectives}.\n"
            f"Scope of the project is {project_scope}.\n"
            f"Detailed Description of Services is {detailed_desc}.\n"
            f"Specific Features are {specific_feature}.\n"
            f"Platforms and Technologies is {platform_tech}.\n"
            f"Integrations is {integrations}.\n"
            f"Design Specifications are {design_specification}.\n"
            f"Out of Scope is {out_of_scope}.\n"
            f"Deliverables are {deliverables}.\n"
            f"Project Timeline and Schedule is {project_timeline}."
        )
        user_query_map = {
            "sow_type": sow_type,
            "work_type": work_type,
            "project_objectives": project_objectives,
            "project_scope": project_scope,
            "detailed_desc": detailed_desc,
            "specific_feature": specific_feature,
            "platform_tech": platform_tech,
            "integrations": integrations,
            "design_specification": design_specification,
            "out_of_scope": out_of_scope,
            "deliverables": deliverables,
            "project_timeline": project_timeline
        }

        response = graph_agentor.invoke({ 'user_query': user_query, 'query_map': user_query_map })
        

        # Process the data (For now, we just return a formatted response)
        sow_response = {
            "status": "success",
            "message": response['formatted_sow'],
            "sow_json": response['sow'],
            "fileName": response['doc_file_path']
        }
        
        return jsonify(sow_response), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Get the request data
        data = request.get_json()
        
        # Extract necessary fields (modify based on your form fields)
        user_query = data.get("message", "Unknown")
        generated_sow = data.get("context", "Unknown")
        
        # Process the data (For now, we just return a formatted response)
        response = graph_agentor.invoke({ 'user_query': user_query, 'flow': 'chat', 'previous_sow': generated_sow })

        sow_response = {
            "status": "success",
            "message": response['formatted_sow'],
            "sow_json": response['sow'],
            "fileName": response['doc_file_path']
        }
        
        return jsonify(sow_response), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/like-sow', methods=['POST'])
def like_sow():
    try:
        # Get the request data
        data = request.get_json()
        
        # Extract necessary fields (modify based on your form fields)
        sow_content = data.get("content", "Unknown")

        docs = [
            Document(    
                page_content=sow_content,
                metadata={"id": str(uuid.uuid4()), "fileName": "user_generated_sow"},
            ),
        ]

        vector_store.add_documents(docs, ids=[doc.metadata["id"] for doc in docs])

        return jsonify({"status": "success", "message": "SOW liked and stored successfully."}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # <--- create db object.
    app.run(debug=True, port=8080)
