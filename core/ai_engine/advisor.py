from .processor import AIProcessor
from .prompts import SYSTEM_PROMPT

class ProjectAdvisor:
    def __init__(self, api_key):
        self.processor = AIProcessor(api_key)
    
    def check_quality(self, text):
        return self.processor.get_analysis(text, SYSTEM_PROMPT)