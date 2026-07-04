

# from agents import (
#     build_reader_agent,
#     build_search_agent,
#     writer_chain,
#     critic_chain,
#     llm
# )

from agents import (
    writer_chain,
    critic_chain,
)

from tools import web_search, scrape_url
import re

MAX_CONTEXT = 2000


def extract_first_url(text):
    match = re.search(r"https?://[^\s]+", text)
    if not match:
        return None
    return match.group(0).rstrip(".,)")


# def compress_text(text: str, limit: int = MAX_CONTEXT):

#     if len(text) <= limit:
#         return text

#     summary = llm.invoke(
#         f"""
#         Summarize the following research content clearly.
#         Keep only important technical facts and insights.

#         Content:
#         {text[:6000]}
#         """
#     )

#     return summary.content


def run_research_pipeline(topic: str):

    state = {}

    # -------------------------------------------------
    # STEP 1 — SEARCH AGENT
    # -------------------------------------------------

    print("\n" + "=" * 50)
    print("STEP 1 - Search Agent")
    print("=" * 50)

    # search_agent = build_search_agent()

    # search_result = search_agent.invoke({
    #     "messages": [
    #         (
    #             "user",
    #             f"""
    #             Find ONLY 3 highly relevant and reliable sources
    #             about: {topic}

    #             Return concise results.
    #             """
    #         )
    #     ]
    # })

    # raw_search = search_result['messages'][-1].content

    # compress search output
    # compressed_search = compress_text(raw_search)

    raw_search = web_search.invoke({"query": topic})

    compressed_search = raw_search[:2000]

    state["search_results"] = compressed_search

    print("\nCompressed Search Results:\n")
    print(compressed_search)

    # -------------------------------------------------
    # STEP 2 — READER AGENT
    # -------------------------------------------------

    print("\n" + "=" * 50)
    print("STEP 2 - Reader Agent")
    print("=" * 50)

    # reader_agent = build_reader_agent()

    # reader_result = reader_agent.invoke({
    #     "messages": [
    #         (
    #             "user",
    #             f"""
    #             From the following summarized search results
    #             choose the BEST source and extract the most
    #             important information.

    #             Topic: {topic}

    #             Search Results:
    #             {compressed_search}
    #             """
    #         )
    #     ]
    # })

    # raw_scraped = reader_result['messages'][-1].content

    # compressed_scraped = compress_text(raw_scraped)

    url = extract_first_url(raw_search)

    if url:
       raw_scraped = scrape_url.invoke({"url": url})
    else:
        raw_scraped = "No valid URL found."

    compressed_scraped = raw_scraped[:2000]

    state["scraped_content"] = compressed_scraped

    print("\nCompressed Scraped Content:\n")
    print(compressed_scraped)

    # -------------------------------------------------
    # STEP 3 — WRITER
    # -------------------------------------------------

    print("\n" + "=" * 50)
    print("STEP 3 - Writer")
    print("=" * 50)

    research_context = f"""
    SEARCH SUMMARY:
    {compressed_search}

    DETAILED INSIGHTS:
    {compressed_scraped}
    """

    report = writer_chain.invoke({
        "topic": topic,
        "research": research_context
    })

    state["report"] = report

    print("\nFinal Report:\n")
    print(report)

    # -------------------------------------------------
    # STEP 4 — CRITIC
    # -------------------------------------------------

    print("\n" + "=" * 50)
    print("STEP 4 - Critic")
    print("=" * 50)

    # short_report = compress_text(report, limit=3000)

    short_report = report[:3000]

    feedback = critic_chain.invoke({
        "report": short_report
    })

    state["feedback"] = feedback

    print("\nCritic Feedback:\n")
    print(feedback)

    return state


if __name__ == "__main__":

    topic = input("\nEnter a research topic: ")

    run_research_pipeline(topic)