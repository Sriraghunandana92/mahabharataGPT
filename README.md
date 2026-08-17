# MahabharataGPT

This is a search system I built over the complete Mahabharata.

"You ask a question in normal English, and it finds the verses that are actually about that topic — even if your question does not use the same words as the text".

For example, if you ask "Who is Yudhishthira?",

It brings back verses describing his birth from Yamadharma and his righteousness. It is not doing a keyword search. "It is matching by meaning".

# The data

I used a structured JSON version of the Mahabharata:

- 2,425 JSON files
- 19 folders (18 parvas and Harivamsha)
- 71,089 verses in total

Each file is one "Adhyaya" (chapter). Every verse in it has four fields: the "verse number", "the Sanskrit shloka", the "English translation", and the "Bhavadeepa commentary".

## How it works

The whole thing runs in four steps, and each step is one Python file.

1. Load the verses (`loader.py`)

This reads all 2,425 JSON files and pulls out every verse into one big list. For each verse I keep the English text plus its book, chapter and verse number, so I always know where a verse came from.

Result: 71,089 verses.

2. Group them into chunks (`chunker.py`)

A single verse is often too short to be useful on its own. So I join consecutive verses together into passages of about 800 characters.

Two rules I follow here:

- Never join verses from different chapters. This keeps the citations honest.
- Stop the chunk once it crosses 800 characters.

Result: 20,159 chunks, about 3-4 verses each.

3. Convert the chunks into numbers and build the index (`build_index.py`)

A computer cannot compare meaning directly, so each chunk is converted into a list of "384 numbers" using the `all-MiniLM-L6-v2` model. Chunks with similar meaning end up with similar numbers.

These 20,159 vectors are then stored in a FAISS (Facebook AI Similarity Search") index, which is built for finding the closest matches quickly.

This step takes about 45 minutes on a normal laptop CPU. But it only has to be done once. After that, searching is instant.

Two files get saved at the end: `mahabharata.index` (the vectors) and `chunks.json` (the actual text, so I can look up what each vector refers to).

4. Search (`search.py`)

When you type a question, it gets converted into 384 numbers the same way. 
FAISS then finds the chunks whose numbers are closest, and those are your results, along with their citation.

## Things I decided along the way

**I embed the English, not the Sanskrit.** 
-The model I am using was trained mainly on English, so English questions match English text much better. The Sanskrit is still kept in the data for later use.

**I normalise the vectors.** 
-This makes the inner product search in FAISS equal to cosine similarity, which is the standard way to compare meaning.

**I used an exact index (IndexFlatIP), not an approximate one.**
-With only about 20,000 vectors, exact search is fast enough and gives perfect results. 

**Chunks never cross chapter boundaries.** Otherwise a citation would point to two different chapters at once, which is useless.

## How to run this on your computer

**Step 1 — Get the code**

```
git clone https://github.com/Sriraghunandana92/mahabharataGPT.git
cd mahabharataGPT
```

**Step 2 — Install the libraries**

```
pip install sentence-transformers faiss-cpu numpy
```

This takes a few minutes. It installs PyTorch as well, which is a large download.

**Step 3 — Check the data loads correctly**

```
python loader.py
```

You should see:

```
Total verses loaded: 71089
```

**Step 4 — Check the chunking**

```
python chunker.py
```

You should see:

```
Total chunks: 20159
```

**Step 5 — Build the index**

```
python build_index.py
```

"This is the slow one. About 45 minutes. The first time you run it, it also downloads the model (about 90 MB), so the screen may look frozen for a minute or two before anything appears. That is normal."

When it finishes you should see:

```
Vector shape: (20159, 384)
Vectors in index: 20159
Saved mahabharata.index and chunks.json
```

**Step 6 — Search**

```
python search.py
```

It will ask you for a question. Type anything, for example:

```
Why did Yudhishthira lose his kingdom in the dice game?
```

It prints the five closest passages, each with a similarity score and the book, chapter and verse it came from.

## Files in this project

```
loader.py         reads the JSON files into a list of verses
chunker.py        groups verses into 800-character passages
build_index.py    creates the embeddings and the FAISS index
search.py         takes a question and returns matching passages
parvas/           the JSON corpus
```

`mahabharata.index` and `chunks.json` are not in this repository. They are generated files, and you get them by running `build_index.py`.

## Current status

The search part is finished and working.

The next step is to add the answer layer — instead of just showing you the matching passages, it will send them to the Claude API and get back a written answer with the verses cited. After that, a FastAPI endpoint and a simple web page.

## What I used

- Python
- sentence-transformers (all-MiniLM-L6-v2) for the embeddings
- FAISS for the vector search
- NumPy
