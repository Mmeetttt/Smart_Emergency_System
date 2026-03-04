import streamlit as st
import pandas as pd
import heapq
import math

#Title 
st.title("Smart Emergency Resource Locator")

# Hash Table (Resource Storage) 
# Using Streamlit session state to persist data
if "resources" not in st.session_state:
    st.session_state.resources = {}

st.subheader("Add Emergency Resource")

# Input Form 
res_id = st.text_input("Resource ID")
res_type = st.selectbox("Resource Type", ["Hospital", "Ambulance", "Fire Truck", "Police Unit", "Rescue Team"])
x = st.number_input("X Location", step=1)
y = st.number_input("Y Location", step=1)
available = st.selectbox("Available", ["Yes", "No"])

# Add Button 
if st.button("Add Resource"):
    if res_id:
        st.session_state.resources[res_id] = {
            "Type": res_type,
            "X": x,
            "Y": y,
            "Available": available
        }
        st.success(f"Resource {res_id} added successfully!")
    else:
        st.warning("Please enter Resource ID")

# Display Table 
st.subheader("Stored Resources")

if st.session_state.resources:
    df = pd.DataFrame.from_dict(st.session_state.resources, orient="index")
    df.index.name = "Resource ID"
    st.dataframe(df)
else:
    st.info("No resources added yet.")

st.divider()
st.subheader("Update Resource Availability")

if st.session_state.resources:
    selected_resource = st.selectbox("Select Resource", list(st.session_state.resources.keys()))
    new_status = st.selectbox("Set Availability", ["Yes", "No"])

    if st.button("Update Resource Status"):
        st.session_state.resources[selected_resource]["Available"] = new_status
        st.success(f"{selected_resource} status updated to {new_status}")
else:
    st.info("No resources available")

st.divider()
st.subheader("Emergency Request")

# Prirority Queue Stoered in Location 
if "emergencies" not in st.session_state:
    st.session_state.emergencies = []

em_type = st.selectbox("Emergency Type", ["Medical", "Fire", "Crime", "Disaster", "Rescue"])

priority_label = st.selectbox(
    "Priority Level",
    [
        "1 - Critical",
        "2 - High",
        "3 - Medium",
        "4 - Low"
    ]
)

priority = int(priority_label[0])

ex = st.number_input("Emergency X", step=1, key="ex")
ey = st.number_input("Emergency Y", step=1, key="ey")

def required_resource_type(emergency):
    mapping = {
        "Medical": ["Hospital", "Ambulance"],
        "Fire": ["Fire Truck"],
        "Crime": ["Police Unit"],
        "Disaster": ["Rescue Team", "Ambulance"],
        "Rescue": ["Rescue Team"]
    }
    return mapping.get(emergency, [])

def find_nearest_resources(x, y, emergency, k=3):
    allowed_types = required_resource_type(emergency)
    distances = []

    for rid, data in st.session_state.resources.items():
        if data["Available"] == "Yes" and data["Type"] in allowed_types:
            dist = math.sqrt((data["X"] - x)**2 + (data["Y"] - y)**2)
            distances.append((rid, dist))

    distances.sort(key=lambda t: t[1])
    return distances[:k]

# Submit Emergency to Queue
if st.button("Submit Emergency"):
    heapq.heappush(st.session_state.emergencies, (priority, em_type, ex, ey))
    st.success("Emergency added to queue")

# Process Next Emergency
if st.button("Process Next Emergency"):

    if not st.session_state.emergencies:
        st.warning("No emergencies in queue")

    else:
        top = heapq.heappop(st.session_state.emergencies)

        nearest_list = find_nearest_resources(top[2], top[3], top[1], 3)

        if nearest_list:
            assigned, dist = nearest_list[0]

            st.session_state.resources[assigned]["Available"] = "No"

            st.success(f"Assigned Resource: {assigned}")
            st.write(f"Distance: {round(dist,2)}")

            st.write("Top Nearest Resources:")
            for rid, d in nearest_list:
                st.write(f"{rid} → {round(d,2)}")

            st.write("Data Structure Used: Priority Queue (Binary Heap)")
            st.write("Time Complexity: O(log n)")

        else:
            st.error("No available resource found")

st.subheader("Pending Emergency Queue")

if st.session_state.emergencies:

    queue_view = []

    for p, t, xq, yq in st.session_state.emergencies:
        queue_view.append({
            "Priority": p,
            "Emergency": t,
            "Location X": xq,
            "Location Y": yq
        })

    queue_view = sorted(queue_view, key=lambda x: x["Priority"])

    df_queue = pd.DataFrame(queue_view)

    st.dataframe(df_queue)

else:
    st.info("No pending emergencies")

st.divider()
st.subheader("Sort Resources by Distance")

sx = st.number_input("Reference X", step=1, key="sx")
sy = st.number_input("Reference Y", step=1, key="sy")

# merge sort 
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i][1] < right[j][1]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result

if st.button("Sort Resources"):
    if not st.session_state.resources:
        st.warning("No resources to sort")
    else:
        distances = []

        for rid, data in st.session_state.resources.items():
            dist = math.sqrt((data["X"] - sx)**2 + (data["Y"] - sy)**2)
            distances.append((rid, dist))

        sorted_list = merge_sort(distances)

        st.success("Resources sorted by distance")
        st.write("Algorithm Used: Merge Sort")
        st.write("Time Complexity: O(n log n)")

        for rid, dist in sorted_list:
            st.write(f"{rid} → Distance: {round(dist,2)}")