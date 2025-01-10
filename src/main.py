from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import json
import os

from .game_master import GameMaster
from .game_state import GameState

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="src/web/static"), name="static")

# Game state models
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

# Game instance
game_master = None

@app.get("/")
async def read_root():
    return FileResponse("src/web/templates/index.html")

@app.post("/api/game/new")
async def new_game():
    global game_master
    game_master = GameMaster()
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
        game_master = GameMaster()
        game_state = game_master.load_game_state(saved_state)
        return game_state
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/game/character-creation")
async def start_character_creation():
    if not game_master:
        raise HTTPException(status_code=400, detail="Game not started")

    return game_master.start_character_creation()