# Chainlit Conversational AI Application

## Overview

This project demonstrates how to integrate a multi-agent conversational AI system using Chainlit and LangChain. The agents handle different roles, including conversation management, procurement assistance, note-taking, and compliance validation.

## Installation

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Install the required dependencies:
    ```bash
    pip install chainlit langchain-openai langchain-core
    ```

3. Set your OpenAI API key in the `agents.py` file:
    ```python
    llm = ChatOpenAI(model="gpt-4-turbo", openai_api_key="YOUR_OPENAI_API_KEY")
    ```

## Running the Application

1. Start the Chainlit application:
    ```bash
    chainlit run app.py
    ```

2. Open your browser and navigate to the provided URL to interact with the chatbot.

## Usage

- The user starts by sending a query, such as "I need to procure laptops for my team."
- The Conversation-Agent manages the interaction and forwards the query to the Procurement-Specialist-Agent.
- The Procurement-Specialist-Agent determines the next steps and requests any additional information needed.
- The Note-Take-Agent creates templates for required information and updates the state with user-provided details.
- The Guardrails-Agent validates user queries for compliance.

## Customization

- Modify `system_prompts` in `agents.py` to change the behavior and responses of each agent.
- Add new tools and integrations as needed.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you have any suggestions or improvements.

## License

This project is licensed under the MIT License.
