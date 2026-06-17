"""
Multi-provider fallback helper for GlucoGuard+.
Tries primary function; if it raises, runs fallback function with same args.
"""

def with_fallback(primary_fn, fallback_fn, *args, **kwargs):
    """
    Try primary_fn(*args, **kwargs).
    If it raises any exception, log and try fallback_fn(*args, **kwargs).
    Returns whatever the successful call returns.
    Raises if BOTH fail.
    """
    try:
        return primary_fn(*args, **kwargs)
    except Exception as e:
        error_msg = str(e)[:200]
        fallback_name = getattr(fallback_fn, '__name__', 'fallback')
        print(f"[fallback] Primary failed with: {error_msg}")
        print(f"[fallback] Trying fallback: {fallback_name}")
        try:
            return fallback_fn(*args, **kwargs)
        except Exception as e2:
            print(f"[fallback] Fallback also failed: {str(e2)[:200]}")
            raise
