from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from config import OPENAI_API_KEY, OPENAI_MODEL

llm = ChatOpenAI(model=OPENAI_MODEL, openai_api_key=OPENAI_API_KEY)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Te llamas David y eres alguein que conoce mucho de anime, responde de forma corta y formal."),
    ("user", "{input}")
])

def get_ai_response(user_input):
    chain = prompt | llm
    result = chain.invoke({"input": user_input})
    return str(result.content)
