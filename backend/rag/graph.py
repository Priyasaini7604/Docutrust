from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.tools.tavily_search import TavilySearchResults
from typing import TypedDict, List
from core.config import GROQ_API_KEY
from rag.retriever import retrieve_chunks
from rag.grader import grade_documents
from rag.rewriter import rewrite_query

# ===== STATE =====
class GraphState(TypedDict):
    question: str
    documents: List[str]
    web_search_needed: bool
    answer: str
    steps: List[dict]

# ===== LLM =====
llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model_name="llama-3.1-8b-instant",
    temperature=0,
)

# ===== NODES =====

def retrieve_node(state: GraphState) -> GraphState:
    """Retrieve relevant chunks from ChromaDB."""
    question = state["question"]
    docs = retrieve_chunks(question)
    state["documents"] = docs
    state["steps"].append({
        "type": "retrieve",
        "step": "Retrieving chunks",
        "message": f"Retrieved {len(docs)} chunks from document"
    })
    return state


def grade_node(state: GraphState) -> GraphState:
    """Grade retrieved chunks for relevance."""
    result = grade_documents(state["question"], state["documents"])
    state["documents"] = result["relevant_docs"]
    state["web_search_needed"] = result["web_search_needed"]
    state["steps"].append({
        "type": "grade",
        "step": "Grading relevance",
        "message": f"{len(result['relevant_docs'])} relevant chunks found"
    })
    return state


def rewrite_node(state: GraphState) -> GraphState:
    """Rewrite query for web search."""
    rewritten = rewrite_query(state["question"])
    state["question"] = rewritten
    state["steps"].append({
        "type": "rewrite",
        "step": "Rewriting query",
        "message": f"Query rewritten: {rewritten}"
    })
    return state


def web_search_node(state: GraphState) -> GraphState:
    """Search web for additional context."""
    try:
        search = TavilySearchResults(k=3)
        results = search.invoke(state["question"])
        from langchain_core.documents import Document
        web_docs = [
            Document(
                page_content=r["content"],
                metadata={"source": r["url"], "page": 0}
            )
            for r in results
        ]
        state["documents"] = web_docs
        state["steps"].append({
            "type": "websearch",
            "step": "Web search",
            "message": f"Found {len(web_docs)} results from web"
        })
    except Exception as e:
        state["steps"].append({
            "type": "websearch",
            "step": "Web search failed",
            "message": "Using available context instead"
        })
    return state


def generate_node(state: GraphState) -> GraphState:
    """Generate final answer with citations."""
    docs = state["documents"]

    context = ""
    citations = []
    for i, doc in enumerate(docs):
        page = doc.metadata.get("page", 0)
        source = doc.metadata.get("source", "document")
        context += f"\n[Source {i+1}, Page {page}]: {doc.page_content}\n"
        citations.append({
            "page": page + 1,
            "source": source,
            "text": doc.page_content[:80]
        })

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a precise document assistant.
    Answer using ONLY the provided context below.
    If the exact answer is in the context, state it directly and confidently.
    If you're not fully certain, say what the context suggests.
    Keep the answer to one short sentence."""),
        ("human", """Context:
    {context}

    Question: {question}

    Answer:""")
    ])

    chain = prompt | llm | StrOutputParser()
    answer = chain.invoke({
        "context": context,
        "question": state["question"]
    })

    state["answer"] = answer
    state["documents"] = citations
    state["steps"].append({
        "type": "generate",
        "step": "Generating answer",
        "message": "Answer generated with citations"
    })
    return state


# ===== CONDITIONAL EDGE =====
def should_web_search(state: GraphState) -> str:
    """Decide whether to search web or generate answer."""
    if state["web_search_needed"]:
        return "rewrite"
    return "generate"


# ===== BUILD GRAPH =====
def build_graph():
    graph = StateGraph(GraphState)

    graph.add_node("retrieve", retrieve_node)
    graph.add_node("grade", grade_node)
    graph.add_node("rewrite", rewrite_node)
    graph.add_node("web_search", web_search_node)
    graph.add_node("generate", generate_node)

    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "grade")
    graph.add_conditional_edges(
        "grade",
        should_web_search,
        {
            "rewrite": "rewrite",
            "generate": "generate"
        }
    )
    graph.add_edge("rewrite", "web_search")
    graph.add_edge("web_search", "generate")
    graph.add_edge("generate", END)

    return graph.compile()


# ===== LAZY LOADING =====
_crag_graph = None

def get_graph():
    global _crag_graph
    if _crag_graph is None:
        _crag_graph = build_graph()
    return _crag_graph


def run_crag(question: str) -> dict:
    """
    Run the full CRAG pipeline for a given question.
    Returns answer, citations, and agent steps.
    """
    initial_state = {
        "question": question,
        "documents": [],
        "web_search_needed": False,
        "answer": "",
        "steps": []
    }

    final_state = get_graph().invoke(initial_state)

    return {
        "answer": final_state["answer"],
        "citations": final_state["documents"],
        "steps": final_state["steps"]
    }