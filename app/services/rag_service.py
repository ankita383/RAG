from app.ingestion.pdf_loader import process_pdf

vector_store = None

def upload_pdf(file_path):
    global vector_store
    vector_store = process_pdf(file_path)
    return {"message": "PDF processed successfully"}


def get_retriever():
    if vector_store is None:
        raise ValueError("Upload a PDF first")
    return vector_store.as_retriever(search_kwargs={"k": 3})