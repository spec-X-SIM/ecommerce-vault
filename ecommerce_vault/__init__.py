from .snippets import SNIPPETS

def show(key=None):
    """
    Displays the cataloged code without executing it.
    If no key is specified, prints every code block in sequence.
    """
    if key is None:
        print("\n" + "=" * 80)
        print("          E-COMMERCE CODE CATALOG (READ-ONLY REFERENCE)")
        print("=" * 80 + "\n")
        for snippet_id, code in SNIPPETS.items():
            print(f">>> SECTION: {snippet_id}\n")
            print(code)
            print("-" * 80 + "\n")
    elif key in SNIPPETS:
        print(f">>> SECTION: {key}\n")
        print(SNIPPETS[key])
    else:
        print(f"Snippet key '{key}' not found.")
        print(f"Available keys: {list(SNIPPETS.keys())}")

# Automatically display all code upon import
show()