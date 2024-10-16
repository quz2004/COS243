In this assignment, you will create a Langchain function call app that retrieves GDP data for two countries, then uses ChatGPT to compare and analyze their economic growth. Follow the steps below to complete the assignment.

## Step 1: Set up the environment

1. Install the required libraries:
   ```
   pip install wbdata langchain openai python-dotenv
   ```

2. Create a `.env` file in your project directory and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Step 2: Load the World Bank data

Create a Python script named `gdp_comparison.py` and add the following code to load the World Bank data:

```python
import wbdata
import pandas as pd
from datetime import datetime

def get_country_gdp(country_code, start_year, end_year):
    # Define the indicator for GDP (constant 2015 US$)
    indicators = {'NY.GDP.MKTP.KD': 'GDP'}

    # Fetch the data
    data = wbdata.get_dataframe(indicators, country=country_code, 
                                data_date=(f"{start_year}:{end_year}"))
    
    # Clean and format the data
    data = data.reset_index()
    data['date'] = pd.to_datetime(data['date']).dt.year
    data = data.sort_values('date')
    
    return data

# Example usage:
# gdp_data = get_country_gdp('USA', 2010, 2020)
# print(gdp_data)
```

## Step 3: Create Langchain function calls

Add the following code to create Langchain function calls for retrieving GDP data:

```python

from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, FunctionMessage


load_dotenv()

chat = ChatOpenAI(temperature=0)

def get_gdp_data(country_code: str, start_year: int, end_year: int) -> str:
    """Get GDP data for a specific country and time range."""
    data = get_country_gdp(country_code, start_year, end_year)
    return data.to_json()

functions = [
    {
        "name": "get_gdp_data",
        "description": "Get GDP data for a specific country and time range",
        "parameters": {
            "type": "object",
            "properties": {
                "country_code": {
                    "type": "string",
                    "description": "The country code (e.g., 'USA' for United States)"
                },
                "start_year": {
                    "type": "integer",
                    "description": "The start year for the data range"
                },
                "end_year": {
                    "type": "integer",
                    "description": "The end year for the data range"
                }
            },
            "required": ["country_code", "start_year", "end_year"]
        }
    }
]

def compare_gdp_growth(country1: str, country2: str, start_year: int, end_year: int) -> str:
    """Compare GDP growth between two countries."""
    
    messages = [
        HumanMessage(content=f"Compare the GDP growth of {country1} and {country2} from {start_year} to {end_year}."),
        AIMessage(content="Certainly! To compare the GDP growth of these two countries, I'll need to retrieve their GDP data for the specified time range. Let me do that for you."),
        FunctionMessage(name="get_gdp_data", content=get_gdp_data(country1, start_year, end_year)),
        AIMessage(content=f"I've retrieved the GDP data for {country1}. Now, let me get the data for {country2}."),
        FunctionMessage(name="get_gdp_data", content=get_gdp_data(country2, start_year, end_year)),
        AIMessage(content=f"Great, I now have the GDP data for both {country1} and {country2}. I'll analyze this data and provide a comparison of their economic growth."),
        HumanMessage(content="Please provide a detailed analysis comparing the GDP growth of the two countries, including growth rates, trends, and any significant observations.")
    ]

    response = chat(messages)
    return response.content

# Example usage:
# result = compare_gdp_growth('USA', 'CHN', 2010, 2020)
# print(result)
```

## Step 4: Create the main application

Add the following code to create the main application that allows users to input countries and year range for comparison:

```python
def main():
    print("Welcome to the GDP Growth Comparison Tool!")
    
    country1 = input("Enter the first country code (e.g., USA): ").upper()
    country2 = input("Enter the second country code (e.g., CHN): ").upper()
    start_year = int(input("Enter the start year: "))
    end_year = int(input("Enter the end year: "))

    print("\nAnalyzing GDP growth...")
    result = compare_gdp_growth(country1, country2, start_year, end_year)
    print("\nAnalysis Results:")
    print(result)

if __name__ == "__main__":
    main()
```

## Your Task

1. Implement the code provided above in the `gdp_comparison.py` file.
2. Test the application with different pairs of countries and time ranges.
3. Analyze the output provided by the ChatGPT model and ensure it provides meaningful insights into the economic growth comparison.
4. (Optional) Extend the application to include additional economic indicators or visualizations of the GDP data.

## Submission

Submit your completed `gdp_comparison.py` file along with a brief report (maximum 500 words) discussing:

1. The challenges you faced while implementing the application.
2. Your observations on the quality and accuracy of the ChatGPT-generated analysis.
3. Suggestions for improving the application or extending its functionality.

 
