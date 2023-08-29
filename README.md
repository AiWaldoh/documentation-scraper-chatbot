## Components

### `scraper.py`
Scrapes website documentation. You need to specify the URL and output directory statically.

### `embedder.py`
Uses Langchain's ReadTheDocsLoader to read the scraped docs and embed them into Pinecone. **Note**: You need to statically specify the path where the scraped files are stored. Update the Pinecone namespace accordingly.

### `retrieval.py`
Backend component for the Streamlit UI to query the Pinecone database.

### `main.py`
Streamlit UI that resembles a ChatGPT web interface. The available docs are specified statically as radio items in this file.

## How to Use

1. **Installation**
    ```bash
    git clone [your-repository-link]
    cd [your-repository-name]
    pip install -r requirements.txt
    ```

2. **Environment Variables**
    Rename `.env.example` to `.env` and fill in the required keys.
    ```env
    OPENAI_API_KEY=
    PINECONE_API_KEY=
    PINECONE_ENV=
    ```

3. **Run Scraper**
    ```bash
    python scraper.py
    ```

4. **Run Embedder**
    Update the file path and Pinecone namespace statically.
    ```bash
    python embedder.py
    ```

5. **Run Streamlit UI**
    ```bash
    streamlit run main.py
    ```
## Contributing

Contributions are welcome! 

## License

This project is licensed under the MIT License.