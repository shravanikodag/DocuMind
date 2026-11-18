from sentence_transformers import SentenceTransformer

class EmbeddingService:
    MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2" # This model produce vector containing 348 numbers per sent.

    def __init__(self):
        self.model = SentenceTransformer(self.MODEL_NAME, device="cpu") #runs the ai model using the CPU

    def generate_embeddings(self, texts): #convert sentece into numerical vectors
        if not texts:
            raise ValueError("No provided for embedding generation.")

        embeddings = self.model.encode(texts, convert_to_numpy=True, normalize_embeddings=True) 
         #encode is the method in self.model to convert sentence into numerical vectors 
         #normalize means  entire vector has a mathematical length of 1
        #texts = ["I love Python", "I enjoy coding"] ,(2, 384)

        return embeddings
    




        
        
