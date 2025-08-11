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


@app.route('/projects/rapid-exit-taxiway')
def project_rapid_exit_taxiway():
    return render_template('rapid-exit-taxiway.html')

@app.route('/projects/remote-apron-iapp')
def project_remote_apron_iapp():
    return render_template('remote-apron-iapp.html')

@app.route('/projects/international-terminal-roof')
def project_international_terminal_roof():
    return render_template('international-terminal-roof.html')

@app.route('/projects/shree-airlines-hangar')
def project_shree_airlines_hangar():
    return render_template('shree-airlines-hangar.html')

@app.route('/projects/medi-pride-hospital')
def project_medi_pride_hospital():
    return render_template('medi-pride-hospital.html')

@app.route('/projects/kushma-resort')
def project_kushma_resort():
    return render_template('kushma-resort.html')

@app.route('/projects/little-angels-school')
def project_little_angels_school():
    return render_template('little-angels-school.html')

@app.route('/projects/blitz-tower')
def project_blitz_tower():
    return render_template('blitz-tower.html')

@app.route('/projects/ksns-headquarters')
def project_ksns_headquarters():
    return render_template('ksns-headquarters.html')

@app.route('/projects/animal-sheds-design')
def project_animal_sheds_design():
    return render_template('animal-sheds-design.html')


@app.route('/resume')
def resume():
    return render_template('resume.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # Access data from the form
        print(f"Name: {form.name.data}")
        print(f"Email: {form.email.data}")
        print(f"Subject: {form.subject.data}")
        print(f"Message: {form.message.data}")

        # Prepare the email to the site owner/admin
        msg_to_admin = Message(
            subject=form.subject.data,
            recipients=[RECEIVER_EMAIL],
            body=f"""
            Name: {form.name.data}
            Email: {form.email.data}
            Subject: {form.subject.data}
            Message: {form.message.data}
            """,
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
            """
        )

        # Prepare the thank-you email to the user
        msg_to_user = Message(
            subject="Thank you for contacting us!",
            recipients=[form.email.data],
            body=f"""
            Hi {form.name.data},

            Thank you for reaching out to me. I have received your message and will get back to you as soon as possible.

            Here's a summary of your message:
            Subject: {form.subject.data}
            Message: {form.message.data}

            Best regards,
            Bikalp Ghimire
            """,
            html=f"""
            <html>
                <body>
                    <p>Hi {form.name.data},</p>
                    <p>Thank you for reaching out to me. I have received your message and will get back to you as soon as possible.</p>
                    <p><strong>Your message:</strong></p>
                    <p><strong>Subject:</strong> {form.subject.data}</p>
                    <p>{form.message.data}</p>
                    <br>
                    <p>Best regards,<br>Bikalp Ghimire</p>
                </body>
            </html>
            """
        )

        try:
            # Send both emails
            mail.send(msg_to_admin)
            mail.send(msg_to_user)
            flash('Message sent successfully! A confirmation email has been sent to you.', 'success')
        except Exception as e:
            flash(f'Error sending message: {e}', 'danger')

        return redirect(url_for('contact'))
    return render_template("contact.html", form=form)


if __name__ == '__main__':
    app.run()