from sqlalchemy.orm import Session
import models, schemas
import json

class StrategyService:
    @staticmethod
    def get_strategy(db: Session, strategy_id: int):
        return db.query(models.Strategy).filter(models.Strategy.id == strategy_id).first()

    @staticmethod
    def get_strategies(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Strategy).offset(skip).limit(limit).all()

    @staticmethod
    def create_strategy(db: Session, strategy: schemas.StrategyCreate):
        db_strategy = models.Strategy(**strategy.model_dump())
        db.add(db_strategy)
        db.commit()
        db.refresh(db_strategy)
        return db_strategy

    @staticmethod
    def update_strategy_state(db: Session, strategy_id: int, state: models.LifecycleState):
        db_strategy = db.query(models.Strategy).filter(models.Strategy.id == strategy_id).first()
        if db_strategy:
            db_strategy.lifecycle_state = state
            db.commit()
            db.refresh(db_strategy)
        return db_strategy

class SourceService:
    @staticmethod
    def create_source(db: Session, source: schemas.SourceCreate):
        db_source = models.Source(**source.model_dump())
        db.add(db_source)
        db.commit()
        db.refresh(db_source)
        return db_source

class MockExtractionService:
    @staticmethod
    def extract_rules_from_source(source_text: str):
        """Mocks LLM/NLP extraction of trading rules from unstructured text."""
        return {
            "entry_conditions": {"mock": "extracted entry"},
            "exit_conditions": {"mock": "extracted exit"},
            "confidence": 0.85
        }

class MockValidationService:
    @staticmethod
    def run_fast_rejection_filter(strategy: schemas.StrategyCreate):
        """Mocks the fast rejection filter."""
        # E.g., check if universe is defined, etc.
        return True, "Passed fast rejection"
