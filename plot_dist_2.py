import json
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict, Counter

def plot_age_group_distributions(json_file_path):
    # Load personas from JSON file
    with open(json_file_path, "r", encoding="utf-8") as f:
        personas = json.load(f)
    
    if not personas:
        print("No personas found in the JSON.")
        return

    # Define custom age bins
    def get_age_group_label(age):
        if age <= 30:
            return "≤30"
        elif 31 <= age <= 50:
            return "31-50"
        else:
            return "50+"

    # Build counters for each age group
    distribution = defaultdict(lambda: {
        "kids_yes": Counter(),  # People with kids
        "kids_no": Counter()    # People without kids
    })
    
    all_occupations = set()  # To store all unique occupation names
    
    for persona in personas:
        age = persona["age"]
        gender = persona["gender"].lower()  # e.g. "mann", "dame"
        kids = persona["kids"]              # Boolean: True = has kids, False = no kids
        occ = persona["occupation"].lower() # e.g. "student", "i arbeid", ...
        occ = occ.capitalize()  # Ensure occupation names are capitalized
        
        bin_label = get_age_group_label(age)
        key = "kids_yes" if kids else "kids_no"  # Split into kids/no kids

        # Store occupation
        all_occupations.add(occ)

        # Count occupation split by gender
        distribution[bin_label][key][(occ, gender)] += 1

    # Define bin order (age groups)
    sorted_bins = ["≤30", "31-50", "50+"]

    # Ensure "Pensjonert/uføretrygdet" appears first, followed by others in alphabetical order
    all_occupations = sorted(all_occupations - {"Pensjonert/uføretrygdet"})  # Remove first
    all_occupations.insert(0, "Pensjonert/uføretrygdet")  # Insert at beginning

    # Define colors
    color_mann = "#67a9cf"  # Medium Blue
    color_dame = "#f33"     # Red

    # Create subplots: (3 age groups) × (2 categories: kids/no kids) = 6 graphs
    fig, axes = plt.subplots(len(sorted_bins), 2, figsize=(18, 12), sharey=True)
    fig.suptitle("Persona Distributions by Age Groups (Stacked Bar Charts)", fontsize=16)

    for i, age_bin in enumerate(sorted_bins):
        for j, key in enumerate(["kids_yes", "kids_no"]):
            ax = axes[i, j]

            # Ensure consistent ordering of occupation categories
            labels = all_occupations  # Use the pre-defined sorted list of occupations
            
            # Extract gender-specific values
            male_counts = [distribution[age_bin][key].get((label, "mann"), 0) for label in labels]
            female_counts = [distribution[age_bin][key].get((label, "dame"), 0) for label in labels]

            # Plot stacked bars
            x_positions = np.arange(len(labels))
            ax.bar(x_positions, male_counts, color=color_mann, label="Mann")
            ax.bar(x_positions, female_counts, bottom=male_counts, color=color_dame, label="Dame")

            # Label axes
            ax.set_xticks(x_positions)
            ax.set_xticklabels(labels, rotation=45, ha="right")
            ax.set_title(f"Aldersgruppe: {age_bin} ({'Har barn' if key == 'kids_yes' else 'Ingen barn'})")
            if i == len(sorted_bins) - 1:
                ax.set_xlabel("Yrke")
            if j == 0:
                ax.set_ylabel("Antall personer")

            # Only show legend for the first subplot
            if i == 0 and j == 0:
                ax.legend()
            else:
                ax.legend().remove()

    plt.tight_layout()
    plt.subplots_adjust(top=0.88)
    plt.show()

# Example usage
if __name__ == "__main__":
    plot_age_group_distributions("personas.json")
