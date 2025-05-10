import os
import tempfile
import json
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from models import ResumeRanker
from file_handler import extract_text

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max upload
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()
ranker = ResumeRanker()

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.lower().split('.')[-1] in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/rank-text', methods=['POST'])
def rank_text():
    """Rank resumes provided as text strings"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        resumes = data.get('resumes', [])
        job_description = data.get('job_description', '')
        
        if not resumes or not job_description:
            return jsonify({'error': 'Both resumes and job description are required'}), 400
            
        # Rank resumes
        ranked_results = ranker.rank_resumes(resumes, job_description)
        
        # Format results
        results = [
            {
                'resume_id': idx,
                'resume_text': resumes[idx][:100] + '...',  # Preview only
                'score': score
            }
            for idx, score in ranked_results
        ]
        
        return jsonify({'results': results})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/rank-files', methods=['POST'])
def rank_files():
    """Rank resumes provided as file uploads"""
    try:
        if 'job_description' not in request.files:
            return jsonify({'error': 'Job description file is required'}), 400
            
        if 'resumes' not in request.files:
            return jsonify({'error': 'Resume files are required'}), 400
        
        # Get job description file
        jd_file = request.files['job_description']
        if jd_file.filename == '' or not allowed_file(jd_file.filename):
            return jsonify({'error': 'Valid job description file is required'}), 400
            
        # Save job description file
        jd_filename = secure_filename(jd_file.filename)
        jd_path = os.path.join(app.config['UPLOAD_FOLDER'], jd_filename)
        jd_file.save(jd_path)
        
        # Extract text from job description
        job_description = extract_text(jd_path)
        
        # Process resume files
        resume_files = request.files.getlist('resumes')
        resume_texts = []
        filenames = []
        
        for resume_file in resume_files:
            if resume_file.filename == '' or not allowed_file(resume_file.filename):
                continue
                
            # Save resume file
            resume_filename = secure_filename(resume_file.filename)
            filenames.append(resume_filename)
            resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_filename)
            resume_file.save(resume_path)
            
            # Extract text from resume
            resume_text = extract_text(resume_path)
            resume_texts.append(resume_text)
            
            # Clean up
            os.remove(resume_path)
        
        # Clean up job description file
        os.remove(jd_path)
        
        if not resume_texts:
            return jsonify({'error': 'No valid resume files provided'}), 400
            
        # Rank resumes
        ranked_results = ranker.rank_resumes(resume_texts, job_description)
        
        # Format results
        results = [
            {
                'resume_id': idx,
                'filename': filenames[idx],
                'score': score,
                'preview': resume_texts[idx][:100] + '...' if len(resume_texts[idx]) > 100 else resume_texts[idx]
            }
            for idx, score in ranked_results
        ]
        
        return jsonify({'results': results})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
