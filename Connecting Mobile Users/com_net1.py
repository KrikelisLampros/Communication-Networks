# ~UTH.gr 
# Department of Computer Science and Biomedical Informatics
# Subject Communication networks
# Krikelis Lampros  

import math
import matplotlib.pyplot as plt

def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def find_nearest_ap(mobile_position, ap_positions):
    distances = [calculate_distance(mobile_position[0], mobile_position[1], ap_position[0], ap_position[1]) for ap_position in ap_positions]
    nearest_ap_index = distances.index(min(distances))
    return nearest_ap_index, min(distances)

def calculate_sum_of_distances(mobile_positions, ap_positions):
    # Calculate the minimum distances for all mobiles
    min_distances = [find_nearest_ap(mobile_position, ap_positions)[1] for mobile_position in mobile_positions]

    # Calculate and return the sum of the minimum distances
    return sum(min_distances)

def main():

    # ~~~Here I am woring on the file and intialize  the mobile users and the Access points 
    # Load input data from MobileData.txt
    with open("MobileData.txt", "r") as file:
        # Read the first line containing M (number of mobile users) and K (number of APs)
        M, K = map(int, file.readline().split())

        ap_loads = [0] * K

        # Read mobile positions
        mobile_positions = [list(map(float, file.readline().split())) for _ in range(M)]

        # Read access point positions
        ap_positions = [list(map(float, file.readline().split())) for _ in range(K)]
        
        # Vector n containing the number of cells assigned to each AP
        connected_mobiles = [find_nearest_ap(mobile_position, ap_positions)[0] for mobile_position in mobile_positions]
        vector_n = [connected_mobiles.count(j) for j in range(K)]
        print(f"We have {len(vector_n)} Vectors/Access Points\nEach Access point containing the following number of users on them: {vector_n} ")

        # Calculate the sum of minimum distances for all mobiles
        sum_of_distances = calculate_sum_of_distances(mobile_positions, ap_positions)
        print(f"Sum of Minimum Distances for All Mobiles: {sum_of_distances}")


        # ~~~~ Here I am storying the calculated distance in the ap loads.

        for i, mobile_position in enumerate(mobile_positions, start=1):
            nearest_ap_index, min_distance = find_nearest_ap(mobile_position, ap_positions)
            # print(f"Mobile User {i}: Nearest AP Index = {nearest_ap_index + 1}, Distance = {min_distance}")

            #  load on the connected AP
            ap_loads[nearest_ap_index] += 1
            # print(f"Load on Each AP: {ap_loads}")

        
        # Find and print the minimum and maximum AP loads
        min_load_ap_index = ap_loads.index(min(ap_loads)) + 1
        max_load_ap_index = ap_loads.index(max(ap_loads)) + 1

        min_load = min(ap_loads)
        max_load = max(ap_loads)

        print(f"Minimum AP Load: AP {min_load_ap_index} with Load {min_load}")
        print(f"Maximum AP Load: AP {max_load_ap_index} with Load {max_load}")
                
        # Visualize the usage of access points with a scatter plot
        plt.figure(figsize=(10, 6))  
        plt.scatter(*zip(*mobile_positions), c=connected_mobiles, cmap='viridis', label='Mobiles', marker='o')
        plt.scatter(*zip(*ap_positions), c='red', label='APs', marker='s')

        # Draw lines connecting mobiles to their nearest APs
        for i, mobile_position in enumerate(mobile_positions, start=1):
            nearest_ap_index, _ = find_nearest_ap(mobile_position, ap_positions)
            plt.plot([mobile_position[0], ap_positions[nearest_ap_index][0]], [mobile_position[1], ap_positions[nearest_ap_index][1]], color='black', linestyle='dashed', linewidth=0.5)
            
            # Adding a label next to each Ap
            plt.text(ap_positions[nearest_ap_index][0], ap_positions[nearest_ap_index][1], f'{nearest_ap_index + 1}', fontsize=8, ha='right')


        plt.xlabel('X-coordinate')
        plt.ylabel('Y-coordinate')
        plt.title('Mobile Connections to Nearest AP')
        plt.legend()
        plt.show()

if __name__ == "__main__":
    main()
