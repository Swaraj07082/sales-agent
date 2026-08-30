import json
import uuid
from langchain.tools import tool
 
def import_deals() -> list[dict[str , str]]:
    with open("CRM/deals.json" , "r" , encoding = "utf-8") as f:
        deals = json.load(f)
        return deals
    
def get_deals(company : str) -> dict[str , str]:
    deals : list[dict[str , str]] = import_deals()
    for deal in deals:
        if deal["name"].strip().lower() == company.strip().lower():
            return deal

    return {"company" : company , "deal" : "No deal found"}

def deal_exist(company : str) -> bool:
    deals : list[dict[str , str]] = import_deals()
    for deal in deals:
        if deal["name"].strip().lower() == company.strip().lower():
            return True

    return False

def update_deal_stage(company : str , new_stage : str) -> dict[str , bool]:
    deals : list[dict[str , str]] = import_deals()

    if not deal_exist(company):
        print(f"No deal found for {company}. Cannot update stage. Check spelling of the company name and try again.")
        return {"success" : False}
    
    for deal in deals:
        if deal["name"].strip().lower() == company.strip().lower():
            deal["stage"] = new_stage
            break
    with open("CRM/deals.json" , "w" , encoding = "utf-8") as f:
        json.dump(deals , f , indent = 4)
        return {"success" : True}

def schedule_meeting(company : str , date : str):
    deals : list[dict[str , str]] = import_deals()

    if not deal_exist(company):
        print(f"No deal found for {company}. Cannot schedule meeting. Check spelling of the company name and try again.")
        return {"success" : False}
    
    for deal in deals:
        if deal["name"].strip().lower() == company.strip().lower():
            deal["meeting_date"] = date
            break
    with open("CRM/deals.json" , "w" , encoding = "utf-8") as f:
        json.dump(deals , f , indent = 4)
        return {"success" : True}

def send_email(subject : str , body : str):
    email = {
        "id" : uuid.uuid4().hex,
        "account_id" : uuid.uuid4().hex,
        "contact_id" : uuid.uuid4().hex,
        "subject" : subject,
        "body" : body,
        "timestamp" : uuid.uuid1().time
    }

    with open("CRM/emails.json" , "r" , encoding = "utf-8") as f:
        emails = json.load(f)
        emails.append(email)

    with open("CRM/emails.json" , "w" , encoding = "utf-8") as f:
        json.dump(emails , f , indent = 4)
        return {"success" : True}