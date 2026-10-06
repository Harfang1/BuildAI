"""
RAG service for streaming responses
"""
import json
import asyncio
import uuid
from datetime import datetime
from rag_engine.rag import stream_rag_with_thinking
from config_loader import settings

# --- Modèle Ollama par défaut ---
DEFAULT_RAG_MODEL = "llama3.2:3b"


async def stream_rag_response(question: str, top_k: int = 5, model: str = None):
    """
    Stream RAG response with instant feedback, real-time token streaming, and citation links.

    Args:
        question: User question
        top_k: Number of top results to retrieve
        model: Model identifier (overridden by settings.RAG_MODEL)

    Yields:
        str: Server-sent events formatted response chunks
    """
    response_model = model or "rag-hybrid"
    ollama_model = settings.RAG_MODEL  # Always use settings.RAG_MODEL (mistral:latest) for Ollama

    try:
        message_id = f"chatcmpl-{uuid.uuid4().hex[:12]}"
        created_timestamp = int(datetime.now().timestamp())

        # Yield immediate connection chunk (<50ms) so LibreChat indicates activity instantly
        initial_chunk = {
            "id": message_id,
            "object": "chat.completion.chunk",
            "created": created_timestamp,
            "model": response_model,
            "choices": [{
                "index": 0,
                "delta": {
                    "role": "assistant",
                    "reasoning_content": "Recherche dans la base documentaire BTP...\n"
                },
                "finish_reason": None
            }]
        }
        yield f"data: {json.dumps(initial_chunk)}\n\n"

        loop = asyncio.get_event_loop()

        # Use the async wrapper to stream in real-time
        async for update in async_rag_stream_wrapper(loop, stream_rag_with_thinking, question, top_k, ollama_model):
            if update['type'] == 'status':
                # Progress / status update in reasoning_content
                status_chunk = {
                    "id": message_id,
                    "object": "chat.completion.chunk",
                    "created": created_timestamp,
                    "model": response_model,
                    "choices": [{
                        "index": 0,
                        "delta": {
                            "reasoning_content": update['content']
                        },
                        "finish_reason": None
                    }]
                }
                yield f"data: {json.dumps(status_chunk)}\n\n"

            elif update['type'] == 'token':
                # Real-time token streaming directly in the message bubble (content)
                token_chunk = {
                    "id": message_id,
                    "object": "chat.completion.chunk",
                    "created": created_timestamp,
                    "model": response_model,
                    "choices": [{
                        "index": 0,
                        "delta": {
                            "content": update['content']
                        },
                        "finish_reason": None
                    }]
                }
                yield f"data: {json.dumps(token_chunk)}\n\n"

            elif update['type'] == 'done':
                break

        # Send final stop signal
        final_chunk = {
            "id": message_id,
            "object": "chat.completion.chunk",
            "created": created_timestamp,
            "model": response_model,
            "choices": [{
                "index": 0,
                "delta": {},
                "finish_reason": "stop"
            }]
        }
        yield f"data: {json.dumps(final_chunk)}\n\n"
        yield "data: [DONE]\n\n"

    except Exception as e:
        error_chunk = {
            "id": f"chatcmpl-{uuid.uuid4().hex[:12]}",
            "object": "chat.completion.chunk",
            "created": int(datetime.now().timestamp()),
            "model": model,
            "choices": [{
                "index": 0,
                "delta": {"content": f"\n\nError: {str(e)}"},
                "finish_reason": "stop"
            }]
        }
        yield f"data: {json.dumps(error_chunk)}\n\n"
        yield "data: [DONE]\n\n"


async def async_rag_stream_wrapper(loop, generator_func, *args):
    """Wrapper to run RAG streaming generator in real-time."""
    import queue
    import threading

    result_queue = queue.Queue()

    def run_generator():
        try:
            for item in generator_func(*args):
                result_queue.put(('item', item))
        except Exception as e:
            result_queue.put(('error', e))
        finally:
            result_queue.put(('done', None))

    # Start generator in background thread
    thread = threading.Thread(target=run_generator, daemon=True)
    thread.start()

    # Yield items as they come
    while True:
        # Non-blocking check with timeout
        def get_with_timeout():
            try:
                return result_queue.get(timeout=0.1)
            except queue.Empty:
                return None

        result = await loop.run_in_executor(None, get_with_timeout)

        if result is None:
            # Queue was empty, continue waiting
            await asyncio.sleep(0.01)
            continue

        msg_type, data = result

        if msg_type == 'item':
            yield data
        elif msg_type == 'error':
            raise data
        elif msg_type == 'done':
            break

    # Wait for thread to finish
    thread.join(timeout=1)
