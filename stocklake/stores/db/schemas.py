from typing import Optional

from pydantic import BaseModel


class NasdaqStockBase(BaseModel):
    symbol: str
    exchange: str
    name: str
    last_sale: float
    pct_change: Optional[float]
    net_change: float
    volume: float
    marketcap: float
    country: str
    ipo_year: int
    industry: str
    sector: str
    url: str


class NasdaqStockCreate(NasdaqStockBase):
    pass


class NasdaqStock(NasdaqStockBase):
    id: int
    created_at: int
    updated_at: int

    class Config:
        from_attributes = True


class PolygonFinancialsDataBase(BaseModel):
    # financials data
    # - balance sheet
    equity_attributable_to_noncontrolling_interest: Optional[float]
    liabilities: Optional[float]
    equity_attributable_to_parent: Optional[float]
    noncurrent_assets: Optional[float]
    liabilities_and_equity: Optional[float]
    assets: Optional[float]
    fixed_assets: Optional[float]
    other_than_fixed_noncurrent_assets: Optional[float]
    noncurrent_liabilities: Optional[float]
    current_assets: Optional[float]
    equity: Optional[float]
    current_liabilities: Optional[float]
    # - cash flow statement
    # net_cash_flow_from_investing_activities: float
    # net_cash_flow_from_operating_activities_continuing: float
    exchange_gains_losses: Optional[float]
    # net_cash_flow_continuing: float
    net_cash_flow: Optional[float]
    net_cash_flow_from_financing_activities: Optional[float]
    # net_cash_flow_from_investing_activities_continuing: float
    # net_cash_flow_from_operating_activities: float
    # net_cash_flow_from_financing_activities_continuing: float
    # - comprehensive income
    # income_loss_attributable_to_noncontrolling_interest: float
    comprehensive_income_loss_attributable_to_parent: Optional[float]
    other_comprehensive_income_loss: Optional[float]
    # other_comprehensive_income_loss_attributable_to_parent: float
    comprehensive_income_loss: Optional[float]
    # - income statement
    # income_loss_before_equity_method_investments: float
    # diluted_earnings_per_share: float
    # income_loss_from_equity_method_investments: float
    operating_expenses: Optional[float]
    # income_loss_from_continuing_operations_after_tax: float
    # preferred_stock_dividends_and_other_adjustments: float
    basic_earnings_per_share: Optional[float]
    cost_of_revenue: Optional[float]
    # net_income_loss_attributable_to_parent: float
    # income_loss_from_continuing_operations_before_tax: float
    # income_tax_expense_benefit_deferred: float
    # costs_and_expenses: float
    gross_profit: Optional[float]
    # benefits_costs_expenses: float
    # participating_securities_distributed_and_undistributed_earnings_loss_basic: float
    # income_tax_expense_benefit: float
    # net_income_loss_attributable_to_noncontrolling_interest: float
    # interest_expense_operating: float
    # net_income_loss_available_to_common_stockholders_basic: float
    revenues: Optional[float]
    # net_income_loss: float
    # operating_income_loss: float
    # meta data
    ticker: str
    start_date: str
    end_date: str
    filing_date: Optional[str]
    cik: str
    company_name: str
    fiscal_period: str
    fiscal_year: str
    source_filing_url: Optional[str]
    source_filing_file_url: Optional[str]


class PolygonFinancialsDataCreate(PolygonFinancialsDataBase):
    pass


class PreprocessedPolygonFinancialsData(PolygonFinancialsDataBase):
    pass


class PolygonFinancialsData(PolygonFinancialsDataBase):
    id: int
    created_at: int
    updated_at: int

    class Config:
        from_attributes = True
