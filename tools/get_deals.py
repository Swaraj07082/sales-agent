import json
import uuid
from typing import Optional, List, Dict, Any

def import_deals() -> List[Dict[str, Any]]:
    with open("CRM/deals.json", "r", encoding="utf-8") as f:
        deals = json.load(f)
        return deals

def _find_deal(company: str) -> Optional[Dict[str, Any]]:
    deals = import_deals()
    comp = company.strip().lower()
    
    # 1. Exact match
    for deal in deals:
        if deal.get("name", "").strip().lower() == comp:
            return deal
            
    # 2. Substring match
    for deal in deals:
        dname = deal.get("name", "").strip().lower()
        if comp in dname or dname in comp:
            return deal
            
    return None

def get_deals(company: str) -> Dict[str, Any]:
    deal = _find_deal(company)
    if deal:
        return {"success": True, **deal}

    return {"company": company, "deal": "No deal found", "success": False}

def deal_exist(company: str) -> bool:
    return _find_deal(company) is not None

def update_deal_stage(company: str, new_stage: str) -> Dict[str, Any]:
    deals = import_deals()
    deal_to_update = _find_deal(company)

    if not deal_to_update:
        print(f"No deal found for {company}. Cannot update stage. Check spelling of the company name and try again.")
        return {"success": False, "error": f"No deal found for {company}"}
    
    for deal in deals:
        if deal["id"] == deal_to_update["id"]:
            deal["stage"] = new_stage
            break
            
    with open("CRM/deals.json", "w", encoding="utf-8") as f:
        json.dump(deals, f, indent=4)
        return {"success": True, "deal_name": deal_to_update["name"], "new_stage": new_stage}

def schedule_meeting(company: str, date: str) -> Dict[str, Any]:
    deals = import_deals()
    deal_to_update = _find_deal(company)

    if not deal_to_update:
        print(f"No deal found for {company}. Cannot schedule meeting. Check spelling of the company name and try again.")
        return {"success": False, "error": f"No deal found for {company}"}
    
    for deal in deals:
        if deal["id"] == deal_to_update["id"]:
            deal["meeting_date"] = date
            break
            
    with open("CRM/deals.json", "w", encoding="utf-8") as f:
        json.dump(deals, f, indent=4)
        return {"success": True, "deal_name": deal_to_update["name"], "meeting_date": date}

def send_email(subject: str, body: str) -> Dict[str, Any]:
    email = {
        "id": uuid.uuid4().hex,
        "account_id": uuid.uuid4().hex,
        "contact_id": uuid.uuid4().hex,
        "subject": subject,
        "body": body,
        "timestamp": uuid.uuid1().time
    }

    try:
        with open("CRM/emails.json", "r", encoding="utf-8") as f:
            emails = json.load(f)
    except Exception:
        emails = []

    emails.append(email)

    with open("CRM/emails.json", "w", encoding="utf-8") as f:
        json.dump(emails, f, indent=4)
        return {"success": True, "subject": subject, "body": body}
