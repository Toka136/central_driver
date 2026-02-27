import os
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
import asyncio
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

driver_metrics = {"eye_status": "searching", "head_status": "searching","phoneHolding":"searching"}

class StatusUpdate(BaseModel):
    service_name: str
    status: str

@app.post("/update-status")
async def update(data: StatusUpdate):
    driver_metrics[data.service_name] = data.status
    return {"status": "ok"}

@app.websocket("/ws/driver-status")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
         while True:
            await websocket.send_json(driver_metrics)
            await asyncio.sleep(0.5)
    except WebSocketDisconnect:
         pass

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)