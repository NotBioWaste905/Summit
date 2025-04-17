from langchain.prompts import ChatPromptTemplate

discussion_start = ChatPromptTemplate.from_template(
    """
    You are a participant in a discussion about {topic}. 
    Your role is to provide insights and perspectives on the topic.
    Keep your responses short and to the point. Answer only from your perspective, don't type other participants answers.
    In the end you all must reach a consensus on the topic.
    If you have nothing to say and you agree on consesus, please say "I have nothing to add to the discussion."
    """
)

discussion_finish = ChatPromptTemplate.from_template(
    """
    Facilitate the discussion results and summarize the key points.
    """
)
