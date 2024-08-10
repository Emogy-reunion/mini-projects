from flask import Blueprint, render_template, request, redirect, jsonify, url_for, send_from_directory, current_app
from form import UploadForm
from werkzeug.utils import secure_filename
import os
from flask_login import login_required, current_user
from model import User, Posts, Images, db
from sqlalchemy.orm import joinedload 


post = Blueprint('post', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    # checks if it is a valid file
    if '.' in filename:
        
        # split the file once from the right using the . as a benchmark
        parts = filename.rsplit('.', 1)
        file_extension = parts[1].lower() # convert the extension to lowercase
        if file_extension in ALLOWED_EXTENSIONS:
            return True
        else:
            return False
    else:
        return False # if no . it cannot contain a valid extension

@post.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    ''' 
    handles uploading of files
    '''
    form = UploadForm()

    if request.method == 'POST':
        form = UploadForm(request.form)
        if form.validate_on_submit():
            title = form.title.data


            if 'files' not in request.files:
                return jsonify({'error': 'No file part in the request. Please make sure to select files for upload.'})

            files = request.files.getlist('files')

            if not files:
                return jsonify({'error': 'No files were selected. Please choose at least one file to upload.'})

            try:
                new_post = Posts(title=title, user_id=current_user.id)
                db.session.add(new_post)
                db.session.commit()

                uploads = []
                for file in files:
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)

                        # Use `current_app` to access the configuration
                        upload_folder = current_app.config['UPLOAD_FOLDER']
                        file.save(os.path.join(upload_folder, filename))
                        image = Images(filename=filename, post_id=new_post.id)
                        db.session.add(image)
                        db.session.commit()
                        uploads.append(filename)
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': 'An unexpected error occured. Try Again!'})

            if uploads:
                return jsonify({'success': 'Uploaded successfully!'})
            else:
                return jsonify({'error': "Failed to upload"})
        else:
            return jsonify({'errors': form.errors})

    return render_template('upload.html', form=form)


@post.route('/uploads')
@login_required
def uploads():
    return render_template('uploads.html')

@post.route('/posts')
@login_required
def posts():
    uploads = Posts.query.filter_by(user_id=current_user.id).order_by(Posts.created_at.desc()).options(joinedload(Posts.images)).all()
    
    posts = []
    for upload in uploads:
        posts.append({
            'title': post.title,
            'created_at': post.created_at,
            'image': post.images[0]
            })
    return jsonify({'posts': posts})

@post.route('/send_images/<filename>')
def send_images(filename):
    return send_from_directory(app.config[UPLOAD_FOLDER], filename)
