from django.conf import settings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from .indexer import get_vectorstore
from documents.models import Document


PROMPT_TEMPLATE = """
تو یک دستیار هوشمند هستی که وظیفه‌ات پاسخگویی دقیق و فقط بر اساس اسناد ارائه‌شده است.
حتی اگر سوال بد، مبهم، بی‌ربط یا بدترین شکل ممکن پرسیده شده باشد، باید بهترین پاسخ ممکن را از درون اسناد استخراج کنی.
به هیچ وجه از اطلاعات بیرونی یا دانش قبلی خود استفاده نکن. اگر سوال به هیچ وجه در اسناد پوشش داده نشده، بگو: "اطلاعات کافی وجود ندارد."
پاسخ باید کاملاً وفادار به متن اسناد باشد، بدون افزودن تفسیر شخصی یا فرضیات.
زبان پاسخ دقیقاً همان زبانی باشد که سوال با آن پرسیده شده است.

اسناد مرتبط:
{context}

سوال: {question}

پاسخ:
"""


def get_llm():
    return ChatOpenAI(
        model=settings.LLM_MODEL,
        openai_api_key=settings.OPENROUTER_API_KEY,
        openai_api_base=settings.OPENROUTER_BASE_URL,
        temperature=0.3,
        default_headers={
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "LLM RAG Django",
        }
    )


def get_answer(question_text: str) -> dict:
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(
        search_type='similarity',
        search_kwargs={'k': 6},
    )

    docs = retriever.invoke(question_text)

    # حذف chunk های تکراری
    seen = set()
    unique_docs = []
    for doc in docs:
        if doc.page_content not in seen:
            seen.add(doc.page_content)
            unique_docs.append(doc)

    # مرتب‌سازی بر اساس طول متن (chunk های طولانی‌تر معمولاً اطلاعات بیشتری دارند)
    unique_docs.sort(key=lambda x: len(x.page_content), reverse=True)
    top_docs = unique_docs[:4]

    context = '\n\n---\n\n'.join([
        f"از سند «{doc.metadata.get('title', 'نامشخص')}»:\n{doc.page_content}"
        for doc in top_docs
    ])

    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    llm = get_llm()
    chain = prompt | llm | StrOutputParser()
    answer = chain.invoke({'context': context, 'question': question_text})

    sources = []
    for doc in top_docs:
        doc_id = doc.metadata.get('document_id')
        try:
            document = Document.objects.get(id=doc_id)
        except Document.DoesNotExist:
            document = None
        sources.append({
            'document': document,
            'chunk': doc.page_content,
        })

    return {
        'answer': answer,
        'sources': sources,
    }
