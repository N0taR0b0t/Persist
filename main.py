from app import create_app
from api_setup import setup_openai_api

if __name__ == "__main__":
    setup_openai_api()
    demo = create_app()
    demo.launch(share=True)  # Set `share=True` if you want to create a public link