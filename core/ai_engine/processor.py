from groq import Groq

class AIProcessor:
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"

    def get_analysis(self, text, system_prompt):
        """إرسال النص للمطابقة الصارمة مع معايير BAU"""
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"حلل الوثيقة التالية بناءً على قالب BAU الصارم: {text[:15000]}"}
                ],
                temperature=0.1 
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"خطأ في الاتصال بـ Groq: {str(e)}"