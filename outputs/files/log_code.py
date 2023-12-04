import seaborn as sns
import pandas as pd
import numpy as np

# Create a sample DataFrame
data = {
    'x': np.random.normal(size=100),
    'y': np.random.normal(size=100)
}
df = pd.DataFrame(data)

# Create a scatterplot using Seaborn
sns.scatterplot(data=df, x='x', y='y')

# Set the title and labels
plt.title('Seaborn Scatterplot')
plt.xlabel('X')
plt.ylabel('Y')

# Show the plot
plt.show()
