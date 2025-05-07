from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()
pdf_path=Path(__file__).parent / "pdf1.pdf"
#creating a pdf loader
loader=PyPDFLoader(pdf_path)
#creating a text splitting unit
text_splitter = RecursiveCharacterTextSplitter(

    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
    is_separator_regex=False,
)
#creating an embedder
embedder=OpenAIEmbeddings(
    api_key=os.getenv('OPENAI_API_KEY'),
    model='text-embedding-3-large'
)
docs=loader.load()
print(len(docs))
split_docs=text_splitter.split_documents(documents=docs)
print(len(split_docs))
#creating  vector store creator
# vector_store=QdrantVectorStore.from_documents(
# documents=[],
# embedding=embedder,
# collection_name="learning_langhain",
# url='http://localhost:6333'
# )
# vector_store.add_documents(documents=split_docs)
# print("ingestion done")

#creating a vector store retreiver
retreiver=QdrantVectorStore.from_existing_collection(
    collection_name="learning_langhain",
    url='http://localhost:6333',
    embedding=embedder
)
print("revelkant chunks===>",search_result)
query=input(">")
search_result=retreiver.similarity_search(
    query=query
)
systtemPrompt=f'''
you are a helpful ai assistant ant goes through the entire given context and gives the user the answers for the question and if the question is out of context you return "sorry the solution to this is not in the given context"

provided context:
{search_result}
'''


