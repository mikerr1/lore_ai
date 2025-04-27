import os
from langchain_community.document_loaders import PyPDFLoader


from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))
LORE_FILES_DIR = os.path.join(PROJECT_DIR, os.environ.get("LORE_FILES_DIR"))
LORE_DB_DIR = os.path.join(PROJECT_DIR, os.environ.get("LORE_DB_DIR"))

lore_file = "Tolkien-J.-The-lord-of-the-rings-HarperCollins-ebooks-2010.pdf"
lore_file = os.path.join(LORE_FILES_DIR, lore_file)


def load_pdf(file:str):
    content = []
    print("Starting PDF loader")
    loader = PyPDFLoader(file)
    content.extend(loader.load())
    print("Load pdf completed")
    return content

file_content = load_pdf(lore_file)
print(file_content)

# Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(file_content)

# Load embedding model
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Vector store
db = Chroma(
    collection_name="lore_collection",
    persist_directory=LORE_DB_DIR,
    embedding_function=embedding_model
)
db.add_documents(chunks)
db.persist()

print(f"✅ Ingested {len(chunks)} lore chunks into ChromaDB!")
