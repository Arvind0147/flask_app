from flask import Flask, request, render_template, jsonify
from google.cloud import storage
import os
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import logging

load_dotenv()

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mssql+pyodbc://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}?"
    "driver=ODBC+Driver+17+for+SQL+Server"
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create the SQLAlchemy db instance
db = SQLAlchemy(app)
def test_conn():
    try:
        logger.info("Attempting database connection...")
        result = db.session.execute(text('SELECT 1')).scalar()
        logger.info(f"Query result: {result}")
        if result == 1:
            logger.info("Database connection successful")
            return True
        else:
            logger.warning(f"Unexpected result from database: {result}")
            return False
    except SQLAlchemyError as e:
        logger.error(f"Database error occurred: {str(e)}")
        return False
    finally:
        logger.info("Closing database session")
        db.session.close()

# Configure this to your GCP project and bucket
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'theta-wave-400523-1ce6711951a9.json'
BUCKET_NAME = 'flask_app_bucket'

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file:
            # Create a Cloud Storage client
            storage_client = storage.Client()

            # Get the bucket
            bucket = storage_client.get_bucket(BUCKET_NAME)

            # Create a new blob and upload the file's content
            blob = bucket.blob(file.filename)
            blob.upload_from_string(
                file.read(),
                content_type=file.content_type
            )

            # Test database connection
            db_connected = test_conn()

            if db_connected:
                return f'Database connection successful!    File {file.filename} uploaded to {BUCKET_NAME}.'
            else:
                return f'File {file.filename} uploaded to {BUCKET_NAME}, but database connection failed.'
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)