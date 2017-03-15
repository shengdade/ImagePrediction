import os

from flask import render_template, request, url_for

from app import webapp
from classify import classify_image

# This is the path to the upload directory
webapp.config['UPLOAD_FOLDER'] = 'app/static/'
# These are the extension that we are accepting to be uploaded
webapp.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'JPG', 'jpeg', 'gif'}


# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in webapp.config['ALLOWED_EXTENSIONS']


@webapp.route('/', methods=['GET'])
@webapp.route('/index', methods=['GET'])
@webapp.route('/main', methods=['GET'])
def index():
    loading_gif = url_for('static', filename='loading.gif')
    return render_template('index.html', imgURL=loading_gif)


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
        file_path = os.path.join(webapp.config['UPLOAD_FOLDER'], filename)
        user_file.save(file_path)
        prediction_list = classify_image(file_path)
        print prediction_list
        return render_template('classify.html', prediction=prediction_list, filename=filename)
    else:
        return render_template('index.html')
