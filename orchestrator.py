#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# orchestrator.py

from agents.language_agent import LanguageAgent
from agents.retriever_agent import RetrieverAgent
from langchain.agents import AgentExecutor
from agents.scraping_agent import ScrapingAgent

from agents.language_agent import LanguageAgent
from agents.retriever_agent import RetrieverAgent
from agents.scraping_agent import ScrapingAgent




class Orchestrator:
    def __init__(self, agent_executor: AgentExecutor):
        self.language_agent = LanguageAgent()
        self.retriever_agent = RetrieverAgent()
        self.agent_executor = agent_executor
        self.scraping_agent = ScrapingAgent()


    def process_query(self, question: str, pdf_path: str = None):
        """
        Process a user query and route it to the appropriate agent.
        Returns the final output (summary or raw text).
        """

        # Basic manual routing based on keywords
        if "Asia tech" in question.lower() or "allocation" in question.lower():
            # Simulate or plug real analytics results
            allocation_today = 22
            allocation_yesterday = 18
            earnings_summary = "TSMC beat estimates by 4%, Samsung missed by 2%"
            sentiment = "neutral with a cautionary tilt due to rising yields"

            summary = self.language_agent.generate_summary(
                allocation_today=allocation_today,
                allocation_yesterday=allocation_yesterday,
                earnings_summary=earnings_summary,
                sentiment=sentiment
            )
            return summary

        elif pdf_path:
            # Use retriever agent to answer from a PDF document
            retriever = self.retriever_agent.get_retriever(pdf_path)
            docs = retriever.invoke(question)
            return docs[0].page_content if docs else "No relevant answer found in document."
            
        elif "news" in question.lower() or "headline" in question.lower():
            headlines = self.scraping_agent.get_market_headlines()
            if isinstance(headlines, list):
                return "\n".join([f"- {h['title']}" for h in headlines])
            else:
                return "Unable to fetch news at the moment."
        

        else:
            # Fallback to generic finance agent (LangChain AgentExecutor)
            result = self.agent_executor.invoke({"input": question})
            return result["output"]


# Example usage (test script)
if __name__ == "__main__":
    from AI_AGENTS import finance_agent_executor  # Adjust import if needed

    orchestrator = Orchestrator(agent_executor=finance_agent_executor)

    question = "What’s our risk exposure in Asia tech stocks today?"
    result = orchestrator.process_query(question)
    print("🧠 Final Output:\n", result)

