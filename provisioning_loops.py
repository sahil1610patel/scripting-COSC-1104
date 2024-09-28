# Author: Kshitiz Pal, Sahil Patel
# Date: 27/09/2024
# Description: Basic cloud resource provisioning with multiple requests and range validation.

# Constants
TOTAL_CPU_CORES = 64
TOTAL_MEMORY_GB = 99.0

# Lists for allocated and pending resources
allocated_resources = []
pending_requests = []

# Variables for available resources
remaining_cpu_cores = TOTAL_CPU_CORES
remaining_memory_gb = TOTAL_MEMORY_GB

# Start loop
keep_going = "yes"
while keep_going == "yes":
    username = input("Enter your username: ")
    required_cpu_cores = int(input("Enter the number of CPU cores: "))
    required_memory_gb = float(input("Enter the amount of memory (GB): "))

    # Range validation: check for non-negative values
    if required_cpu_cores <= 0 or required_memory_gb <= 0:
        print("Invalid input. CPU cores and memory must be positive numbers.")
    else:
        # Check if resources are available
        if required_cpu_cores <= remaining_cpu_cores and required_memory_gb <= remaining_memory_gb:
            allocated_resources.append([username, required_cpu_cores, required_memory_gb])
            remaining_cpu_cores -= required_cpu_cores
            remaining_memory_gb -= required_memory_gb
        else:
            pending_requests.append([username, required_cpu_cores, required_memory_gb])

    keep_going = input("Do you want to make another request? (yes/no): ")

# Display results
print("\nAllocated Resources:")
for resource in allocated_resources:
    print("User:", resource[0], "\tCPU cores:", resource[1], "\tMemory (GB):", resource[2])

print("\nPending Requests:")
for request in pending_requests:
    print("User:", request[0], "\tCPU cores:", request[1], "\tMemory (GB):", request[2])
