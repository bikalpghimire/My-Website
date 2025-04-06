from flask import Flask, flash, redirect, render_template, request, url_for
from forms import ContactForm
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

load_dotenv()


APP_SECRET_KEY = os.getenv('APP_SECRET_KEY')
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')
RECEIVER_EMAIL = os.getenv('RECEIVER_EMAIL')

# Initialize the Flask application
app = Flask(__name__)

app.secret_key = APP_SECRET_KEY

# Flask-Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = SENDER_EMAIL
app.config['MAIL_PASSWORD'] = SENDER_PASSWORD
app.config['MAIL_DEFAULT_SENDER'] = SENDER_EMAIL

# Initialize Flask-Mail
mail = Mail(app)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/projects')
def projects():
    return render_template('projects.html')


@app.route('/resume')
def resume():
    return render_template('resume.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # Access data with form.name.data, form.email.data, etc.
        print(f"Name: {form.name.data}")
        print(f"Email: {form.email.data}")
        print(f"Subject: {form.subject.data}")
        print(f"Message: {form.message.data}")

        # Prepare the email message
        msg = Message(
            subject=form.subject.data,
            recipients=[RECEIVER_EMAIL],
            body=f"""
            Name: {form.name.data}
            Email: {form.email.data}
            Subject: {form.subject.data}
            Message: {form.message.data}
            """,  # Plain text version of the email (for clients that don't support HTML)
            html=f"""
            <html>
                <body>
                    <h2>Contact Form Submission</h2>
                    <p><strong>Name:</strong> {form.name.data}</p>
                    <p><strong>Email:</strong> {form.email.data}</p>
                    <p><strong>Subject:</strong> {form.subject.data}</p>
                    <p><strong>Message:</strong></p>
                    <p>{form.message.data}</p>
                </body>
            </html>
            """  # HTML version of the email for better formatting
        )
        
        try:
            # Send the email
            mail.send(msg)
            flash('Message sent successfully!', 'success')
        except Exception as e:
            flash(f'Error sending message: {e}', 'danger')

        return redirect(url_for('contact'))
    return render_template("contact.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)