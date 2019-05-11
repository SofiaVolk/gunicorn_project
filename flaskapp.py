from flask import Flask

app = Flask(__name__)
# mysql+pymysql://username:password@server/db
str = f"mysql+pymysql://root:atom_pass@127.0.0.1/atom_db?charset=utf8mb4"
app.config['SQLALCHEMY_DATABASE_URI'] = str
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_RECORD_QUERIES'] = True

