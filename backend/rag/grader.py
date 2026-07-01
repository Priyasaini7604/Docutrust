from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from core.config import GROQ_API_KEY

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model_name="llama-3.1-8b-instant",
    temperature=0,
)

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a document relevance grader.
    Given a user question and a retrieved document chunk,
    determine if the chunk is relevant to the question.
    
    Reply with ONLY one word: yes or no
    Return 'yes' if the chunk contains ANY information that could 
    help answer the question, even partially.
    Only return 'no' if the chunk is completely unrelated."""),
    ("human", """Question: {question}
    
    Document chunk:
    {document}
    
    Relevant? (yes/no):""")
])

chain = prompt | llm | StrOutputParser()

def grade_documents(question: str, documents: list) -> dict:
    """
    Grade each retrieved document chunk for relevance.
    """
    relevant_docs = []
    web_search_needed = False

    for doc in documents:
        try:
            result = chain.invoke({
                "question": question,
                "document": doc.page_content
            })
            if "yes" in result.lower():
                relevant_docs.append(doc)
        except Exception:
            relevant_docs.append(doc)

    if len(relevant_docs) == 0:
        web_search_needed = True

    return {
        "relevant_docs": relevant_docs,
        "web_search_needed": web_search_needed
    }