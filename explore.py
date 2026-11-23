# explore.py: look at the structure of the law before we model anything
from collections import Counter
from lxml import etree

tree = etree.parse("data/I-3.3.xml")
root = tree.getroot()
LIMS = "{http://justice.gc.ca/lims}"

# 1. Which building blocks does the Act use, and how many of each?
tags = Counter(el.tag for el in root.iter() if isinstance(el.tag, str))
print("Most common tags:")
for tag, n in tags.most_common(15):
    print(f"  {tag:25} {n}")

# 2. Look at one real provision: section 84
for sec in root.iter("Section"):
    if sec.findtext("Label") == "84":
        print("\nSection 84 marginal note:", sec.findtext("MarginalNote"))
        print("Last amended:", sec.get(f"{LIMS}lastAmendedDate"))
        for sub in sec.findall("Subsection")[:4]:
            label = sub.findtext("Label")
            note = sub.findtext("MarginalNote")
            text = " ".join("".join(sub.itertext()).split())[:160]
            print(f"  84{label}  [{note}]  {text}...")
        break

# 3. How are defined terms marked?
defs = root.findall(".//Definition")
print(f"\n{len(defs)} definitions, e.g.:", [d.findtext(".//DefinedTermEn") for d in defs[:5]])