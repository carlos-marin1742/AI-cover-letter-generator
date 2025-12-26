from flask import Flask, request, render_template
import os
from logic import generate_letter

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def handle_generate():
    #getting data from form
    job_description = request.form['job_description']
    resume_file = request.files['resume']

    #saving the file temporarily
    file_path=os.path.join(app.config['UPLOAD_FOLDER'], resume_file.filename)
    resume_file.save(file_path)

    #calling the logic function to generate cover letter
    cover_letter = generate_letter(file_path, job_description) 

    #showinng the result in the result.html template
    return render_template('result.html', cover_letter=cover_letter)

if __name__ == '__main__':
    app.run(debug=True)