from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas, services, database
from fastapi.middleware.cors import CORSMiddleware

database.init_db()

app = FastAPI(title="Quant Research Brain API")

# Add CORS middleware for local frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
get_db = database.get_db

@app.get("/")
def read_root():
    return {"message": "Welcome to the Quant Research Brain API"}

@app.post("/sources/", response_model=schemas.SourceResponse)
def create_source(source: schemas.SourceCreate, db: Session = Depends(get_db)):
    return services.SourceService.create_source(db=db, source=source)

@app.post("/strategies/", response_model=schemas.StrategyResponse)
def create_strategy(strategy: schemas.StrategyCreate, db: Session = Depends(get_db)):
    is_valid, reason = services.MockValidationService.run_fast_rejection_filter(strategy)
    if not is_valid:
        raise HTTPException(status_code=400, detail=f"Strategy rejected: {reason}")
    return services.StrategyService.create_strategy(db=db, strategy=strategy)

@app.get("/strategies/", response_model=List[schemas.StrategyResponse])
def read_strategies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    strategies = services.StrategyService.get_strategies(db, skip=skip, limit=limit)
    return strategies

@app.get("/strategies/{strategy_id}", response_model=schemas.StrategyResponse)
def read_strategy(strategy_id: int, db: Session = Depends(get_db)):
    db_strategy = services.StrategyService.get_strategy(db, strategy_id=strategy_id)
    if db_strategy is None:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return db_strategy

@app.put("/strategies/{strategy_id}/state", response_model=schemas.StrategyResponse)
def update_strategy_state(strategy_id: int, state: models.LifecycleState, db: Session = Depends(get_db)):
    db_strategy = services.StrategyService.update_strategy_state(db, strategy_id=strategy_id, state=state)
    if db_strategy is None:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return db_strategy

@app.post("/extract-rules/")
def extract_rules(source_text: str):
    return services.MockExtractionService.extract_rules_from_source(source_text)
