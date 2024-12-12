# import yfinance as yf

# def fetch_data(ticker, start_date, end_date):
#     """
#     Fetch historical price data for a given stock ticker.
#     """
#     data = yf.download(ticker, start=start_date, end=end_date)
#     return data

# if __name__ == "__main__":
#     # Fetch data for Apple (AAPL) as an example
#     ticker = "AAPL"
#     start_date = "2022-01-01"
#     end_date = "2023-01-01"
#     data = fetch_data(ticker, start_date, end_date)
#     print(data.head())

#     # Save to a CSV file for later use
#     data.to_csv(f"{ticker}_data.csv")
import pandas as pd
import matplotlib.pyplot as plt


class TradingSimulator:
    def __init__(self, initial_cash=100000):
        """
        Initialize the trading simulator with initial cash and no positions.
        """
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.position = 0
        self.trades = []  # Stores trade history
        self.portfolio_value = []

    def load_data(self, file_path):
        """
        Load historical price data from a CSV file and fix its structure.
        """
        # Load the file, skipping the first two rows
        self.data = pd.read_csv(file_path, skiprows=2)
        
        # Assign proper column names
        self.data.columns = ["Date", "Adj Close", "Close", "High", "Low", "Open", "Volume"]
        
        # Set the 'Date' column as the index
        self.data.set_index("Date", inplace=True)
        self.data.index = pd.to_datetime(self.data.index)  # Ensure the index is datetime
        
        print("Data loaded successfully!")
        print(self.data.head())  # Display the first few rows for verification

    def reset(self):
        """
        Reset the simulator to its initial state.
        """
        self.cash = self.initial_cash
        self.position = 0
        self.trades = []
        self.portfolio_value = []

    def calculate_portfolio_value(self, current_price):
        """
        Calculate the total portfolio value.
        """
        return self.cash + self.position * current_price

    def moving_average_strategy(self, short_window=5, long_window=20):
        """
        Apply a moving average crossover strategy.
        - Buy when the short-term moving average crosses above the long-term moving average.
        - Sell when it crosses below.
        """
        self.data["Short_MA"] = self.data["Close"].rolling(window=short_window).mean()
        self.data["Long_MA"] = self.data["Close"].rolling(window=long_window).mean()
        self.data["Signal"] = 0  # Default signal is 0 (no action)
        # Apply signals only where both moving averages exist
        self.data.loc[self.data["Short_MA"] > self.data["Long_MA"], "Signal"] = 1  # Buy signal
        self.data.loc[self.data["Short_MA"] <= self.data["Long_MA"], "Signal"] = -1  # Sell signal
        self.data.dropna(inplace=True)  # Remove rows with NaN values
        print("Strategy applied! Signals generated.")
        print(self.data[["Short_MA", "Long_MA", "Signal"]].head())  # Verify signals

    def plot_portfolio(self):
        """
        Plot the portfolio value over time.
        """
        plt.figure(figsize=(12, 6))
        plt.plot(self.data.index, self.data["Portfolio_Value"], label="Portfolio Value")
        plt.plot(self.data.index, self.data["Close"], label="Stock Price", alpha=0.6)
        plt.title("Portfolio Value and Stock Price Over Time")
        plt.xlabel("Date")
        plt.ylabel("Value")
        plt.legend()
        plt.grid()
        plt.show()


    def simulate_trades(self):
        """
        Simulate trades based on the generated signals.
        """
        self.cash = float(self.initial_cash)  # Ensure cash is float
        self.position = 0
        self.data["Portfolio_Value"] = 0.0  # Initialize portfolio value tracking

        for index, row in self.data.iterrows():
            current_price = row["Close"]
            signal = row["Signal"]

            # Buy signal: Only buy if we have enough cash
            if signal == 1 and self.cash >= current_price:
                self.position += 1  # Buy one share
                self.cash -= current_price
                print(f"Buy executed on {index}: Price = {current_price:.2f}, Cash = {self.cash:.2f}, Position = {self.position}")

            # Sell signal: Only sell if we hold positions
            elif signal == -1 and self.position > 0:
                self.position -= 1  # Sell one share
                self.cash += current_price
                print(f"Sell executed on {index}: Price = {current_price:.2f}, Cash = {self.cash:.2f}, Position = {self.position}")

            # Calculate total portfolio value
            portfolio_value = self.cash + self.position * current_price
            self.data.at[index, "Portfolio_Value"] = portfolio_value

        print("Trade simulation complete!")
        print(self.data[["Close", "Signal", "Portfolio_Value"]].tail())  # Verify results
        print("Trade simulation complete!")
        print(self.data[["Close", "Signal", "Portfolio_Value"]].tail())  # Verify results

        # Final Summary
        total_portfolio_value = self.cash + (self.position * self.data["Close"].iloc[-1])
        print(f"\nFinal Portfolio Summary:")
        print(f"  Cash: {self.cash:.2f}")
        print(f"  Positions: {self.position}")
        print(f"  Total Portfolio Value: {total_portfolio_value:.2f}")
        print(f"  Profit/Loss: {((total_portfolio_value - self.initial_cash) / self.initial_cash) * 100:.2f}%")



if __name__ == "__main__":
    # Initialize the simulator
    simulator = TradingSimulator(initial_cash=100000)

    # Load historical data
    simulator.load_data("AAPL_data.csv")

    # Apply moving average crossover strategy
    simulator.moving_average_strategy(short_window=5, long_window=20)

    # Simulate trades based on signals
    simulator.simulate_trades()
