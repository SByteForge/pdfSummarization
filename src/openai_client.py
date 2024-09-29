
from langchain_community.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback
from src.config import Config

class OpenAIClient:
    """Class to interact with OpenAI API."""

    @staticmethod
    def summarize(knowledge_base, query):
        """Generate a summary using OpenAI's API."""
        llm = ChatOpenAI(model=Config.MODEL_NAME, temperature=0.8)
        chain = load_qa_chain(llm, chain_type='stuff')
        
        with get_openai_callback() as cost:
            response = chain.run(input_documents=knowledge_base.similarity_search(query), question=query)
            print(cost)  # Log the cost of the operation
            return response
