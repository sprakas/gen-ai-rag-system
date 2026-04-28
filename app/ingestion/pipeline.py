from pathlib import Path

from langchain_community.document_loaders import TextLoader, PyPDFLoader


DATA_DIR = Path(__file__).resolve().parents[1] / "data"

TEXT_EXTENSIONS = {".txt", ".md", ".markdown"}


def load_all_docs():
    documents = []
    text_dir = DATA_DIR / "docs"
    pdf_dir = DATA_DIR / "pdfs"

    # Load text and markdown files (recursively)
    if text_dir.exists():
        for file_path in text_dir.rglob("*"):
            if not file_path.is_file():
                continue
            ext = file_path.suffix.lower()
            if ext in TEXT_EXTENSIONS:
                loader = TextLoader(str(file_path), autodetect_encoding=True)
                documents.extend(loader.load())

    # Load PDFs (recursively)
    if pdf_dir.exists():
        for file_path in pdf_dir.rglob("*.pdf"):
            if file_path.is_file():
                loader = PyPDFLoader(str(file_path))
                documents.extend(loader.load())

    return documents
