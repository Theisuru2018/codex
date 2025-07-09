import os
import json
from flask import Flask, render_template, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename
import pandas as pd

app = Flask(__name__)
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
QUIZ_FILE = os.path.join(DATA_DIR, 'quizzes.json')
RESULTS_DIR = os.path.join(DATA_DIR, 'results')

os.makedirs(RESULTS_DIR, exist_ok=True)


def load_quizzes():
    if os.path.exists(QUIZ_FILE):
        with open(QUIZ_FILE, 'r') as f:
            return json.load(f)
    return {}


def save_quizzes(data):
    with open(QUIZ_FILE, 'w') as f:
        json.dump(data, f, indent=2)


@app.route('/')
def index():
    quizzes = load_quizzes()
    return render_template('index.html', quizzes=quizzes)


@app.route('/quiz/new', methods=['GET', 'POST'])
def new_quiz():
    if request.method == 'POST':
        quizzes = load_quizzes()
        qid = str(len(quizzes) + 1)
        title = request.form['title']
        questions = []
        for i in range(1, 11):
            text = request.form.get(f'q{i}')
            if not text:
                continue
            options = [request.form.get(f'q{i}_o{j}') for j in range(1, 5)]
            answer = request.form.get(f'q{i}_ans')
            questions.append({
                'text': text,
                'options': options,
                'answer': int(answer) if answer is not None else None
            })
        quizzes[qid] = {'title': title, 'questions': questions}
        save_quizzes(quizzes)
        return redirect(url_for('index'))
    return render_template('new_quiz.html')


@app.route('/sheet/<quiz_id>')
def sheet(quiz_id):
    quizzes = load_quizzes()
    quiz = quizzes.get(quiz_id)
    if not quiz:
        return 'Quiz not found', 404
    return render_template('sheet.html', quiz=quiz, quiz_id=quiz_id)


@app.route('/mark/manual/<quiz_id>', methods=['GET', 'POST'])
def manual_mark(quiz_id):
    quizzes = load_quizzes()
    quiz = quizzes.get(quiz_id)
    if not quiz:
        return 'Quiz not found', 404
    if request.method == 'POST':
        index_number = request.form['index']
        answers = [int(request.form.get(f'q{i}', 0)) for i in range(len(quiz['questions']))]
        score = 0
        per_q = []
        for i, ans in enumerate(answers):
            correct = quiz['questions'][i]['answer']
            if ans == correct:
                score += 1
                per_q.append(1)
            else:
                per_q.append(0)
        result_file = os.path.join(RESULTS_DIR, f'{quiz_id}.json')
        if os.path.exists(result_file):
            with open(result_file, 'r') as f:
                results = json.load(f)
        else:
            results = {}
        results[index_number] = {'answers': answers, 'per_q': per_q, 'score': score}
        with open(result_file, 'w') as f:
            json.dump(results, f, indent=2)
        return redirect(url_for('manual_mark', quiz_id=quiz_id))
    return render_template('manual_mark.html', quiz=quiz, quiz_id=quiz_id)


@app.route('/export/<quiz_id>')
def export_results(quiz_id):
    result_file = os.path.join(RESULTS_DIR, f'{quiz_id}.json')
    if not os.path.exists(result_file):
        return 'No results', 404
    with open(result_file, 'r') as f:
        results = json.load(f)
    rows = []
    for index, data in results.items():
        row = {'Index': index}
        for i, grade in enumerate(data['per_q'], start=1):
            row[f'Q{i}'] = grade
        row['Total'] = data['score']
        rows.append(row)
    df = pd.DataFrame(rows)
    xls_path = os.path.join(RESULTS_DIR, f'{quiz_id}.xlsx')
    df.to_excel(xls_path, index=False)
    return send_file(xls_path, as_attachment=True)


# Placeholder for scanned sheet processing via AMC
def process_scanned_sheet(file_path, quiz_id):
    """Process scanned sheet using AMC. This function is a placeholder."""
    # Here you would call AMC commands to recognize the sheet
    pass


if __name__ == '__main__':
    app.run(debug=True)
