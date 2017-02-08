import os
# We'll render HTML templates and access data sent by POST
# using the request object from flask. Redirect and url_for
# will be used to redirect the user once the upload is done
# and send_from_directory will help us to send/show on the
# browser the file that the user just uploaded
from flask import render_template, request, redirect, url_for

# Initialize the Flask application
from app import webapp

# Import classification function
from classify import classify_image

# This is the path to the upload directory
webapp.config['UPLOAD_FOLDER'] = 'app/static/'
# These are the extension that we are accepting to be uploaded
webapp.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in webapp.config['ALLOWED_EXTENSIONS']


# This route will show a form to perform an AJAX request
# jQuery is loaded to execute the request and update the
# value of the operation
@webapp.route('/')
def index():
    return render_template('index.html')


# Route that will process the file upload
@webapp.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded user_file
    user_file = request.files['file']
    # Check if the user_file is one of the allowed types/extensions
    if user_file and allowed_file(user_file.filename):
        # Make the filename safe, remove unsupported chars
        filename = user_file.filename
        # Move the user_file form the temporal folder to
        # the upload folder we setup
        user_file.save(os.path.join(webapp.config['UPLOAD_FOLDER'], filename))
        # Redirect the user to the uploaded_file route, which
        # will basically show on the browser the uploaded user_file
        return redirect(url_for('classify', filename=filename))


# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@webapp.route('/uploads/<filename>', methods=['GET'])
def classify(filename):
    file_path = os.path.join(webapp.config['UPLOAD_FOLDER'], filename)
    prediction_list = classify_image(file_path)
    print prediction_list
    return render_template('classify.html', prediction=prediction_list, filename=filename)
