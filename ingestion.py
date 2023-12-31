import os
from langchain.document_loaders import ReadTheDocsLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone

# pinecone.init(
#     api_key=os.environ["PINECONE_API_KEY"],
#     environment=os.environ["PINECONE_ENVIRONMENT_REGION"],
# )


def ingest_docs() -> None:
    loader = ReadTheDocsLoader(path="/home/joe/Desktop/My Coding Projects/AI/MyProjects/documentation-helper/langchain-docs")
    raw_documents = loader.load()
    print(f"loaded {len(raw_documents) }documents")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=100, separators=["\n\n", "\n", " ", ""]
    )
    documents = text_splitter.split_documents(documents=raw_documents)
    print(f"Splitted into {len(documents)} chunks")

    for doc in documents:
        old_path = doc.metadata["source"]
        new_url = old_path.replace("langchain-docs", "https:/")
        doc.metadata.update({"source": new_url})
    print(documents[-1]["source"])
    print(f"Going to insert {len(documents)} to Pinecone")
    embeddings = OpenAIEmbeddings()
    Pinecone.from_documents(
        documents[3969:], embeddings, index_name="langchain-doc-index"
    )
    print("****** Added to Pinecone vectorstore vectors")


if __name__ == "__main__":
    ingest_docs()
