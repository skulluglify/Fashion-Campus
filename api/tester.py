class COL:
    PASSED = "\033[92m\033[1mSIP \u2713\033[0m"
    WARNING = "\033[93m\033[1m???"
    FAILED = "\033[91m\033[1m\u2717\033[0m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    BLUE = "\033[94m"
    UNDERLINE = "\033[4m"


# x = COL.__dict__.keys()
# skip_atr = ["__module__", "__dict__", "__weakref__", "__doc__"]
# for i in x:
#     if i in skip_atr:
#         continue
#     col = getattr(COL, i) 
#     print(f"{col}")
# print()