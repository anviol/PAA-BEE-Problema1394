import sys

def main():
    input = sys.stdin.read
    data = input().strip().split('\n')
    
    results = []
    for line in data:
        a, b = map(int, line.split())
        if a == 0 and b == 0:
            break
        results.append(str(a + b))
    
    print("\n".join(results))

if __name__ == "__main__":
    main()