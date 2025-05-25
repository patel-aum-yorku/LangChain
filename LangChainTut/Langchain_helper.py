import os
from secret_key import API_KEY
os.environ['GEMINI_API_KEY'] = API_KEY


#Intialize the LLM
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.6,
    google_api_key=os.environ.get("GEMINI_API_KEY")
)



def generate_restaurant_name_and_items(cuisine):
   
    # Prompt template for generating restaurant name and menu items
    from langchain_core.prompts import PromptTemplate
    # it helps avoid writing same prompt again and again
    propmpt_template_name = PromptTemplate(
    input_variables=['cusine'],
    template = "I want to open a restaurant for {cusine} food, give me one fancy name for it."
    )

    propmpt_template_items = PromptTemplate(
    input_variables=['restuarant_name'],
    template = "Suggest me some menu items for {restuarant_name}. Return a it as a comma separated list. Just Give me the items, no other text."
    )
    from langchain.chains import LLMChain
    # chain 1
    name_chain = LLMChain(llm=llm, prompt=propmpt_template_name, output_key="restuarant_name")# chain 1

    # chain 2
    item_chain = LLMChain(llm=llm, prompt=propmpt_template_items, output_key = "menu_items") #chain 2

    from langchain.chains import SequentialChain
    seuqnetial_chain = SequentialChain(
        chains = [name_chain, item_chain],
        input_variables = ['cusine'],# the input cuisine
        output_variables = ['restuarant_name', 'menu_items'] # we want two outputs name and items
        )
    
    response = seuqnetial_chain({'cusine': cuisine})
    return response

if __name__ == "__main__":
    print(generate_restaurant_name_and_items("Indian"))