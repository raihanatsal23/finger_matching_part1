# import csv
# import numpy as np
# import math
# import os

# # Paths to directories and files
# csv_input_path = "./output/minutiae_data.csv"  # Path to the CSV file with minutiae data
# csv_output_path = "./output/matching_results.csv"  # Path to save the matching results

# # Euclidean distance calculation
# def euclidean_distance(p1, p2):
#     return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

# # Load minutiae data from the CSV file and group by image name
# def load_minutiae_from_csv(filepath):
#     minutiae_data = {}
#     with open(filepath, mode='r') as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#             image_name = row["Image"]
#             locX = int(row["X"])
#             locY = int(row["Y"])
#             orientation = float(row["Orientation"])
#             minutiae_type = row["Minutiae Type"]

#             if image_name not in minutiae_data:
#                 minutiae_data[image_name] = []
#             minutiae_data[image_name].append(((locX, locY), orientation, minutiae_type))
    
#     print(f"Loaded minutiae data for {len(minutiae_data)} images.")
#     return minutiae_data

# # Matching function based on Euclidean distance and orientation difference
# def match_minutiae(input_minutiae, target_minutiae, position_threshold=20, orientation_threshold=0.30):
#     match_count = 0
#     for (input_point, input_orientation, _) in input_minutiae:
#         for (target_point, target_orientation, _) in target_minutiae:
#             distance = euclidean_distance(input_point, target_point)
#             orientation_diff = abs(input_orientation - target_orientation)
#             if orientation_diff > math.pi:
#                 orientation_diff = 2 * math.pi - orientation_diff  # Adjust for circular orientation difference

#             if distance <= position_threshold and orientation_diff <= orientation_threshold:
#                 match_count += 1
#                 break  # Stop after finding the first close match to avoid double-counting

#     score = match_count / max(len(input_minutiae), len(target_minutiae)) if max(len(input_minutiae), len(target_minutiae)) > 0 else 0
#     return score

# def main():
#     # Load minutiae data from the single CSV file
#     minutiae_data = load_minutiae_from_csv(csv_input_path)

#     # Open CSV file to write the matching results
#     with open(csv_output_path, mode='w', newline='') as csv_file:
#         csv_writer = csv.writer(csv_file)
#         csv_writer.writerow(["Image1", "Image2", "Score"])  # Write CSV header

#         # Set to keep track of matched pairs to avoid duplicate comparisons
#         matched_pairs = set()

#         # Iterate over each pair of images for matching, including self-matching
#         for input_image_name, input_minutiae in minutiae_data.items():
#             for target_image_name, target_minutiae in minutiae_data.items():
#                 # Check if this pair has already been compared
#                 pair = tuple(sorted([input_image_name, target_image_name]))
#                 if pair in matched_pairs:
#                     continue  # Skip if already matched

#                 # Mark this pair as matched
#                 matched_pairs.add(pair)

#                 # Perform matching and save the result
#                 score = match_minutiae(input_minutiae, target_minutiae)
                
#                 # Print result to terminal and save to CSV
#                 print(f"{input_image_name}, {target_image_name}, {score:.2f}")
#                 csv_writer.writerow([input_image_name, target_image_name, f"{score:.2f}"])

# if __name__ == "__main__":
#     main()

################################################################################################################################################

# import csv
# import numpy as np
# import math
# import os

# # Paths to directories and files
# csv_input_path = "./output/minutiae_data.csv"  # Path to the CSV file with minutiae data
# csv_output_path = "./output/matching_results.csv"  # Path to save the matching results

# # Euclidean distance calculation
# def euclidean_distance(p1, p2):
#     return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

# # Load minutiae data from the CSV file and group by image name
# def load_minutiae_from_csv(filepath):
#     minutiae_data = {}
#     with open(filepath, mode='r') as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#             image_name = row["Image"]
#             locX = int(row["X"])
#             locY = int(row["Y"])
#             orientation = float(row["Orientation"])
#             minutiae_type = row["Minutiae Type"]

#             if image_name not in minutiae_data:
#                 minutiae_data[image_name] = []
#             minutiae_data[image_name].append(((locX, locY), orientation, minutiae_type))
    
#     print(f"Loaded minutiae data for {len(minutiae_data)} images.")
#     return minutiae_data

# # Matching function based on Euclidean distance and orientation difference
# def match_minutiae(input_minutiae, target_minutiae, position_threshold=15, orientation_threshold=0.15):
#     match_count = 0
#     for (input_point, input_orientation, _) in input_minutiae:
#         for (target_point, target_orientation, _) in target_minutiae:
#             distance = euclidean_distance(input_point, target_point)
#             orientation_diff = abs(input_orientation - target_orientation)
#             if orientation_diff > math.pi:
#                 orientation_diff = 2 * math.pi - orientation_diff  # Adjust for circular orientation difference

#             if distance <= position_threshold and orientation_diff <= orientation_threshold:
#                 match_count += 1
#                 break  # Stop after finding the first close match to avoid double-counting

#     score = match_count / max(len(input_minutiae), len(target_minutiae)) if max(len(input_minutiae), len(target_minutiae)) > 0 else 0
#     return score

# def main():
#     # Load minutiae data from the single CSV file
#     minutiae_data = load_minutiae_from_csv(csv_input_path)

#     # Open CSV file to write the matching results
#     with open(csv_output_path, mode='w', newline='') as csv_file:
#         csv_writer = csv.writer(csv_file)
#         csv_writer.writerow(["Image1", "Image2", "Score"])  # Write CSV header

#         # Set to keep track of matched pairs to avoid duplicate comparisons
#         matched_pairs = set()

#         # Iterate over each pair of images for matching
#         for input_image_name, input_minutiae in minutiae_data.items():
#             for target_image_name, target_minutiae in minutiae_data.items():
#                 # Skip self-matching
#                 if input_image_name == target_image_name:
#                     continue

#                 # Check if this pair has already been compared
#                 pair = tuple(sorted([input_image_name, target_image_name]))
#                 if pair in matched_pairs:
#                     continue  # Skip if already matched

#                 # Mark this pair as matched
#                 matched_pairs.add(pair)

#                 # Perform matching and save the result
#                 score = match_minutiae(input_minutiae, target_minutiae)
                
#                 # Print result to terminal and save to CSV
#                 print(f"{input_image_name}, {target_image_name}, {score:.2f}")
#                 csv_writer.writerow([input_image_name, target_image_name, f"{score:.2f}"])

# if __name__ == "__main__":
#     main()

################################################################################################################################################

import csv
import numpy as np
import math
import os

# Paths to directories and files
csv_input_path = "./output/minutiae_data.csv"  # Path to the CSV file with minutiae data
csv_output_path = "./output/matching_results.csv"  # Path to save the matching results

# Euclidean distance calculation
def euclidean_distance(p1, p2):
    return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

# Load minutiae data from the CSV file and group by image name
def load_minutiae_from_csv(filepath):
    minutiae_data = {}
    with open(filepath, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            image_name = row["Image"]
            locX = int(row["X"])
            locY = int(row["Y"])
            orientation = float(row["Orientation"])
            minutiae_type = row["Minutiae Type"]

            if image_name not in minutiae_data:
                minutiae_data[image_name] = []
            minutiae_data[image_name].append(((locX, locY), orientation, minutiae_type))
    
    print(f"Loaded minutiae data for {len(minutiae_data)} images.")
    return minutiae_data

# Matching function based on Euclidean distance and orientation difference
def match_minutiae(input_minutiae, target_minutiae, position_threshold=18, orientation_threshold=0.15):
    match_count = 0
    for (input_point, input_orientation, input_type) in input_minutiae:
        for (target_point, target_orientation, target_type) in target_minutiae:
            # Only match minutiae with the same type
            if input_type != target_type:
                continue

            distance = euclidean_distance(input_point, target_point)
            orientation_diff = abs(input_orientation - target_orientation)
            if orientation_diff > math.pi:
                orientation_diff = 2 * math.pi - orientation_diff  # Adjust for circular orientation difference

            if distance <= position_threshold and orientation_diff <= orientation_threshold:
                match_count += 1
                break  # Stop after finding the first close match to avoid double-counting

    # Calculate matching score
    max_minutiae = max(len(input_minutiae), len(target_minutiae))
    score = match_count / max_minutiae if max_minutiae > 0 else 0
    return score

def main():
    # Load minutiae data from the single CSV file
    minutiae_data = load_minutiae_from_csv(csv_input_path)

    # Open CSV file to write the matching results
    with open(csv_output_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Image1", "Image2", "Score"])  # Write CSV header

        # Set to keep track of matched pairs to avoid duplicate comparisons
        matched_pairs = set()

        # Iterate over each pair of images for matching
        for input_image_name, input_minutiae in minutiae_data.items():
            for target_image_name, target_minutiae in minutiae_data.items():
                # Skip self-matching
                if input_image_name == target_image_name:
                    continue

                # Check if this pair has already been compared
                pair = tuple(sorted([input_image_name, target_image_name]))
                if pair in matched_pairs:
                    continue  # Skip if already matched

                # Mark this pair as matched
                matched_pairs.add(pair)

                # Perform matching and save the result
                score = match_minutiae(input_minutiae, target_minutiae)
                
                # Print result to terminal and save to CSV
                print(f"{input_image_name}, {target_image_name}, {score:.2f}")
                csv_writer.writerow([input_image_name, target_image_name, f"{score:.2f}"])

if __name__ == "__main__":
    main()



