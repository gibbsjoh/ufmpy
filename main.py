# Example / testing for ufmpy
# Micropython calls boot.py then main.py
# This is an example main.py to call the functions in ufmpy (for testing as well as a guide)

# import the file. it must be in the same directory as main.py, but you could change that
import ufmpy

# get a token for the specified FM solution
token = ufmpy.fmGetToken("MyFMSolution")
print(token)
