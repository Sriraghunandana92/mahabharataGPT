from loader import load_verses

MAX_CHARS = 800


def make_chunks():
    verses = load_verses()
    chunks = []
    current = []
    current_len = 0

    for i, v in enumerate(verses):
        same_chapter = (
            current
            and current[0]["book"] == v["book"]
            and current[0]["chapter"] == v["chapter"]
        )

        if current and (not same_chapter or current_len + len(v["english"]) > MAX_CHARS):
            chunks.append(build_chunk(current))
            current = []
            current_len = 0

        current.append(v)
        current_len += len(v["english"])

    if current:
        chunks.append(build_chunk(current))

    return chunks


def build_chunk(group):
    first = group[0]
    last = group[-1]
    text = " ".join(v["english"] for v in group)

    return {
        "book": first["book"],
        "chapter": first["chapter"],
        "verse_start": first["verse"],
        "verse_end": last["verse"],
        "text": text,
        "citation": f"Book {first['book']}, Chapter {first['chapter']}, Verses {first['verse']}-{last['verse']}",
    }


if __name__ == "__main__":
    chunks = make_chunks()
    print("Total chunks:", len(chunks))
    print("\nFirst chunk:")
    print(chunks[0]["citation"])
    print(chunks[0]["text"][:300])