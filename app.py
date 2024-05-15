from flask import Flask, render_template, redirect, url_for, request, session
import os
from itertools import groupby

import multiprocessing
import argparse

import analyzer_classes
import analysis_results


# analyzers.Goblint(), analyzers.Locksmith(), 
analyzers_list = [analyzer_classes.Goblint(), analyzer_classes.Locksmith(), analyzer_classes.Relay()]

app = Flask(__name__, static_url_path='/static')

results_folder = './static/files/results'
upload_files_folder = './static/files/uploaded_files'
app.config['UPLOAD_FOLDER'] = upload_files_folder
app.config['SECRET_KEY'] = 'saladus'



def analyze_file(file, filename):

    filename_no_ext = os.path.splitext(filename)[0]
    with open(f'{upload_files_folder}/{filename}', 'wb') as f:
        f.write(file)

    processes = [multiprocessing.Process(target=target.run_analyzer(filename_no_ext)) for target in analyzers_list]

    for process in processes:
        process.start()
    for process in processes:
        process.join()

# on True ainult juhul kui fail ise ja kõikide analüsaatorite tulemuste failid eksisteerivad
def file_previously_analyzed(filename):
    if os.path.exists(os.path.join( upload_files_folder, filename)):
        if os.path.exists(os.path.join(results_folder, os.path.splitext(filename)[0])):
            for analyzer in analyzers_list:
                analyzer_file = analyzer.name + '.txt'
                if not os.path.exists(os.path.join(results_folder, os.path.splitext(filename)[0], analyzer_file)):
                    return False
            return True
    return False

def list_uploaded_files():
    return os.listdir(upload_files_folder)

@app.route('/', methods=['GET', 'POST'])
def upload():

    existing_files = list_uploaded_files()

    if request.method == 'POST':

        if 'file' in request.files:

            uploaded_file = request.files['file']
            filename = uploaded_file.filename
            
            if filename.endswith('.c'):
                # sessiooni jaoks faili sisu ja faili nimi 
                session['uploaded_file'] = uploaded_file.read()
                session['filename'] = filename
                if file_previously_analyzed(filename):
                    return redirect(url_for('handle_existing_file'))
                else: 
                    analyze_file(session['uploaded_file'], filename)
                    return redirect(url_for('results', filename=filename))
            else:
                return render_template('upload.html', message="Please upload a C file.", existing_files=existing_files)
            
        # kui fail mis juba varem salvestatud
        elif 'existing_file' in request.form:
            filename = request.form['existing_file']
            return redirect(url_for('results', filename=filename))
        
    return render_template('upload.html', existing_files=existing_files)


@app.route('/get_file_contents', methods=['POST'])
def get_file_contents():
    filename = request.json['filename']
    file_path = os.path.join(upload_files_folder, filename)
    
    with open(file_path, 'r') as f:
        file_contents = f.read()
    
    return file_contents


@app.route('/handle_existing_file', methods=['GET', 'POST'])
def handle_existing_file():
    if 'uploaded_file' in session and 'filename' in session:
        uploaded_file = session['uploaded_file']
        filename = session['filename']

        if request.method == 'POST':
            action = request.form['action']

            if action == 'save':
                analyze_file(uploaded_file, filename)
                return redirect(url_for('results', filename=filename))
            elif action == 'discard':
                return redirect(url_for('results', filename=filename))
        return render_template('handle_existing_file.html', filename=filename)
    else:
        # kui jama siis algusesse tagasi
        return redirect(url_for('upload'))

@app.route('/results/<filename>')
def results(filename):
    
    filename_no_ext = os.path.splitext(filename)[0]

    results = []
    analyzers_for_table = []

    for analyzer in analyzers_list:
        single_res = analyzer.find_race_lines(filename_no_ext)
        results += flatten_groups(analyzer.name, single_res)
        analyzers_for_table.append(analyzer.name)

    results = sorted(results, key=lambda info: info.line.loc)

    dres = {}
    for k,v in groupby(results, key=lambda info: info.line.loc):
        dres[k] = list(v)
    
    return render_template('results.html', filename=filename, analysis_results=dres, analyzers_for_table=analyzers_for_table)

def flatten_groups(analyzer, groups):
    x = []
    for group in groups:
        for access in group.accesses:
            flat_line_info = analysis_results.FlatLineInfo(access, group, analyzer)

            x.append(flat_line_info)

    return x

@app.context_processor
def my_utils():
    def get_analyzer_line(analyzer, flat_line_list):
        return [line.line.info for line in flat_line_list if line.analyzer == analyzer]
    
    def get_analyzer_group(analyzer, flat_line_list):
        result = []
        for line in flat_line_list:
            if line.analyzer == analyzer and line.group.info not in result:
                result.append(line.group.info)


        return result

    def get_analyzers(line_list):
        return [line.analyzer for line in line_list]
    
    def get_targetvars(line_list):
        targetvars = set()
        for line in line_list:
            targetvars.add(line.group.targetvar)
        return targetvars
    
    return dict(get_analyzer_line=get_analyzer_line, get_analyzer_group=get_analyzer_group,get_analyzers=get_analyzers, get_targetvars=get_targetvars)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version', version='CoOpeRace version: 1.0')
    args = parser.parse_args()
    app.run(debug=True, host='192.168.42.141', port=5000)
