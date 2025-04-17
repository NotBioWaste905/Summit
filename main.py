from dotenv import load_dotenv

from langchain_community.chat_models import ChatOpenAI

from summit.discussion import Discussion

load_dotenv()

disc = Discussion(
    participants={
        "Alice": {"model": ChatOpenAI(model="gpt-4o-mini"), "finished": False},
        "Bob": {"model": ChatOpenAI(model="gpt-4o-mini"), "finished": False},
        "Charlie": {"model": ChatOpenAI(model="gpt-4.1-mini"), "finished": False},
        "Dave": {"model": ChatOpenAI(model="gpt-4.1-mini"), "finished": False},
        "Eve": {"model": ChatOpenAI(model="gpt-4.1-mini"), "finished": False},
    },
    topic="Research idea for the LLM improvement. It must be a detailed plan with concrete hypotheses and experiments.",
)

disc.run()
