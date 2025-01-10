from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional, Dict
import json
import os

from src.game_master_web import GameMasterWeb
from src.game_state import GameState

app = FastAPI()

app.mount("/static", StaticFiles(directory="src/web/static"), name="static")

class GameAction(BaseModel):
    action: str

class GameOption(BaseModel):
    optionIndex: int
    option: dict

class GameResponse(BaseModel):
    messages: List[dict]
    stateUpdate: Optional[dict]
    diceRolls: Optional[List[dict]]
    options: Optional[List[dict]]
    questUpdates: Optional[List[dict]]
    locationUpdate: Optional[dict]

# New chat models
class ChatRequest(BaseModel):
    userMessage: str

class ChatResponse(BaseModel):
    messages: List[Dict[str, str]]
    diceRolls: Optional[List[dict]] = None
    questUpdates: Optional[List[dict]] = None
    locationUpdate: Optional[dict] = None
    stateUpdate: Optional[dict] = None

game_master = None

@app.get("/")
async def read_root():
    return FileResponse("src/web/templates/index.html")

@app.post("/api/game/new")
async def new_game():
    global game_master
    game_master = GameMasterWeb()
    initial_state = game_master.start_game()
    return initial_state

@app.post("/api/game/action")
async def handle_action(action: GameAction):
    if not game_master:
        raise HTTPException(status_code=400, detail="Game not started")

    result = game_master.handle_action(action.action)
    return GameResponse(**result)

@app.post("/api/game/select-option")
async def select_option(option: GameOption):
    if not game_master:
        raise HTTPException(status_code=400, detail="Game not started")

    result = game_master.handle_option_selection(option.optionIndex, option.option)
    return GameResponse(**result)

@app.post("/api/game/save")
async def save_game(state: dict):
    if not game_master:
        raise HTTPException(status_code=400, detail="Game not started")

    try:
        with open("game_save.json", "w") as f:
            json.dump(state, f)
        return {"message": "Game saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/game/load")
async def load_game(saved_state: dict):
    global game_master
    try:
        game_master = GameMasterWeb()
        game_state = game_master.load_game_state(saved_state)
        return game_state
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/game/character-creation")
async def start_character_creation():
    if not game_master:
        raise HTTPException(status_code=400, detail="Game not started")

    return game_master.start_character_creation()

# New chat endpoint
@app.post("/api/chat", response_model=ChatResponse)
async def chat(chat_req: ChatRequest):
    if not game_master:
        raise HTTPException(status_code=400, detail="Game not started")

    user_message = chat_req.userMessage
    result = game_master.handle_action(user_message)

    return ChatResponse(
        messages=[
            {"sender": "Game Master", "content": result["messages"][0]["content"]},
        ],
        diceRolls=result.get("diceRolls"),
        questUpdates=result.get("questUpdates"),
        locationUpdate=result.get("locationUpdate"),
        stateUpdate=result.get("stateUpdate")
    )
