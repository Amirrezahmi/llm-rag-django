from django.conf import settings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from .extractor import extract_text


def get_vectorstore():
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=settings.OPENROUTER_API_KEY,
        openai_api_base="https://openrouter.ai/api/v1",
        http_client=None,
    )
    return Chroma(
        persist_directory=settings.CHROMA_PERSIST_DIR,
        embedding_function=embeddings,
    )


def index_document(document):
    file_path = document.file.path
    text = extract_text(file_path)

    document.content = text
    document.is_indexed = False
    document.save(update_fields=['content', 'is_indexed'])

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    chunks = text_splitter.split_text(text)

    vectorstore = get_vectorstore()
    vectorstore.add_texts(
        texts=chunks,
        metadatas=[{'document_id': document.id, 'title': document.title} for _ in chunks],
        ids=[f"doc_{document.id}_chunk_{i}" for i, _ in enumerate(chunks)],
    )

    document.is_indexed = True
    document.save(update_fields=['is_indexed'])


def delete_document_index(document_id: int):
    vectorstore = get_vectorstore()
    results = vectorstore.get(where={'document_id': document_id})
    if results and results.get('ids'):
        vectorstore.delete(ids=results['ids'])

