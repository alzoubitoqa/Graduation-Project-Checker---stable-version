import docx
from pypdf import PdfReader

class GraduationAI:
    def __init__(self, api_key):
        # المحرك لا يحتاج لتخزين المفتاح هنا لأننا نمرره للـ AIProcessor
        pass

    def extract_text(self, uploaded_file):
        """استخراج النص من PDF أو Word بناءً على نوع الملف المرفوع"""
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        try:
            if file_extension == 'pdf':
                reader = PdfReader(uploaded_file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() or ""
                return text
            
            elif file_extension == 'docx':
                doc = docx.Document(uploaded_file)
                text = [para.text for para in doc.paragraphs]
                return "\n".join(text)
            
            return None
        except Exception as e:
            return f"خطأ في قراءة الملف: {str(e)}"