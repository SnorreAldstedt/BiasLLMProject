
import json
from collections import Counter
import matplotlib.pyplot as plt


def get_age_group(age):
    """Return the age group as a string based on the age."""
    if 18 <= age <= 30:
        return "18-30"
    elif 31 <= age <= 50:
        return "31-50"
    else:
        return "51+"

def check_personas_distribution(file_path):
    """Load personas from file and create distribution counters."""
    with open(file_path, "r", encoding="utf-8") as f:
        personas = json.load(f)
    
    # Prepare counters for each age group
    distribution = {
        "18-30": {
            "count": 0,
            "gender": Counter(),
            "kids": Counter(),
            "occupation": Counter()
        },
        "31-50": {
            "count": 0,
            "gender": Counter(),
            "kids": Counter(),
            "occupation": Counter()
        },
        "51+": {
            "count": 0,
            "gender": Counter(),
            "kids": Counter(),
            "occupation": Counter()
        }
    }
    
    # Populate the counters
    for persona in personas:
        age = persona["age"]
        gender = persona["gender"]
        have_kids = persona["kids"]
        occupation = persona["occupation"]
        
        group = get_age_group(age)
        distribution[group]["count"] += 1
        distribution[group]["gender"][gender] += 1
        distribution[group]["kids"][str(have_kids)] += 1  # store "True"/"False" strings
        distribution[group]["occupation"][occupation] += 1
    
    # Print distribution summaries (optional)
    for group_name, data in distribution.items():
        print(f"--- Age Group: {group_name} ---")
        print(f"Total in group: {data['count']}")
        print("Gender counts:", dict(data["gender"]))
        print("Kids counts:", dict(data["kids"]))
        print("Occupation counts:", dict(data["occupation"]))
        print()
        
    print("Overall personas:", len(personas))
    
    # Plot distribution graphs
    plot_distribution(distribution)

def plot_distribution(distribution):
    """Creates bar charts for gender, kids, and occupation distribution per age group."""
    
    # We'll create a 3-row (one per age group), 3-column (gender, kids, occupation) figure
    fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(12, 10))
    fig.suptitle("Persona Distribution by Age Group", fontsize=16, y=1.02)
    plt.tight_layout()
    
    # For consistent ordering, let's define age groups in a list
    age_groups = ["18-30", "31-50", "51+"]
    columns = ["gender", "kids", "occupation"]
    
    for row_idx, group_name in enumerate(age_groups):
        for col_idx, col_key in enumerate(columns):
            ax = axes[row_idx, col_idx]
            counter_data = distribution[group_name][col_key]
            
            # Convert counter to two lists for plotting
            labels = list(counter_data.keys())
            values = list(counter_data.values())
            
            ax.bar(labels, values, color="skyblue")
            ax.set_title(f"{group_name} - {col_key.capitalize()}")
            ax.set_ylabel("Count")
            # Rotate x labels if they’re long (e.g. occupations)
            ax.set_xticklabels(labels, rotation=45, ha="right")
    
    plt.show()

if __name__ == "__main__":
    check_personas_distribution("personas.json")