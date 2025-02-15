# Preview exported_comments.md
# main.py
import pandas as pd
from  langchain import  RecurrentTopicChain,  Chain
from  lxml import  etree
import  config
import  datetime
from  datetime  import  dateparse
from  prom import  import  message_topic_prompt
import streamlit as st
import os

def  extract_comment(config,start_date,  end_date):
	cert_alert_request  =  checkpoint_alert_request
	domain_code='CERTIFICATION_ALERT',  "BACKTESTING_IM_VALID_ALERT",  "CCO_ALERT",  "CERTIFICATION_IM_VALID_ALERT",  "CWD_ALERT",  "DAILYUSE_ALERT",  "INCREATRIR
	start_date=datetime.strptime(start_date,  '%Y-%m-%d')
	end_date=datetime.strptime(end_date,  '%Y-%m-%d')

	print('extracting  certification alerts......')
	cert_df  =  checkpoint_query.alerts(alert_query_request=cert_alert_request)
	cert_df.to_csv('Output/CERTIFICATION_ALERT_{start_date}_{end_date}.csv')
	print('certification  alerts extraction  completed')
	return  cert_df

def  extract_ia_comment(config,start_date,  end_date):
	ia_alert_request  =  INCOMEATRIBUTION_ALERT
	domain_code='INCREATRIBUTION_ALERT'
	start_date=datetime.strptime(start_date,  '%Y-%m-%d')
	end_date=datetime.strptime(end_date,  '%Y-%m-%d')

	print('extracting  income attribution  alerts......')
	ia_df  =  checkpoint_query.alerts(alert_query_request=ia_alert_request)
	ia_df.to_csv('Output/INCREATRIBUTION_ALERT_{start_date}_{end_date}.csv')
	print('Income  attribution  alerts extraction  completed')
	return  ia_df

def  cert_data_tidying(cert_df,  desk):
	cert_df  =  cert_df[(cert_df['parameter_name']  ==  desk)]  [(cert_df['trading_desk']  ==  desk)]  [(cert_df['comment'].str.contains(desk,  na=False))]
	cert_df['comment_concat']  =  'Error Message: '+  cert_df['error_message'].fillna('')+ 'No Comment:'+  cert_df['comment'].fillna('')+ 'No  Comment:'+  "a  Managerial  Validation  Comment"'+
	# group the comments by date and indicator
	grouped_cert_comments  =  cert_df.groupby(['as_of_date',  'indicator_name'])[['comment_concat']].apply(lambda x:  x.tolist()).reset_index()
	#format the dates for LIM
	grouped_cert_comments['as_of_date']  =  pd.to_datetime(grouped_cert_comments['as_of_date']).dt.date
	grouped_cert_comments['as_of_date']  =  grouped_cert_comments['as_of_date'].astype(str)  # Convert date to string
	grouped_cert_comments["Comment  for  LIM"]  =  [
	"Certification  Alert  Comment:  "+
	alert
	for  alert
	in
	grouped_cert_comments['comment_concat']
	]
	grouped_cert_comments["comment_concat"]=  grouped_cert_comments["as_of_date"].apply(lambda x: ','.join(x))

	return  grouped_cert_comments

def  pd_data_tidying(ia_df,  desk):
	# Income Attribution data handling
	ia_df  =  ia_df[(ia_df['parameter_name']  ==  desk)]  [(ia_df['trading_desk']  ==  desk)]
	ia_df['comment_concat']  =  'Error  Message: '+  ia_df['error_message'].fillna('')+ 'No Comment:'+  ia_df['comment'].fillna('')+  'No  seg_mbc_comment:'+  ia_df['seg_mbc_comment'].fillna('')+'No  seg_mbc_comment:'+'a  Managerial  Vali
	# group the comments by date and indicator
	grouped_IA_comments  =  ia_df.groupby(['as_of_date'])[['comment_concat']].apply(lambda x:  x.tolist()).reset_index()
	#format the dates for LIM
	grouped_IA_comments['as_of_date']  =  pd.to_datetime(grouped_IA_comments['as_of_date']).dt.date
	grouped_IA_comments['as_of_date']  =  grouped_IA_comments['as_of_date'].astype(str)
	grouped_IA_comments.rename(columns={'comment_concat':  'Income  Attribution  Alert  Comment for  LIM'},  inplace=True)
	return  grouped_IA_comments

def  pnl_data_tidying(pnl_comment_df,  desk):
	# P&L data tidying
	pnl_comment  =  pnl_comment_df[(pnl_comment_df['FC']  ==  desk)]
	pnl_comment['value_Label']  =  pnl_comment[['Label1',  'Label2',  'Label3']].apply(list).reset_index()
	pnl_comment['as_of_date']  =  pd.to_datetime(pnl_comment['as_of_date']).dt.date.astype(str)
	pnl_comment.rename(columns={'comments':  'P&L  Comment  for  LIM'},  inplace=True)
	return  grouped_IA_comments

#extract  cert_comment(config.start_date,config,end_date)
# extract  IA_comment(config.start_date,config,end_date)

def  merge(grouped_cert_comments,  grouped_IA_comments,  grouped_pnl_comments):
	# Merge the dataframes
	merged_df  =  pd.merge(grouped_cert_comments,  grouped_IA_comments,  on='as_of_date',  how='outer')
	merged_df  =  pd.merge(merged_df,  grouped_pnl_comments,  on='as_of_date',  right_on='value_Label',  how='outer')
	# fix the Lambda function to handle non-list values correctly
	merged_df['Cert  Comment  for  LIM']  =  merged_df.apply(lambda x:  ','.join(x)  if  isinstance(x,  list)  else  x)
	merged_df['Income  Attribution  Alert  Comment for  LIM']  =  merged_df.apply(lambda x:  ','.join(x)  if  isinstance(x,  list)  else  x)
	def  create_final_comment(cert_comment,  ia_comment,  pnl_comment):
		comment  =  []
		if  cert_comment:
			comments.append("Certification  Alert  Comment:"+  cert_comment)
		if  ia_comment:
			comments.append("Income  Attribution  Alert  Comment:"+  ia_comment)
		if  pnl_comment:
			comments.append("P&L  Comment:"+  pnl_comment)
		return  ', '.join(comments)  if  comments  else  pd.NA

	merged_df['Comment  for  LIM']  =  merged_df.apply(
	lambda  row:  ','.join(row)  if  isinstance(row,  list)  else  row,
	axis=1
	)
	return  merged_df

#Rewinding  Global recurrent  topic
#Extract comments for review using langChain
#analyze  all  comments......
comments_text  =  "\n".join([f"Comment  (id={i+1}):  {comment}"  for  i,  comment  in  enumerate(comments)])
#testing
result  =  alertchain.invoke({"query":  comments_text})

# Extract  structured summary
#no_explanation
explanations=["No  explanations",  "No summary available",  "No explanation"]
patterns=["No  patterns",  "No  explanation available"]
tech=["No  tech",  "No Technical Issues Identified"]
risk=["No  risk",  "No  risk control",  "No risk control identified"]
next=["No  next",  "No next steps",  "No next steps Identified"]

# Format the top topics with their explanations
formatted_topics_explanations  =  []
for i,  topic  in  enumerate(top_topics):
	explanation_list  =  explanations[i]  if  i  <  len(explanations)  else  ["No explanation available"]
	formatted_explanation  =  ",  ".join(f"({exp})"  for  exp  in  enumerate(explanation_list))
	formatted_topics_explanations.append(
		f"Top Topic  ({i+1}):  {topic}\nFormatted  Explanation"
	)

formatted_topics_explanations_text  =  "\n".join(formatted_topics_explanations)

structured_summary  =  {
"Formatted  Explanations":formatted_topics_explanations_text,
"Patterns":patterns,
"Technical Issues":tech,
"Risk Controls":risk,
"Next Step":next,
"Note:  The  review  generated  by  AI  serves  as  a  guiding  tool,  please  apply  professional  judgment  and  use  with  caution."
}

return  structured_summary

# Analyse cert comment
def  analyze_alert_comment(comments):
	comments_text  =  "\n".join([f"Comment  (id={i+1}):  {comment}"  for  i,  comment  in  enumerate(comments)])
	result  =  alertchain.invoke({"query":  comments_text})

	primarymat  =
	top_topics  =  result.get("top_topics",  "No summary available")
	explanations=result.get("explanations",  ["No  explanation available"])
	patterns=result.get("patterns",  ["No  patterns available"])
	tech  =  result.get("tech",  "No technical issues Identified")
	risk_controls  =  result.get("risk_controls",  "No risk control identified")
	next_steps  =  result.get("next_steps",  "No next steps identified")

	# Format the top topics with their explanations
	formatted_topics_explanations  =  []
	for  i,  topic  in  enumerate(top_topics):
		explanation_list  =  explanations[i]  if  i  <  len(explanations)  else  ["No explanation available"]
		formatted_explanation  =  ",  ".join(f"({exp})"  for  exp  in  enumerate(explanation_list))
		formatted_topics_explanations.append(
			f"Top Topic  ({i+1}):  {topic}\nFormatted  Explanation"
		)

	formatted_topics_explanations_text  =  "\n".join(formatted_topics_explanations)

	structured_summary  =  {
	"Formatted  Explanations":formatted_topics_explanations_text,
	"Patterns":patterns,
	"Technical Issues":tech,
	"Risk Controls":risk_controls,
	"Next Step":next_steps,
	"Note:  The  review  generated  by  AI  serves  as  a  guiding  tool,  please  apply  professional  judgment  and  use  with  caution."
	}

	return  structured_summary

def create_output_directory():
    if not os.path.exists('Output'):
        os.makedirs('Output')

def validate_desk(df, desk):
    """Validate if desk exists in the dataset"""
    return desk in df['parameter_name'].unique() or desk in df['trading_desk'].unique()

def save_markdown_output(summary, filename):
    """Save summary to markdown file with timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = f"Output/{filename}_{timestamp}.md"
    with open(filepath, 'w') as f:
        f.write(str(summary))
    return filepath

def main():
    st.title("Comment Analysis Dashboard")
    
    # Create sidebar for inputs
    st.sidebar.header("Configuration")
    
    # File uploaders
    cert_file = st.sidebar.file_uploader("Upload Certification Alert file", type=['csv'])
    ia_file = st.sidebar.file_uploader("Upload Income Attribution Alert file", type=['csv'])
    pnl_file = st.sidebar.file_uploader("Upload PNL file", type=['csv'])
    
    # Date selection
    start_date = st.sidebar.date_input("Start Date")
    end_date = st.sidebar.date_input("End Date")
    
    # Initialize session state for desk options
    if 'desk_options' not in st.session_state:
        st.session_state.desk_options = []
    
    # Update desk options when files are uploaded
    if cert_file is not None:
        cert_df = pd.read_csv(cert_file)
        desk_options = cert_df['parameter_name'].unique()
        st.session_state.desk_options = desk_options
    
    # Desk selection
    desk = st.sidebar.selectbox(
        "Select Desk",
        options=st.session_state.desk_options if st.session_state.desk_options else ['Upload files first']
    )
    
    create_output_directory()
    
    if st.sidebar.button("Analyze Comments"):
        if cert_file is None or ia_file is None or pnl_file is None:
            st.error("Please upload all required files")
            return
            
        # Load data
        cert_df = pd.read_csv(cert_file)
        ia_df = pd.read_csv(ia_file)
        pnl_df = pd.read_csv(pnl_file)
        
        # Validate desk
        if not validate_desk(cert_df, desk):
            st.error(f"Selected desk '{desk}' not found in the dataset!")
            return
            
        # Process data
        with st.spinner("Processing comments..."):
            grouped_cert_comments = cert_data_tidying(cert_df, desk)
            grouped_ia_comments = pd_data_tidying(ia_df, desk)
            grouped_pnl_comments = pnl_data_tidying(pnl_df, desk)
            
            # Merge and analyze
            merged_df = merge(grouped_cert_comments, grouped_ia_comments, grouped_pnl_comments)
            all_cert_comments = grouped_cert_comments["Cert Comment for LIM"].dropna().tolist()
            all_ia_comments = grouped_ia_comments["Income Attribution Alert Comment for LIM"].dropna().tolist()
            all_comments = merged_df['Comment for LIM'].dropna().tolist()
            
            # Generate summaries
            cert_summary = analyze_alert_comment(all_cert_comments)
            ia_summary = analyze_alert_comment(all_ia_comments)
            comment_summary = analyze_alert_comment(all_comments)
            
            # Save outputs
            cert_filepath = save_markdown_output(cert_summary, "cert_summary")
            ia_filepath = save_markdown_output(ia_summary, "ia_summary")
            comment_filepath = save_markdown_output(comment_summary, "comment_summary")
            
            # Display results in tabs
            tab1, tab2, tab3 = st.tabs(["Certification Summary", "IA Summary", "Combined Summary"])
            
            with tab1:
                st.markdown("### Certification Alert Summary")
                st.markdown(cert_summary)
                st.download_button(
                    "Download Certification Summary",
                    str(cert_summary),
                    file_name=f"cert_summary_{datetime.now().strftime('%Y%m%d')}.md"
                )
            
            with tab2:
                st.markdown("### Income Attribution Summary")
                st.markdown(ia_summary)
                st.download_button(
                    "Download IA Summary",
                    str(ia_summary),
                    file_name=f"ia_summary_{datetime.now().strftime('%Y%m%d')}.md"
                )
            
            with tab3:
                st.markdown("### Combined Summary")
                st.markdown(comment_summary)
                st.download_button(
                    "Download Combined Summary",
                    str(comment_summary),
                    file_name=f"comment_summary_{datetime.now().strftime('%Y%m%d')}.md"
                )

if __name__ == "__main__":
    main()

