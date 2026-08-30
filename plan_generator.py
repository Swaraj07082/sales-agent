from run_llm import run_llm

messages = run_llm("Move Acme Expansion Project to Negotiation and Schedule meeting Tuesday and Notify owner")

import sys

# for msg in messages:
#     if hasattr(msg, "role"):
#         try:
#             print(f"[{msg.role}] {msg.content}")
#         except UnicodeEncodeError:
#             print(f"[{msg.role}] {msg.content.encode('ascii', 'ignore').decode('ascii')}")
#         if getattr(msg, "tool_calls", None):
#             for t in msg.tool_calls:
#                 print(f"  -> Tool Call: {t.function.name} {t.function.arguments}")
#     elif isinstance(msg, dict):
#         try:
#             print(f"[{msg.get('role', 'unknown')}] {msg.get('name', '')}: {msg.get('content', '')}")
#         except UnicodeEncodeError:
#             pass

print(messages)
