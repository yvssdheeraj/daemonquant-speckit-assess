from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey, Enum, Float, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()

class LifecycleState(str, enum.Enum):
    IDEA_CAPTURED = "IDEA_CAPTURED"
    NEEDS_RULE_CLARIFICATION = "NEEDS_RULE_CLARIFICATION"
    SIGNAL_CONTRACT_DRAFTED = "SIGNAL_CONTRACT_DRAFTED"
    AWAITING_HUMAN_REVIEW = "AWAITING_HUMAN_REVIEW"
    RESEARCHING = "RESEARCHING"
    BACKTESTING = "BACKTESTING"
    OPTIMIZING = "OPTIMIZING"
    ROBUSTNESS_TESTING = "ROBUSTNESS_TESTING"
    PORTFOLIO_EVALUATION = "PORTFOLIO_EVALUATION"
    PAPER_SIMULATION = "PAPER_SIMULATION"
    FORWARD_TESTING = "FORWARD_TESTING"
    APPROVED_FOR_DEPLOYMENT = "APPROVED_FOR_DEPLOYMENT"
    DEPLOYED_EXTERNALLY = "DEPLOYED_EXTERNALLY"
    CAPITAL_ALLOCATION_CANDIDATE = "CAPITAL_ALLOCATION_CANDIDATE"
    UNDER_REVIEW = "UNDER_REVIEW"
    RETIRED = "RETIRED"
    REJECTED = "REJECTED"

class PortabilityStatus(str, enum.Enum):
    PORTABLE = "PORTABLE"
    PARTIALLY_PORTABLE = "PARTIALLY_PORTABLE"
    RESEARCH_ONLY = "RESEARCH_ONLY"

class Source(Base):
    __tablename__ = 'sources'

    id = Column(Integer, primary_key=True, index=True)
    source_type = Column(String)
    source_url = Column(String, nullable=True)
    author_or_channel = Column(String, nullable=True)
    site_name = Column(String, nullable=True)
    capture_timestamp = Column(DateTime, default=datetime.utcnow)
    original_text_or_summary = Column(Text, nullable=True)
    extracted_claims = Column(JSON, nullable=True)
    user_notes = Column(Text, nullable=True)
    copyright_status = Column(String, nullable=True)
    compliance_status = Column(String, nullable=True)
    ingestion_method = Column(String)
    attribution_required = Column(Boolean, default=False)
    storage_policy = Column(String, nullable=True)

    strategies = relationship("Strategy", back_populates="source")

class UniverseDefinition(Base):
    __tablename__ = 'universe_definitions'

    id = Column(Integer, primary_key=True, index=True)
    universe_name = Column(String)
    universe_type = Column(String)
    selection_rule = Column(JSON)
    effective_date = Column(DateTime, default=datetime.utcnow)
    constituent_symbols = Column(JSON)
    data_source = Column(String)
    version_hash = Column(String)
    survivorship_bias_policy = Column(String)
    reconstitution_policy = Column(String)

    strategies = relationship("Strategy", back_populates="universe")

class Strategy(Base):
    __tablename__ = 'strategies'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    lifecycle_state = Column(Enum(LifecycleState), default=LifecycleState.IDEA_CAPTURED)
    source_id = Column(Integer, ForeignKey('sources.id'))
    universe_id = Column(Integer, ForeignKey('universe_definitions.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    source = relationship("Source", back_populates="strategies")
    universe = relationship("UniverseDefinition", back_populates="strategies")
    signal_contract = relationship("SignalContract", back_populates="strategy", uselist=False)
    backtests = relationship("BacktestReport", back_populates="strategy")
    bias_checks = relationship("BiasCheck", back_populates="strategy")
    portfolio_impacts = relationship("PortfolioImpact", back_populates="strategy")

class SignalContract(Base):
    __tablename__ = 'signal_contracts'

    id = Column(Integer, primary_key=True, index=True)
    strategy_id = Column(Integer, ForeignKey('strategies.id'), unique=True)
    rule_expression = Column(JSON)
    entry_conditions = Column(JSON)
    exit_conditions = Column(JSON)
    stop_loss_rule = Column(JSON, nullable=True)
    target_rule = Column(JSON, nullable=True)
    position_sizing_rule = Column(JSON, nullable=True)
    risk_management_rule = Column(JSON, nullable=True)
    parameter_schema = Column(JSON, nullable=True)
    timeframe = Column(String)
    evaluation_frequency = Column(String)
    data_dependencies = Column(JSON)
    feature_dependencies = Column(JSON)
    data_normalization_assumptions = Column(JSON)
    transaction_cost_assumptions = Column(JSON)
    slippage_assumptions = Column(JSON)
    benchmark_assumptions = Column(JSON)
    version_hash = Column(String)
    portability_status = Column(Enum(PortabilityStatus))
    non_portable_components = Column(JSON, nullable=True)
    bias_check_status = Column(String)
    created_by = Column(String)
    approved_by = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    strategy = relationship("Strategy", back_populates="signal_contract")

class BacktestReport(Base):
    __tablename__ = 'backtest_reports'

    id = Column(Integer, primary_key=True, index=True)
    strategy_id = Column(Integer, ForeignKey('strategies.id'))
    total_return = Column(Float)
    cagr = Column(Float)
    max_drawdown = Column(Float)
    sharpe_ratio = Column(Float)
    win_rate = Column(Float)
    profit_factor = Column(Float)
    total_trades = Column(Integer)
    benchmark_return = Column(Float)
    alpha = Column(Float, nullable=True)
    beta = Column(Float, nullable=True)
    report_data = Column(JSON) # Store full report detail here
    execution_timestamp = Column(DateTime, default=datetime.utcnow)
    recommendation = Column(String)

    strategy = relationship("Strategy", back_populates="backtests")

class BiasCheck(Base):
    __tablename__ = 'bias_checks'

    id = Column(Integer, primary_key=True, index=True)
    strategy_id = Column(Integer, ForeignKey('strategies.id'))
    check_type = Column(String)
    severity = Column(String)
    evidence = Column(Text)
    affected_backtest_runs = Column(JSON)
    recommendation = Column(Text)
    human_review_required = Column(Boolean, default=False)

    strategy = relationship("Strategy", back_populates="bias_checks")

class PortfolioImpact(Base):
    __tablename__ = 'portfolio_impacts'

    id = Column(Integer, primary_key=True, index=True)
    strategy_id = Column(Integer, ForeignKey('strategies.id'))
    correlation_with_existing = Column(Float)
    marginal_sharpe_contribution = Column(Float)
    aggregate_drawdown_impact = Column(Float)
    capital_allocation_scenario = Column(JSON)
    risk_of_ruin_estimate = Column(Float)
    evaluation_timestamp = Column(DateTime, default=datetime.utcnow)

    strategy = relationship("Strategy", back_populates="portfolio_impacts")
