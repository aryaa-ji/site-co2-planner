# Site & CO2 Planner
# For each building element: how many days, how many trucks, how much CO2?
# Run:  python planner.py

import math
import pandas as pd
import matplotlib.pyplot as plt

# ---- 1. Assumptions (change these) ----
CO2_STANDARD = 196      # kg CO2 per m3, normal concrete C30/37 (ÖKOBAUDAT)
CO2_LOW_CARBON = 127    # kg CO2 per m3, low-carbon concrete with CEM III/B cement
CONCRETE_WEIGHT = 2.4   # tonnes per m3
TRUCK_LOAD = 24         # tonnes per truck

# ---- 2. Read the quantities from my Revit model ----
data = pd.read_csv("quantities.csv")

# ---- 3. Calculate ----
# Days = pieces / pieces per day (rounded up)
data["days"] = [math.ceil(p / r) for p, r in zip(data["pieces"], data["pieces_per_day"])]

# Trucks = weight / truck load (rounded up)
data["weight_t"] = data["concrete_m3"] * CONCRETE_WEIGHT
data["trucks"] = [math.ceil(w / TRUCK_LOAD) for w in data["weight_t"]]

# CO2 = concrete volume x CO2 per m3 (kg -> tonnes)
data["co2_standard_t"] = data["concrete_m3"] * CO2_STANDARD / 1000
data["co2_low_carbon_t"] = data["concrete_m3"] * CO2_LOW_CARBON / 1000

# ---- 4. Totals ----
days = data["days"].sum()
trucks = data["trucks"].sum()
co2_std = data["co2_standard_t"].sum()
co2_low = data["co2_low_carbon_t"].sum()
saving = (co2_std - co2_low) / co2_std * 100

print(data.round(1).to_string(index=False))
print(f"\nConstruction time: {days} working days")
print(f"Truck deliveries:  {trucks}")
print(f"CO2 normal concrete:     {co2_std:.0f} t")
print(f"CO2 low-carbon concrete: {co2_low:.0f} t  ({saving:.0f} % less)")

# ---- 5. Save results ----
data.round(1).to_excel("results.xlsx", index=False)

data.plot.barh(x="element", y=["co2_standard_t", "co2_low_carbon_t"],
               color=["#2a78d6", "#1baf7a"], figsize=(8, 4))
plt.legend(["Normal concrete", "Low-carbon concrete"])
plt.xlabel("t CO2")
plt.ylabel("")
plt.title(f"CO2 of concrete: normal vs. low-carbon ({saving:.0f} % less)")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("co2_chart.png", dpi=150)
