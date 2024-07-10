from typing import Dict, List, TypedDict, Union


class AgentState(TypedDict):
    current_speaker: str
    user_query: str
    query_fulfilled: bool
    category: Union[str, None]
    sub_category: Union[str, None]
    required_info_template: Union[Dict[str, str], None]
    captured_info: Union[Dict[str, Union[str, int, bool]], None]
    messages: List[Dict[str, Union[str, Dict[str, Union[str, int, bool]]]]]


# Initial state
initial_state: AgentState = {
    "current_speaker": "",
    "user_query": "",
    "query_fulfilled": False,
    "category": None,
    "sub_category": None,
    "required_info_template": None,
    "captured_info": {},
    "messages": []
## Commented out the below code as it confuses the conversation agent to behave as intended
#     "required_info_template": {
#   "Title": "",
#   "Description": {
#     "Business need": "",
#     "Project scope": "",
#     "Expected deliverables": "",
#     "Impact if not approved": "",
#     "Type of contract": "",
#     "Estimated cost": ""
#   },
#   "Category": "",
#   "Financial Details": {
#     "Start Date": "",
#     "End Date": "",
#     "Expected Amount": "",
#     "Funding Source": ""
#   }
# }
# ,
#     "captured_info": {
#   "Title": "",
#   "Description": {
#     "Business need": "",
#     "Project scope": "",
#     "Expected deliverables": "",
#     "Impact if not approved": "",
#     "Type of contract": "",
#     "Estimated cost": ""
#   },
#   "Category": "",
#   "Financial Details": {
#     "Start Date": "",
#     "End Date": "",
#     "Expected Amount": "",
#     "Funding Source": ""
#   }
# },
#     "messages": [],
#     "response":"",
#     "last_message":{}
}
