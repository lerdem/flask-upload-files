from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename
from uuid import uuid4


app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = 'static'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////{}/filestorage.db'.format(BASE_DIR)
# sudo apt install sqlite3
# sqlite3 filestorage.db
# для установки и создания БД

# для создания таблици в интерпритеторе python запустите команды
# >>> from app import db
# >>> db.create_all()
# >>> exit()

db = SQLAlchemy(app)


class FileContents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    path_to_file = db.Column(db.String(400))


def create_upload_folder():
    if not os.path.exists(os.path.join(BASE_DIR, UPLOAD_FOLDER)):
        os.mkdir(os.path.join(BASE_DIR, UPLOAD_FOLDER))




@app.route('/')
def index():
    create_upload_folder()
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['inputFile']
    new_file_name = '{}{}'.format(uuid4(), secure_filename(file.filename))
    path = os.path.join(BASE_DIR, UPLOAD_FOLDER, new_file_name)
    file.save(path)
    new_file = FileContents(name=new_file_name, path_to_file=path)
    db.session.add(new_file)
    db.session.commit()
    return 'Файл {} сохранен в БД'.format(new_file_name)


@app.route('/show-all')
def show_all():
    file_data = FileContents.query.all()
    return render_template('show-all.html', file_data=file_data)


if __name__ == '__main__':
    app.run(debug=True)
