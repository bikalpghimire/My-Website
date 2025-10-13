from flask import Flask, flash, redirect, render_template, request, url_for
from forms import ContactForm
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os
import resend

load_dotenv()


APP_SECRET_KEY = os.getenv('APP_SECRET_KEY')
resend.api_key = os.getenv('RESEND_API_KEY')

# Initialize the Flask application
app = Flask(__name__)

app.secret_key = APP_SECRET_KEY


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
        name = form.name.data
        email = form.email.data
        subject = form.subject.data
        message = form.message.data

        msg_to_admin = {
            "from": "My Website <bikalp@bikalpghimire.com.np>",
            "to": ["bikalpghimire@gmail.com"],
            "subject": f"New Contact Form Submission: {subject}",
            "html": f"""
                <h2>Contact Form Submission</h2>
                <p><strong>Name:</strong> {name}</p>
                <p><strong>Email:</strong> {email}</p>
                <p><strong>Subject:</strong> {subject}</p>
                <p><strong>Message:</strong></p>
                <p>{message}</p>
            """,
        }

        msg_to_user = {
            "from": "Bikalp <bikalp@bikalpghimire.com.np>",
            "to": [email],
            "subject": "Thank you for contacting me!",
            "html": f"""
                <p>Hi {name},</p>
                <p>Thank you for reaching out. I’ve received your message and will get back to you soon.</p>
                <p><strong>Your message:</strong> {message}</p>
                <br>
                <p>Best regards,<br><b>Bikalp Ghimire</b></p>
            """,
        }

        try:
            resend.Emails.send(msg_to_admin)
            resend.Emails.send(msg_to_user)
            flash('Message sent successfully!', 'success')
        except Exception as e:
            flash(f'Error sending message: {e}', 'danger')

        return redirect(url_for('contact'))

    return render_template("contact.html", form=form)


if __name__ == '__main__':
    app.run()