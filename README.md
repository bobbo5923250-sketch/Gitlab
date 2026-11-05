# Hi, I'm Your Name 👋

**AI Engineer** based in Bangkok, Thailand. I build LLM applications, retrieval systems and ML services that run end to end, and I measure whether they work before calling them done.

🌐 **Portfolio:** [bobbo5923250-sketch.github.io](https://bobbo5923250-sketch.github.io) · 📫 **Email:** you@example.com · 💼 [LinkedIn](https://www.linkedin.com/in/your-username)

---

## 🚀 Featured projects

| Project | What it does | Highlights |
| --- | --- | --- |
| [**RAG Doc Chat**](https://github.com/bobbo5923250-sketch/rag-doc-chat) | Chat with your own PDFs; answers cite the source file and page | Local LLM via Ollama · multilingual `bge-m3` embeddings · reduced Thai→Chinese language drift from 2/10 to 0/20 answers |
| [**Tool-using AI Agent**](https://github.com/bobbo5923250-sketch/ai-agent) | LLM agent that searches the web, calculates, and analyses CSV files | Agent loop written from scratch (no LangChain) · safe AST calculator · 18/18 correct on a fixed Thai/English test set |
| [**Thai Sentiment API**](https://github.com/bobbo5923250-sketch/thai-sentiment-api) | Sentiment classifier for Thai social-media posts, served as a REST API | Macro-F1 0.591 / accuracy 0.678 on 2,674 test posts · FastAPI + Docker + CI |
| [**Object Detection App**](https://github.com/bobbo5923250-sketch/object-detection-app) | Detects 80 object types in photos or from a webcam | YOLO11 · ~56 ms per image on CPU · Gradio web demo + batch CLI |

Every project runs **locally on free, open models**, includes automated tests (24 in total), and documents what I tried, what failed, and how I fixed it.

---

## 🛠️ Tech stack

**LLM & GenAI** — RAG · AI agents & tool calling · prompt engineering · embeddings · Ollama · Typhoon / Llama / Qwen

**Machine learning** — PyTorch · scikit-learn · Ultralytics YOLO · PyThaiNLP · NLP · computer vision

**Engineering** — Python · FastAPI · Streamlit · Gradio · Docker · GitHub Actions · pytest · Git

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?logo=pytorch&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?logo=scikitlearn&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-000000?logo=ollama&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?logo=githubactions&logoColor=white)

---

## 🧭 How I work

- **Measure first.** Every claim in my READMEs comes from a real run — test-set scores, confusion matrices, latency, error counts.
- **Fix the cause, not the symptom.** When prompting couldn't stop an LLM from switching to Chinese, I compared models and switched to a Thai-tuned one.
- **Give models tools for what they're bad at.** My agent calls a CSV tool instead of adding up numbers itself.

## 🌱 Currently learning

- Fine-tuning Thai transformers (WangchanBERTa) and comparing them with classical baselines
- Evaluating RAG systems: retrieval hit rate and answer faithfulness
- Deploying models to the cloud

---

<sub>💬 Open to AI / ML engineering roles — feel free to reach out.</sub>
