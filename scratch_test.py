import sys
import os
sys.path.append(os.getcwd())
from tools.get_deals import update_deal_stage

print(type(update_deal_stage))
try:
    res = update_deal_stage.invoke({"company": "Acme", "new_stage": "Negotiation"})
    print("Invoke worked:", res)
except Exception as e:
    print("Invoke failed:", e)

try:
    res = update_deal_stage(company="Acme", new_stage="Negotiation")
    print("Direct worked:", res)
except Exception as e:
    print("Direct failed:", e)
