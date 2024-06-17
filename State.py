from typing import TypedDict, List, Dict, Any, Annotated
import operator
from langchain_core.messages import BaseMessage

class ProcurementState(TypedDict):
    hardware_info: Dict[str, Any]
    software_info: Dict[str, Any]
    current_category: str
    messages: Annotated[List[BaseMessage], operator.add]
