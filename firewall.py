# firewall.py - USM Security Governance Module

def usm_security_firewall(sql_query: str):
    """
    USM Principle: Threat Detection & Prevention.
    Inspects generated SQL queries and blocks unauthorized/destructive keywords.
    """
    forbidden_words = ["drop", "delete", "update", "insert", "alter", "truncate", "exec"]
    query_lower = sql_query.lower()
    
    for word in forbidden_words:
        if word in query_lower:
            return False, f"🚨 USM Security Alert: Blocked unauthorized '{word.upper()}' command!"
    
    return True, "✅ USM Security Check Passed: Query is safe (Read-Only)."