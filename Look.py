view: market_summary {
  derived_table: {
    sql: 
      SELECT
        SUM(price * quantity) / 10000000 AS total_market_value_cr
      FROM your_schema.your_transaction_table ;;
  }

  measure: total_market_value {
    type: number
    sql: ${TABLE}.total_market_value_cr ;;
    value_format: "0.00"
    label: "Total Market Value (Cr)"
    description: "Total market traded value across all stocks and all transactions"
  }
}

#In model File
explore: market_summary {
  label: "Market Summary"
  description: "Pre-aggregated total value for all stocks and trades"
}