import matplotlib.pyplot as plt
import numpy as np

# Data
cases = ['Neutral Position', 'Directional (X 2x, Y 0.5x)', 'Directional (Y 2x, X 0.5x)']
position_values = [103070573.41129702, 83390403.90696032, 174286029.62128225]
hodl_values = [97695219.9, 166345378.5, 77892671.25]

# Compute differences for IL/IG
differences = [p - h for p, h in zip(position_values, hodl_values)]

x = np.arange(len(cases))
width = 0.35

fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.bar(x - width/2, position_values, width, label='Position Value')
bars2 = ax.bar(x + width/2, hodl_values, width, label='Hodl Value')
ax.axhline(0, color='black', linewidth=1, linestyle='--')  

# Annotate IL/IG
for i, diff in enumerate(differences):
    ax.text(i, diff, f"{'IG' if diff > 0 else 'IL'}\n{diff:.2f}",
            ha='center', va='bottom' if diff > 0 else 'top', fontsize=10, color='red')

ax.set_xlabel('Cases')
ax.set_ylabel('Value')
ax.set_title('Impermanent Loss (IL) vs Impermanent Gain (IG)')
ax.set_xticks(x)
ax.set_xticklabels(cases)
ax.legend()

plt.tight_layout()
plt.show()
