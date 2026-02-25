import sys

def simple_progress(current: int, total: int):
    """
    Very simple textual progress indicator.
    """
    if total <= 0:
        return
    percent = (current / total) * 100
    sys.stdout.write(f"\rProgress: {current}/{total} ({percent:.1f}%)")
    sys.stdout.flush()
    if current == total:
        sys.stdout.write("\n")
