from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import openai
from langchain_community.chat_models import ChatOpenAI
from langchain.callbacks import get_openai_callback
from pypdf import PdfReader


def process_text(text):
    """
    Process the given string by spilling them into chunks and converting 
    these chunks into embeddings to form a knoledge base.
    """
    
    #Initalize a text splitter to devide the text into managable chunks
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000, 
        chunk_overlap=200,
        length_function=len
    )
    
    chunks=text_splitter.split_text(text) #split text into chunks
    
    #load model from genrating embedding from Huggingface
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    
    #Create FAISS indext from the text chunk using embeddings
    knowledgebase= FAISS.from_texts(chunks, embeddings)
    
    return knowledgebase




def summarizer(pdf):
    
    if pdf is not None:
        # If a PDF file is provided
        
        
        # Read the PDF file
        pdf_reader = PdfReader(pdf)
        text = ""
        
        #Extract from each page of the pdf
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
            
            
        # Process the extracted text to create a knowledge base
        knowledgeBase = process_text(text)
        
        # Define the query for summarization
        query= "Summarize the content of uploaded PDF file in approximatly 3-5 sentences."
        
        if query:
            #perform the simmilarity search in the knowledge base using the query:
            docs = knowledgeBase.similarity_search(query)
            
            
            #Specify the model to use for genrating the summary
            OpenAIModel="gpt-3.5-turbo-16k"
            llm=ChatOpenAI(model=OpenAIModel, temperature=0.8)
            
            
            #Load a question-answering chain with the specified model
            chain=load_qa_chain(llm,chain_type='stuff')
            
            with get_openai_callback() as cost:
                # Run the chain to get a response and track the cost
                response = chain.run(input_documents=docs, question=query)
                print(cost)  # Print the cost of the operation
                return response  # Return the generated summary
            