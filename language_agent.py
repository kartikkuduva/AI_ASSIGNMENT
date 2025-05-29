#!/usr/bin/env python
# coding: utf-8

# In[1]:


# agents/language_agent.py

from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
import os

class LanguageAgent:
    def __init__(self, model_name="llama3-8b-8192"):
        self.groq_api_key = os.getenv("groq_api")  # Or pass explicitly
        self.llm = ChatGroq(api_key=self.groq_api_key, model=model_name)

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", 
             "You are a financial assistant generating spoken daily summaries for a portfolio manager. "
             "Be concise, use data from the input, and explain like a Bloomberg analyst."),
            ("human", 
             "Data:\n"
             "- Asia tech allocation today: {allocation_today}%\n"
             "- Allocation yesterday: {allocation_yesterday}%\n"
             "- Earnings: {earnings_summary}\n"
             "- Market sentiment: {sentiment}\n\n"
             "Now generate a spoken market brief.")
        ])

        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def generate_summary(self, allocation_today, allocation_yesterday, earnings_summary, sentiment):
        return self.chain.run({
            "allocation_today": allocation_today,
            "allocation_yesterday": allocation_yesterday,
            "earnings_summary": earnings_summary,
            "sentiment": sentiment
        })

