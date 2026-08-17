import json
import glob

def load_verses():
    files = glob.glob("parvas/**/*.json", recursive=True)
    all_verses = []

    for path in files:
        if path.endswith("index.json"):
            continue

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        book = data.get("book")
        chapter = data.get("chapter")

        for v in data.get("verses", []):
            english = (v.get("english") or "").strip()
            if not english:
                continue

            all_verses.append({
                "book": book,
                "chapter": chapter,
                "verse": v.get("verse"),
                "english": english,
                "sanskrit": (v.get("sanskrit") or "").strip(),
            })

    return all_verses


if __name__ == "__main__":
    verses = load_verses()
    print("Total verses loaded:", len(verses))
    print("\nFirst verse:")
    print(verses[0])