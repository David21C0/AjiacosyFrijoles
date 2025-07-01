from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from config import OPENAI_API_KEY, OPENAI_MODEL

llm = ChatOpenAI(model=OPENAI_MODEL, openai_api_key=OPENAI_API_KEY)

prompt = ChatPromptTemplate.from_messages([
    ("user", "{input}")
])

def get_ai_response(user_input):
    chain = prompt | llm
    result = chain.invoke({"input": user_input})
    return str(result.content)
