import streamlit as st
import pandas as pd
import heapq
import math
from difflib import get_close_matches

st.set_page_config(page_title="Smart Emergency System", layout="wide")
st.title("Smart Emergency Resource System")

# LOAD DATA 
@st.cache_data
def load_data():
    df = pd.read_csv("processed_hospitals.csv")

    # BEDS 
    df["beds"] = pd.to_numeric(df["beds"], errors="coerce")

    # remove unrealistic values
    df.loc[df["beds"] > 2000, "beds"] = None

    # fill missing values with median
    df["beds"] = df["beds"].fillna(df["beds"].median())

    return df

df = load_data()

# HASH TABLE 
if "resources" not in st.session_state:
    resources = {}
    for i, row in df.iterrows():
        resources[i] = {
            "name": row["name"],
            "district": row["district"],
            "state": row["state"],
            "beds": int(row["beds"]),
            "lat": row["lat"],
            "lon": row["lon"],
            "emergency": bool(row["emergency"]),
            "ambulance": bool(row["ambulance"]),
            "available": True
        }
    st.session_state.resources = resources
else:
    resources = st.session_state.resources

# SIDEBAR 
page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Search Hospital", "Filter Hospitals", "Emergency System", "About Project"]
)

# DASHBOARD 
if page == "Dashboard":

    st.header("Dashboard")

    total = len(resources)
    available = sum([1 for r in resources.values() if r["available"]])
    busy = total - available

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Hospitals", total)
    col2.metric("Available", available)
    col3.metric("Busy", busy)

    st.subheader("Top Districts")
    st.bar_chart(df["district"].value_counts().head(10))

# SEARCH  
elif page == "Search Hospital":

    st.header("Search Hospital")

    name = st.text_input("Type hospital name")

    if name:

        # STEP 1: direct substring search 
        result = df[df["name"].str.contains(name, case=False, na=False)]

        # STEP 2: if nothing found, use fuzzy matching
        if result.empty:
            from difflib import get_close_matches

            names_list = df["name"].dropna().tolist()
            matches = get_close_matches(name, names_list, n=10, cutoff=0.6)

            result = df[df["name"].isin(matches)]

        # OUTPUT
        if not result.empty:
            st.dataframe(result)
        else:
            st.warning("No hospital found")

# FILTER 
elif page == "Filter Hospitals":

    st.header("Filter Hospitals")

    district = st.selectbox("District", ["All"] + sorted(df["district"].unique()))

    
    max_beds = int(min(df["beds"].max(), 1000))

    min_beds = st.slider("Minimum Beds", 0, max_beds, 50)

    emergency_only = st.checkbox("Emergency Only")

    filtered = df.copy()

    if district != "All":
        filtered = filtered[filtered["district"] == district]

    filtered = filtered[filtered["beds"] >= min_beds]

    if emergency_only:
        filtered = filtered[filtered["emergency"] == True]

    st.dataframe(filtered)

# EMERGENCY 
elif page == "Emergency System":

    st.header("Emergency System")

    if "queue" not in st.session_state:
        st.session_state.queue = []

    etype = st.selectbox("Type", ["Medical", "Fire", "Accident"])
    priority = st.selectbox("Priority", [1, 2, 3])

    ex = st.number_input("Latitude", value=19.07)
    ey = st.number_input("Longitude", value=72.87)

    def distance(x1, y1, x2, y2):
        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

    if st.button("Add Emergency"):
        heapq.heappush(st.session_state.queue, (priority, etype, ex, ey))
        st.success("Emergency Added")

    st.subheader("Queue")
    for q in sorted(st.session_state.queue):
        st.write(q)

    if st.button("Process Emergency"):

        if st.session_state.queue:

            p, t, x, y = heapq.heappop(st.session_state.queue)

            distances = []

            for r in resources.values():
                if r["available"]:
                    d = distance(x, y, r["lat"], r["lon"])
                    score = d - (r["beds"] * 0.01)
                    distances.append((r, score, d))

            distances.sort(key=lambda x: x[1])

            nearest = distances[:5]

            best, _, best_dist = nearest[0]
            best["available"] = False

            st.success(f"Assigned: {best['name']}")
            st.write(f"Distance: {round(best_dist,2)} units")

            st.subheader("Top 5 Nearby Hospitals")

            table = []
            for r, _, d in nearest:
                table.append({
                    "Hospital": r["name"],
                    "District": r["district"],
                    "Beds": r["beds"],
                    "Distance": round(d, 2)
                })

            st.dataframe(pd.DataFrame(table))

#  ABOUT 
elif page == "About Project":

    st.header("About Project")

    st.write("""
    Smart Emergency Resource Allocation System is a simulation-based application designed to efficiently manage emergency situations using core data structures and algorithms. The system focuses on assigning the most suitable hospital based on priority, distance, and availability using a real-world dataset.

    1. Objective of the System
    - To efficiently allocate hospitals during emergency situations
    - To minimize response time using optimized algorithms
    - To demonstrate real-world application of data structures
    - To improve decision-making using data-driven logic

    2. Dataset Details
    - Dataset sourced from Open Government Data Platform India (data.gov.in)
    - Provided by National Health Portal (NHP), Government of India
    - Contains hospital name, state, district, coordinates, beds, emergency services
    - Preprocessed to remove invalid values and ensure accuracy

    3. Data Structures Used

    a) Hash Table (Dictionary)
    - Used to store hospital data
    - Key: hospital ID
    - Value: hospital details
    - Time Complexity:
      - Insertion: O(1)
      - Access: O(1)
      - Update: O(1)

    b) Priority Queue (Binary Heap)
    - Implemented using heapq
    - Stores emergency requests based on priority
    - Lower value = higher priority
    - Time Complexity:
      - Insertion (push): O(log n)
      - Deletion (pop): O(log n)
      - Peek: O(1)

    4. Algorithms Used

    a) Distance Calculation (Euclidean Distance)
    - Formula used:
      √((x2 - x1)^2 + (y2 - y1)^2)
    - Used to find nearest hospital
    - Time Complexity: O(1) per calculation

    b) Selection Logic (Improved Allocation)
    - Uses both distance and bed capacity
    - Score = distance - (beds × factor)
    - Ensures better hospital selection

    c) Sorting (for nearest hospitals)
    - Hospitals sorted based on score
    - Time Complexity: O(n log n)

    5. System Workflow
    - Load and preprocess dataset
    - Store hospital data in hash table
    - User inputs emergency details (type, priority, location)
    - Emergency added to priority queue
    - Highest priority emergency processed first
    - Distance calculated to all available hospitals
    - Best hospital selected using scoring logic
    - Hospital assigned and marked unavailable
    - Top nearby hospitals displayed

    6. Features Implemented
    - Emergency management system
    - Priority-based processing
    - Nearest hospital allocation
    - Hospital search with typo tolerance
    - Filtering hospitals by district and beds
    - Dashboard with data visualization
    - Real dataset integration

    7. Time Complexity Summary
    - Data loading: O(n)
    - Hash table operations: O(1)
    - Priority queue operations: O(log n)
    - Distance computation: O(n)
    - Sorting hospitals: O(n log n)

    8. Space Complexity
    - Hash table storage: O(n)
    - Priority queue: O(e), where e = number of emergencies
    - Dataframe storage: O(n)

    9. Future Enhancements
    - Integration with real-time APIs
    - GPS-based accurate distance calculation
    - Live hospital data updates
    - Ambulance tracking system
    - Machine learning for prediction

    This project demonstrates how data structures like hash tables and priority queues can be effectively used to solve real-world problems such as emergency resource allocation in healthcare systems.
    """)