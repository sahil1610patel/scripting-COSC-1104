# Author: Kshitiz Pal, Sahil Patel
# Date: 27/09/2024
# Description: Simulates a cloud resource provisioning system.

TOTAL_CPU_CORES = 64
TOTAL_MEMORY_GB = 99.0

required_cpu_cores = int(input("Enter the number of required CPU cores: "))
required_memory_gb = float(input("Enter the amount of required memory (GB): "))

if required_cpu_cores <= TOTAL_CPU_CORES and required_memory_gb <= TOTAL_MEMORY_GB:
    print("Resources provisioned successfully.")
    TOTAL_CPU_CORES -= required_cpu_cores
    TOTAL_MEMORY_GB -= required_memory_gb
else:
    print("Resource request exceeds capacity. Provisioning failed.")

print(f"Remaining CPU cores: {TOTAL_CPU_CORES}")
print(f"Remaining memory (GB): {TOTAL_MEMORY_GB}")
