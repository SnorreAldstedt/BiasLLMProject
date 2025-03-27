import json
import math
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict, Counter

def plot_10yr_distributions(json_file_path):
    # 1) Load personas from JSON file
    with open(json_file_path, "r", encoding="utf-8") as f:
        personas = json.load(f)
    
    if not personas:
        print("No personas found in the JSON.")
        return

    # 2) Determine min/max ages in the data
    all_ages = [p["age"] for p in personas]
    min_age = min(all_ages)
    max_age = max(all_ages)
    
    # We’ll define bins in steps of 10 years
    start_bin = 20 * (min_age // 20)
    if start_bin > min_age:
        start_bin -= 20
    end_bin = 20 * (math.ceil(max_age / 20.0) + 1)
    bin_edges = list(range(start_bin, end_bin + 1, 20))

    # 3) Function to determine which bin label an age belongs to
    def get_10yr_bin_label(age):
        for i in range(len(bin_edges) - 1):
            low = bin_edges[i]
            high = bin_edges[i+1]
            if low <= age < high:
                return f"{low}-{high-1}"
        # If age >= bin_edges[-1], put in final bracket
        return f"{bin_edges[-1]}+"

    # 4) Build counters for each bin
    distribution = defaultdict(lambda: {
        "gender": Counter(),
        "kids": Counter(),
        "occupation": Counter()
    })
    
    for persona in personas:
        age = persona["age"]
        gender = persona["gender"].lower()         # e.g. "mann", "dame"
        kids = str(persona["kids"])                # "True", "False"
        occ = persona["occupation"].lower()        # e.g. "student", "i arbeid", ...
        
        bin_label = get_10yr_bin_label(age)
        distribution[bin_label]["gender"][gender] += 1
        distribution[bin_label]["kids"][kids] += 1
        distribution[bin_label]["occupation"][occ] += 1

    # 5) Sort bin labels in ascending numeric order
    def bin_label_key(label):
        # label is like "20-29" => split by '-' => "20", "29"
        # or "90+" => remove '+'
        base = label.split('-')[0].replace('+', '')
        return int(base)
    
    sorted_bins = sorted(distribution.keys(), key=bin_label_key)
    x_positions = np.arange(len(sorted_bins))

    # 6) Prepare figure with 3 subplots
    fig, axes = plt.subplots(1, 3, figsize=(16, 5), sharey=False)
    fig.suptitle("Persona Distributions by 10-year Age Intervals", fontsize=14, y=1.05)
    

    color_mann = "#457B9D"   # Medium Blue
    color_dame = "#E63946"   # Red

    mann_counts = [distribution[b]["gender"].get("mann", 0) for b in sorted_bins]
    dame_counts = [distribution[b]["gender"].get("dame", 0) for b in sorted_bins]

    axes[0].bar(
        x_positions, 
        mann_counts, 
        color=color_mann, 
        label="mann"
    )
    axes[0].bar(
        x_positions, 
        dame_counts, 
        bottom=mann_counts, 
        color=color_dame, 
        label="dame"
    )
    axes[0].set_xticks(x_positions)
    axes[0].set_xticklabels(sorted_bins, rotation=45, ha="right")
    axes[0].set_ylabel("Count")
    axes[0].set_title("Gender Distribution")
    axes[0].legend()

    color_kids_true = "#2A9D8F"  # Teal
    color_kids_false = "#F4A261" # Peach

    kids_true = [distribution[b]["kids"].get("True", 0) for b in sorted_bins]
    kids_false = [distribution[b]["kids"].get("False", 0) for b in sorted_bins]

    axes[1].bar(
        x_positions, 
        kids_true, 
        color=color_kids_true, 
        label="Har barn"
    )
    axes[1].bar(
        x_positions, 
        kids_false, 
        bottom=kids_true, 
        color=color_kids_false, 
        label="Ingen barn"
    )
    axes[1].set_xticks(x_positions)
    axes[1].set_xticklabels(sorted_bins, rotation=45, ha="right")
    axes[1].set_title("Kids Distribution")
    axes[1].legend()


    occ_categories = ["student", "i arbeid", "arbeidsledig", "pensjonert/uføretrygdet"]
    occ_colors = ["#A8DADC", "#1D3557", "#E9C46A", "#606C38"]

    bottom_acc = np.zeros(len(sorted_bins))
    for occ_name, color in zip(occ_categories, occ_colors):
        counts = [distribution[b]["occupation"].get(occ_name, 0) for b in sorted_bins]
        axes[2].bar(
            x_positions, 
            counts, 
            bottom=bottom_acc, 
            color=color, 
            label=occ_name
        )
        bottom_acc = [x + y for x, y in zip(bottom_acc, counts)]

    axes[2].set_xticks(x_positions)
    axes[2].set_xticklabels(sorted_bins, rotation=45, ha="right")
    axes[2].set_title("Occupation Distribution")
    axes[2].legend()

    plt.tight_layout()
    plt.show()

# Example usage
if __name__ == "__main__":
    plot_10yr_distributions("personas.json")
