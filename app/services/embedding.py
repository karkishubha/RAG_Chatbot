from typing import Sequence, List
from app.config import settings
from cohere import ClientV2


class EmbeddingClient:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or settings.EMBEDDING_API_KEY
        self.client = ClientV2(self.api_key)

    async def embed_texts(self, texts: Sequence[str]) -> List[List[float]]:
        response = self.client.embed(
            model="embed-english-v2.0",
            texts=texts,
            input_type="search_document"
        )

        
        valid_embeddings = []
        for e in response.embeddings:
            if isinstance(e, list) and all(isinstance(x, float) for x in e):
                valid_embeddings.append(e)
            else:
                
                valid_embeddings.append([0.0] * 4096)

        return valid_embeddings


    async def generate_text(self, prompt: str) -> str:
        response = self.client.chat(
            model="command-a-03-2025",
            messages=[{"role": "user", "content": prompt}]
        )
       
        try:
            return response.message.content[0].text.strip()
        except (AttributeError, IndexError, KeyError) as e:
            print(f"Error accessing response content: {e}")
            return ""