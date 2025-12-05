#.\.venv\Scripts\Activate.ps1
#python svm.py
 
import numpy as np

class UnderstandableSVM:
    def __init__(self, learning_speed=0.001, regularization_strength=0.01, iterations=1000):
        # 'lr' or 'alpha' -> learning_speed
        self.learning_speed = learning_speed
        # 'lambda' -> regularization_strength (keeps the model simple)
        self.regularization_strength = regularization_strength
        self.iterations = iterations
        
        # 'w' or 'weights' -> boundary_normal_vector
        # This defines the angle/direction of the dividing line
        self.boundary_normal_vector = None
        
        # 'b' or 'bias' -> boundary_offset
        # This shifts the line away from the center (0,0)
        self.boundary_offset = None

    def fit(self, inputs, targets):
        """
        Train the model.
        inputs: the data points (X)
        targets: the group labels, either -1 or 1 (y)
        """
        n_samples, n_features = inputs.shape
        
        # Initialize our line definition (weights) to zeros
        self.boundary_normal_vector = np.zeros(n_features)
        self.boundary_offset = 0

        # The Training Loop (Gradient Descent)
        for _ in range(self.iterations):
            
            for index, point in enumerate(inputs):
                # The correct group (-1 or 1) for this point
                correct_group = targets[index]
                
                # Check where the point falls relative to our current line
                # Mathematical formula: w * x + b
                # If the result is positive, it predicts Group 1. Negative -> Group -1.
                prediction_score = np.dot(point, self.boundary_normal_vector) + self.boundary_offset
                
                # 'Hinge Loss' Check:
                # We want the (correct_group * score) to be >= 1.
                # If it's less than 1, the point is either on the wrong side
                # OR it's too close to the line (inside the margin).
                margin_safety_check = correct_group * prediction_score

                if margin_safety_check >= 1:
                    # The point is safely on the correct side.
                    # We only gently nudge the line to keep it simple (Regularization).
                    # w = w - learning_speed * (2 * lambda * w)
                    self.boundary_normal_vector -= self.learning_speed * (2 * self.regularization_strength * self.boundary_normal_vector)
                else:
                    # The point is WRONG (or unsafe).
                    # We assume this point is a "Support Vector" and move the line based on it.
                    
                    # Update angle (w):
                    # w = w - learning_speed * (2 * lambda * w - y * x)
                    gradient = (2 * self.regularization_strength * self.boundary_normal_vector) - (correct_group * point)
                    self.boundary_normal_vector -= self.learning_speed * gradient
                    
                    # Update offset (b):
                    # b = b - learning_speed * (-y)
                    self.boundary_offset -= self.learning_speed * (-correct_group)

    def predict(self, inputs):
        """Predict the group for new data points."""
        # Calculate: input * vector + offset
        approx = np.dot(inputs, self.boundary_normal_vector) + self.boundary_offset
        
        # Return -1 or 1 based on the sign of the result
        return np.sign(approx)

# --- Example Usage ---
if __name__ == "__main__":
    # 1. Create dummy data
    # Group A (Class -1) are near [2, 3]
    # Group B (Class 1) are near [8, 9]
    X_train = np.array([
        [1, 2], [2, 3], [3, 3], [2, 1],  # Group A
        [8, 9], [7, 9], [9, 8], [8, 8]   # Group B
    ])
    y_train = np.array([-1, -1, -1, -1, 1, 1, 1, 1])

    # 2. Initialize and Train
    classifier = UnderstandableSVM(learning_speed=0.01, iterations=1000)
    classifier.fit(X_train, y_train)

    print("Training complete.")
    print(f"Angle Vector (w): {classifier.boundary_normal_vector}")
    print(f"Offset (b): {classifier.boundary_offset}")

    # 3. Test
    test_point = np.array([[1.5, 2.5], [8.5, 9.0]])
    predictions = classifier.predict(test_point)
    
    print("\nPredictions:")
    print(f"Point [1.5, 2.5] (Should be -1): {predictions[0]}")
    print(f"Point [8.5, 9.0] (Should be  1): {predictions[1]}")