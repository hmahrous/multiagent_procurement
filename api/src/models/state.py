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


needs_to_capture = {
    "1. Initiating a Sourcing Request": {
        "New Request": "",
        "Title": "",
        "Detailed description": {
            "Business need": "",
            "Project scope": "",
            "Expected deliverables": "",
            "Impact if not approved": "",
            "Type of contract": "",
            "Cost": ""
        }
    },
    "2. Category Selection and Financial Details": {
        "Category": "",
        "Start Date": "",
        "End Date": "",
        "Expected Amount": ""
    },
    "3. Deal Financials and Duration": {
        "Deal Presenter": "",
        "Available Funds": "",
        "Funding Type": "",
        "Cost Center": "",
        "GCRS Company Details": ""
    },
    "4. Cost Breakdown": {
        "Cost Breakdown": [
            {
                "Spend Type": "",
                "Expected Delivery Date": "",
                "Cost": ""
            },
            {
                "Spend Type": "",
                "Expected Delivery Date": "",
                "Cost": ""
            }
        ]
    },
    "5. Integration Budget and Technology Replacement": {
        "Integration Budget": "",
        "Replacing Technology": "",
        "Details": "",
        "Decommissioning Timeline": ""
    },
    "6. Software Purchase": {
        "Purchasing Software": "",
        "Software Known": ""
    },
    "7. Vendor Products": {
        "Category": "",
        "IT Capabilities": "",
        "Vendor": "",
        "Vendor Product": "",
        "Standard Status": "",
        "Action": ""
    },
    "8. Chain IQ Involvement": "",
    "9. Cost Commitment Approvers": {
        "Cost Commitment Approver 1": "",
        "Cost Commitment Approver 2": ""
    },
    "10. Business/Budget Owner Specification": {
        "Business/Budget Owner Details": {
            "Division": "",
            "Area": "",
            "Unit": "",
            "Sector": "",
            "Segment": ""
        }
    }
}


# Initial state
initial_state: AgentState = {
    "current_speaker": "",
    "user_query": "",
    "query_fulfilled": False,
    "category": None,
    "sub_category": None,
    "required_info_template": None,
    "captured_info": needs_to_capture,
    "messages": []
}
