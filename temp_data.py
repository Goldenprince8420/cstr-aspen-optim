import sobol_seq
import numpy as np

n_features = 10
num_points = 10
points = np.random.rand(n_features, num_points)

print(points.shape)


# def _quasi_monte_carlo(self):
#         # Generate a Sobol sequence for n_variables
#         sobol_points = sobol_seq.i4_sobol_generate(self.n_features, self.num_points)
#
#         # Initialize an empty array to store the samples
#         self.samples = np.zeros((self.num_points, self.n_features))
#
#         # Scale and shift the Sobol points to match the specified variable ranges
#         for i in range(self.n_features):
#             self.samples[:, i] = self.variable_ranges[i][0] + sobol_points[:, i] * (
#                     self.variable_ranges[i][1] - self.variable_ranges[i][0])
#
#         return self.samples
