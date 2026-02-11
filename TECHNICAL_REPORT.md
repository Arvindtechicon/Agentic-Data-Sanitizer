# Technical Report: Agentic Data Sanitizer (Agentic Pipeline)

## 1. Project Overview
The **Agentic Data Sanitizer** is a high-integrity data analysis agent built to solve the "Garbage In, Garbage Out" problem in AI-driven analytics. By implementing the **Agentic Pipeline Architecture**, the agent ensures that every visualization is preceded by automated data auditing, cleaning, and anomaly detection.

### 🧼 The Philosophy: Why "Sanitizer"?
Most AI data projects focus on the "pretty pictures" (visuals). But in a corporate environment, **dirty data is the enemy.** 
- If a laptop is priced at `$1,200` but the AI reads it as a string instead of a number, the total sales will be zero. 
- If someone types `$999,999` by mistake, your average sales chart will look like a spike to the moon.

We chose the name **Sanitizer** because this agent doesn't just "chat"—it scrubs. It removes the "bacteria" (errors, outliers, duplicates) from your raw CSV files so you can trust the results. It's the difference between a "Doodle" and a "Decision-Ready Report."

---

## 2. The Agentic Pipeline Architecture
The system follows a strict 4-stage sequential execution:

### Phase 1: VALIDATION (The Audit)
- **Integrity Checks**: Detects missing values, duplicates, and cardinality issues.
- **Health Scoring**: Generates a 0-100% score based on data completeness.
- **Type Compliance**: Verifies that numeric columns aren't polluted with strings.

### Phase 2: PREPROCESSING (The Treatment)
- **Standardization**: Normalizes categorical text and standardizes snake_case column headers.
- **Data Casting**: Converts informal date strings into high-performance `datetime64` objects.
- **Error Correction**: Strips currency symbols, handles negative values, and imputes missing data using Median/Mode strategies.

### Phase 3: ANOMALY DETECTION (The Insight)
- **Statistical Filtering**: Uses the **Interquartile Range (IQR)** method to isolate outliers.
- **Event Tagging**: Flags "Black Swan" events or data entry errors for separate analysis.

### Phase 4: VISUALIZATION (The Output)
- **Clean Rendering**: Plots only the validated and processed data.
- **Contextual Highlighting**: Automatically highlights identified anomalies in red or specialized callouts within the charts.

---

## 3. Tech Stack
- **Frontend**: Streamlit (Premium UI with custom CSS)
- **LLM**: Google Gemini 2.5 Flash (Acting as a Senior Data Engineer)
- **Execution Engine**: E2B Code Interpreter (Secure, Isolated Linux Sandbox)
- **Analysis Libraries**: Pandas, NumPy, Scipy
- **Visualization**: Matplotlib, Seaborn, Plotly

---

## 4. Key Implementation Details
### Dynamic System Prompting
The agent's behavior is governed by a strict system instruction that forces it to produce a `🛡️ Data Health Report` and a `🧹 Cleaning Log` as artifacts. This ensures the user is aware of every modification made to their data.

### Secure Sandbox Execution
All AI-generated Python code is executed in an **E2B Sandbox**. This isolation prevents potential "Prompt Injection" attacks or malicious code from affecting the host system while allowing complex operations like image generation and large-scale data manipulation.

### Context-Aware Recommendation Engine
The UI features a dynamic, color-coded suggestion system that analyzes the schema of the uploaded dataset. It proactively recommends powerful, simple prompts like "Analyze the entire revenue stream and perform anomaly detection," eliminating the need for complex prompt engineering while ensuring the Agentic Pipeline is fully utilized.

---

## 🧪 User Testing Guide: Scenario Comparison

This project includes two datasets to demonstrate the "Agentic Pipeline" effectiveness. Here is how to test them and what to expect from the AI Agent.

### Scenario A: The "Ideal" Case
**File**: `test_sales_data.csv`  
**User Prompt**: *"Analyze the entire dataset and show me the regional trends."*

*   **How the AI Thinks**: "The data is already clean. I will perform a quick validation (Audit), confirm 100% health, and proceed directly to aggregation and plotting."
*   **Resulting Response**: 
    1.  **Audit**: Shows 0 missing values, 0 duplicates.
    2.  **Cleaning**: Reports "No cleaning required."
    3.  **Visualization**: A clean, sharp bar chart showing North, South, East, and West performance.

---

### Scenario B: The "Real-World" Case (Dirty Data)
**File**: `uncleaned_sales_data.csv`  
**User Prompt**: *"Analyze the entire revenue stream and perform anomaly detection."*

*   **How the AI Thinks**: 
    1.  **Diagnosis**: "Wait, 'Sales' has a `$` in one row and a missing value in another. The category 'electronics' is duplicated due to casing issues."
    2.  **Strategic Treatment**: "I will strip the `$`, fill the missing sales with the median, and lowercase all categories before grouping."
    3.  **Anomaly Detection**: "I see a $999,999 laptop Sale. That's a 1.5 * IQR outlier. I'll flag it so it doesn't break the chart scale."
*   **Resulting Response**:
    1.  **🛡️ Data Health Report**: "Health Score: 82%. Issues found in 'Sales' and 'Category'."
    2.  **🧹 Cleaning Log**: "Converted '01/04/23' to Datetime; Fixed '$80' to 80; Imputed 1 missing value; Merged 3 duplicate categories."
    3.  **📊 Intelligent Visuals**: A chart that correctly combines ALL electronics sales into one bar and excludes the $999k outlier to keep the graph readable.

---

## 🚀 Real-World Experimental Test Cases (Pick & Paste)

Use these prompts with the `uncleaned_sales_data.csv` to see the agent's complex reasoning:

| Goal | User Prompt (Copy-Paste this) | What to Look For |
| :--- | :--- | :--- |
| **Integrity Audit** | *"Analyze the entire dataset and perform a deep health audit."* | Look for the **Health Score** and the list of inconsistent formats found. |
| **Fraud Spotting** | *"Analyze the entire revenue stream and perform anomaly detection."* | The agent should isolate the **$999k laptop** as an IQR outlier. |
| **Time Series Audit** | *"Analyze the entire timeline and perform a trend growth study."* | Check the **Cleaning Log** for "Standardized date formats" (mixed DD/MM and MM/DD). |
| **Regional Mix** | *"Analyze the entire segmentation and perform a category distribution audit."* | The agent will merge "electronics" and "ELECTRONICS" correctly. |

## 6. Usage Scenarios

The **Agentic Data Sanitizer** is designed for environments where data comes from multiple, unstandardized sources. Key applications include:

### 💼 1. Corporate Sales Operations
*   **The Problem:** Sales teams from different regions upload spreadsheets with varying currency formats ($ vs €), mixed date formats (MM/DD vs DD/MM), and inconsistent product naming.
*   **The Sanitizer Solution:** Automatically standardizes all regional uploads into a single, clean master dataframe before generating quarterly performance charts.

### 🏭 2. Supply Chain & Logistics
*   **The Problem:** Sensor data from warehouses often contains "ghost" readings (outliers) or missing timestamps due to connectivity drops.
*   **The Sanitizer Solution:** Identifies sensor malfunctions using IQR anomaly detection and imputes missing temporal data to provide an accurate lead-time analysis.

### 📑 3. Financial Audit & Compliance
*   **The Problem:** Large transaction logs often contain double-entries or manual input errors (e.g., adding an extra zero to a price).
*   **The Sanitizer Solution:** Flags high-variance transactions as "Black Swan" events and generates a Health Score to certify the data's reliability for audit purposes.

### 🏥 4. Healthcare Data Research
*   **The Problem:** Patient records often have missing fields or inconsistent categorical labels for conditions.
*   **The Sanitizer Solution:** Standardizes medical terminology using categorical casing and fills non-critical missing values with statistical averages to ensure research integrity.

---
Build with ❤️ by Aravind S Gudi
