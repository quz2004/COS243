# Building a World Bank Data Visual Analyzer with LangChain and Function Calling

This tutorial will guide you through building a sophisticated data analysis system that combines LangChain, OpenAI's GPT-4o-mini, and the World Bank API. We'll create a system that can:
1. Parse natural language queries using function calling
2. Fetch and visualize World Bank data
3. Analyze trends using multi-modal AI

## Prerequisites

```bash
pip install langchain openai plotly pandas wbdata python-dotenv
```

## Part 1: Setting Up Environment and Constants

First, let's set up our environment and define our data structures:

```python
from dotenv import load_dotenv
import os
load_dotenv()

# Initialize AI models
query_parser = ChatOpenAI(model="gpt-4o-mini", temperature=0)
analysis_chat = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Define available data
INDICATORS = {
    'education': {'SE.XPD.TOTL.GD.ZS': 'Government expenditure on education (% of GDP)'},
    'gdp': {'NY.GDP.MKTP.KD': 'GDP (constant 2015 US$)'},
    'health': {'SH.XPD.CHEX.GD.ZS': 'Current health expenditure (% of GDP)'}
}

COUNTRIES = {
    'japan': 'JPN',
    'china': 'CHN',
    'usa': 'USA',
    'india': 'IND'
}
```

## Part 2: Query Parsing with Function Calling

The magic happens in our query parser. Let's break down how function calling works:

```python
def parse_query(query: str) -> Dict:
    function_schema = {
        "name": "extract_query_parameters",
        "description": "Extract the indicator type and countries from the query",
        "parameters": {
            "type": "object",
            "properties": {
                "indicator": {
                    "type": "string",
                    "enum": list(INDICATORS.keys()),
                    "description": "The type of indicator being requested"
                },
                "countries": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": list(COUNTRIES.keys())
                    },
                    "description": "List of countries mentioned in the query"
                }
            },
            "required": ["indicator", "countries"]
        }
    }

    messages = [
        HumanMessage(content=f'Extract the indicator and countries from: "{query}"')
    ]

    response = query_parser.invoke(
        messages,
        functions=[function_schema],
        function_call={"name": "extract_query_parameters"}
    )

    return json.loads(response.additional_kwargs['function_call']['arguments'])
```

Key points about function calling:
1. The `function_schema` defines the expected output structure
2. `enum` fields restrict values to our predefined options
3. The model will structure its response to match this schema exactly

## Part 3: Data Visualization

Next, we create our plotting functions:

```python
def create_trend_plot(df: pd.DataFrame, indicator_name: str, value_column: str) -> Tuple[go.Figure, str]:
    """Create and encode a plot for analysis."""
    fig = px.line(df, x='date', y=value_column, color='country',
                  title=f'{indicator_name} Trends')
    
    fig.show()  # Display in console
    return fig, encode_plot_to_base64(fig)  # Return for AI analysis
```

## Part 4: Multi-modal Analysis

The analysis phase uses vision capabilities:

```python
def analyze_plot(fig_base64: str, indicator: str, countries: List[str]) -> str:
    messages = [
        HumanMessage(content=[
            {
                "type": "text",
                "text": f"Analyze {indicator} trends for {', '.join(countries)}:"
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{fig_base64}"
                }
            }
        ])
    ]
    
    return analysis_chat.invoke(messages).content
```

## Part 5: Putting It All Together

Here's how to assemble the components:

1. Create a new Python file (`world_bank_analyzer.py`)
2. Import required libraries
3. Copy the constants (INDICATORS, COUNTRIES)
4. Add the helper functions
5. Implement the main analysis function:

```python
def analyze_with_plots(query: str) -> str:
    # 1. Parse query
    params = parse_query(query)
    
    # 2. Fetch data
    dfs = [get_country_data(country, params['indicator']) 
           for country in params['countries']]
    
    # 3. Create visualization
    fig, img_base64 = create_trend_plot(pd.concat(dfs))
    
    # 4. Analyze with AI
    return analyze_plot(img_base64, params['indicator'], params['countries'])
```

## Exercise: Migrating to DeepInfra

As an exercise, modify the code to use DeepInfra's Llama-3.2-11B-Vision-Instruct model:

1. Sign up for DeepInfra API access
2. Install their Python client:
```bash
pip install deepinfra
```

3. Modify the model initialization:
```python
from deepinfra import ChatCompletion

def get_deepinfra_chat():
    return ChatCompletion(
        model="meta-llama/Llama-3.2-11B-Vision-Instruct",
        api_key=os.getenv("DEEPINFRA_API_KEY")
    )
```

4. Research DeepInfra's documentation for:
   - Function calling format
   - Image input format
   - Response structure

Hints for migration:
- DeepInfra uses a different format for sending images
- You'll need to modify the message structure
- Function calling might have a slightly different syntax
- Check their documentation for rate limits and pricing

## Challenge Questions

1. How would you modify the function schema to include date ranges?
2. Can you add error handling for rate limits?
3. How would you implement caching for frequently requested data?
4. How could you optimize the image encoding for faster analysis?

## Next Steps

1. Add more indicators and countries
2. Implement data caching
3. Add comparative analysis between indicators
4. Create a web interface using Gradio and deploy on HF space

Remember to always check the API documentation and update your dependencies regularly!
 
## Rubric
- Migration of code to use deepinfra 60%
- Completion of any two of the challenge questions 40%
- Any part of next steps 10% bonus
