#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
huggingface_api = os.getenv("huggingface_api")
langsmith_api = os.getenv("langsmith_api")
langchain_api = os.getenv("langchain_api")
groq_api = os.getenv("groq_api")


# In[2]:


from langchain.text_splitter import RecursiveCharacterTextSplitter


# In[3]:


from langchain_community.document_loaders import PyPDFLoader


# In[4]:


from langchain_community.embeddings import OllamaEmbeddings
# embeddings = (OllamaEmbeddings(model="llama3.2:1b"))


# In[5]:


from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field


# In[6]:


from typing import Literal


# In[7]:


from langchain_groq import ChatGroq


# In[8]:


from langchain_core.tools import tool,StructuredTool
from datetime import date


# In[9]:


import yfinance as yf


# In[10]:


# from agents.retriever_agent import RetrieverAgent

# retriever_agent = RetrieverAgent()
# retriever = retriever_agent.get_retriever(pdf_path)


# In[11]:


from langchain_core.tools import tool, StructuredTool
from datetime import date

@tool
def company_information(ticker: str) -> dict:
    """Use this tool to retrieve company information like address, industry, sector, company officers, business summary, website,
       marketCap, current price, ebitda, total debt, total revenue, debt-to-equity, etc."""
    
    ticker_obj = yf.Ticker(ticker)
    ticker_info = ticker_obj.get_info()

    return ticker_info


# In[12]:


@tool
def last_dividend_and_earnings_date(ticker: str) -> dict:
    """
    Use this tool to retrieve company's last dividend date and earnings release dates.
    It does not provide information about historical dividend yields.
    """
    ticker_obj = yf.Ticker(ticker)
    
    return ticker_obj.get_calendar()

@tool
def summary_of_mutual_fund_holders(ticker: str) -> dict:
    """
    Use this tool to retrieve company's top mutual fund holders. 
    It also returns their percentage of share, stock count and value of holdings.
    """
    ticker_obj = yf.Ticker(ticker)
    mf_holders = ticker_obj.get_mutualfund_holders()
    
    return mf_holders.to_dict(orient="records")

@tool
def summary_of_institutional_holders(ticker: str) -> dict:
    """
    Use this tool to retrieve company's top institutional holders. 
    It also returns their percentage of share, stock count and value of holdings.
    """
    ticker_obj = yf.Ticker(ticker)   
    inst_holders = ticker_obj.get_institutional_holders()
    
    return inst_holders.to_dict(orient="records")

@tool
def stock_grade_updrages_downgrades(ticker: str) -> dict:
    """
    Use this to retrieve grade ratings upgrades and downgrades details of particular stock.
    It'll provide name of firms along with 'To Grade' and 'From Grade' details. Grade date is also provided.
    """
    ticker_obj = yf.Ticker(ticker)
    
    curr_year = date.today().year
    
    upgrades_downgrades = ticker_obj.get_upgrades_downgrades()
    upgrades_downgrades = upgrades_downgrades.loc[upgrades_downgrades.index > f"{curr_year}-01-01"]
    upgrades_downgrades = upgrades_downgrades[upgrades_downgrades["Action"].isin(["up", "down"])]
    
    return upgrades_downgrades.to_dict(orient="records")

@tool
def stock_splits_history(ticker: str) -> dict:
    """
    Use this tool to retrieve company's historical stock splits data.
    """
    ticker_obj = yf.Ticker(ticker)
    hist_splits = ticker_obj.get_splits()
    
    return hist_splits.to_dict()

@tool
def stock_news(ticker: str) -> dict:
    """
    Use this to retrieve latest news articles discussing particular stock ticker.
    """
    ticker_obj = yf.Ticker(ticker)
    
    return ticker_obj.get_news()










# In[13]:


from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder

tools = [
         company_information,
         last_dividend_and_earnings_date,
         stock_splits_history,
         summary_of_mutual_fund_holders,
         summary_of_institutional_holders, 
         stock_grade_updrages_downgrades,
         stock_news
         
    
]

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. Try to answer user query using available tools.",
        ),
        MessagesPlaceholder(variable_name="messages"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

llama3 = ChatGroq(api_key=groq_api , model="llama3-8b-8192", temperature=0)

finance_agent = create_tool_calling_agent(llama3, tools, prompt)


# In[14]:


finance_agent_executor = AgentExecutor(agent=finance_agent, tools=tools, verbose=True)


# In[15]:


from langchain_core.messages import HumanMessage


# In[ ]:





# In[ ]:




