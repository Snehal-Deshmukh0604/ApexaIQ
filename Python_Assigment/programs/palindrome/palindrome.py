"""
Palindrome Detection Utility.

This module provides functions to detect palindromes in strings,
sentences, and numbers with various validation methods.
"""

import re
from typing import List, Union


def is_string_palindrome(text: str, case_sensitive: bool = False) -> bool:
    """
    Check if a string is palindrome.
    
    Args:
        text (str): String to check
        case_sensitive (bool): Whether to consider case, defaults to False
        
    Returns:
        bool: True if palindrome, False otherwise
    """
    if not text:
        return False
    
    # Clean the string: remove non-alphanumeric characters
    cleaned = re.sub(r'[^a-zA-Z0-9]', '', text)
    
    if not case_sensitive:
        cleaned = cleaned.lower()
    
    return cleaned == cleaned[::-1]


def is_sentence_palindrome(sentence: str) -> bool:
    """
    Check if a sentence is palindrome (ignoring spaces, punctuation, case).
    
    Args:
        sentence (str): Sentence to check
        
    Returns:
        bool: True if palindrome, False otherwise
    """
    if not sentence:
        return False
    
    # Remove all non-alphanumeric characters and convert to lowercase
    cleaned = re.sub(r'[^a-zA-Z0-9]', '', sentence).lower()
    
    return cleaned == cleaned[::-1]


def is_number_palindrome(number: int) -> bool:
    """
    Check if a number is palindrome.
    
    Args:
        number (int): Number to check
        
    Returns:
        bool: True if palindrome, False otherwise
    """
    if number < 0:
        return False
    
    original = number
    reversed_num = 0
    
    while number > 0:
        digit = number % 10
        reversed_num = reversed_num * 10 + digit
        number = number // 10
    
    return original == reversed_num


def find_palindromes_in_range(start: int, end: int) -> List[int]:
    """
    Find all palindrome numbers in a given range.
    
    Args:
        start (int): Start of range (inclusive)
        end (int): End of range (inclusive)
        
    Returns:
        List[int]: List of palindrome numbers in the range
    """
    palindromes = []
    for num in range(start, end + 1):
        if is_number_palindrome(num):
            palindromes.append(num)
    return palindromes


def demonstrate_palindrome():
    """
    Demonstrate palindrome detection with various examples.
    """
    print("=== Palindrome Detection Demonstration ===")
    
    # String palindromes
    test_strings = [
        "racecar",
        "A man a plan a canal Panama",
        "hello",
        "12321",
        "Madam",
        "Was it a car or a cat I saw?"
    ]
    
    print("\n--- String Palindrome Tests ---")
    for test_str in test_strings:
        result = is_string_palindrome(test_str)
        sentence_result = is_sentence_palindrome(test_str)
        print(f"'{test_str}' -> String: {result}, Sentence: {sentence_result}")
    
    # Number palindromes
    test_numbers = [121, 123, 12321, 12345, 1, 22, 333]
    
    print("\n--- Number Palindrome Tests ---")
    for num in test_numbers:
        result = is_number_palindrome(num)
        print(f"{num} -> {result}")
    
    # Find palindromes in range
    print("\n--- Palindromes in Range (100-200) ---")
    palindromes = find_palindromes_in_range(100, 200)
    print(f"Palindromes: {palindromes}")
    
    # Case sensitivity test
    print("\n--- Case Sensitivity Test ---")
    case_tests = ["Racecar", "RACECAR", "hello"]
    for test_str in case_tests:
        sensitive = is_string_palindrome(test_str, case_sensitive=True)
        insensitive = is_string_palindrome(test_str, case_sensitive=False)
        print(f"'{test_str}' -> Case Sensitive: {sensitive}, Insensitive: {insensitive}")


if __name__ == "__main__":
    demonstrate_palindrome()