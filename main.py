
import smtplib
import os

from flask import Flask, render_template, flash
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, EmailField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email
from secrets import token_hex


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')

app = Flask(__name__)
app.config['SECRET_KEY'] = token_hex(16)


csrf = CSRFProtect()
csrf.init_app(app)
Bootstrap5(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact_page():
    form = ContactForm()

    if form.validate_on_submit():

        # Send email here
        try:
            with smtplib.SMTP('smtp.gmail.com') as connection:
                connection.starttls()
                connection.login(user=os.environ.get('SENDER_EMAIL'), password=os.environ.get('SENDER_PASSWORD'))
                connection.sendmail(from_addr=form.email.data,
                                    to_addrs=os.environ.get('RECEIVER_EMAIL'),
                                    msg=f"Subject:New Message from site\n\n"
                                        f"Name: {form.name.data}\n"
                                        f"Email: {form.email.data}\n"
                                        f"Message: {form.message.data}")

            form = ContactForm()
            flash('Message sent successfully!', 'success')
        except Exception as e:
            print(e)
            flash('Message was not sent, please try again later.', 'danger')

    return render_template('contact.html', form=form)

@app.route('/projects')
def projects_page():
    return render_template('projects.html')

if __name__ == '__main__':
    app.run(debug=True)