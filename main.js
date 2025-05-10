document.addEventListener('DOMContentLoaded', function() {
    const fileForm = document.getElementById('file-form');
    const textForm = document.getElementById('text-form');
    const addResumeBtn = document.getElementById('add-resume-btn');
    const resumeContainer = document.getElementById('resume-container');
    const resultsContainer = document.getElementById('results-container');
    const resultsTableBody = document.getElementById('results-table-body');
    const loadingIndicator = document.getElementById('loading');
    const errorMessage = document.getElementById('error-message');
    
    // Add another resume text area
    addResumeBtn.addEventListener('click', function() {
        const resumeCount = document.querySelectorAll('.resume-entry').length + 1;
        
        const resumeDiv = document.createElement('div');
        resumeDiv.className = 'resume-entry mb-3';
        resumeDiv.innerHTML = `
            <label class="form-label">Resume ${resumeCount}</label>
            <textarea class="form-control resume-text" rows="5" required></textarea>
        `;
        
        resumeContainer.appendChild(resumeDiv);
    });
    
    // Handle file form submission
    fileForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const jobDescriptionFile = document.getElementById('job-description-file').files[0];
        const resumeFiles = document.getElementById('resume-files').files;
        
        if (!jobDescriptionFile || resumeFiles.length === 0) {
            showError('Please select a job description file and at least one resume file.');
            return;
        }
        
        // Create FormData
        const formData = new FormData();
        formData.append('job_description', jobDescriptionFile);
        
        for (let i = 0; i < resumeFiles.length; i++) {
            formData.append('resumes', resumeFiles[i]);
        }
        
        // Send API request
        showLoading(true);
        
        fetch('/api/rank-files', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => handleResults(data))
        .catch(error => {
            showError('An error occurred: ' + error.message);
        })
        .finally(() => {
            showLoading(false);
        });
    });
    
    // Handle text form submission
    textForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const jobDescription = document.getElementById('job-description-text').value;
        const resumeTextareas = document.querySelectorAll('.resume-text');
        
        const resumes = [];
        resumeTextareas.forEach(textarea => {
            if (textarea.value.trim()) {
                resumes.push(textarea.value);
            }
        });
        
        if (!jobDescription || resumes.length === 0) {
            showError('Please enter a job description and at least one resume.');
            return;
        }
        
        // Send API request
        showLoading(true);
        
        fetch('/api/rank-text', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                job_description: jobDescription,
                resumes: resumes
            })
        })
        .then(response => response.json())
        .then(data => handleResults(data))
        .catch(error => {
            showError('An error occurred: ' + error.message);
        })
        .finally(() => {
            showLoading(false);
        });
    });
    
    // Handle results display
    function handleResults(data) {
        if (data.error) {
            showError(data.error);
            return;
        }
        
        if (!data.results || data.results.length === 0) {
            showError('No results returned.');
            return;
        }
        
        // Clear previous results
        resultsTableBody.innerHTML = '';
        
        // Display results
        data.results.forEach((result, index) => {
            const row = document.createElement('tr');
            
            // Determine score class
            let scoreClass = 'score-low';
            if (result.score >= 0.7) {
                scoreClass = 'score-high';
            } else if (result.score >= 0.4) {
                scoreClass = 'score-medium';
            }
            
            // Create resume name/identifier
            let resumeName = result.filename || `Resume ${result.resume_id + 1}`;
            
            row.innerHTML = `
                <td>${index + 1}</td>
                <td>
                    <div><strong>${resumeName}</strong></div>
                    <div class="resume-preview">${result.preview || ''}</div>
                </td>
                <td><span class="score-pill ${scoreClass}">${(result.score * 100).toFixed(1)}%</span></td>
            `;
            
            resultsTableBody.appendChild(row);
        });
        
        // Show results container
        resultsContainer.classList.remove('d-none');
        
        // Scroll to results
        resultsContainer.scrollIntoView({ behavior: 'smooth' });
    }
    
    // Show/hide loading indicator
    function showLoading(isLoading) {
        if (isLoading) {
            loadingIndicator.classList.remove('d-none');
            errorMessage.classList.add('d-none');
            resultsContainer.classList.add('d-none');
        } else {
            loadingIndicator.classList.add('d-none');
        }
    }
    
    // Show error message
    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.classList.remove('d-none');
        resultsContainer.classList.add('d-none');
    }
});
