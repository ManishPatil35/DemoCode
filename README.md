import os
from google.cloud import storage
from dotenv import load_dotenv

# Load configuration from .env
load_dotenv()

BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")
UPLOAD_DIR = os.getenv("GCS_UPLOAD_DIR", "")
LOCAL_DIR = os.getenv("LOCAL_UPLOAD_DIR", "data/")
CREDENTIALS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")

# If credentials are explicitly defined, set the environment variable
if CREDENTIALS_PATH:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_PATH

def upload_files():
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_NAME)
    except Exception as e:
        print("❌ Failed to connect to GCS:", e)
        return

    files_uploaded = 0
    for filename in os.listdir(LOCAL_DIR):
        local_path = os.path.join(LOCAL_DIR, filename)

        if not os.path.isfile(local_path):
            continue

        blob_path = os.path.join(UPLOAD_DIR, filename).replace("\\", "/")
        blob = bucket.blob(blob_path)

        try:
            blob.upload_from_filename(local_path)
            print(f"✅ Uploaded {filename} → gs://{BUCKET_NAME}/{blob_path}")
            files_uploaded += 1
        except Exception as upload_error:
            print(f"❌ Failed to upload {filename}: {upload_error}")

    if files_uploaded == 0:
        print("⚠️  No files uploaded.")
    else:
        print(f"🎉 Done. {files_uploaded} files uploaded.")

if __name__ == "__main__":
    upload_files()