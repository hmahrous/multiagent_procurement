from typing import List, Dict, Any
from Agents import agents
import json
from State import initial_state

class MessagingPoolManager:
    def __init__(self, agents):
        self.pool: List[Dict[str, Any]] = []
        self.subscriptions: Dict[str, List[str]] = {}
        self.processed_messages: Dict[str, List[str]] = {}
        self.msg_id_counter = 1
        self.agents = agents
        self._initialize_subscriptions()

    def _initialize_subscriptions(self):
        # Subscribe agents to specific senders
        self.subscribe("Conversation-Agent", ["user", "Guardrails-Agent", "Procurement-Specialist-Agent"])
        self.subscribe("Procurement-Specialist-Agent", ["Conversation-Agent"])
        self.subscribe("Note-Take-Agent", ["user", "Procurement-Specialist-Agent"])
        self.subscribe("Guardrails-Agent", ["Conversation-Agent", "user"])

    def add_message(self, message: Dict[str, Any]):
        message['id'] = self._get_next_msg_id()
        self.pool.append(message)

    def subscribe(self, agent_name: str, senders: List[str]):
        self.subscriptions[agent_name] = senders
        self.processed_messages[agent_name] = []

    def get_messages(self, agent_name: str) -> List[Dict[str, Any]]:
        senders = self.subscriptions.get(agent_name, [])
        return [msg for msg in self.pool if
                msg['from'] in senders and msg['id'] not in self.processed_messages[agent_name]]

    def mark_as_processed(self, agent_name: str, message_id: str):
        self.processed_messages[agent_name].append(message_id)

    def _get_next_msg_id(self):
        msg_id = f"msg{self.msg_id_counter}"
        self.msg_id_counter += 1
        return msg_id

    async def process_messages(self, mode="group"):
        results = []
        while True:
            if not self.pool:
                return results  # Return if no messages in the pool
            else:
                for agent_name in self.subscriptions:
                    messages = self.get_messages(agent_name)
                    for message in messages:
                        self.mark_as_processed(agent_name, message['id'])
                    response = await self._handle_messages(agent_name, messages, mode)
                    if response:
                        results.append(response)
                        print(f'this is response: {response}')
                        if 'to' in response:
                            if response['to'] == 'user':
                                return results if mode == 'group' else response

    async def _handle_messages(self, agent_name, messages, mode):
        message_contents = self._prepare_message_contents(agent_name, messages)
        response = await self.send_message(agent_name, message_contents)
        return response

    def _prepare_message_contents(self, agent_name, messages):
        common_content = {
            "from": (" & ").join([message["from"] for message in messages]),
            "role": "assistant"
        }
        if agent_name in ["Conversation-Agent", "Procurement-Specialist-Agent"]:
            common_content[
                "content"] = f'continue from history conversations: ...{str(initial_state["messages"][-3:])} \n previously captured_info {initial_state["captured_info"]} \n current query:' + \
                             "\n".join([f'{message["from"]}:{message["content"]}' for message in messages])
            
        elif agent_name == "Note-Take-Agent":
            common_content["content"] = f'continue from history conversations: ...{str(initial_state["messages"][-3:])} \n' + \
                                        f'your previously captured template from previous messages: {initial_state["required_info_template"]} \n previously captured_info {initial_state["captured_info"]}. \n please only update. \n current message:' + \
                                        "\n".join([f'{message["from"]}:{message["content"]}' for message in messages])
            
        else:
            common_content["content"] = "\n".join([f'{message["from"]}:{message["content"]}' for message in messages])
            
        return common_content

    async def send_message(self, agent_name: str, message: Dict[str, Any]):
        agent = self._get_agent_by_name(agent_name)
        if agent:
            initial_state["current_speaker"] = agent_name
            response = agent.receive_message(message)
            if response:
                formatted_response = self._format_response(agent_name, response)
                await self._handle_agent_response(agent_name, formatted_response)
                #self.add_message(formatted_response)
                return formatted_response

    def _format_response(self, role, response):
        if isinstance(response, dict):
            return response
        try:
            response = json.loads(response)
            try:
                response = json.loads(response["content"])
                return response
            except:
                return response
        except:
            return self._get_default_response_format(role, response)

    def _get_default_response_format(self, role, response):
        if role == "Conversation-Agent":
            return {
                "type": "query",
                "content": response,
                "from": "Conversation-Agent",
                "role": "assistant",
                "to": "Procurement-Specialist-Agent"
            }
        elif role == "Procurement-Specialist-Agent":
            return {
                "type": "instruction",
                "content": response,
                "from": "Procurement-Specialist-Agent",
                "role": "assistant",
                "to": ["Conversation-Agent", "Note-Take-Agent"]
            }
        elif role == "Note-Take-Agent":
            return {
                "type": "template",
                "content": response,
                "from": "Note-Take-Agent",
                "role": "assistant",
            }
        elif role == "Guardrails-Agent":
            return {
                "type": "validation",
                "content": response,
                "from": "Guardrails-Agent",
                "role": "assistant"
            }

    async def _handle_agent_response(self, agent_name: str, formatted_response: Dict[str, Any]):
        """
        Handle the response from the agent, send it back to the user if necessary,
        and add it to the message pool.
        """
        if agent_name == "Note-Take-Agent":
            if formatted_response["type"] == "template":
                initial_state["required_info_template"] = formatted_response["content"]
            if formatted_response["type"] == "state_update":
                initial_state["captured_info"] = formatted_response["content"]
        if agent_name == "Conversation-Agent":
            if formatted_response["to"] == "user":
                initial_state["query_fulfilled"] = True

        self.add_message(formatted_response)

    async def prompt_user_input(self, message: Dict[str, Any] = None):
        initial_state["current_speaker"] = "user"
        user_input = input(f"{message['content']}")
        await self.add_user_message(message['content'], user_input)

    async def add_user_message(self, query: str, content: str):
        message = {
            "content": content,
            "from": "user",
            "role": "user",
            "to": "Conversation-Agent"
        }
        initial_state["user_query"] = content
        initial_state["messages"].append({"you": query, "user": content})
        self.add_message(message)
        return await self.process_messages()

    def _get_agent_by_name(self, agent_name: str):
        return self.agents.get(agent_name, None)






# from typing import List, Dict, Any
# import chainlit as cl
# from Agents import agents
# import json
# from State import initial_state


# class MessagingPoolManager:
#     def __init__(self, agents):
#         self.pool: List[Dict[str, Any]] = []
#         self.subscriptions: Dict[str, List[str]] = {}
#         self.processed_messages: Dict[str, List[str]] = {}
#         self.msg_id_counter = 1
#         self.agents = agents
#         self._initialize_subscriptions()

#     def _initialize_subscriptions(self):
#         # Subscribe agents to specific senders
#         self.subscribe("Conversation-Agent", ["user", "Guardrails-Agent", "Procurement-Specialist-Agent"])
#         self.subscribe("Procurement-Specialist-Agent", ["Conversation-Agent"])
#         self.subscribe("Note-Take-Agent", ["user", "Procurement-Specialist-Agent"])
#         self.subscribe("Guardrails-Agent", ["Conversation-Agent", "user"])

#     def add_message(self, message: Dict[str, Any]):
#         message['id'] = self._get_next_msg_id()
#         self.pool.append(message)

#     def subscribe(self, agent_name: str, senders: List[str]):
#         self.subscriptions[agent_name] = senders
#         self.processed_messages[agent_name] = []

#     def get_messages(self, agent_name: str) -> List[Dict[str, Any]]:
#         senders = self.subscriptions.get(agent_name, [])
#         return [msg for msg in self.pool if
#                 msg['from'] in senders and msg['id'] not in self.processed_messages[agent_name]]

#     def mark_as_processed(self, agent_name: str, message_id: str):
#         self.processed_messages[agent_name].append(message_id)

#     def _get_next_msg_id(self):
#         msg_id = f"msg{self.msg_id_counter}"
#         self.msg_id_counter += 1
#         return msg_id

#     async def process_messages(self):
#         while True:
#             if not self.pool:
#                 await self.prompt_user_input()
#             else:
#                 for agent_name in self.subscriptions:
#                     messages = self.get_messages(agent_name)
#                     for message in messages:
#                         self.mark_as_processed(agent_name, message['id'])
#                     await self._handle_messages(agent_name, messages)

#     async def _handle_messages(self, agent_name, messages):
#         message_contents = self._prepare_message_contents(agent_name, messages)
#         await self.send_message(agent_name, message_contents)

#     def _prepare_message_contents(self, agent_name, messages):
#         common_content = {
#             "from": (" & ").join([message["from"] for message in messages]),
#             "role": "assistant"
#         }
#         if agent_name in ["Conversation-Agent", "Procurement-Specialist-Agent"]:
#             common_content[
#                 "content"] = f'continue from history conversations: ...{str(initial_state["messages"][-3:])} \n previously captured_info {initial_state["captured_info"]} \n current query:' + \
#                              "\n".join([f'{message["from"]}:{message["content"]}' for message in messages])
            
#         elif agent_name == "Note-Take-Agent":
#             common_content["content"] = f'continue from history conversations: ...{str(initial_state["messages"][-3:])} \n' + \
#                                         f'your previously captured template from previous messages: {initial_state["required_info_template"]} \n previously captured_info {initial_state["captured_info"]}. \n please only update. \n current message:' + \
#                                         "\n".join([f'{message["from"]}:{message["content"]}' for message in messages])
            
#         else:
#             common_content["content"] = "\n".join([f'{message["from"]}:{message["content"]}' for message in messages])
            
#         return common_content

#     async def send_message(self, agent_name: str, message: Dict[str, Any]):
#         agent = self._get_agent_by_name(agent_name)
#         if agent:
#             initial_state["current_speaker"] = agent_name
#             response = agent.receive_message(message)
#             if response:
#                 formatted_response = self._format_response(agent_name, response)
#                 await self._handle_agent_response(agent_name, formatted_response)
#                 self.add_message(formatted_response)
#                 if formatted_response.get('to') == 'user':
#                     await self.prompt_user_input(formatted_response)

#     def _format_response(self, role, response):
#         if isinstance(response, dict):
#             return response
#         try:
#             response = json.loads(response)
#             try:
#                 response = json.loads(response["content"])
#                 return response
#             except:
#                 return response
#         except:
#             return self._get_default_response_format(role, response)

#     def _get_default_response_format(self, role, response):
#         if role == "Conversation-Agent":
#             return {
#                 "type": "query",
#                 "content": response,
#                 "from": "Conversation-Agent",
#                 "role": "assistant",
#                 "to": "Procurement-Specialist-Agent"
#             }
#         elif role == "Procurement-Specialist-Agent":
#             return {
#                 "type": "instruction",
#                 "content": response,
#                 "from": "Procurement-Specialist-Agent",
#                 "role": "assistant",
#                 "to": ["Conversation-Agent", "Note-Take-Agent"]
#             }
#         elif role == "Note-Take-Agent":
#             return {
#                 "type": "template",
#                 "content": response,
#                 "from": "Note-Take-Agent",
#                 "role": "assistant",
#             }
#         elif role == "Guardrails-Agent":
#             return {
#                 "type": "validation",
#                 "content": response,
#                 "from": "Guardrails-Agent",
#                 "role": "assistant"
#             }

#     async def _handle_agent_response(self, agent_name: str, formatted_response: Dict[str, Any]):
#         """
#         Handle the response from the agent, send it back to the user if necessary,
#         and add it to the message pool.
#         """
#         if agent_name == "Note-Take-Agent":
#             if formatted_response["type"] == "template":
#                 initial_state["required_info_template"] = formatted_response["content"]
#             if formatted_response["type"] == "state_update":
#                 initial_state["captured_info"] = formatted_response["content"]
#         if agent_name == "Conversation-Agent":
#             if formatted_response["to"] == "user":
#                 initial_state["query_fulfilled"] = True

#         classes = {
#             "Conversation-Agent": "message-conversation-agent",
#             "Procurement-Specialist-Agent": "message-procurement-specialist-agent",
#             "Note-Take-Agent": "message-note-take-agent",
#             "Guardrails-Agent": "message-guardrails-agent",
#             "user": "message-user"
#         }
#         class_name = classes.get(agent_name, "message-user")
#         formatted_message = f'<span class="{class_name}">{agent_name}: {formatted_response["content"]}</span>'

#         # Use Chainlit's safe HTML rendering method if available
#         await cl.Message(content=formatted_message).send()

#         self.add_message(formatted_response)

#     async def prompt_user_input(self, message: Dict[str, Any] = None):
#         initial_state["current_speaker"] = "user"
#         user_input = await cl.AskUserMessage(content=f"{message['content']}", timeout=600).send()
#         user_input = user_input["output"]
#         await self.add_user_message(message['content'], user_input)

#     async def add_user_message(self, query: str, content: str):
#         message = {
#             "content": content,
#             "from": "user",
#             "role": "user",
#             "to": "Conversation-Agent"
#         }
#         initial_state["user_query"] = content
#         initial_state["messages"].append({"you": query, "user": content})
#         self.add_message(message)
#         await self.process_messages()

#     def _get_agent_by_name(self, agent_name: str):
#         return self.agents.get(agent_name, None)


#pool_manager = MessagingPoolManager(agents)
