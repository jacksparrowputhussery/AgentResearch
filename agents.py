from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url
from dotenv import load_dotenv

load_dotenv()

# Model Setup
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
)


# 1st Agent — Search
def build_search_agent():
    return create_react_agent(
        model=llm,
        tools=[web_search],
        prompt="You are a research assistant. Use the web_search tool to find recent, "
               "reliable information on the given topic. Always use the web_search tool.",
    )


# 2nd Agent — Reader
def build_reader_agent():
    return create_react_agent(
        model=llm,
        tools=[scrape_url],
        prompt="You are a web reader assistant. Use the scrape_url tool to fetch and "
               "extract detailed content from URLs. Always use the scrape_url tool.",
    )


# Writer Chain
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional."""),
])

writer_chain = writer_prompt | llm | StrOutputParser()


# Critic Chain
critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
])

critic_chain = critic_prompt | llm | StrOutputParser()
