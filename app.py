from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm

"""
# db create & connect
conn=sqlite3.connect('database.db')
print("create & connect database")

# table create
conn.execute(
    '''
    create table users(name text, password text)
    '''
)
print("create table")

conn.close()
"""

app = Flask(__name__)
app.config["SECRET_KEY"] = '123654'

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        return redirect(url_for('main'))
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)