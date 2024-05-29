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


# class PolygonFinancialsData(Base):
#     __tablename__ = "polygonapi_financials_data"
#     # financials data
#     # - balance sheet
#     id = Column(Integer, primary_key=True)
#     balance_sheet_equity_attributable_to_noncontrolling_interest = Column(Float)
#     balance_sheet_liabilities = Column(Float)
#     balance_sheet_equity_attributable_to_parent = Column(Float)
#     balance_sheet_noncurrent_assets = Column(Float)
#     balance_sheet_liabilities_and_equity = Column(Float)
#     balance_sheet_assets = Column(Float)
#     balance_sheet_fixed_assets = Column(Float)
#     balance_sheet_other_than_fixed_noncurrent_assets = Column(Float)
#     balance_sheet_noncurrent_liabilities = Column(Float)
#     balance_sheet_current_assets = Column(Float)
#     balance_sheet_equity = Column(Float)
#     balance_sheet_current_liabilities = Column(Float)
#     # - cash flow statement
#     cash_flow_statement_net_cash_flow_from_investing_activities = Column(Float)
#     cash_flow_statement_net_cash_flow_from_operating_activities_continuing = Column(
#         Float
#     )
#     cash_flow_statement_exchange_gains_losses = Column(Float)
#     cash_flow_statement_net_cash_flow_continuing = Column(Float)
#     cash_flow_statement_net_cash_flow = Column(Float)
#     cash_flow_statement_net_cash_flow_from_financing_activities = Column(Float)
#     cash_flow_statement_net_cash_flow_from_investing_activities_continuing = Column(
#         Float
#     )
#     cash_flow_statement_net_cash_flow_from_operating_activities = Column(Float)
#     cash_flow_statement_net_cash_flow_from_financing_activities_continuing = Column(
#         Float
#     )
#     # - comprehensive income
#     comprehensive_income_comprehensive_income_loss_attributable_to_noncontrolling_interest = Column(
#         Float
#     )
#     comprehensive_income_comprehensive_income_loss_attributable_to_parent = Column(
#         Float
#     )
#     comprehensive_income_other_comprehensive_income_loss = Column(Float)
#     comprehensive_income_other_comprehensive_income_loss_attributable_to_parent = (
#         Column(Float)
#     )
#     comprehensive_income_comprehensive_income_loss = Column(Float)
#     # - income statement
#     income_statement_income_loss_before_equity_method_investments = Column(Float)
#     income_statement_diluted_earnings_per_share = Column(Float)
#     income_statement_income_loss_from_equity_method_investments = Column(Float)
#     income_statement_operating_expenses = Column(Float)
#     income_statement_income_loss_from_continuing_operations_after_tax = Column(Float)
#     income_statement_preferred_stock_dividends_and_other_adjustments = Column(Float)
#     income_statement_basic_earnings_per_share = Column(Float)
#     income_statement_cost_of_revenue = Column(Float)
#     income_statement_net_income_loss_attributable_to_parent = Column(Float)
#     income_statement_income_loss_from_continuing_operations_before_tax = Column(Float)
#     income_statement_income_tax_expense_benefit_deferred = Column(Float)
#     income_statement_costs_and_expenses = Column(Float)
#     income_statement_gross_profit = Column(Float)
#     income_statement_benefits_costs_expenses = Column(Float)
#     income_statement_participating_securities_distributed_and_undistributed_earnings_loss_basic = Column(
#         Float
#     )
#     income_statement_income_tax_expense_benefit = Column(Float)
#     income_statement_net_income_loss_attributable_to_noncontrolling_interest = Column(
#         Float
#     )
#     income_statement_interest_expense_operating = Column(Float)
#     income_statement_net_income_loss_available_to_common_stockholders_basic = Column(
#         Float
#     )
#     income_statement_revenues = Column(Float)
#     income_statement_net_income_loss = Column(Float)
#     income_statement_operating_income_loss = Column(Float)
#     # meta data
#     ticker = Column(String)
#     start_date = Column(String)
#     end_date = Column(String)
#     filing_date = Column(String)
#     cik = Column(String)
#     company_name = Column(String)
#     fiscal_period = Column(String)
#     fiscal_year = Column(String)
#     source_filing_url = Column(String)
#     source_filing_file_url = Column(String)
