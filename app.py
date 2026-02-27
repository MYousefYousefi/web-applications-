from flask import Flask, render_template, request, redirect, send_file, jsonify
import pandas as pd
import json
from io import BytesIO

app = Flask(__name__)

# Tasks kist in memory
tasks = []

# read from JSON file if available
try:
    with open('tasks.json', 'r') as f:
        tasks = json.load(f)

except :
    tasks = []
    
def save_tasks():
    with open('tasks.json', 'w') as f:
        json.dump(tasks, f, indent=4)
    
@app.route('/', methods=['GET', 'POST'])
def index():
    global tasks
    if request.method == 'POST':
        # add new from Task form
        title = request.form.get('title')
        description = request.form.get('description')
        status = request.form.get('status')
        if title :
            tasks.append({
                'title' : title,
                'description' : description,
                'status' : status
            })
            save_tasks()
        return redirect('/')
    return render_template('index.html', tasks=tasks)

@app.route('/delete.<int:index>')
def delete_task(index):
    global tasks
    if 0 <= index < len(tasks):
        tasks.pop(index)
        save_tasks()
    return redirect('/')

@app.route('/edit/<int:index>', methods=['Post'])
def edit_task(index):
    global tasks
    if 0 <= index < len(tasks):
        tasks[index]['title'] = request.form.get('title')
        tasks[index]['description'] = request.form.get('description')
        tasks[index]['status'] = request.form.get('status')
        save_tasks()
    return redirect('/')

@app.route('/import_excel', methods=['POST'])
def import_excel():
    global tasks
    file = request.files['file']
    if file:
        df = pd.read_excel(file)
        for _, row in df.iterrows():
            tasks.append({
                'title': row.get('title', ''),
                'description': row.get('description', ''),
                'status': row.get('status', 'Pending')
            })
        save_tasks()
    return redirect('/')

@app.route('/download_jason')
def download_json():
    json_data = json.dumps(tasks, indent=4)
    buffer = BytesIO()
    buffer.write(json_data.encode())
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='tasks.jason', mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True)

            