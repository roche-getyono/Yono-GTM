import os

def verify_structure():
    required_dirs = ['directives', 'execution', '.tmp']
    status = {}
    for d in required_dirs:
        status[d] = os.path.exists(d)
    
    env_exists = os.path.exists('.env')
    
    print("--- System Structure Report ---")
    for d, exists in status.items():
        print(f"{d}: {'[OK]' if exists else '[MISSING]'}")
    print(f".env: {'[OK]' if env_exists else '[MISSING] (Note: Optional but recommended for API keys)'}")
    print("-------------------------------")

if __name__ == "__main__":
    verify_structure()
