from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.sql import func

from stocklake.stores.db.database import Base


class NasdaqApiData(Base):
    __tablename__ = "nasdaq_api_data"

    id = Column(Integer, primary_key=True)
    exchange = Column(String(10))
    symbol = Column(String(10))
    name = Column(String(256))
    last_sale = Column(Float)
    pct_change = Column(Float)
    net_change = Column(Float)
    volume = Column(Float)
    marketcap = Column(Float)
    country = Column(String)
    ipo_year = Column(Integer)
    industry = Column(String)
    sector = Column(String)
    url = Column(String)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )


class PolygonFinancialsData(Base):
    __tablename__ = "polygonapi_financials_data"
    # financials data
    # - balance sheet
    id = Column(Integer, primary_key=True)
    equity_attributable_to_noncontrolling_interest = Column(Float)
    liabilities = Column(Float)
    equity_attributable_to_parent = Column(Float)
    noncurrent_assets = Column(Float)
    liabilities_and_equity = Column(Float)
    assets = Column(Float)
    fixed_assets = Column(Float)
    other_than_fixed_noncurrent_assets = Column(Float)
    noncurrent_liabilities = Column(Float)
    current_assets = Column(Float)
    equity = Column(Float)
    current_liabilities = Column(Float)
    # - cash flow statement
    # net_cash_flow_from_investing_activities = Column(Float)
    # net_cash_flow_from_operating_activities_continuing = Column(Float)
    exchange_gains_losses = Column(Float)
    # net_cash_flow_continuing = Column(Float)
    net_cash_flow = Column(Float)
    net_cash_flow_from_financing_activities = Column(Float)
    # net_cash_flow_from_investing_activities_continuing = Column(Float)
    # net_cash_flow_from_operating_activities = Column(Float)
    # net_cash_flow_from_financing_activities_continuing = Column(Float)
    # - comprehensive income
    loss_attributable_to_noncontrolling_interest = Column(Float)
    loss_attributable_to_parent = Column(Float)
    other_comprehensive_income_loss = Column(Float)
    # other_comprehensive_income_loss_attributable_to_parent = Column(Float)
    comprehensive_income_loss = Column(Float)
    # - income statement
    income_loss_before_equity_method_investments = Column(Float)
    # diluted_earnings_per_share = Column(Float)
    # income_loss_from_equity_method_investments = Column(Float)
    operating_expenses = Column(Float)
    # income_loss_from_continuing_operations_after_tax = Column(Float)
    # preferred_stock_dividends_and_other_adjustments = Column(Float)
    basic_earnings_per_share = Column(Float)
    cost_of_revenue = Column(Float)
    # net_income_loss_attributable_to_parent = Column(Float)
    # income_loss_from_continuing_operations_before_tax = Column(Float)
    # income_tax_expense_benefit_deferred = Column(Float)
    # costs_and_expenses = Column(Float)
    gross_profit = Column(Float)
    # benefits_costs_expenses = Column(Float)
    # participating_securities_distributed_and_undistributed_earnings_loss_basic = Column(
    # Float
    # )
    # income_tax_expense_benefit = Column(Float)
    # net_income_loss_attributable_to_noncontrolling_interest = Column(Float)
    # interest_expense_operating = Column(Float)
    # net_income_loss_available_to_common_stockholders_basic = Column(Float)
    revenues = Column(Float)
    # net_income_loss = Column(Float)
    # operating_income_loss = Column(Float)
    # meta data
    ticker = Column(String)
    start_date = Column(String)
    end_date = Column(String)
    filing_date = Column(String)
    cik = Column(String)
    company_name = Column(String)
    fiscal_period = Column(String)
    fiscal_year = Column(String)
    source_filing_url = Column(String)
    source_filing_file_url = Column(String)
