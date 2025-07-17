import os
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatGroq  # from langchain-community

# Initialize Groq LLM
llm = ChatGroq(
    temperature=0.3,
    model_name="mixtral-8x7b-32768",  # or "llama3-70b-8192"
    groq_api_key=os.getenv("GROQ_API_KEY")
)

# Prompt Template for Summarization
prompt = PromptTemplate.from_template("""
Summarize the following YouTube transcript in {lang}. Provide:
Summary:
(short summary)

Key Takeaways:
- (bullet points)

Transcript:
{text}
""")

# LangChain LLM Chain
chain = LLMChain(llm=llm, prompt=prompt)

# Final Summarizer Function
def summarize_text(text, lang='en'):
    if len(text) > 3000:
        text = text[:3000]
    result = chain.run(text=text, lang=lang)
    return result
