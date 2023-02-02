from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
import surveys

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

survey = surveys.satisfaction_survey

@app.route('/')
def satisfaction():
    
    return render_template('satisfaction.html', survey=survey)


@app.route('/questions/<int:num>')
def questions(num):
    answers = session['responses']
    if len(answers) < num or num < len(answers):
        flash('Invalid question! Redirecting...')
        return redirect(f'/questions/{len(answers)}')
    elif num == len(survey.questions):
        return redirect('/thankyou')
    else:
        question = surveys.satisfaction_survey.questions[num]
        return render_template('questions.html', question=question, num=num)

@app.route('/answer', methods=['POST'])
def answers():
    answers = session['responses']
    answer = request.form.get('answer')
    answers.append(answer)
    session['responses'] = answers
    return redirect(f'/questions/{len(answers)}')

@app.route('/thankyou')
def thanks():
    return "<h1>Thank You!</h1>"

@app.route('/session', methods = ['POST'])
def startSession():
    session["responses"] = []
    return redirect('/questions/0')