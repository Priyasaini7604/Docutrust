from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from core.config import GROQ_API_KEY

# Initialize Groq LLM
llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model_name="llama3-8b-8192",
    temperature=0,
)

# Grading prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a document relevance grader.
    Given a user question and a retrieved document chunk, 
    determine if the chunk is relevant to the question.
    
    Return a JSON with a single key 'score' with value 'yes' or 'no'.
    Example: {{"score": "yes"}} or {{"score": "no"}}
    
    Be strict — only return 'yes' if the chunk directly answers the question."""),
    ("human", """Question: {question}
    
    Document chunk:
    {document}
    
    Is this chunk relevant to the question?""")
])

grader_chain = prompt | llm | JsonOutputParser()

def grade_documents(question: str, documents: list) -> dict:
    """
    Grade each retrieved document chunk for relevance.
    Returns relevant docs and a flag if web search is needed.
    """
    relevant_docs = []
    web_search_needed = False

    for doc in documents:
        result = grader_chain.invoke({
            "question": question,
            "document": doc.page_content
        })

        if result.get("score") == "yes":
            relevant_docs.append(doc)

    # If no relevant docs found, web search is needed
    if len(relevant_docs) == 0:
        web_search_needed = True

    return {
        "relevant_docs": relevant_docs,
        "web_search_needed": web_search_needed
    }