import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import numpy as np

# Sample data
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

# Create the plot
fig, ax = plt.subplots()

# Plot lines
line1, = ax.plot(x, y1, color='blue', label='Sine Wave')
line2, = ax.plot(x, y2, color='green', label='Cosine Wave')

# Plot filled areas with patterns
ax.fill_between(x, y1, color='blue', alpha=0.3, hatch='/', label='Sine Fill')
ax.fill_between(x, y2, color='green', alpha=0.3, hatch='\\', label='Cosine Fill')

# Create custom legend handles
line1_handle = mlines.Line2D([], [], color='blue', label='Sine Wave', linestyle='-')
line2_handle = mlines.Line2D([], [], color='green', label='Cosine Wave', linestyle='-')

fill1_handle = mpatches.Patch(color='blue', alpha=0.3, hatch='/', label='Sine Fill')
fill2_handle = mpatches.Patch(color='green', alpha=0.3, hatch='\\', label='Cosine Fill')

# Combine handles
handles = [line1_handle, line2_handle, fill1_handle, fill2_handle]
labels = [handle.get_label() for handle in handles]

# Create legend
ax.legend(handles=handles, labels=labels, loc='upper right')

# Show the plot
# plt.show()
