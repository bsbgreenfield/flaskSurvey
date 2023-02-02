from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
import surveys

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

responses = []
survey = surveys.satisfaction_survey

@app.route('/')
def satisfaction():
    
    return render_template('satisfaction.html', survey=survey)


@app.route('/questions/<int:num>')
def questions(num):
    if len(responses) < num or num < len(responses):
        flash('Invalid question! Redirecting...')
        return redirect(f'/questions/{len(responses)}')
    elif num == len(survey.questions):
        return redirect('/thankyou')
    else:
        question = surveys.satisfaction_survey.questions[num]
        return render_template('questions.html', question=question, num=num)

@app.route('/answer/', methods=['POST'])
def answers():
    answer = request.form.get('answer')
    responses.append(answer)
    return redirect(f'/questions/{len(responses)}')

@app.route('/thankyou')
def thanks():
    return "<h1>Thank You!</h1>"
