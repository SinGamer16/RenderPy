import os
import sys

# Ensure project root is on sys.path when submodules are executed directly
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root not in sys.path:
    sys.path.insert(0, root)
