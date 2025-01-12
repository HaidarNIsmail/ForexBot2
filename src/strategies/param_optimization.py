import pandas as pd

def run_backtest(df):
    # Simplified backtest function
    df['Strategy_Returns'] = df['Buy_Signal'] * (df['Close'].pct_change()) - df['Sell_Signal'] * (df['Close'].pct_change())
    total_return = (df['Strategy_Returns'] + 1).prod() - 1
    sharpe_ratio = df['Strategy_Returns'].mean() / df['Strategy_Returns'].std() * (252 ** 0.5)
    return total_return, sharpe_ratio

if __name__ == "__main__":
    # Load data
    df = pd.read_csv('C:/Users/haida/PycharmProjects/ForexBot2/data/data_with_signals.csv')

    # Define parameter grid
    param_grid = {
        'stop_loss_pct': [0.005, 0.01, 0.015],
        'take_profit_pct': [0.01, 0.02, 0.03],
        'adx_threshold': [20, 25, 30],
    }

    best_sharpe = float('-inf')
    best_params = None

    for sl_pct in param_grid['stop_loss_pct']:
        for tp_pct in param_grid['take_profit_pct']:
            for adx_thr in param_grid['adx_threshold']:
                # Update parameters
                df['Stop_Loss'] = df['Close'] * (1 - sl_pct)
                df['Take_Profit'] = df['Close'] * (1 + tp_pct)
                df['ADX_Threshold'] = adx_thr

                # Run backtest
                total_return, sharpe_ratio = run_backtest(df)

                if sharpe_ratio > best_sharpe:
                    best_sharpe = sharpe_ratio
                    best_params = {'stop_loss_pct': sl_pct, 'take_profit_pct': tp_pct, 'adx_threshold': adx_thr}

    print(f"Best Sharpe Ratio: {best_sharpe}")
    print(f"Best Parameters: {best_params}")
