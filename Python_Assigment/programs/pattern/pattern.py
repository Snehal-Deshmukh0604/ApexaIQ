"""
Three Essential Patterns Program
"""

def print_patterns(size):
    """Print three different patterns"""
    
    print("1. Right Triangle:")
    for i in range(1, size + 1):
        print('*' * i)
    
    print("\n2. Pyramid:")
    for i in range(1, size + 1):
        spaces = ' ' * (size - i)
        stars = '*' * (2 * i - 1)
        print(spaces + stars)
    
    print("\n3. Diamond:")
    # Top half
    for i in range(1, size + 1):
        spaces = ' ' * (size - i)
        stars = '*' * (2 * i - 1)
        print(spaces + stars)
    # Bottom half
    for i in range(size - 1, 0, -1):
        spaces = ' ' * (size - i)
        stars = '*' * (2 * i - 1)
        print(spaces + stars)

# Run the program
if __name__ == "__main__":
    size = 4
    print(f"Patterns for size {size}:\n")
    print_patterns(size)