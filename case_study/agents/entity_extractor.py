from smolagents import CodeAgent, LiteLLMModel
import yaml
from case_study.agents.final_answer_structurer import FinalAnswerStructurer
from case_study.rag.config import settings
from case_study.rag.vector_store import VectorStore
from case_study.tools.retriever import RetrieverTool


vector_store = VectorStore()
vector_store.load()

model = LiteLLMModel(model_id=settings.GROQ_MODEL, api_key=settings.GROQ_API_KEY)
final_answer_tool = FinalAnswerStructurer()
retriever_tool = RetrieverTool(vector_db=vector_store)

with open("case_study/prompts/prompts.yaml", "r") as stream:
    prompt_templates = yaml.safe_load(stream)

agent = CodeAgent(tools=[retriever_tool], model=model, max_steps=6)
