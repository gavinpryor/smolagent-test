import os
import subprocess
import streamlit as st
from smolagents import CodeAgent, DuckDuckGoSearchTool, HfApiModel

model = HfApiModel(token=TOKEN)

agent = CodeAgent(tools=[DuckDuckGoSearchTool()], model=model, add_base_tools=True, additional_authorized_imports=["requests", "kbcstorage.client"])

# streamlit
st.title("Keboola Project Agent Test")
st.write("Ask questions about your Keboola project")

api_token = st.text_input("Enter your Keboola project API token:", type="password")

query = st.text_area("Enter your question:")

if st.button("Ask"):
    if not api_token:
        st.error("Please provide your Keboola project API token.")
    elif not query:
        st.error("Please enter a question.")
    else:
        with st.spinner("Generating a response..."):
            try:
                new_query = f"""Here are some links to the Storage API and Keboola CLI documentation:
                https://developers.keboola.com/cli/structure/ 
                https://keboola.docs.apiary.io/#reference/tables/unload-data-asynchronously/link-shared-bucket 
                https://github.com/keboola/sapi-python-client
                Here is a link to the Keboola Storage Python Client Library documentation:
                https://developers.keboola.com/integrate/storage/python-client/
                Search those links and retain the information. Here is the keboola project url:
                https://connection.europe-west3.gcp.keboola.com/
                Here is an example of a Keboola Extractor. Names of files are written before each code in brackets:
                [config.json]{{
                "parameters": {{
                    "#api_token": "KBC::ProjectSecureGKMS::eJwBdQGK/mE6Mjp7aToxO3M6MTIyOiLe9QIA38Wb1ZHHzrwfZyQsqVViljLMB7sWThsvoWYIM6bowHmX9I0rdspyLauLEdX31zE/DRFILGe9qbUPqH6UXjPw9+rfSSz3cySd+In1gUtezAyqwwR2XCCWmVd3RZKwfDTpa5/25yIizwjr6KOqD7SBAP0rWngHvSI7aTowO3M6MjE5OiIKJAAuMnUn0tvrCM428Mv2nzGDW01vy59m/G0KcJVk5fhOrqv1nhKyAQAAG4n8FpSOGYTKYIkncMt/fim+9x03nlZ8R6BirGLKvfivDuamv9oresLs0cK0B8emXD/eXpUu78Pd5njYSkXi9ZkGm+y9s88LKZp58OIKdBvlH8IvEGOqwzeVdVaMEV1RL3kWXuR6aEmynx+sLGvCMJgkuuIWWFcZnI8OdAR57KxnFCDYe57yk8s/8hOH4WYchiraoKkn99+sSQ5toDvmWpkRBpnC2gsu5Jgb3BXw3hQiO330V7Em",
                    "api_version": "2024-01",
                    "endpoints": {{
                    "customers": true,
                    "events": [],
                    "inventory": true,
                    "orders": true,
                    "product_metafields": false,
                    "products": true,
                    "variant_metafields": false
                    }},
                    "loading_options": {{
                    "date_since": "6 months ago",
                    "date_to": "1 day ago",
                    "incremental_output": 1
                    }},
                    "shop": "keboola-sample-data.myshopify.com"
                }},
                "processors": {{
                    "before": [],
                    "after": []
                }}
                }}
                [meta.json]{{
                "name": "Data Source [IN-ECOMMERCE-SHOPIFY] /JEJMHsJU",
                "isDisabled": false
                }}
                
                Using the information you gathered from the docs and 
                Using the Keboola Storage API token: {api_token}, {query}. Actually perform the actions using Python code
                and the requests library.
                """
                response = agent.run(new_query)
                st.success("Response: ")
                st.write(response)
            except Exception as e:
                st.error(f"{e}")

if st.checkbox("Show agent logs"):
    st.write(agent.logs)
