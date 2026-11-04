class TextChunker:
    @staticmethod
    def chunk_text(text, chunk_size=500, overlap=100):
        if chunk_size<=0:
            raise ValueError("Chunk size must be positive. ")
        if overlap < 0 or overlap >=chunk_size:
            raise ValueError("Overlap must be non negative and smaller than chunk size.")

        text = " ".join(text.split())

        if not text:
            return []
        chunks = []
        start = 0

        while start < len(text):
            end = min(start + chunk_size, len(text))

            if end < len(text):
                boundary = text.rfind(" ", start, end)

                if boundary > start:
                    end = boundary
            chunk = text[start:end].strip()

            if chunk:
                chunks.append(chunk)

            if end >= len(text):
                break

            start = max(start+1,end-overlap)
        return chunks

    @staticmethod
    def chunk_pages(extracted_pages, chunk_size=500, overlap=100):
        all_chunks = []
        chunk_index = 0

        for page in extracted_pages:
            page_chunks = TextChunker.chunk_text(
                page["content"],
                chunk_size,
                overlap
            )

            for content in page_chunks:

                all_chunks.append(
                    {
                    "chunk_index": chunk_index,
                    "page_number": page["page_number"],
                    "content": content
                    }
                )
                chunk_index += 1
        return all_chunks
    

        
        
