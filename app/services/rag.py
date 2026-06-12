from langchain_groq import ChatGroq
from app.core.config import get_settings
from app.services.embedding import embed_query
from app.services.pinecone_service import query_vectors
from app.services.redis_service import get_chat_history, save_chat_history

settings = get_settings()

llm = ChatGroq(api_key=settings.GROQ_API_KEY, model_name=settings.GROQ_MODEL)

BOOKING_PROMPT = """
You are a helpful assistant that answers questions based on the provided context.
Answer questions about any document — reports, research papers, CVs, or any other content.
Base your answers strictly on the context provided. Do not assume the document is a CV or resume.
Be precise — if something was evaluated but rejected, say so. If something was actually used, say so.
Do not confuse "mentioned" with "used". Only state something was used if the context explicitly says so.

You also help users book interviews. If the user wants to book an interview and provides
name, email, date, and time all at once, immediately respond with the JSON block below.
Do not ask for confirmation. Do not ask again for details already provided.
If some details are missing, ask only for the missing ones.

Once you have all four details (name, email, date, time), respond ONLY with this JSON and nothing else:
{{"action": "book_interview", "name": "...", "email": "...", "date": "...", "time": "..."}}

Context:
{context}

Chat History:
{history}

User: {question}
Assistant:
"""

async def get_rag_response(session_id: str, question: str) -> dict:
    history = await get_chat_history(session_id)

    embedding = embed_query(question)
    matches = query_vectors(embedding, top_k=10)
    context = "\n".join([m["metadata"]["text"] for m in matches if "text" in m["metadata"]])

    history_text = "\n".join(
        [f"{msg['role'].capitalize()}: {msg['content']}" for msg in history]
    )

    prompt = BOOKING_PROMPT.format(
        context=context,
        history=history_text,
        question=question
    )

    response = await llm.ainvoke(prompt)
    answer = response.content

    history.append({"role": "user", "content": question})
    history.append({"role": "assistant", "content": answer})
    await save_chat_history(session_id, history)

    return {"answer": answer, "session_id": session_id}