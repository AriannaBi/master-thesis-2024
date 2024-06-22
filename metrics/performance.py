import matplotlib.pyplot as plt

# Sample data
depths = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
execution_times = [0.01, 0.02, 0.04, 0.08, 0.15, 0.30, 0.60, 1.20, 2.40, 4.80]  # example values
memory_usages = [10, 12, 15, 20, 30, 45, 70, 100, 150, 220]  # example values in MB
accuracies = [100, 100, 100, 100, 98, 95, 90, 85, 75, 60]  # example percentage values

# Plot Execution Time vs. Depth
plt.figure()
plt.plot(depths, execution_times, marker='o')
plt.xlabel('Depth of Formula')
plt.ylabel('Execution Time (s)')
plt.title('Execution Time vs. Depth')
plt.grid(True)
plt.show()

# Plot Memory Usage vs. Depth
plt.figure()
plt.plot(depths, memory_usages, marker='o')
plt.xlabel('Depth of Formula')
plt.ylabel('Memory Usage (MB)')
plt.title('Memory Usage vs. Depth')
plt.grid(True)
plt.show()

# Plot Accuracy vs. Depth
plt.figure()
plt.plot(depths, accuracies, marker='o')
plt.xlabel('Depth of Formula')
plt.ylabel('Accuracy (%)')
plt.title('Accuracy vs. Depth')
plt.grid(True)
plt.show()
