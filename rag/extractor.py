from docx import Document as DocxDocument


def extract_text_from_docx(file_path: str) -> str:
    doc = DocxDocument(file_path)
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    return '\n'.join(paragraphs)


def extract_text(file_path: str) -> str:
    if file_path.endswith('.docx'):
        return extract_text_from_docx(file_path)
    raise ValueError(f"Unsupported file format: {file_path}")
