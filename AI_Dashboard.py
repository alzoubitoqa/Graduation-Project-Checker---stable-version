import streamlit as st
from core.ai_engine.advisor import ProjectAdvisor
from core.ai_engine_v2 import GraduationAI

# إعدادات الواجهة
st.set_page_config(page_title="BAU Strict Advisor", page_icon="🎓", layout="centered")

st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🎓 مدقق الجودة لمشروع التخرج لطلبة كلية الذكاء الاصطناعي - BAU</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>دعم ملفات PDF و Word | فحص الفصول </p>", unsafe_allow_html=True)

if "GROQ_API_KEY" in st.secrets:
    advisor = ProjectAdvisor(st.secrets["GROQ_API_KEY"])
    extractor = GraduationAI(st.secrets["GROQ_API_KEY"])

    # السماح برفع النوعين
    uploaded_file = st.file_uploader("📂 ارفع وثيقة المشروع (PDF أو Word)", type=['pdf', 'docx'])
    
    if uploaded_file:
        with st.spinner("🔍 جاري الفحص والمطابقة مع شروط جامعة البلقاء..."):
            text = extractor.extract_text(uploaded_file)
            if text:
                report = advisor.check_quality(text)
                
                st.divider()
                # عرض جوهر الفكرة والتقرير بشكل منظم
                if "# 💡 جوهر فكرة المشروع" in report:
                    parts = report.split("## 📝 ملخص تقييم الحالة")
                    st.info(parts[0]) 
                    
                    with st.expander("👁️ عرض التقرير الأكاديمي الكامل والنواقص", expanded=True):
                        st.markdown("## 📝 ملخص تقييم الحالة" + parts[1])
                else:
                    st.markdown(report)
                
                st.download_button("📥 تحميل قائمة التعديلات", report, file_name="BAU_Mandatory_Edits.md")
else:
    st.error("⚠️ يرجى ضبط GROQ_API_KEY في ملف secrets.toml")