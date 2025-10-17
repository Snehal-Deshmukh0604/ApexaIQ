class InsufficientBalanceError(Exception):
    """Custom exception for insufficient balance scenarios."""
    
    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        super().__init__(f"Insufficient balance: ${balance}. Required: ${amount}")


class BankAccount:
    """
    A class representing a bank account with basic operations.
    
    Attributes:
        account_holder (str): Name of the account holder
        balance (float): Current account balance
        account_number (str): Unique account identifier
    """
    
    def __init__(self, account_holder: str, initial_balance: float = 0.0):
        """
        Initialize BankAccount instance.
        
        Args:
            account_holder (str): Name of account holder
            initial_balance (float): Starting balance, defaults to 0.0
            
        Raises:
            ValueError: If initial_balance is negative
        """
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative")
        
        self.account_holder = account_holder
        self.balance = initial_balance
        self.account_number = self._generate_account_number()
    
    def _generate_account_number(self) -> str:
        """Generate a unique account number using timestamp."""
        import time
        return f"ACC{int(time.time()) % 100000:05d}"
    
    def deposit(self, amount: float) -> str:
        """
        Deposit money into the account.
        
        Args:
            amount (float): Amount to deposit
            
        Returns:
            str: Confirmation message with new balance
            
        Raises:
            ValueError: If amount is not positive
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        
        self.balance += amount
        return f"Deposited ${amount:.2f}. New balance: ${self.balance:.2f}"
    
    def withdraw(self, amount: float) -> str:
        """
        Withdraw money from the account.
        
        Args:
            amount (float): Amount to withdraw
            
        Returns:
            str: Confirmation message with new balance
            
        Raises:
            ValueError: If amount is not positive
            InsufficientBalanceError: If withdrawal amount exceeds balance
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        
        if amount > self.balance:
            raise InsufficientBalanceError(self.balance, amount)
        
        self.balance -= amount
        return f"Withdrew ${amount:.2f}. New balance: ${self.balance:.2f}"
    
    def check_balance(self) -> str:
        """
        Check current account balance.
        
        Returns:
            str: Current balance information
        """
        return f"Account balance for {self.account_holder}: ${self.balance:.2f}"
    
    def __str__(self) -> str:
        """String representation of BankAccount."""
        return f"BankAccount(holder='{self.account_holder}', balance=${self.balance:.2f})"


# Demonstration and testing
if __name__ == "__main__":
    try:
        # Create account
        account = BankAccount("John Doe", 1000.0)
        print(account)
        
        # Test deposits
        print(account.deposit(500.0))
        print(account.deposit(250.50))
        
        # Test withdrawals
        print(account.withdraw(300.0))
        print(account.check_balance())
        
        # Test insufficient balance
        print(account.withdraw(2000.0))
        
    except InsufficientBalanceError as e:
        print(f"Transaction failed: {e}")
    except ValueError as e:
        print(f"Error: {e}")