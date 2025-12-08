import requests


LM_STUDIO_API_URL = "http://127.0.0.1:1234/v1/chat/completions"


MODEL_NAME = "phi-3.1-mini-4k-instruct"


MAX_CHUNKS = 3
MAX_TOTAL_CONTEXT_CHARS = 2000
 


def answer_question_with_context(question, chunks):
    """
    מקבלת שאלה + רשימת chunks (תוצאות מהחיפוש),
    בונה מהם קונטקסט ושולחת למודל ב-LM Studio.
    מחזירה את תשובת המודל כמחרוזת.
    """

  
    limited_chunks = chunks[:MAX_CHUNKS]

    context_parts = []
    total_chars = 0

    for ch in limited_chunks:
      
        text = getattr(ch, "content", str(ch))

        remaining = MAX_TOTAL_CONTEXT_CHARS - total_chars
        if remaining <= 0:
            break

      
        if len(text) > remaining:
            text = text[:remaining]

        context_parts.append(text)
        total_chars += len(text)

    context = "\n\n".join(context_parts)


  
    print(f"[LLM] using {len(context)} chars, {len(context_parts)} chunks")


    if context.strip():
        user_content = f"Context:\n{context}\n\nQuestion: {question}"
    else:
        user_content = f"Question: {question}"

    payload = {
        "model": MODEL_NAME,
        "max_tokens": 150,     
        "temperature": 0.2,     
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant that answers using only the given context.",
            },
            {
                "role": "user",
                "content": user_content,
            },
        ],
    }

    try:
        response = requests.post(
            LM_STUDIO_API_URL,
            json=payload,
            timeout=120,  
        )
    except Exception as e:
       
        return f"LLM request failed: {e}"

  
    if response.status_code != 200:
        return f"LLM error (HTTP {response.status_code}): {response.text}"

   
    data = response.json()
    try:
        return data["choices"][0]["message"]["content"]
    except Exception:
        return f"Unexpected LLM response format: {data}"
