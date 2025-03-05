import pandas as pd
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import pm4py

def load_email_data(file_path):
    """
    Load email metadata from a CSV file.
    Expects an 'epoch' column for the timestamp.
    """
    df = pd.read_csv(file_path)
    if 'epoch' in df.columns:
        # Convert epoch (assumed seconds) to datetime
        df['timestamp'] = pd.to_datetime(df['epoch'], unit='s')
    else:
        raise ValueError("Missing 'epoch' column for timestamp conversion.")
    return df

def combine_text_fields(row, fields=['subject', 'snippet']):
    """
    Combine several textual fields into one string.
    Adjust the list of fields based on what is available.
    """
    text = ""
    for field in fields:
        if field in row and pd.notnull(row[field]):
            text += str(row[field]) + " "
    return text.strip()

def assign_clusters(df, n_clusters=5, text_fields=['subject', 'snippet']):
    """
    Use TF-IDF and KMeans clustering on combined text fields to assign a cluster
    label to each email. The cluster label is used as a surrogate process case id.
    """
    # Combine chosen text fields into a single column for clustering
    df['combined_text'] = df.apply(lambda row: combine_text_fields(row, fields=text_fields), axis=1)
    
    # Convert text to a TF-IDF feature matrix
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(df['combined_text'])
    
    # Cluster the emails; tune n_clusters as appropriate
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df['cluster'] = kmeans.fit_predict(X)
    
    return df

def extract_recipients(recipient_field):
    """
    Attempt to parse the recipient field.
    If it’s a string representation of a list, evaluate it.
    Otherwise, return it as a single-item list.
    """
    try:
        recipients = ast.literal_eval(recipient_field)
        if isinstance(recipients, list):
            return recipients
        else:
            return [recipients]
    except Exception:
        return [recipient_field]

def preprocess_email_data(df):
    """
    Build an event log for process mining.
    
    Here:
    - The 'cluster' column (from clustering) is used as the case identifier.
    - For each email, we generate:
        - An "Email Sent" event (from the sender)
        - One "Email Received" event per recipient.
    """
    if 'cluster' not in df.columns:
        # Fall back: each email is its own process instance.
        df['cluster'] = df.index
    df['case_id'] = df['cluster'].astype(str)
    
    events = []
    for _, row in df.iterrows():
        # "Email Sent" event using the sender's email
        events.append({
            "timestamp": row["timestamp"],
            "case_id": row["case_id"],
            "activity": "Email Sent",
            "resource": row.get("senderEmail", "unknown")
        })
        # "Email Received" event(s) for each recipient
        recipients = extract_recipients(row.get("cecipientEmail", "unknown"))
        for rec in recipients:
            rec_clean = rec.strip() if isinstance(rec, str) else rec
            events.append({
                "timestamp": row["timestamp"],
                "case_id": row["case_id"],
                "activity": "Email Received",
                "resource": rec_clean
            })
    event_log_df = pd.DataFrame(events)
    return event_log_df

def mine_process_model(event_log_df):
    """
    Discover and visualize process models using pm4py.
    
    The function:
    - Formats the event log for pm4py.
    - Discovers a Directly-Follows Graph (DFG).
    - Discovers a Petri net model (using the Alpha Miner).
    """
    event_log = pm4py.format_dataframe(
        event_log_df, 
        case_id='case_id', 
        activity_key='activity', 
        timestamp_key='timestamp',
        resource_key='resource'
    )
    
    # Discover the Directly-Follows Graph (DFG)
    dfg, start_acts, end_acts = pm4py.discover_dfg(event_log)
    pm4py.view_dfg(dfg, start_acts, end_acts)
    
    # Discover a Petri net model using the Alpha Miner
    net, im, fm = pm4py.discover_petri_net_alpha(event_log)
    pm4py.view_petri_net(net, im, fm)
    
    return net, im, fm

# Main Execution
if __name__ == "__main__":
    # Update the file path to your dataset
    file_path = "messy_email_metadata.csv"
    df = load_email_data(file_path)
    
    # Cluster emails based on text fields to group them into process instances.
    # You can adjust the number of clusters (n_clusters) and the text fields as needed.
    df = assign_clusters(df, n_clusters=5, text_fields=['subject', 'snippet'])
    
    # Preprocess the data to create an event log.
    event_log_df = preprocess_email_data(df)
    
    # Perform process mining.
    mine_process_model(event_log_df)