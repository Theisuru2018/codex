# MCQ Manager

This project provides a simple web application to create multiple choice questionnaires (MCQ), mark them manually or via optical mark recognition (OMR) using Auto Multiple Choice (AMC), and export results to Excel.

## Features

- Create quizzes with up to 10 questions and four options per question.
- Generate answer sheets that can be printed for students.
- Mark completed sheets manually by clicking selected answers.
- Placeholder function for integrating AMC to process scanned sheets.
- Export results to Excel with index numbers, per-question grades, and total score.

## Installation

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the application:

```bash
python app/app.py
```

The server will start at `http://127.0.0.1:5000`.

## Notes

- OMR processing requires [Auto Multiple Choice](https://www.auto-multiple-choice.net/) and is not fully implemented in this example. The `process_scanned_sheet` function should be adapted to call AMC commands and update results accordingly.
- Results and quiz data are stored in `app/data/` as JSON files.
