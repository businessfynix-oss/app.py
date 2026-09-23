import os
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import json

app = FastAPI()

SYSTEM_PROMPT = """Act as the FYNIX Business Solutions AI Assistant, an elite corporate advisor for Saudi market entry and institutional readiness under Vision 2030. Your tone is prestigious, professional, and highly strategic (B2B executive style). When a user asks about expanding or launching a business in Saudi Arabia, immediately structure your responses into actionable phases: Market Entry Legal Compliance, Government Relations (ZATCA, Qiwa, GOSI, Muqeem), and Institutional Readiness. Balance your outputs between high-end English consulting terminology and flawless professional Arabic script."""

@app.post("/")
async def poe_bot_responder(request: Request):
    try:
        body = await request.json()
    except Exception:
        body = {}
        
    async def event_generator():
        response_text = f"مرحباً بك في منصة فينكس الذكية المخصصة للاستشارات الجغرافية والاستراتيجية.\n\n{SYSTEM_PROMPT}\n\nكيف يمكنني خدمة تموضع منشأتك الاستراتيجي في السوق السعودي اليوم تحت مظلة رؤية 2030؟"
        yield f"event: text\ndata: {json.dumps({'text': response_text})}\n\n"
        yield "event: done\ndata: {}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
