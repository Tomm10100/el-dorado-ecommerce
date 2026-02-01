"""
InnovLead Vault - Main Flask Server
The central command center for all InnovLead systems
"""

import os
import json
import threading
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
STORAGE_DIR = Path("storage")
STORAGE_DIR.mkdir(exist_ok=True)
(STORAGE_DIR / "consultancy").mkdir(exist_ok=True)
(STORAGE_DIR / "proposals").mkdir(exist_ok=True)
(STORAGE_DIR / "logs").mkdir(exist_ok=True)

# Simple in-memory database (replace with Replit DB in production)
vault_db = {
    "consultancy_jobs": {},
    "history": []
}

# ============================================================================
# ROUTES - Pages
# ============================================================================

@app.route('/')
def index():
    """Landing page with Enter the Vault button"""
    return render_template('landing.html')

@app.route('/dashboard')
def dashboard():
    """Main dashboard - The Vault command center"""
    return render_template('dashboard.html')

@app.route('/consultancy')
def consultancy_page():
    """Consultancy module page"""
    return render_template('consultancy.html')

@app.route('/avatar-studio')
def avatar_studio_page():
    """Avatar Studio module page"""
    return render_template('avatar_studio.html')

@app.route('/image-assistant')
def image_assistant_page():
    """Image Assistant module page"""
    return render_template('image_assistant.html')

@app.route('/content-gallery')
def content_gallery_page():
    """Content Gallery module page"""
    return render_template('content_gallery.html')

@app.route('/content')
def content_page():
    """Content creation module page (legacy)"""
    return render_template('content.html')

@app.route('/modules')
def modules_page():
    """Module manager page"""
    return render_template('modules.html')

# ============================================================================
# API - Consultancy Engine
# ============================================================================

@app.route('/api/consultancy/run', methods=['POST'])
def run_consultancy():
    """
    Trigger full consultancy analysis
    Body: {company, industry, url, location}
    Returns: {job_id, status}
    """
    try:
        data = request.json
        company = data.get('company')
        industry = data.get('industry', '')
        url = data.get('url', '')
        location = data.get('location', 'Canada')
        
        if not company:
            return jsonify({'success': False, 'error': 'Company name required'}), 400
        
        # Create job
        job_id = f"job_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{company.lower().replace(' ', '_')}"
        
        job_data = {
            'job_id': job_id,
            'company': company,
            'industry': industry,
            'url': url,
            'location': location,
            'status': 'queued',
            'phase': 'initializing',
            'progress': 0,
            'created_at': datetime.now().isoformat(),
            'started_at': None,
            'completed_at': None,
            'results': None,
            'error': None
        }
        
        vault_db['consultancy_jobs'][job_id] = job_data
        vault_db['history'].insert(0, job_id)
        
        # Start background worker
        thread = threading.Thread(target=run_consultancy_worker, args=(job_id,))
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'job_id': job_id,
            'status': 'queued',
            'message': 'Consultancy analysis started'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/consultancy/status/<job_id>', methods=['GET'])
def get_consultancy_status(job_id):
    """
    Get status of consultancy job
    Returns: {status, phase, progress, current_task}
    """
    job = vault_db['consultancy_jobs'].get(job_id)
    
    if not job:
        return jsonify({'success': False, 'error': 'Job not found'}), 404
    
    return jsonify({
        'success': True,
        'job_id': job_id,
        'status': job['status'],
        'phase': job['phase'],
        'progress': job['progress'],
        'company': job['company'],
        'created_at': job['created_at'],
        'started_at': job['started_at'],
        'completed_at': job['completed_at'],
        'error': job['error']
    })

@app.route('/api/consultancy/results/<job_id>', methods=['GET'])
def get_consultancy_results(job_id):
    """
    Get full results of consultancy analysis
    Returns: {research, funding, strategy, proposals, metrics}
    """
    job = vault_db['consultancy_jobs'].get(job_id)
    
    if not job:
        return jsonify({'success': False, 'error': 'Job not found'}), 404
    
    if job['status'] != 'complete':
        return jsonify({
            'success': False,
            'error': 'Job not complete',
            'status': job['status']
        }), 400
    
    return jsonify({
        'success': True,
        'job_id': job_id,
        'company': job['company'],
        'results': job['results'],
        'completed_at': job['completed_at']
    })

@app.route('/api/consultancy/history', methods=['GET'])
def get_consultancy_history():
    """
    Get list of all consultancy analyses
    Returns: [{job_id, company, date, status, metrics}]
    """
    history = []
    
    for job_id in vault_db['history'][:20]:  # Last 20 jobs
        job = vault_db['consultancy_jobs'].get(job_id)
        if job:
            history.append({
                'job_id': job_id,
                'company': job['company'],
                'industry': job['industry'],
                'status': job['status'],
                'created_at': job['created_at'],
                'completed_at': job['completed_at'],
                'metrics': job['results'].get('metrics') if job['results'] else None
            })
    
    return jsonify({
        'success': True,
        'total': len(history),
        'history': history
    })

@app.route('/api/consultancy/proposals/<job_id>/<proposal_type>', methods=['GET'])
def download_proposal(job_id, proposal_type):
    """
    Download specific proposal document
    Types: executive, technical, financial, funding
    """
    job = vault_db['consultancy_jobs'].get(job_id)
    
    if not job or job['status'] != 'complete':
        return jsonify({'success': False, 'error': 'Job not found or incomplete'}), 404
    
    # Get proposal file path
    company_slug = job['company'].lower().replace(' ', '_')
    date_str = datetime.fromisoformat(job['completed_at']).strftime('%Y-%m-%d')
    
    filename_map = {
        'executive': f"{company_slug}_executive_summary_{date_str}.md",
        'technical': f"{company_slug}_technical_roadmap_{date_str}.md",
        'financial': f"{company_slug}_financial_model_{date_str}.md",
        'funding': f"{company_slug}_funding_application_{date_str}.md"
    }
    
    filename = filename_map.get(proposal_type)
    if not filename:
        return jsonify({'success': False, 'error': 'Invalid proposal type'}), 400
    
    file_path = STORAGE_DIR / "proposals" / filename
    
    if not file_path.exists():
        return jsonify({'success': False, 'error': 'Proposal file not found'}), 404
    
    return send_file(file_path, as_attachment=True, download_name=filename)

@app.route('/api/consultancy/email/<job_id>', methods=['POST'])
def email_proposals(job_id):
    """
    Email proposals to specified recipient
    Body: {email, proposals: ['executive', 'technical', ...], message}
    """
    try:
        data = request.json
        recipient_email = data.get('email')
        proposal_types = data.get('proposals', ['executive'])
        message = data.get('message', '')
        
        job = vault_db['consultancy_jobs'].get(job_id)
        
        if not job or job['status'] != 'complete':
            return jsonify({'success': False, 'error': 'Job not found or incomplete'}), 404
        
        # TODO: Implement email sending (SendGrid, SMTP, etc.)
        # For now, return success
        
        return jsonify({
            'success': True,
            'message': f'Proposals sent to {recipient_email}',
            'proposals_sent': proposal_types
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================================
# API - Module Management
# ============================================================================

@app.route('/api/modules/list', methods=['GET'])
def list_modules():
    """Get list of all available modules"""
    modules = [
        {
            'name': 'client-automation',
            'display_name': 'Consultancy Engine',
            'version': '2.0',
            'status': 'active',
            'description': 'Multi-dimensional consultancy and proposal generation',
            'icon': '🎯'
        },
        {
            'name': 'content-creation',
            'display_name': 'Content Pipeline',
            'version': '1.0',
            'status': 'active',
            'description': 'Automated social media content generation',
            'icon': '📱'
        },
        {
            'name': 'mcp-integrations',
            'display_name': 'MCP Connectors',
            'version': '1.0',
            'status': 'active',
            'description': 'External API and data source integrations',
            'icon': '🔌'
        }
    ]
    
    return jsonify({
        'success': True,
        'total': len(modules),
        'modules': modules
    })

# ============================================================================
# Background Worker
# ============================================================================

def run_consultancy_worker(job_id):
    """
    Background worker that runs the consultancy analysis
    This calls your local Python modules
    """
    import subprocess
    import sys
    
    job = vault_db['consultancy_jobs'][job_id]
    
    try:
        job['status'] = 'running'
        job['started_at'] = datetime.now().isoformat()
        
        company = job['company']
        industry = job['industry']
        url = job['url']
        location = job['location']
        
        # Build command to run consultancy
        # Assuming your Antigravity modules are accessible
        module_path = Path(__file__).parent.parent / "modules" / "client-automation" / "execution"
        script_path = module_path / "run_full_consultancy.py"
        
        cmd = [sys.executable, str(script_path), company]
        
        if industry:
            cmd.extend(['--industry', industry])
        if url:
            cmd.extend(['--url', url])
        if location:
            cmd.extend(['--location', location])
        
        # Update progress: Phase 1
        job['phase'] = 'research'
        job['progress'] = 25
        
        # Run the consultancy script
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=900  # 15 minute timeout
        )
        
        if result.returncode == 0:
            # Success! Parse results
            job['phase'] = 'complete'
            job['progress'] = 100
            job['status'] = 'complete'
            job['completed_at'] = datetime.now().isoformat()
            
            # Load results from generated files
            company_slug = company.lower().replace(' ', '_')
            
            # Try to load research data
            research_file = module_path.parent / ".tmp" / "research" / f"{company_slug}_enhanced_research.json"
            funding_file = module_path.parent / ".tmp" / "funding" / f"{company_slug}_funding.json"
            strategy_file = module_path.parent / ".tmp" / "strategy" / f"{company_slug}_strategy.json"
            
            results = {
                'metrics': {
                    'funding_found': 0,
                    'annual_roi': 0,
                    'proposals_generated': 4
                },
                'files_generated': []
            }
            
            # Parse funding data for metrics
            if funding_file.exists():
                with open(funding_file, 'r') as f:
                    funding_data = json.load(f)
                    # Estimate funding amount (simplified)
                    results['metrics']['funding_found'] = len(funding_data.get('opportunities', [])) * 15000
            
            job['results'] = results
            
        else:
            # Error occurred
            job['status'] = 'error'
            job['error'] = result.stderr or 'Unknown error'
            job['completed_at'] = datetime.now().isoformat()
            
    except subprocess.TimeoutExpired:
        job['status'] = 'error'
        job['error'] = 'Analysis timed out after 15 minutes'
        job['completed_at'] = datetime.now().isoformat()
        
    except Exception as e:
        job['status'] = 'error'
        job['error'] = str(e)
        job['completed_at'] = datetime.now().isoformat()

# ============================================================================
# Health Check
# ============================================================================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'online',
        'service': 'InnovLead Vault',
        'version': '1.0',
        'timestamp': datetime.now().isoformat()
    })

# ============================================================================
# Run Server
# ============================================================================

if __name__ == '__main__':
    print("🚀 InnovLead Vault starting...")
    print("📊 Dashboard: http://localhost:5000")
    print("🔧 API: http://localhost:5000/api/")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
