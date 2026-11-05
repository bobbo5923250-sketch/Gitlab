// =============================================================
//  แก้ข้อมูลของคุณที่ไฟล์นี้ไฟล์เดียว — ไม่ต้องแตะ HTML/CSS
// =============================================================
window.PORTFOLIO = {
  name: "Your Name",
  role: "AI Engineer",
  tagline:
    "I build production-ready LLM applications, retrieval systems, and ML pipelines — from prototype to deployment.",
  location: "Bangkok, Thailand",
  email: "you@example.com",
  resumeUrl: "", // เช่น "resume.pdf" (วางไฟล์ไว้ในโฟลเดอร์เดียวกัน) — เว้นว่างเพื่อซ่อนปุ่ม
  socials: [
    { label: "GitHub", url: "https://github.com/bobbo5923250-sketch" },
    { label: "LinkedIn", url: "https://www.linkedin.com/in/your-username" },
    { label: "Hugging Face", url: "https://huggingface.co/your-username" },
  ],

  about: [
    "I'm an AI engineer focused on turning large language models and machine learning research into reliable software that people actually use.",
    "My work spans retrieval-augmented generation, agent tooling, model fine-tuning and evaluation, and the MLOps needed to keep models healthy in production.",
  ],

  stats: [
    { value: "4", label: "End-to-end AI projects" },
    { value: "100%", label: "Runs locally on free models" },
    { value: "19", label: "Automated tests" },
  ],

  skills: [
    {
      group: "LLM & GenAI",
      items: ["RAG", "Agents & Tool Use", "Prompt Engineering", "Fine-tuning (LoRA/QLoRA)", "LLM Evaluation", "Embeddings"],
    },
    {
      group: "Machine Learning",
      items: ["PyTorch", "Hugging Face Transformers", "scikit-learn", "Computer Vision", "NLP", "Time Series"],
    },
    {
      group: "MLOps & Infra",
      items: ["Docker", "FastAPI", "MLflow", "GitHub Actions", "AWS / GCP", "Vector DBs (pgvector, Qdrant)"],
    },
    {
      group: "Languages",
      items: ["Python", "SQL", "TypeScript", "Bash"],
    },
  ],

  projects: [
    {
      title: "RAG Doc Chat",
      summary:
        "Chat with your own PDFs and text files. Answers are grounded in the documents with numbered citations to file and page — fully local with Ollama.",
      highlights: [
        "Sentence-aware chunking with overlap; multilingual bge-m3 embeddings (Thai + English)",
        "NumPy cosine vector store with save/load — no external database",
        "Similarity threshold + grounded prompt to reduce hallucinations; streaming Streamlit UI",
      ],
      tags: ["LLM", "RAG", "Ollama", "Streamlit"],
      repo: "https://github.com/bobbo5923250-sketch/rag-doc-chat",
      demo: "",
      featured: true,
    },
    {
      title: "Tool-using AI Agent",
      summary:
        "An LLM agent that decides when to search the web, calculate, check the time or read files — built on native tool calling without LangChain.",
      highlights: [
        "Hand-written agent loop (~60 lines) with step limit and visible reasoning trace",
        "Safe AST-based calculator and path-traversal protection for file access",
        "Web UI showing every tool call, plus a terminal mode",
      ],
      tags: ["LLM", "Agents", "Tool Calling", "Ollama"],
      repo: "https://github.com/bobbo5923250-sketch/ai-agent",
      demo: "",
      featured: true,
    },
    {
      title: "Thai Sentiment API",
      summary:
        "Thai social-media sentiment classifier (pos / neu / neg / question) served as a production-style REST API.",
      highlights: [
        "Compared char n-gram vs. PyThaiNLP word features; selected on a validation split",
        "Test accuracy 0.678, macro-F1 0.591 on 2,674 Wisesight posts, with confusion-matrix error analysis",
        "FastAPI + Docker + pytest + GitHub Actions CI",
      ],
      tags: ["NLP", "Thai", "scikit-learn", "FastAPI", "Docker"],
      repo: "https://github.com/bobbo5923250-sketch/thai-sentiment-api",
      demo: "",
      featured: true,
    },
    {
      title: "Object Detection Web App",
      summary:
        "Detects 80 everyday object types in photos or from a webcam using YOLO11, with a web demo and a batch CLI.",
      highlights: [
        "~56 ms per image on a laptop CPU with yolo11n",
        "Confidence threshold and class filtering; CSV report for whole folders",
        "Tests guard against RGB/BGR colour mix-ups",
      ],
      tags: ["Computer Vision", "YOLO", "PyTorch", "Gradio"],
      repo: "https://github.com/bobbo5923250-sketch/object-detection-app",
      demo: "",
      featured: false,
    },
  ],

  experience: [
    {
      role: "AI Engineer",
      company: "Company Name",
      period: "2024 — Present",
      points: [
        "Led development of an internal LLM assistant used by 500+ employees",
        "Built an evaluation harness that gates every model and prompt change",
      ],
    },
    {
      role: "Machine Learning Engineer",
      company: "Previous Company",
      period: "2022 — 2024",
      points: [
        "Deployed forecasting and classification models serving 1M+ predictions per day",
        "Cut model training cost by 40% through data pipeline optimisation",
      ],
    },
  ],

  education: [
    {
      degree: "B.Eng. Computer Engineering",
      school: "University Name",
      period: "2018 — 2022",
    },
  ],

  certifications: [
    "Deep Learning Specialization — DeepLearning.AI",
    "AWS Certified Machine Learning — Specialty",
  ],
};
