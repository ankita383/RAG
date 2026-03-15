from fastapi import APIRouter, UploadFile, File
import shutil
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
import os
from dotenv import load_dotenv
from app.services.rag_service import upload_pdf, get_retriever

load_dotenv()

router = APIRouter()

llm = ChatGroq(
   model="llama-3.1-8b-instant",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)

@router.post("/upload_pdf")
async def upload_pdf_route(file: UploadFile = File(...)):
    file_path = f"data/uploaded_pdfs/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return upload_pdf(file_path)


@router.post("/ask")
async def ask_question(question: str):
    retriever = get_retriever()
    docs = retriever.invoke(question)
    context = "\n\n".join([doc.page_content for doc in docs])
    prompt = f"""
    Answer the question using the context below.
    Context:
    {context}
    Question:
    {question}
    """
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"answer": response.content}