# Legal-GraphRAG

# GraphRAG for Legal Document Analysis and Retrieval

> A Graph-Augmented Retrieval Framework for Indian Legal Judgments using Structure-Aware Chunking, Region-Aware Metadata Extraction, Bipartite Citation Graphs, and Hybrid Dense-Graph Ranking.

---

## Overview

Legal judgments are often hundreds of pages long, contain OCR noise, inconsistent formatting, complex legal terminology, and extensive citation networks. Traditional retrieval systems based solely on keyword matching or semantic embeddings frequently miss important precedents because they ignore citation authority and legal document structure.

This project proposes a **GraphRAG-based legal retrieval framework** that combines dense semantic retrieval with citation graph reasoning to improve retrieval quality over standard embedding-based methods.

The system transforms raw judicial PDF documents into semantically indexed legal chunks connected through a citation graph, enabling authority-aware retrieval.

---

# Features

- Two-pass document cleaning
- Region-aware legal metadata extraction
- Structure-aware legal chunking
- Bipartite Citation Graph construction
- Personalized PageRank based graph scoring
- Hybrid Dense + Graph retrieval
- Multi-model embedding evaluation
- Statistical significance validation
- Complete benchmarking on Indian legal judgments

---

# Dataset

| Property | Value |
|----------|-------|
| Domain | Indian Supreme Court Judgments |
| Documents | 145 PDF Judgments |
| Final Chunks | 6,597 |
| Evaluation Queries | 20 Complex Legal Queries |
| Chunk Size | ~250 words |
| Overlap | 50 words |

---

# Project Pipeline

```
Raw PDF Judgments
        │
        ▼
Text Extraction
        │
        ▼
Two-Pass Cleaning
        │
        ▼
LMIE Metadata Extraction
        │
        ▼
Structure-Aware Chunking
        │
        ▼
Embedding Generation
        │
        ▼
FAISS Dense Index
        │
        ▼
Citation Graph Construction
        │
        ▼
Personalized PageRank
        │
        ▼
Hybrid Dense + Graph Ranking
        │
        ▼
Evaluation
```

---

# Architecture

## Stage 1 — Document Preprocessing

### Pass 1 : Structural Cleaning

Removes layout noise while preserving legal paragraph structure.

Operations include

- Unicode normalization
- Header removal
- Footer removal
- Page number removal
- Repeated line detection
- Broken paragraph repair

---

### Pass 2 : Semantic Cleaning

Improves semantic consistency before embedding generation.

Operations include

- OCR correction
- Citation normalization
- Legal abbreviation normalization
- Whitespace normalization
- Character correction

---

# Stage 2 — LMIE (Legal Metadata Extraction Engine)

A custom region-aware metadata extraction engine designed specifically for Indian legal judgments.

Extracted metadata includes

- Case ID
- Case Title
- Court Name
- Bench Size
- Judges
- Petitioners
- Respondents
- Decision Date
- Neutral Citation
- Acts
- Case Citations

Unlike generic regex extraction, LMIE performs:

- Region-aware parsing
- Legal heuristics
- Validation
- Confidence scoring

---

# Stage 3 — Structure-Aware Chunking

Traditional fixed-size chunking often splits legal arguments across chunk boundaries.

Instead, the proposed system first classifies document regions before chunk generation.

Regions include

- Header
- Body
- Decision
- Order

Chunking parameters

- Chunk length ≈ 250 words
- Context overlap = 50 words

This preserves legal reasoning continuity.

---

# Stage 4 — Bipartite Citation Graph

Instead of a traditional knowledge graph, this project constructs a **Bipartite Citation Graph**.

Node Set A

- Legal Chunks

Node Set B

- Legal Authorities
    - Acts
    - Articles
    - Previous Cases
    - Sections

Edges represent citation relationships.

Example

```
Chunk A -------- Article 21

Chunk B -------- IPC 302

Chunk C -------- Article 21
```

This allows authority propagation through shared citations.

---

# Graph Scoring

The graph is scored using

## Personalized PageRank

Used to estimate legal authority.

Parameters

```
alpha = 0.85
max_iter = 100
tol = 1e-5
```

---

# Embedding Models Evaluated

| Model | Dimension | Domain |
|---------|-----------|------------|
| MiniLM | 384 | General |
| BGE v1.5 | 768 | General Retrieval |
| LegalBERT | 768 | EU/US Legal |
| InLegalBERT | 768 | Indian Legal |

---

# Dense Retrieval

Embeddings are indexed using

- FAISS
- Cosine Similarity

Candidate retrieval

```
Top 100
```

Final returned

```
Top 5
```

---

# Hybrid Retrieval

Final ranking combines dense similarity and graph authority.

Formula

```
Final Score

= 0.3 × Dense Similarity

+ 0.7 × Personalized PageRank
```

where

Dense Similarity

- FAISS cosine similarity

Graph Score

- Personalized PageRank

---

# Evaluation Metrics

The following retrieval metrics were used

- Precision@1
- Precision@3
- Precision@5
- Recall@3
- Recall@5
- MRR
- MAP
- NDCG@5

Primary evaluation metric

```
NDCG@5
```

---

# Statistical Validation

Performance improvements were validated using

## Wilcoxon Signed-Rank Test

Used to verify statistical significance.

GraphRAG-BGE vs BGE

```
p-value = 0.0020
```

---

## Bootstrap Confidence Interval

- 2000 resamples
- 95% Confidence Interval

Used to measure retrieval consistency.

---

# Experimental Results

## Best Retriever

```
GraphRAG-BGE
```

Performance

| Metric | Value |
|---------|--------|
| NDCG@5 | 0.9922 |
| MRR | 1.0000 |
| MAP | 0.2948 |

---

## Performance Ranking

1. GraphRAG-BGE
2. GraphRAG-InLegalBERT
3. GraphRAG-MiniLM
4. BGE
5. GraphRAG-LegalBERT
6. MiniLM
7. InLegalBERT
8. LegalBERT

---

# Key Findings

- Graph augmentation improved every embedding model.
- BGE achieved the strongest standalone retrieval.
- Domain-specific embeddings benefited significantly after graph augmentation.
- Personalized PageRank effectively captured citation authority.
- Structure-aware chunking preserved legal reasoning better than fixed-length chunking.

---

# Technologies Used

Programming

- Python

Libraries

- NetworkX
- FAISS
- SentenceTransformers
- Transformers
- NumPy
- Pandas
- PyMuPDF
- Regex
- Scikit-learn
- SciPy
- Matplotlib

Embedding Models

- all-MiniLM-L6-v2
- BGE v1.5
- LegalBERT
- InLegalBERT

---

# Project Structure

```
GraphRAG-Legal/
│
├── data/
│   ├── raw_pdfs/
│   ├── cleaned_text/
│   ├── metadata/
│   ├── chunks/
│   └── experiments/
│
├── models/
│
├── embeddings/
│
├── faiss/
│
├── graph/
│
├── notebooks/
│
├── reports/
│
├── results/
│
├── model_comparison.ipynb
│
├── requirements.txt
│
└── README.md
```

---

# Future Work

- Dynamic query-dependent hybrid weighting
- Temporal citation graph
- Neo4j-based legal knowledge graph
- LLM-assisted legal summarization
- Multi-jurisdiction legal retrieval
- Graph Neural Networks

---

# References

1. Edge et al. — From Local to Global: A GraphRAG Approach to Query-Focused Summarization (2024)

2. Paul et al. — InLegalBERT (2022)

3. Chalkidis et al. — LegalBERT (2020)

4. Xiao et al. — BGE (2023)

5. Wang et al. — MiniLM (2020)

6. Johnson et al. — FAISS (2019)

---

# Authors

**Snehashish Das**
**Gungun Sharma**
**Sruti Mishra**

Master of Computer Applications (MCA)

University of Calcutta

---

# Citation

If you use this work in your research, please cite:

```bibtex
@project{das2026graphrag,
  title={GraphRAG for Legal Document Analysis and Retrieval},
  author={Snehashish Das},
  year={2026},
  institution={University of Calcutta}
}
```

---

## License

This project is intended for academic and research purposes.
