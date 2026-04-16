# Smart Emergency Resource Allocation System

## 📌 Overview
The Smart Emergency Resource Allocation System is a simulation-based application designed to efficiently manage emergency situations by assigning the most suitable hospital based on priority, distance, and availability. The system uses real-world hospital data and applies data structures and algorithms to improve decision-making.

## 🎯 Objectives
- Efficiently allocate hospitals during emergencies  
- Minimize response time using optimized algorithms  
- Demonstrate real-world application of data structures  
- Improve decision-making using data-driven logic  

## 🧠 Key Concepts Used
- Hash Table (Dictionary) → Fast data access (O(1))  
- Priority Queue (Min Heap) → Emergency handling (O(log n))  
- Greedy Approach → Best hospital selection  
- Sorting (Timsort) → Ranking hospitals (O(n log n))  
- Scoring System → Combines distance and bed availability
  
## ⚙️ Technologies Used
- Python  
- Streamlit  
- Pandas  
- NumPy  
- heapq (Priority Queue)  
- math (Distance Calculation)  
- difflib (Fuzzy Search)  
- Jupyter Notebook (Data Preprocessing)  

## 📊 Dataset
- Source: Open Government Data (OGD) Platform India (data.gov.in)  
- Dataset: Hospital Directory (National Health Portal)  
- Provided by: Ministry of Health and Family Welfare, Government of India  

### Dataset Includes:
- Hospital name  
- State and district  
- Coordinates (latitude, longitude)  
- Bed availability  
- Emergency services  
- Ambulance details  

## 🔄 System Workflow
1. Load and preprocess dataset  
2. Store hospital data using hash table  
3. Accept emergency input (type, priority, location)  
4. Store emergencies in priority queue  
5. Process highest priority emergency  
6. Calculate distance to all hospitals  
7. Apply scoring (distance + beds)  
8. Select best hospital  
9. Assign hospital and update availability  
10. Display nearby hospitals  

## 🚀 Features
- Emergency management system  
- Priority-based processing  
- Nearest hospital allocation  
- Hospital search with typo tolerance  
- Filter hospitals by district and beds  
- Dashboard visualization  
- Real dataset integration  

## ⏱ Time Complexity
- Emergency Processing → O(n log n)  
- Priority Queue Operations → O(log n)  
- Hash Table Access → O(1)  
- Search → O(n)  
- Filtering → O(n)
  
## 💾 Space Complexity
- Hospital data storage → O(n)  
- Emergency queue → O(e)
  
## ✅ Advantages
- Fast and efficient system  
- Real-world dataset usage  
- Scalable design  
- Easy to understand  
- Practical implementation of DSA
  
## ⚠️ Limitations
- No real-time data integration  
- Uses static dataset  
- Distance may be approximate (if not using GPS-based formula)  
- No live hospital availability updates
  
## 🔮 Future Enhancements
- Real-time API integration  
- GPS-based accurate distance calculation  
- Live hospital data updates  
- Ambulance tracking system  
- Machine learning for prediction  
