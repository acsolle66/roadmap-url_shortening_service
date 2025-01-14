import os
from pathlib import Path
from environs import Env

env = Env()
env.read_env()

MONGO_URI = env.str("MONGO_URI")

BASE_DIR = Path(__file__).resolve().parent

STATIC_PATH = Path("pages/static")
STATIC_ROOT = os.path.join(BASE_DIR, STATIC_PATH)

TEMPLATE_PATH = Path("pages/templates")
TEMPLATE_ROOT = os.path.join(BASE_DIR, TEMPLATE_PATH)
