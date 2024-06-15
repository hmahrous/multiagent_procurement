from typing import TypedDict, Union, List, Dict

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
initial_state = AgentState(
    current_speaker="user",
    user_query="",
    query_fulfilled=False,
    category=None,
    sub_category=None,
    required_info_template=None,
    captured_info={},
    messages=[]
)