from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from core.config import GROQ_API_KEY

# Initialize Groq LLM
llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model_name="llama-3.1-8b-instant",
    temperature=0,
)

# Rewriter prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a query rewriter.
    Your job is to rewrite a user question to make it 
    more specific and better for web search.
    Return only the rewritten query, nothing else."""),
    ("human", """Original question: {question}
    
    Rewrite this question for better web search results:""")
])

rewriter_chain = prompt | llm | StrOutputParser()

def rewrite_query(question: str) -> str:
    """
    Rewrite the user query for better web search results.
    """
    rewritten = rewriter_chain.invoke({"question": question})
    return rewritten.strip()