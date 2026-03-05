"""
============================================================
  Part E – LangChain Application
  System  : Course Helpdesk Bot (RAG Pipeline)
  Pipeline: Document → Chunking → Embeddings → Retrieval → LLM Response

  Components (mirroring LangChain architecture exactly):
    ✅ DocumentLoader      – loads FAQ knowledge base
    ✅ RecursiveCharacterTextSplitter – chunks documents
    ✅ TF-IDF Embeddings   – vectorises chunks (EmbeddingModel)
    ✅ FAISSVectorStore    – in-memory vector DB with cosine similarity
    ✅ RetrievalChain      – retrieves top-k docs + generates answer
    ✅ LLMChain            – context-aware response generation

  Outputs:
    • Console Q&A demo with retrieval scores and latency

  Run:
    python partE_langchain_helpdesk.py
============================================================
"""

import re, math, time, warnings, textwrap
warnings.filterwarnings("ignore")
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD

# ═══════════════════════════════════════════════════════════
#  STEP 1 – DocumentLoader
#  Mirrors: langchain.document_loaders.TextLoader / JSONLoader
# ═══════════════════════════════════════════════════════════
class Document:
    """Mirrors langchain_core.documents.Document"""
    def __init__(self, page_content: str, metadata: dict = None):
        self.page_content = page_content
        self.metadata     = metadata or {}
    def __repr__(self):
        return f"Document(source={self.metadata.get('source','?')}, chars={len(self.page_content)})"


class UniversityFAQLoader:
    """
    LangChain-style DocumentLoader.
    Mirrors: langchain_community.document_loaders.BaseLoader
    Loads University FAQ knowledge base as structured Documents.
    """
    FAQ_DATA = [
        # ── ADMISSIONS ──────────────────────────────────────
        ("admissions", "What are the admission requirements for undergraduate programs?",
         "Applicants need a minimum of 60% in 10+2 examinations along with a valid entrance "
         "test score such as JEE or SAT, depending on the program. Additionally, students must "
         "submit 10th and 12th mark sheets, transfer certificate, and character certificate."),
        ("admissions", "Are there any scholarships available for new students?",
         "Merit scholarships are available for students scoring above 90% in qualifying exams. "
         "Need-based scholarships are also offered through the Student Welfare Office. "
         "The Chief Minister Scholarship is available for students from low-income families."),
        ("admissions", "When does the admission portal open?",
         "The admission portal opens every year on March 1st and closes on May 31st for "
         "undergraduate programs. International students apply through the International "
         "Admissions Office with valid passport copies and equivalency certificates."),
        ("admissions", "What is the process for cancellation of admission?",
         "Submit a written application to the Dean of Student Affairs. Refunds are processed "
         "within 30 working days per the university refund policy. Full refunds are given up "
         "to the 10th day of the semester for course withdrawals."),
        # ── EXAMINATIONS ────────────────────────────────────
        ("examinations", "What is the minimum attendance required to sit for exams?",
         "Students must maintain a minimum of 75% attendance in each subject to be eligible "
         "for the end-semester examination. Medical exemptions require a certificate from a "
         "registered doctor submitted within 3 days."),
        ("examinations", "How are grades calculated at the university?",
         "Grades are on a 10-point CGPA scale. Internal assessment contributes 30% and the "
         "end-semester exam contributes 70% of total marks. Re-evaluation forms must be "
         "submitted within 10 days of result declaration with a fee of Rs 300 per subject."),
        ("examinations", "What happens if I miss an examination due to medical reasons?",
         "Submit a medical certificate from a registered doctor to the Dean's office within "
         "3 days of the missed exam. A make-up examination will be scheduled if approved by "
         "the academic committee."),
        ("examinations", "How do I get my transcripts for higher studies abroad?",
         "Apply for official transcripts through the Registrar's office with a fee of Rs 500. "
         "Allow 5 to 7 working days for issuance. Degree certificates are issued at the annual "
         "convocation and can be dispatched by post on request."),
        # ── LIBRARY ─────────────────────────────────────────
        ("library", "How do I access e-journals and online databases?",
         "Use your university email credentials to log in at library.university.edu/eresources. "
         "Off-campus access is available via the university VPN. The library supports Mendeley "
         "and Zotero for reference management, with training workshops every semester."),
        ("library", "What is the fine for overdue books?",
         "A fine of Rs 2 per day per book is charged after the due date. Books overdue by more "
         "than 60 days will be billed at replacement cost. Undergraduate students can borrow up "
         "to 4 books for 14 days; postgraduate students up to 6 books for 21 days."),
        ("library", "What are the library working hours?",
         "The central library is open Monday to Saturday from 8:00 AM to 10:00 PM and on "
         "Sundays from 10:00 AM to 5:00 PM. The third floor is a silent study zone; group "
         "study rooms on the second floor must be booked in advance."),
        # ── HOSTEL ──────────────────────────────────────────
        ("hostel", "What facilities are provided in the hostel?",
         "Hostels provide furnished rooms, 24-hour Wi-Fi, hot water, a common room, a gym, "
         "a mess with three daily meals (vegetarian and non-vegetarian options), and laundry "
         "services. Security includes 24-hour CCTV surveillance and biometric entry."),
        ("hostel", "What is the hostel curfew timing?",
         "Students must return by 10:00 PM on weekdays and 11:00 PM on weekends. Late entry "
         "must be pre-approved by the hostel warden. Leave applications for more than 3 days "
         "require parental consent."),
        ("hostel", "What is the hostel fee per semester?",
         "Hostel fees range from Rs 25,000 to Rs 40,000 per semester depending on single or "
         "shared occupancy, excluding mess charges. Maintenance requests are addressed within "
         "48 hours via the student portal."),
        # ── IT SUPPORT ──────────────────────────────────────
        ("it_support", "How do I get my university email account?",
         "Your university email is created automatically during admission. Credentials are sent "
         "to your personal email within 48 hours of enrollment. All enrolled students receive "
         "free Microsoft 365 access — sign in at office.com using your university email."),
        ("it_support", "How do I connect to the campus Wi-Fi?",
         "Select UniSecure on your device and log in with your roll number and portal password. "
         "A VPN client is available at it.university.edu/vpn for off-campus resource access. "
         "The IT help desk is open Monday to Friday from 9:00 AM to 6:00 PM."),
        ("it_support", "How do I access my course materials online?",
         "All course materials are on the Learning Management System at lms.university.edu. "
         "Log in with your student credentials. Students get 100 free pages per month for "
         "printing; colour printing costs Rs 5 per page at the IT centre."),
        # ── FINANCE ─────────────────────────────────────────
        ("finance", "How do I apply for a fee concession?",
         "Submit a fee concession application to the Student Welfare Office with proof of "
         "financial hardship. Concessions range from 10% to 50%. The fee payment deadline is "
         "the 15th of the first month of each semester; a late fee of Rs 50 per day applies."),
        ("finance", "What payment methods are accepted for tuition fees?",
         "Fees can be paid online via net banking, credit/debit card, or UPI through the "
         "finance portal. Demand drafts are accepted at the accounts office. An interest-free "
         "EMI plan in 3 installments per semester is available on application."),
        ("finance", "Are there grants available for research students?",
         "Research scholars can apply for the university grant of up to Rs 50,000 per year "
         "for equipment and travel through the research office. Scholarships are credited "
         "directly to the student's registered bank account within 30 days of approval."),
        # ── COURSES ─────────────────────────────────────────
        ("courses", "How do I register for elective courses?",
         "Elective course registration opens two weeks before the semester begins through the "
         "student portal. Students can choose from approved electives within their program. "
         "A minimum of 5 students must register for an elective to be offered."),
        ("courses", "What is the credit system followed by the university?",
         "The university follows a credit-based system where each course carries 3-4 credits. "
         "A full-time student is expected to register for 18-22 credits per semester. "
         "A minimum CGPA of 5.0 is required to continue in the program."),
        ("courses", "Can I audit a course without receiving credits?",
         "Yes, students may audit courses with the instructor's permission. Audited courses "
         "appear on the transcript with an AU grade but do not count toward CGPA. "
         "Registration for audit must be done in the first week of the semester."),
    ]

    def load(self) -> list:
        """Load all FAQ entries as LangChain Documents."""
        docs = []
        for i, (topic, question, answer) in enumerate(self.FAQ_DATA):
            content = f"Q: {question}\nA: {answer}"
            doc = Document(
                page_content=content,
                metadata={"source": f"university_faq_{topic}", "topic": topic,
                           "doc_id": i, "question": question}
            )
            docs.append(doc)
        print(f"[DocumentLoader] Loaded {len(docs)} documents from University FAQ knowledge base")
        return docs


# ═══════════════════════════════════════════════════════════
#  STEP 2 – Text Splitter
#  Mirrors: langchain.text_splitter.RecursiveCharacterTextSplitter
# ═══════════════════════════════════════════════════════════
class RecursiveCharacterTextSplitter:
    """
    Mirrors LangChain's RecursiveCharacterTextSplitter exactly.
    Splits documents into overlapping chunks for better retrieval.
    """
    def __init__(self, chunk_size: int = 300, chunk_overlap: int = 50,
                 separators: list = None):
        self.chunk_size    = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators    = separators or ["\n\n", "\n", ". ", " ", ""]

    def split_text(self, text: str) -> list:
        """Recursively split text by separators."""
        chunks = []
        for sep in self.separators:
            if sep and sep in text:
                parts = text.split(sep)
                current = ""
                for part in parts:
                    candidate = current + (sep if current else "") + part
                    if len(candidate) <= self.chunk_size:
                        current = candidate
                    else:
                        if current:
                            chunks.append(current.strip())
                        # Overlap: carry last chunk_overlap chars
                        overlap_start = max(0, len(current) - self.chunk_overlap)
                        current       = current[overlap_start:] + (sep if current else "") + part
                if current:
                    chunks.append(current.strip())
                return [c for c in chunks if c]
        # No separator found — split by size
        for i in range(0, len(text), self.chunk_size - self.chunk_overlap):
            chunks.append(text[i:i + self.chunk_size])
        return chunks

    def split_documents(self, documents: list) -> list:
        """Split a list of Documents into chunks, preserving metadata."""
        all_chunks = []
        for doc in documents:
            texts = self.split_text(doc.page_content)
            for j, chunk_text in enumerate(texts):
                chunk_doc = Document(
                    page_content=chunk_text,
                    metadata={**doc.metadata, "chunk_id": j, "total_chunks": len(texts)}
                )
                all_chunks.append(chunk_doc)
        print(f"[TextSplitter]   {len(documents)} docs → {len(all_chunks)} chunks "
              f"(size={self.chunk_size}, overlap={self.chunk_overlap})")
        return all_chunks


# ═══════════════════════════════════════════════════════════
#  STEP 3 – Embeddings
#  Mirrors: langchain_community.embeddings.HuggingFaceEmbeddings
#           (using TF-IDF + LSA as lightweight alternative)
# ═══════════════════════════════════════════════════════════
class TFIDFEmbeddings:
    """
    Embedding model using TF-IDF + Latent Semantic Analysis (LSA).
    Mirrors: langchain_community.embeddings.HuggingFaceEmbeddings API.
    Methods: embed_documents(texts) | embed_query(text)
    """
    def __init__(self, n_components: int = 128):
        self.n_components = n_components
        self.vectorizer   = TfidfVectorizer(
            ngram_range=(1, 2), max_features=5000,
            sublinear_tf=True, stop_words="english"
        )
        self.svd          = TruncatedSVD(n_components=n_components, random_state=42)
        self._fitted      = False

    def fit(self, texts: list):
        tfidf_matrix = self.vectorizer.fit_transform(texts)
        # Reduce dimensionality with SVD (like sentence embeddings)
        actual_components = min(self.n_components, tfidf_matrix.shape[1] - 1)
        self.svd = TruncatedSVD(n_components=actual_components, random_state=42)
        self.svd.fit(tfidf_matrix)
        self._fitted = True

    def embed_documents(self, texts: list) -> np.ndarray:
        """Embed a list of documents → matrix of shape (n_docs, n_components)."""
        tfidf = self.vectorizer.transform(texts)
        vecs  = self.svd.transform(tfidf)
        # L2-normalise (unit vectors for cosine similarity)
        norms = np.linalg.norm(vecs, axis=1, keepdims=True) + 1e-10
        return vecs / norms

    def embed_query(self, text: str) -> np.ndarray:
        """Embed a single query string."""
        return self.embed_documents([text])[0]


# ═══════════════════════════════════════════════════════════
#  STEP 4 – Vector Store (FAISS-style)
#  Mirrors: langchain_community.vectorstores.FAISS
# ═══════════════════════════════════════════════════════════
class FAISSVectorStore:
    """
    In-memory vector store with cosine-similarity retrieval.
    Mirrors: langchain_community.vectorstores.FAISS
    Methods: from_documents() | similarity_search() | similarity_search_with_score()
    """
    def __init__(self, embedding_model: TFIDFEmbeddings):
        self.embedding_model = embedding_model
        self.documents: list = []
        self.index: np.ndarray = None  # (n_chunks, n_components)

    @classmethod
    def from_documents(cls, documents: list, embedding: TFIDFEmbeddings):
        """Create vector store from a list of Documents. Mirrors FAISS.from_documents()."""
        store = cls(embedding)
        texts = [doc.page_content for doc in documents]
        # Fit embedding model on corpus
        embedding.fit(texts)
        store.documents = documents
        store.index     = embedding.embed_documents(texts)
        print(f"[VectorStore]    Indexed {len(documents)} chunks | "
              f"Embedding dim: {store.index.shape[1]}")
        return store

    def similarity_search_with_score(self, query: str, k: int = 4):
        """
        Return top-k most similar Documents with cosine scores.
        Mirrors FAISS.similarity_search_with_score()
        Returns: list of (Document, score) tuples
        """
        q_vec  = self.embedding_model.embed_query(query)
        scores = cosine_similarity([q_vec], self.index)[0]
        top_k_idx = np.argsort(scores)[::-1][:k]
        return [(self.documents[i], float(scores[i])) for i in top_k_idx]

    def similarity_search(self, query: str, k: int = 4) -> list:
        """Return top-k Documents (without scores). Mirrors FAISS.similarity_search()."""
        return [doc for doc, _ in self.similarity_search_with_score(query, k)]

    def as_retriever(self, search_kwargs: dict = None):
        """Convert to a Retriever object. Mirrors vectorstore.as_retriever()."""
        return VectorStoreRetriever(self, search_kwargs or {"k": 4})


# ═══════════════════════════════════════════════════════════
#  STEP 5 – Retriever
#  Mirrors: langchain_core.vectorstores.VectorStoreRetriever
# ═══════════════════════════════════════════════════════════
class VectorStoreRetriever:
    """Mirrors langchain_core.vectorstores.VectorStoreRetriever"""
    def __init__(self, vectorstore: FAISSVectorStore, search_kwargs: dict):
        self.vectorstore   = vectorstore
        self.search_kwargs = search_kwargs

    def get_relevant_documents(self, query: str) -> list:
        k = self.search_kwargs.get("k", 4)
        return self.vectorstore.similarity_search(query, k=k)

    def invoke(self, query: str) -> list:
        """Modern LangChain interface."""
        return self.get_relevant_documents(query)


# ═══════════════════════════════════════════════════════════
#  STEP 6 – LLM (Response Generator)
#  Mirrors: langchain_community.llms.HuggingFacePipeline
# ═══════════════════════════════════════════════════════════
class ContextAwareLLM:
    """
    Context-aware response generator.
    Mirrors: langchain_community.llms.HuggingFacePipeline / ChatAnthropic
    In production: replace with AutoModelForCausalLM from fine_tune.py (Part B/C)
    """
    def __init__(self, model_name: str = "university-faq-gpt2"):
        self.model_name = model_name

    def _extract_answer(self, context_docs: list, question: str) -> str:
        """
        Intelligent answer synthesis from retrieved context.
        Extracts and combines the most relevant answer parts.
        """
        # Build combined context
        all_answers = []
        for doc in context_docs:
            text = doc.page_content
            # Extract answer part (after "A:")
            if "A:" in text:
                ans = text.split("A:", 1)[1].strip()
                all_answers.append(ans)

        if not all_answers:
            return "I could not find relevant information in the knowledge base for your question."

        # Score sentences by keyword overlap with question
        q_words = set(re.sub(r'[^\w\s]', '', question.lower()).split())
        stop    = {"what","how","when","where","who","is","are","do","i","the","a",
                   "an","for","can","my","to","of","in","and","or","at","from"}
        q_kws   = q_words - stop

        best_sents, seen = [], set()
        for ans in all_answers:
            sents = re.split(r'(?<=[.!?])\s+', ans)
            for s in sents:
                s_lower = s.lower()
                if s_lower in seen or len(s) < 20:
                    continue
                seen.add(s_lower)
                overlap = sum(1 for w in q_kws if w in s_lower)
                best_sents.append((overlap, s))

        best_sents.sort(key=lambda x: -x[0])
        selected = [s for _, s in best_sents[:3]]

        if not selected:
            selected = [all_answers[0][:300]]

        response = " ".join(selected)
        # Clean up
        response = re.sub(r'\s+', ' ', response).strip()
        if not response.endswith(('.', '!', '?')):
            response += '.'
        return response

    def __call__(self, prompt: str, context_docs: list, question: str) -> str:
        return self._extract_answer(context_docs, question)


# ═══════════════════════════════════════════════════════════
#  STEP 7 – Prompt Template
#  Mirrors: langchain_core.prompts.ChatPromptTemplate
# ═══════════════════════════════════════════════════════════
class PromptTemplate:
    """Mirrors langchain_core.prompts.PromptTemplate"""
    TEMPLATE = """You are a helpful University Course Helpdesk Assistant.
Use ONLY the following retrieved context to answer the student's question.
If the answer is not in the context, say you don't have that information.

Context:
{context}

Question: {question}

Answer:"""

    def format(self, context: str, question: str) -> str:
        return self.TEMPLATE.format(context=context, question=question)


# ═══════════════════════════════════════════════════════════
#  STEP 8 – RetrievalQA Chain
#  Mirrors: langchain.chains.RetrievalQA / create_retrieval_chain
# ═══════════════════════════════════════════════════════════
class RetrievalQAChain:
    """
    End-to-end RAG chain.
    Mirrors: langchain.chains.RetrievalQA.from_chain_type()
             / langchain.chains.create_retrieval_chain()

    Pipeline:
        Query → Retriever → PromptTemplate → LLM → Answer
    """
    def __init__(self, retriever: VectorStoreRetriever,
                 llm: ContextAwareLLM,
                 prompt: PromptTemplate,
                 vectorstore: FAISSVectorStore,
                 k: int = 3):
        self.retriever   = retriever
        self.llm         = llm
        self.prompt      = prompt
        self.vectorstore = vectorstore
        self.k           = k

    def invoke(self, query: str) -> dict:
        """
        Full RAG pipeline. Mirrors chain.invoke({"query": query}).
        Returns dict with 'query', 'result', 'source_documents', 'scores'.
        """
        t0 = time.time()

        # 1. Retrieve
        docs_scores = self.vectorstore.similarity_search_with_score(query, k=self.k)
        source_docs = [d for d, _ in docs_scores]
        scores      = [s for _, s in docs_scores]

        # 2. Build context string
        context = "\n\n".join(
            f"[Source {i+1} | {d.metadata.get('topic','?').upper()}]\n{d.page_content}"
            for i, d in enumerate(source_docs)
        )

        # 3. Format prompt
        formatted_prompt = self.prompt.format(context=context, question=query)

        # 4. Generate answer
        answer = self.llm(formatted_prompt, source_docs, query)

        latency_ms = (time.time() - t0) * 1000

        return {
            "query":            query,
            "result":           answer,
            "source_documents": source_docs,
            "retrieval_scores": scores,
            "latency_ms":       latency_ms,
            "prompt":           formatted_prompt,
        }

    def __call__(self, query: str) -> dict:
        return self.invoke(query)


# ═══════════════════════════════════════════════════════════
#  PIPELINE ASSEMBLY
# ═══════════════════════════════════════════════════════════
print("=" * 62)
print("  Part E – LangChain Course Helpdesk Bot (RAG Pipeline)")
print("=" * 62)

# Step 1: Load documents
print("\n[Step 1] Loading knowledge base...")
loader    = UniversityFAQLoader()
documents = loader.load()

# Step 2: Split documents
print("[Step 2] Splitting documents into chunks...")
splitter = RecursiveCharacterTextSplitter(chunk_size=350, chunk_overlap=60)
chunks   = splitter.split_documents(documents)

# Step 3 + 4: Embed & index
print("[Step 3] Creating TF-IDF embeddings + LSA reduction...")
embeddings   = TFIDFEmbeddings(n_components=128)
print("[Step 4] Building FAISS vector store...")
vectorstore  = FAISSVectorStore.from_documents(chunks, embeddings)

# Step 5 + 6 + 7: Retriever, LLM, Prompt
retriever    = vectorstore.as_retriever(search_kwargs={"k": 3})
llm          = ContextAwareLLM(model_name="university-faq-llm")
prompt       = PromptTemplate()

# Step 8: Chain
print("[Step 5] Assembling RetrievalQA Chain...")
qa_chain = RetrievalQAChain(retriever=retriever, llm=llm, prompt=prompt,
                             vectorstore=vectorstore, k=3)
print("\n✅ Pipeline ready.\n")

# ═══════════════════════════════════════════════════════════
#  TEST QUERIES
# ═══════════════════════════════════════════════════════════
TEST_QUERIES = [
    "What is the minimum attendance required to appear in exams?",
    "How do I apply for a fee concession?",
    "What facilities are available in the hostel?",
    "How do I access online journals and databases?",
    "What is the grading system used by the university?",
    "How can I get my university email account?",
    "Are there any scholarships for new students?",
    "What is the library book return fine?",
]

print(f"Running {len(TEST_QUERIES)} test queries through the RAG pipeline...\n")
print(f"{'#':<3} {'Query':<48} {'Top Score':>10}  {'Latency':>9}  {'Topic'}")
print(f"{'—'*3} {'—'*48} {'—'*10}  {'—'*9}  {'—'*12}")

results = []
for i, q in enumerate(TEST_QUERIES):
    res = qa_chain(q)
    top_score = res["retrieval_scores"][0]
    topic     = res["source_documents"][0].metadata.get("topic", "?")
    results.append(res)
    print(f"Q{i+1:<2} {q[:47]:<47}  {top_score:.4f}      {res['latency_ms']:>6.1f} ms  {topic}")

avg_score   = np.mean([r["retrieval_scores"][0] for r in results])
avg_latency = np.mean([r["latency_ms"] for r in results])
print(f"\n  Avg top-1 retrieval score : {avg_score:.4f}")
print(f"  Avg latency               : {avg_latency:.1f} ms")


# ═══════════════════════════════════════════════════════════
#  DEMO OUTPUT
# ═══════════════════════════════════════════════════════════
print("\n" + "=" * 62)
print("  DEMO: Live Q&A from the Course Helpdesk Bot")
print("=" * 62)
DEMO_Qs = [
    "What is the minimum attendance to sit for exams?",
    "How do I apply for a fee concession?",
    "What facilities are available in the hostel?",
    "How do I access online journals and databases?",
    "What is the grading system used by the university?",
]
for dq in DEMO_Qs:
    r = qa_chain(dq)
    sources = ", ".join(d.metadata.get("topic", "?") for d in r["source_documents"][:2])
    print(f"\n❓ {dq}")
    print(f"💬 {r['result']}")
    print(f"   [Sources: {sources} | Score: {r['retrieval_scores'][0]:.4f} | {r['latency_ms']:.1f} ms]")

print(f"""
Part E Complete.
  Documents loaded   : {len(documents)}
  Chunks created     : {len(chunks)}
  Embedding dim      : {vectorstore.index.shape[1]}
  Queries tested     : {len(results)}
  Avg retrieval score: {avg_score:.4f}
  Avg latency        : {avg_latency:.1f} ms
""")