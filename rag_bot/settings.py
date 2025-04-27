import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))
LORE_FILES_DIR = os.path.join(PROJECT_DIR, os.environ.get("LORE_FILES_DIR"))
if not os.path.exists(LORE_FILES_DIR):
    os.makedirs(LORE_FILES_DIR)

LORE_DB_DIR = os.path.join(PROJECT_DIR, os.environ.get("LORE_DB_DIR"))
if not os.path.exists(LORE_DB_DIR):
    os.makedirs(LORE_DB_DIR)

lore_file = "EJ1172284.pdf"
lore_file = os.path.join(LORE_FILES_DIR, lore_file)
