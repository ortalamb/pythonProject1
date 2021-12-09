""" A personalized multiple choice quiz questions"""
from flask import Flask, request, redirect, url_for

"""Extracting the data from the files into 2 lists """

question = ""
questions = []
for line in open('questions.txt'):
    if line != '\n':
        question += line
    else:
        questions.append(question)
        question = ""

answers=[line.strip()for line in open('answers.txt')]

"""Building the server """

app = Flask(__name__)

@app.route('/')
def index():
    login= f"""
            <h1>Login Form</h1>
            <form action="/login" method="post">
            <label for="uname"><b>Username</b></label>
            <input type="text" placeholder="Enter Username" name="uname" required>
            <input type="submit" value="Login">
            </form>"""
    return login

@app.route('/login', methods=['POST'])
def login():
    info = request.form
    username=info.get('uname')
    return redirect(url_for('form', username=username))

@app.route('/form/<username>')
def form(username):
    result = f"""<h1> Here is your quiz {username}</h1>
    <body style="background-color:powderblue;">
    <form action="/submit/{username}" method="post">"""
    for i, question in enumerate(questions):
        result += f"""
    <h2>Question # {i+1}</h2>
    <pre>{question}</pre>
    <form action="/submit" method="post">
    <label for="ans{i}">Your answer is:</label><br>
    <input type="text" id="ans{i}" name="ans{i}" value=""><br><br>
    """
    result+=f"""<input type="submit" value="Submit">
    </form>"""
    return result

@app.route('/submit/<username>', methods=['POST'])
def submit(username):
    data= request.form
    score = 0
    for i,ans in enumerate(answers):
        if ans == data[f"ans{i}"]:
            score += 1
    result=f"""<h1 style="background-color:Orange;"><center>{username} your score is {score}/{len(answers)}</center></h1>"""
    if score/len(answers)==1:
        result+=f"""
        <h1 style="background-color:Yellow;"><center>Excellent!!!</center></h1>"""
    elif score/len(answers)>0.5:
        result += f"""
        <h1 style="background-color:Yellow;"><center>Good job!</center></h1>"""
    else:
        result += f"""
                <h1 style="background-color:Yellow;"><center>Try again 😉 </center></h1>"""
    return result

if __name__ == '__main__':
 app.run(debug=True)