# =========================
# MINIO / S3 CONFIG
# =========================
from pathlib import Path
from environs import Env

BASE_DIR = Path(__file__).resolve().parent.parent

env = Env()
env.read_env()


AWS_ACCESS_KEY_ID = env('DOCKER_COMPOSE_MINIO_ROOT_USER',"")
AWS_SECRET_ACCESS_KEY = env('DOCKER_COMPOSE_MINIO_ROOT_PASSWORD',"")

AWS_STORAGE_BUCKET_NAME = "videos"
AWS_S3_REGION_NAME = "us-east-1"

AWS_S3_ENDPOINT_URL = "http://minio:9000"

AWS_S3_SIGNATURE_VERSION = "s3v4"

AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None

AWS_QUERYSTRING_AUTH = True
