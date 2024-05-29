from pydantic import BaseModel


class NasdaqStockBase(BaseModel):
    symbol: str
    exchange: str
    name: str
    last_sale: float
    pct_change: float
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
    balance_sheet_equity_attributable_to_noncontrolling_interest: float
    balance_sheet_liabilities: float
    balance_sheet_equity_attributable_to_parent: float
    balance_sheet_noncurrent_assets: float
    balance_sheet_liabilities_and_equity: float
    balance_sheet_assets: float
    balance_sheet_fixed_assets: float
    balance_sheet_other_than_fixed_noncurrent_assets: float
    balance_sheet_noncurrent_liabilities: float
    balance_sheet_current_assets: float
    balance_sheet_equity: float
    balance_sheet_current_liabilities: float
    # - cash flow statement
    cash_flow_statement_net_cash_flow_from_investing_activities: float
    cash_flow_statement_net_cash_flow_from_operating_activities_continuing: float
    cash_flow_statement_exchange_gains_losses: float
    cash_flow_statement_net_cash_flow_continuing: float
    cash_flow_statement_net_cash_flow: float
    cash_flow_statement_net_cash_flow_from_financing_activities: float
    cash_flow_statement_net_cash_flow_from_investing_activities_continuing: float
    cash_flow_statement_net_cash_flow_from_operating_activities: float
    cash_flow_statement_net_cash_flow_from_financing_activities_continuing: float
    # - comprehensive income
    comprehensive_income_comprehensive_income_loss_attributable_to_noncontrolling_interest: (
        float
    )
    comprehensive_income_comprehensive_income_loss_attributable_to_parent: float
    comprehensive_income_other_comprehensive_income_loss: float
    comprehensive_income_other_comprehensive_income_loss_attributable_to_parent: float
    comprehensive_income_comprehensive_income_loss: float
    # - income statement
    income_statement_income_loss_before_equity_method_investments: float
    income_statement_diluted_earnings_per_share: float
    income_statement_income_loss_from_equity_method_investments: float
    income_statement_operating_expenses: float
    income_statement_income_loss_from_continuing_operations_after_tax: float
    income_statement_preferred_stock_dividends_and_other_adjustments: float
    income_statement_basic_earnings_per_share: float
    income_statement_cost_of_revenue: float
    income_statement_net_income_loss_attributable_to_parent: float
    income_statement_income_loss_from_continuing_operations_before_tax: float
    income_statement_income_tax_expense_benefit_deferred: float
    income_statement_costs_and_expenses: float
    income_statement_gross_profit: float
    income_statement_benefits_costs_expenses: float
    income_statement_participating_securities_distributed_and_undistributed_earnings_loss_basic: (
        float
    )
    income_statement_income_tax_expense_benefit: float
    income_statement_net_income_loss_attributable_to_noncontrolling_interest: float
    income_statement_interest_expense_operating: float
    income_statement_net_income_loss_available_to_common_stockholders_basic: float
    income_statement_revenues: float
    income_statement_net_income_loss: float
    income_statement_operating_income_loss: float
    # meta data
    ticker: str
    start_date: str
    end_date: str
    filing_date: str
    cik: str
    company_name: str
    fiscal_period: str
    fiscal_year: str
    source_filing_url: str
    source_filing_file_url: str


class PolygonFinancialsDataCreate(PolygonFinancialsDataBase):
    pass


class PolygonFinancialsData(PolygonFinancialsDataBase):
    id: int
    created_at: int
    updated_at: int

    class Config:
        from_attributes = True
