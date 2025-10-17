"""
Fibonacci Series Generator.

This module provides functions to generate Fibonacci series
using different approaches including iterative and recursive methods.
"""

from typing import List, Generator


def fibonacci_iterative(n: int) -> List[int]:
    """
    Generate Fibonacci series using iterative approach.
    
    Args:
        n (int): Number of terms to generate
        
    Returns:
        List[int]: Fibonacci series
        
    Raises:
        ValueError: If n is not positive
    """
    if n <= 0:
        raise ValueError("Number of terms must be positive")
    elif n == 1:
        return [0]
    
    series = [0, 1]
    for i in range(2, n):
        series.append(series[i-1] + series[i-2])
    
    return series


def fibonacci_recursive(n: int) -> List[int]:
    """
    Generate Fibonacci series using recursive approach.
    
    Args:
        n (int): Number of terms to generate
        
    Returns:
        List[int]: Fibonacci series
        
    Raises:
        ValueError: If n is not positive
    """
    if n <= 0:
        raise ValueError("Number of terms must be positive")
    
    def fib_helper(count: int) -> List[int]:
        if count == 1:
            return [0]
        elif count == 2:
            return [0, 1]
        else:
            prev_series = fib_helper(count - 1)
            prev_series.append(prev_series[-1] + prev_series[-2])
            return prev_series
    
    return fib_helper(n)


def fibonacci_generator(n: int) -> Generator[int, None, None]:
    """
    Generate Fibonacci series using generator (memory efficient).
    
    Args:
        n (int): Number of terms to generate
        
    Yields:
        int: Next Fibonacci number
        
    Raises:
        ValueError: If n is not positive
    """
    if n <= 0:
        raise ValueError("Number of terms must be positive")
    
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b


def demonstrate_fibonacci():
    """
    Demonstrate different Fibonacci generation methods.
    """
    print("=== Fibonacci Series Demonstration ===")
    
    # Test iterative approach
    print("\n--- Iterative Approach (10 terms) ---")
    try:
        series = fibonacci_iterative(10)
        print(f"Fibonacci series: {series}")
    except ValueError as e:
        print(f"Error: {e}")
    
    # Test recursive approach
    print("\n--- Recursive Approach (8 terms) ---")
    try:
        series = fibonacci_recursive(8)
        print(f"Fibonacci series: {series}")
    except ValueError as e:
        print(f"Error: {e}")
    
    # Test generator approach
    print("\n--- Generator Approach (12 terms) ---")
    try:
        series = list(fibonacci_generator(12))
        print(f"Fibonacci series: {series}")
    except ValueError as e:
        print(f"Error: {e}")
    
    # Performance comparison for large numbers
    print("\n--- Large Series (20 terms) ---")
    try:
        iterative = fibonacci_iterative(20)
        generator = list(fibonacci_generator(20))
        print(f"Iterative result: {iterative}")
        print(f"Generator result: {generator}")
        print(f"Results match: {iterative == generator}")
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    demonstrate_fibonacci()