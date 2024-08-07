from flask import Blueprint, render_template, request, redirect, flash, url_for, send_from_directory
from form import UploadForm
from werkzeug.utils import secure_filename
import os
from flask_login import login_required, current_user
from model import User, Posts, Images
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
    if request.method == 'GET':
        form = UploadForm()
        return render_template('upload.html', form=form)

    form = UploadForm(request.form)

    if form.validate_on_submit():
        title = form.title.data
        files = form.files.data

        try:
            new_post = Posts(title=title, user_id=current_user.id)
            db.session.add(new_post)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash('An error occured. Try Again!', 'danger')
            return redirect(request.url)

        if not files:
            flash('No files selected!', 'danger')
            return redirect(request.url)

        uploads = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config[UPLOAD_FOLDER], filename))
                
                try:
                    image = Images(filename=filename, post_id=new_post.id)
                    db.session.add(image)
                    db.session.commit()
                    uploads.append(filename)
                except Exception as e:
                    db.session.rollback()
                    flash('An error occured. Try Again!', 'danger')
                    return redirect(request.url)
        if uploads:
            return redirect(url_for('post.uploads'))
        else:
            flash('No photo was uploaded. Try Again!', 'danger')
            return redirect(request.url)
    else:
        return jsonify({'errors': form.errors}), 400


@post.route('/uploads')
@login_required
def uploads():
    posts = Posts.query.filter_by(user_id=current_user.id).options(joinedload(Posts.images)).all()
    return render_template('uploads.html', posts=posts)

@post.route('/send_images/<filename>')
def send_images(filename):
    return send_from_directory(app.config[UPLOAD_FOLDER], filename)
