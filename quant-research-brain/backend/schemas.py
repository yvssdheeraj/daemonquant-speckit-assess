from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
from models import LifecycleState, PortabilityStatus

# Source Schemas
class SourceBase(BaseModel):
    source_type: str
    source_url: Optional[str] = None
    author_or_channel: Optional[str] = None
    site_name: Optional[str] = None
    original_text_or_summary: Optional[str] = None
    extracted_claims: Optional[Dict[str, Any]] = None
    user_notes: Optional[str] = None
    copyright_status: Optional[str] = None
    compliance_status: Optional[str] = None
    ingestion_method: str
    attribution_required: bool = False
    storage_policy: Optional[str] = None

class SourceCreate(SourceBase):
    pass

class SourceResponse(SourceBase):
    id: int
    capture_timestamp: datetime

    class Config:
        from_attributes = True

# Universe Definition Schemas
class UniverseDefinitionBase(BaseModel):
    universe_name: str
    universe_type: str
    selection_rule: Dict[str, Any]
    constituent_symbols: List[str]
    data_source: str
    version_hash: str
    survivorship_bias_policy: str
    reconstitution_policy: str

class UniverseDefinitionCreate(UniverseDefinitionBase):
    pass

class UniverseDefinitionResponse(UniverseDefinitionBase):
    id: int
    effective_date: datetime

    class Config:
        from_attributes = True

# Signal Contract Schemas
class SignalContractBase(BaseModel):
    rule_expression: Dict[str, Any]
    entry_conditions: Dict[str, Any]
    exit_conditions: Dict[str, Any]
    stop_loss_rule: Optional[Dict[str, Any]] = None
    target_rule: Optional[Dict[str, Any]] = None
    position_sizing_rule: Optional[Dict[str, Any]] = None
    risk_management_rule: Optional[Dict[str, Any]] = None
    parameter_schema: Optional[Dict[str, Any]] = None
    timeframe: str
    evaluation_frequency: str
    data_dependencies: Dict[str, Any]
    feature_dependencies: Dict[str, Any]
    data_normalization_assumptions: Dict[str, Any]
    transaction_cost_assumptions: Dict[str, Any]
    slippage_assumptions: Dict[str, Any]
    benchmark_assumptions: Dict[str, Any]
    version_hash: str
    portability_status: PortabilityStatus
    non_portable_components: Optional[Dict[str, Any]] = None
    bias_check_status: str
    created_by: str
    approved_by: Optional[str] = None

class SignalContractCreate(SignalContractBase):
    pass

class SignalContractResponse(SignalContractBase):
    id: int
    strategy_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Backtest Report Schemas
class BacktestReportBase(BaseModel):
    total_return: float
    cagr: float
    max_drawdown: float
    sharpe_ratio: float
    win_rate: float
    profit_factor: float
    total_trades: int
    benchmark_return: float
    alpha: Optional[float] = None
    beta: Optional[float] = None
    report_data: Dict[str, Any]
    recommendation: str

class BacktestReportCreate(BacktestReportBase):
    pass

class BacktestReportResponse(BacktestReportBase):
    id: int
    strategy_id: int
    execution_timestamp: datetime

    class Config:
        from_attributes = True

# Bias Check Schemas
class BiasCheckBase(BaseModel):
    check_type: str
    severity: str
    evidence: str
    affected_backtest_runs: Dict[str, Any]
    recommendation: str
    human_review_required: bool = False

class BiasCheckCreate(BiasCheckBase):
    pass

class BiasCheckResponse(BiasCheckBase):
    id: int
    strategy_id: int

    class Config:
        from_attributes = True

# Portfolio Impact Schemas
class PortfolioImpactBase(BaseModel):
    correlation_with_existing: float
    marginal_sharpe_contribution: float
    aggregate_drawdown_impact: float
    capital_allocation_scenario: Dict[str, Any]
    risk_of_ruin_estimate: float

class PortfolioImpactCreate(PortfolioImpactBase):
    pass

class PortfolioImpactResponse(PortfolioImpactBase):
    id: int
    strategy_id: int
    evaluation_timestamp: datetime

    class Config:
        from_attributes = True

# Strategy Schemas
class StrategyBase(BaseModel):
    name: str
    description: Optional[str] = None
    lifecycle_state: LifecycleState = LifecycleState.IDEA_CAPTURED

class StrategyCreate(StrategyBase):
    source_id: Optional[int] = None
    universe_id: Optional[int] = None

class StrategyResponse(StrategyBase):
    id: int
    source_id: Optional[int]
    universe_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    source: Optional[SourceResponse] = None
    universe: Optional[UniverseDefinitionResponse] = None
    signal_contract: Optional[SignalContractResponse] = None
    backtests: List[BacktestReportResponse] = []
    bias_checks: List[BiasCheckResponse] = []
    portfolio_impacts: List[PortfolioImpactResponse] = []

    class Config:
        from_attributes = True
