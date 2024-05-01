from dotenv import load_dotenv
from typing import Tuple
import os
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI

from output_parsers import summary_parser, Summary
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent


def ice_breaker_with(name: str) -> Tuple[Summary, str]:
    linkedin_username = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_username, mock=True)
    summary_template = """
    given the Linkedin information {information} about a person I want you to create:
    1. A short summary
    2. Two interesting facts about them
    \n{format_instructions}
    """
    summary_prompt_template = PromptTemplate(input_variables=["information"],
                                             template=summary_template,
                                             partial_variables={
                                                 "format_instructions": summary_parser.get_format_instructions()
                                             })
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    chain = summary_prompt_template | llm | summary_parser
    res: Summary = chain.invoke(input={"information": linkedin_data})
    return res, linkedin_data.get("profile_pic_url")


if __name__ == "__main__":
    load_dotenv()
    print("Ice breaker enter")
    ice_breaker_with(name="Dam Thi Anh Data Scientist")
