from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + str(BASE_DIR) + '/filestorage.db'
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
    name = db.Column(db.String(300))
    data = db.Column(db.LargeBinary)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['inputFile']
    new_file = FileContents(name=file.filename, data=file.read())
    db.session.add(new_file)
    db.session.commit()
    return 'Файл {} сохранен в БД'.format(file.filename)

if __name__ == '__main__':
    print(BASE_DIR)
    print(app.config['SQLALCHEMY_DATABASE_URI'])
    app.run(debug=True)

