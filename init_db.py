import os
import google.generativeai as genai
import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings
from google.api_core import retry
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))

class GeminiEmbeddingFunction(EmbeddingFunction):
    document_mode = True

    def __call__(self, input: Documents) -> Embeddings:
        task_type = "retrieval_document" if self.document_mode else "retrieval_query"
        retry_policy = {"retry": retry.Retry(predicate=retry.if_transient_error)}

        response = genai.embed_content(
            model="models/text-embedding-004",
            content=input,
            task_type=task_type,
            request_options=retry_policy,
        )
        return response["embedding"]

def initialize_db():
    """Initialize and populate the ChromaDB instance."""
    chroma_client = chromadb.Client(config={
        "storage": {
            "type": "disk",
            "path": "./chromadb_storage"  # Path for persistent storage
        }
    })

    # Create or get the collection
    DB_NAME = "cory_db"
    embed_fn = GeminiEmbeddingFunction()
    embed_fn.document_mode = True

    db = chroma_client.get_or_create_collection(name=DB_NAME, embedding_function=embed_fn)

    # Add resume text to the collection
    resume_text = """Cory DeWitt
    773-749-3827 | cjdewitt@usc.edu | Github | LinkedIn
    EDUCATION
    University of Southern California Graduating May 2025
    Degree: Bachelor’s in Computer Science
    Los Angeles, CA
    August 2021 – Present
    - QuestBridge National Match Recipient ~ full-ride to attend USC out of 25,000 applicants
    - Dean's List Fall and Spring 2022
    - Shift SC’s Ethics of Artificial Intelligence Initiative Lead
    Relevant Coursework: Artificial Intelligence, Software Engineering, Data Structures, Algorithms, C++, Python, IOS Development, Linear Algebra, Calculus, Discrete Mathematics, Embedded Systems
    Relevant Skills: Python, C/C++, Swift, Java, TensorFlow, PyTorch, SQL, HTML, CSS, Flask, Django, R, Matlab, LIBGDX, Angr, Ghidra
    WORK EXPERIENCE
    Software Engineering Intern Mountain View, California Google LLC May 2024 - August 2024
    - Developed and deployed the Iterative Development Cycle (IDC) framework to enhance Gemini’s programming capabilities. Focused on agent orchestration and task-specific operations to effectively emulate the software engineering lifecycle.
    - Established a comprehensive performance evaluation system for IDC, utilizing open-source benchmarks to assess the code generation and correction capabilities of deployed agents, achieving a 97.46% test accuracy across diverse programming challenges.
    - Built a time-series analytics dashboard using internal Google technologies to monitor IDC’s performance metrics, accuracy rates, and system scalability, facilitating continuous improvement.
    - Deployed five AI agents, or Gems, in production environments. Each Gem is a custom instance of Gemini, acting as an expert in a specific domain or field.
    - Contributed to over 70 code submission and reviews, gaining an in-depth understanding of Gemini’s core infrastructure, microservices architecture, and large-scale distributed systems.
    - Presented my internship deliverables at four internal and public events, showcasing advancements in Gemini powered technologies.
    Undergraduate Researcher Marina Del Rey, California USC Information Science Institute STEEL Lab December 2022 - May 2024
    - Employed reverse engineering practices on the microcontrollers' firmware of various IoT devices, mainly autonomous drones, to enhance cyberattack resilience.
    - Leveraged OpenAI’s “text-davinci-002” large language model for cognitive data capture from unstructured/structured data sources.
    - Developed SensorLoader to extract communication data from microcontrollers, enhancing the cyber-physical security of IoT devices.
    - Earned funding from DARPA, NSF, and ISI. Published a paper in the International Workshop on Security and Privacy of Sensing Systems (Sensors S&P ‘23) in Istanbul, Turkey.
    PROJECTS
    - Research-GPT: Created an academic research assistant powered by OpenAI's GPT-3.5 language model, streamlining literature reviews and knowledge discovery in the academic domain. Integrated Python and Flask to seamlessly connect with ArXiv API for academic paper retrieval and metadata. Leveraged Python libraries for efficient literature searches based on subject matter and PDF text analysis.
    - Duel Doodle Jump: Developed a multiplayer web application of the popular video game Doodle Jump as a part of a team. Focused on the game functionality and game physics using Java and LIBGDX.
    - NBA Data Analysis: Engineered a web application using Python, SQL, Flask, HTML, and CSS, enabling users to explore NBA player statistics since 1993. Utilized machine learning to forecast hypothetical season stats with matplotlib and pandas. In the process of acquiring a domain for the project's web presence.
    - Mind-Mate: Developed an IOS mobile application with Swift, leveraged AI to serve as a pocket companion that advocates for mental health. Recommends locations and events based on mental state."""
    db.add(documents=[resume_text], ids=["resume_doc"])

    print("Database initialized and populated with resume text.")
    return db  # Return the database instance for app usage

if __name__ == "__main__":
    initialize_db()