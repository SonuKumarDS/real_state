def match_property_investor(prop, inv):
    score = 0.0
    reasons, concerns = [], []

    if prop.city and inv.location and prop.city.lower() in inv.location.lower():
        score += 25
        reasons.append("Investor location appears compatible with property city.")
    else:
        concerns.append("Location match not verified.")

    if prop.asking_price is not None:
        if inv.min_price is not None and prop.asking_price >= inv.min_price:
            score += 10
        if inv.max_price is not None and prop.asking_price <= inv.max_price:
            score += 15
        if inv.min_price is not None and inv.max_price is not None:
            if inv.min_price <= prop.asking_price <= inv.max_price:
                reasons.append("Asking price falls inside investor budget.")
            else:
                concerns.append("Asking price is outside the stated budget.")
    else:
        concerns.append("Property asking price is unavailable.")

    ptype = prop.property_type.lower()
    if inv.property_types and any(x.strip().lower() in ptype for x in inv.property_types.split(",")):
        score += 15
        reasons.append("Property type matches investor preference.")

    if inv.strategies:
        score += 15
        reasons.append("Investor has a documented investment strategy.")
    else:
        concerns.append("Investment strategy is not documented.")

    if inv.cash_buyer:
        score += 10
        reasons.append("Investor is marked as a cash buyer.")
    score = min(score, 100)
    return score, reasons, concerns
