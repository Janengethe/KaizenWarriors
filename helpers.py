#!/usr/bin/env python3

def logged_in(current_user: int) -> bool:
    """returns True if user is logged in"""
    try:
        _ = current_user.id
        return True
    except:
        return False
