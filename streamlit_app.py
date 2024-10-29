# import streamlit as st
# import requests
# import pandas as pd
# from langchain_core.messages import AIMessage, HumanMessage
# from dotenv import load_dotenv
# import re
# import json
# from datetime import datetime
# import os

# # Load environment variables
# load_dotenv()

# # Initialize session state variables
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
# if "search_history" not in st.session_state:
#     st.session_state.search_history = {}
# if "last_keywords" not in st.session_state:
#     st.session_state.last_keywords = []
# if "selected_problem" not in st.session_state:
#     st.session_state.selected_problem = None
# if "pending_feedback" not in st.session_state:
#     st.session_state.pending_feedback = False
# if "problem_offset" not in st.session_state:
#     st.session_state.problem_offset = 0

# # Set up the Streamlit app
# st.set_page_config(page_title="HitLit", page_icon="🤖", initial_sidebar_state="expanded")

# # Add custom CSS to style the title
# st.markdown("""
#     <style>
#     .reportview-container {
#         margin-top: -2em;
#     }
#     MainMenu {visibility: hidden;}
#     .stDeployButton {display:none;}
#     footer {visibility: hidden;}
#     .header-container {
#         display: flex;
#         justify-content: flex-start;
#         align-items: center;
#         padding: 0;
#         margin: 0;
#     }
#     .title {
#         font-size: 35px;
#         font-weight: bold;
#         margin: 0;
#         padding: 0;
#         text-align: center;
#         font-family: 'Courier New', Courier, monospace;
#         color: #FF5733;
#     }
#     </style>
#     """, unsafe_allow_html=True)

# # Add the custom title
# st.markdown('<div class="header-container"><span class="title">♨️ HITLIT</span></div>', unsafe_allow_html=True)

# # Load the CSV file
# @st.cache_data
# def load_csv(file_path):
#     return pd.read_csv(file_path)

# # Replace with your CSV file path
# csv_file_path = r"\\kor2fs03\V-V--Testing$\03_Validation_Software\LLBP\VALSW_LL_BP_SPL_V1.1.csv"
# csv_data = load_csv(csv_file_path)

# def clean_and_split_query(query):
#     filler_words = {'um', 'like', 'you', 'know', 'so', 'well', 'actually', 'basically', 'just', 'really'}
#     stop_words = {'is', 'are', 'was', 'were', 'what', 'who', 'how', 'where', 'when', 'why',
#                   'i', 'me', 'you', 'his', 'her', 'ok', 'bye', 'i am sorry', 'it is what it is', 'it','is','on','over','under','inside','an','a','the', 'does','con',
#                   'get', 'got', 'have', 'had', 'has', 'should', 'not', 'use', 'mobile','team','Team','Verdict','an','no','not','but','T','15','with','off'}
#     cleaned_query = re.sub(r'[^\w\s]', '', query)
#     words = cleaned_query.lower().split()
#     filtered_words = [word for word in words if word not in filler_words and word not in stop_words]
#     return filtered_words

# # Function to get problems based on keyword search with pagination
# def get_problems_by_keyword(keywords, offset=0, limit=5):
#     search_columns = ['Keywords(One word)', 'ASIC/Module']
#     problem_column = 'Problem'
    
#     # Match the query keywords in the 'Keywords' and 'ASIC/Module' columns
#     csv_data['match_score'] = csv_data[search_columns].apply(lambda row: sum(keyword in str(row).lower() for keyword in keywords), axis=1)
#     matched_problems = csv_data[csv_data['match_score'] > 0]  # Get matches
#     matched_problems = matched_problems.iloc[offset:offset + limit]  # Apply pagination

#     if not matched_problems.empty:
#         return matched_problems[problem_column].tolist()  # Return a list of problems
#     else:
#         return []

# # Function to get root cause and solution based on the selected problem
# def get_root_cause_and_solution(problem):
#     problem_row = csv_data[csv_data['Problem'] == problem]
#     if not problem_row.empty:
#         root_cause = problem_row['Root cause'].values[0]
#         solution = problem_row['Solution'].values[0]
#         return root_cause, solution
#     return None, None

# def query_csv(query):
#     keywords = clean_and_split_query(query)
#     st.session_state.last_keywords = keywords
#     problems = get_problems_by_keyword(keywords, offset=st.session_state.problem_offset)
    
#     if problems:
#         st.session_state.pending_feedback = True
#         return problems
#     else:
#         return "No problems found for the given keyword."

# # Detect greetings and inappropriate language
# def detect_greeting(query):
#     greetings = {
#         "hi": "Hello! How can I assist you today?",
#         "hello": "Hello! Have a great day.",
#         "hey": "Hello! How can I assist you today?",
#         "good morning": "Good morning! Have a nice day.",
#         "good afternoon": "Good afternoon! Have a great day.",
#         "good evening": "Good evening! Go and have snacks.",
#         "good night": "Good night! Sleep well."
#     }
#     for key, value in greetings.items():
#         if key in query.lower():
#             return value
#     return None

# def detect_inappropriate_language(query):
#     inappropriate_phrases = ["brutal", "badword", "i hate you", "fuck you", "i love you", "i want to marry you"]
#     return any(phrase in query.lower() for phrase in inappropriate_phrases)

# def get_response(query):
#     greeting_response = detect_greeting(query)
#     if greeting_response:
#         return greeting_response

#     if detect_inappropriate_language(query):
#         return "I didn't get you..."

#     if "problems" in query.lower() or "issues" in query.lower() or "difficulties" in query.lower():
#         problems = query_csv(query)
#         if isinstance(problems, list) and problems:
#             st.session_state.chat_history.append(AIMessage("Here are the top problems related to your query. Please select one:"))
#             return problems
#         return problems

#     return "What do you want to know about this?"

# # Sidebar
# st.sidebar.title("Search History")

# # Display conversation
# for message in st.session_state.chat_history:
#     if isinstance(message, HumanMessage):
#         with st.chat_message("Human"):
#             st.markdown(message.content)
#     else:
#         with st.chat_message("AI"):
#             st.markdown(message.content)

# # User input
# user_query = st.chat_input("Your message")
# if user_query:
#     st.session_state.chat_history.append(HumanMessage(user_query))

#     with st.chat_message("Human"):
#         st.markdown(user_query)

#     with st.chat_message("AI"):
#         ai_response = get_response(user_query)
#         if isinstance(ai_response, list):
#             # Display the problems as radio buttons
            
#             selected_problem = st.radio("Select a problem:", ai_response, key="problems_radio")
#             if selected_problem:
#                 st.session_state.selected_problem = selected_problem
#                 st.session_state.chat_history.append(AIMessage(f"Do you want the root cause and solution for '{selected_problem}'?"))
#                 st.session_state.pending_feedback = True

#             # Option to see more problems
#             if st.button("Show more problems"):
#                 st.session_state.problem_offset += 5
#                 more_problems = query_csv(user_query)
#                 st.write(more_problems)

#         else:
#             st.markdown(ai_response)
#             st.session_state.chat_history.append(AIMessage(ai_response))

# # Feedback section
# feedback_placeholder = st.empty()
# if st.session_state.pending_feedback and st.session_state.selected_problem:
#     with feedback_placeholder.container():
#         col1, col2 = st.columns([1, 1])
#         with col1:
#             if st.button("👍"):
#                 st.write("Here is the root cause and solution for the selected problem:")
#                 root_cause, solution = get_root_cause_and_solution(st.session_state.selected_problem)
#                 if root_cause and solution:
#                     st.markdown(f"**Root Cause:** {root_cause}")
#                     st.markdown(f"**Solution:** {solution}")
#                     st.session_state.chat_history.append(AIMessage(f"Root Cause: {root_cause}\nSolution: {solution}"))
#                 else:
#                     st.markdown("No root cause or solution found.")
#                 st.session_state.pending_feedback = False
#         with col2:
#             if st.button("👎"):
#                 st.write("Okay, no root cause and solution will be provided.")
#                 st.session_state.pending_feedback = False
# import streamlit as st
# import pandas as pd
# import re

# # Initialize session state variables
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
# if "search_history" not in st.session_state:
#     st.session_state.search_history = {}
# if "last_keywords" not in st.session_state:
#     st.session_state.last_keywords = []
# if "selected_problem" not in st.session_state:
#     st.session_state.selected_problem = None
# if "pending_feedback" not in st.session_state:
#     st.session_state.pending_feedback = False
# if "problem_offset" not in st.session_state:
#     st.session_state.problem_offset = 0

# # Set up the Streamlit app
# st.set_page_config(page_title="HitLit", page_icon="🤖", initial_sidebar_state="expanded")

# # Load the CSV file
# @st.cache_data
# def load_csv(file_path):
#     return pd.read_csv(file_path)

# # Replace with your CSV file path
# csv_file_path = r"\\kor2fs03\V-V--Testing$\03_Validation_Software\LLBP\VALSW_LL_BP_SPL_V1.1.csv"
# csv_data = load_csv(csv_file_path)

# def clean_and_split_query(query):
#     filler_words = {'um', 'like', 'you', 'know', 'so', 'well', 'actually', 'basically', 'just', 'really'}
#     stop_words = {'is', 'are', 'was', 'were', 'what', 'who', 'how', 'where', 'when', 'why',
#                   'i', 'me', 'you', 'his', 'her', 'ok', 'bye', 'i am sorry', 'it is what it is', 'it','is','on','over','under','inside','an','a','the', 'does','con',
#                   'get', 'got', 'have', 'had', 'has', 'should', 'not', 'use', 'mobile','team','Team','Verdict','an','no','not','but','T','15','with','off'}
#     cleaned_query = re.sub(r'[^\w\s]', '', query)
#     words = cleaned_query.lower().split()
#     filtered_words = [word for word in words if word not in filler_words and word not in stop_words]
#     return filtered_words

# # Function to get problems based on keyword search
# def get_problems_by_keyword(keywords):
#     search_columns = ['Keywords(One word)', 'ASIC/Module']
#     problem_column = 'Problem'
    
#     # Match the query keywords in the 'Keywords' and 'ASIC/Module' columns
#     csv_data['match_score'] = csv_data[search_columns].apply(lambda row: sum(keyword in str(row).lower() for keyword in keywords), axis=1)
#     matched_problems = csv_data[csv_data['match_score'] > 0]  # Get matches

#     if not matched_problems.empty:
#         return matched_problems[problem_column].tolist()  # Return a list of problems
#     else:
#         return []

# # Function to get root cause and solution based on the selected problem
# def get_root_cause_and_solution(problem):
#     problem_row = csv_data[csv_data['Problem'] == problem]
#     if not problem_row.empty:
#         root_cause = problem_row['Root cause'].values[0]
#         solution = problem_row['Solution'].values[0]
#         return root_cause, solution
#     return None, None

# def query_csv(query):
#     keywords = clean_and_split_query(query)
#     st.session_state.last_keywords = keywords
#     problems = get_problems_by_keyword(keywords)
    
#     if problems:
#         st.session_state.pending_feedback = True
#         return problems
#     else:
#         return "No problems found for the given keyword."

# # Detect greetings and inappropriate language
# def detect_greeting(query):
#     greetings = {
#         "hi": "Hello! How can I assist you today?",
#         "hello": "Hello! Have a great day.",
#         "hey": "Hello! How can I assist you today?",
#         "good morning": "Good morning! Have a nice day.",
#         "good afternoon": "Good afternoon! Have a great day.",
#         "good evening": "Good evening! Go and have snacks.",
#         "good night": "Good night! Sleep well."
#     }
#     for key, value in greetings.items():
#         if key in query.lower():
#             return value
#     return None

# def detect_inappropriate_language(query):
#     inappropriate_phrases = ["brutal", "badword", "i hate you", "fuck you", "i love you", "i want to marry you"]
#     return any(phrase in query.lower() for phrase in inappropriate_phrases)

# def get_response(query):
#     greeting_response = detect_greeting(query)
#     if greeting_response:
#         return greeting_response

#     if detect_inappropriate_language(query):
#         return "I didn't get you..."

#     if "problems" in query.lower() or "issues" in query.lower() or "difficulties" in query.lower():
#         problems = query_csv(query)
#         if isinstance(problems, list) and problems:
#             st.session_state.chat_history.append(f"Here are the top problems related to your query. Please select one:")
#             return problems
#         return problems

#     return "What do you want to know about this?"

# # Sidebar
# st.sidebar.title("Search History")

# # Display conversation
# for message in st.session_state.chat_history:
#     st.write(message)

# # User input
# user_query = st.text_input("Your message")
# if user_query:
#     st.session_state.chat_history.append(user_query)

#     ai_response = get_response(user_query)

#     if isinstance(ai_response, list) and ai_response:
#         # Display the problems as radio buttons
#         selected_problem = st.radio("Select a problem:", options=ai_response, index=0)  # Default selection to first problem
        
#         # Update selected problem
#         st.session_state.selected_problem = selected_problem
        
#         # Ask for feedback after selection
#         st.session_state.chat_history.append(f"Do you want the root cause and solution for '{selected_problem}'?")

#         # Option to get root cause and solution
#         if st.button("Get Root Cause and Solution"):
#             root_cause, solution = get_root_cause_and_solution(selected_problem)
#             if root_cause and solution:
#                 st.write(f"**Root Cause:** {root_cause}")
#                 st.write(f"**Solution:** {solution}")
#                 st.session_state.chat_history.append(f"Root Cause: {root_cause}\nSolution: {solution}")
#             else:
#                 st.write("No root cause or solution found.")
#                 st.session_state.chat_history.append("No root cause or solution found.")

#     else:
#         st.write(ai_response)
#         st.session_state.chat_history.append(ai_response)

# import streamlit as st
# import pandas as pd
# import re

# # Initialize session state variables
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
# if "search_history" not in st.session_state:
#     st.session_state.search_history = {}
# if "last_keywords" not in st.session_state:
#     st.session_state.last_keywords = []
# if "selected_problem" not in st.session_state:
#     st.session_state.selected_problem = None
# if "pending_feedback" not in st.session_state:
#     st.session_state.pending_feedback = False
# if "problem_offset" not in st.session_state:
#     st.session_state.problem_offset = 0

# # Set up the Streamlit app
# st.set_page_config(page_title="HitLit", page_icon="🤖", initial_sidebar_state="expanded")

# # Load the CSV file
# @st.cache_data
# def load_csv(file_path):
#     return pd.read_csv(file_path)

# # Replace with your CSV file path
# csv_file_path = r"\\kor2fs03\V-V--Testing$\03_Validation_Software\LLBP\VALSW_LL_BP_SPL_V1.1.csv"
# csv_data = load_csv(csv_file_path)

# def clean_and_split_query(query):
#     filler_words = {'um', 'like', 'you', 'know', 'so', 'well', 'actually', 'basically', 'just', 'really'}
#     stop_words = {'is', 'are', 'was', 'were', 'what', 'who', 'how', 'where', 'when', 'why',
#                   'i', 'me', 'you', 'his', 'her', 'ok', 'bye', 'i am sorry', 'it is what it is', 'it','is','on','over','under','inside','an','a','the', 'does','con',
#                   'get', 'got', 'have', 'had', 'has', 'should', 'not', 'use', 'mobile','team','Team','Verdict','an','no','not','but','T','15','with','off'}
#     cleaned_query = re.sub(r'[^\w\s]', '', query)
#     words = cleaned_query.lower().split()
#     filtered_words = [word for word in words if word not in filler_words and word not in stop_words]
#     return filtered_words

# # Function to get problems based on keyword search
# def get_problems_by_keyword(keywords):
#     search_columns = ['Keywords(One word)', 'ASIC/Module']
#     problem_column = 'Problem'
    
#     # Match the query keywords in the 'Keywords' and 'ASIC/Module' columns
#     csv_data['match_score'] = csv_data[search_columns].apply(lambda row: sum(keyword in str(row).lower() for keyword in keywords), axis=1)
#     matched_problems = csv_data[csv_data['match_score'] > 0]  # Get matches

#     if not matched_problems.empty:
#         return matched_problems[problem_column].tolist()  # Return a list of problems
#     else:
#         return []

# # Function to get root cause and solution based on the selected problem
# def get_root_cause_and_solution(problem):
#     problem_row = csv_data[csv_data['Problem'] == problem]
#     if not problem_row.empty:
#         root_cause = problem_row['Root cause'].values[0]
#         solution = problem_row['Solution'].values[0]
#         return root_cause, solution
#     return None, None

# def query_csv(query):
#     keywords = clean_and_split_query(query)
#     st.session_state.last_keywords = keywords
#     problems = get_problems_by_keyword(keywords)
    
#     if problems:
#         st.session_state.pending_feedback = True
#         return problems
#     else:
#         return "No problems found for the given keyword."

# # Detect greetings and inappropriate language
# def detect_greeting(query):
#     greetings = {
#         "hi": "Hello! How can I assist you today?",
#         "hello": "Hello! Have a great day.",
#         "hey": "Hello! How can I assist you today?",
#         "good morning": "Good morning! Have a nice day.",
#         "good afternoon": "Good afternoon! Have a great day.",
#         "good evening": "Good evening! Go and have snacks.",
#         "good night": "Good night! Sleep well."
#     }
#     for key, value in greetings.items():
#         if key in query.lower():
#             return value
#     return None

# def detect_inappropriate_language(query):
#     inappropriate_phrases = ["brutal", "badword", "i hate you", "fuck you", "i love you", "i want to marry you"]
#     return any(phrase in query.lower() for phrase in inappropriate_phrases)

# def get_response(query):
#     greeting_response = detect_greeting(query)
#     if greeting_response:
#         return greeting_response

#     if detect_inappropriate_language(query):
#         return "I didn't get you..."

#     if "problems" in query.lower() or "issues" in query.lower() or "difficulties" in query.lower():
#         problems = query_csv(query)
#         if isinstance(problems, list) and problems:
#             st.session_state.chat_history.append(f"Here are the top problems related to your query. Please select one:")
#             return problems
#         return problems

#     return "What do you want to know about this?"

# # Sidebar
# st.sidebar.title("Search History")

# # Display conversation
# for message in st.session_state.chat_history:
#     st.write(message)

# # Clear chat button
# if st.button("Clear Chat"):
#     st.session_state.chat_history = []
#     st.session_state.last_keywords = []
#     st.session_state.selected_problem = None
#     st.session_state.pending_feedback = False
#     st.session_state.problem_offset = 0

# # User input at the bottom
# st.text_input("Your message", key="user_input")

# if st.session_state.user_input:
#     user_query = st.session_state.user_input
#     st.session_state.chat_history.append(user_query)

#     ai_response = get_response(user_query)

#     if isinstance(ai_response, list) and ai_response:
#         # Display the problems as radio buttons
#         selected_problem = st.radio("Select a problem:", options=ai_response, index=0)  # Default selection to first problem
        
#         # Update selected problem
#         st.session_state.selected_problem = selected_problem
        
#         # Ask for feedback after selection
#         st.session_state.chat_history.append(f"Do you want the root cause and solution for '{selected_problem}'?")

#         # Option to get root cause and solution
#         if st.button("Get Root Cause and Solution"):
#             root_cause, solution = get_root_cause_and_solution(selected_problem)
#             if root_cause and solution:
#                 st.write(f"**Root Cause:** {root_cause}")
#                 st.write(f"**Solution:** {solution}")
#                 st.session_state.chat_history.append(f"Root Cause: {root_cause}\nSolution: {solution}")
#             else:
#                 st.write("No root cause or solution found.")
#                 st.session_state.chat_history.append("No root cause or solution found.")

#     else:
#         st.write(ai_response)
#         st.session_state.chat_history.append(ai_response)

# import streamlit as st
# import pandas as pd
# import re

# # Initialize session state variables
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
# if "last_keywords" not in st.session_state:
#     st.session_state.last_keywords = []
# if "selected_problem" not in st.session_state:
#     st.session_state.selected_problem = None
# if "pending_feedback" not in st.session_state:
#     st.session_state.pending_feedback = False

# # Set up the Streamlit app
# st.set_page_config(page_title="HitLit", page_icon="🤖", initial_sidebar_state="expanded")

# # Load the CSV file
# @st.cache_data
# def load_csv(file_path):
#     return pd.read_csv(file_path)

# # Replace with your CSV file path
# csv_file_path = r"\\kor2fs03\V-V--Testing$\03_Validation_Software\LLBP\VALSW_LL_BP_SPL_V1.1.csv"
# csv_data = load_csv(csv_file_path)

# def clean_and_split_query(query):
#     filler_words = {'um', 'like', 'you', 'know', 'so', 'well', 'actually', 'basically', 'just', 'really'}
#     stop_words = {'is', 'are', 'was', 'were', 'what', 'who', 'how', 'where', 'when', 'why',
#                   'i', 'me', 'you', 'his', 'her', 'ok', 'bye', 'i am sorry', 'it is what it is', 'it','is','on','over','under','inside','an','a','the', 'does','con',
#                   'get', 'got', 'have', 'had', 'has', 'should', 'not', 'use', 'mobile','team','Team','Verdict','an','no','not','but','T','15','with','off'}
#     cleaned_query = re.sub(r'[^\w\s]', '', query)
#     words = cleaned_query.lower().split()
#     filtered_words = [word for word in words if word not in filler_words and word not in stop_words]
#     return filtered_words

# # Function to get problems based on keyword search
# def get_problems_by_keyword(keywords):
#     search_columns = ['Keywords(One word)', 'ASIC/Module']
#     problem_column = 'Problem'
    
#     # Match the query keywords in the 'Keywords' and 'ASIC/Module' columns
#     csv_data['match_score'] = csv_data[search_columns].apply(lambda row: sum(keyword in str(row).lower() for keyword in keywords), axis=1)
#     matched_problems = csv_data[csv_data['match_score'] > 0]  # Get matches

#     if not matched_problems.empty:
#         return matched_problems[problem_column].tolist()  # Return a list of problems
#     else:
#         return []

# # Function to get root cause and solution based on the selected problem
# def get_root_cause_and_solution(problem):
#     problem_row = csv_data[csv_data['Problem'] == problem]
#     if not problem_row.empty:
#         root_cause = problem_row['Root cause'].values[0]
#         solution = problem_row['Solution'].values[0]
#         return root_cause, solution
#     return None, None

# def query_csv(query):
#     keywords = clean_and_split_query(query)
#     st.session_state.last_keywords = keywords
#     problems = get_problems_by_keyword(keywords)
    
#     if problems:
#         st.session_state.pending_feedback = True
#         return problems
#     else:
#         return "No problems found for the given keyword."

# # Detect greetings and inappropriate language
# def detect_greeting(query):
#     greetings = {
#         "hi": "Hello! How can I assist you today?",
#         "hello": "Hello! Have a great day.",
#         "hey": "Hello! How can I assist you today?",
#         "good morning": "Good morning! Have a nice day.",
#         "good afternoon": "Good afternoon! Have a great day.",
#         "good evening": "Good evening! Go and have snacks.",
#         "good night": "Good night! Sleep well."
#     }
#     for key, value in greetings.items():
#         if key in query.lower():
#             return value
#     return None

# def detect_inappropriate_language(query):
#     inappropriate_phrases = ["brutal", "badword", "i hate you", "fuck you", "i love you", "i want to marry you"]
#     return any(phrase in query.lower() for phrase in inappropriate_phrases)

# def get_response(query):
#     greeting_response = detect_greeting(query)
#     if greeting_response:
#         return greeting_response

#     if detect_inappropriate_language(query):
#         return "I didn't get you..."

#     if "problems" in query.lower() or "issues" in query.lower() or "difficulties" in query.lower():
#         problems = query_csv(query)
#         if isinstance(problems, list) and problems:
#             st.session_state.chat_history.append(f"Here are the top problems related to your query. Please select one:")
#             return problems
#         return problems

#     return "What do you want to know about this?"

# # Sidebar
# st.sidebar.title("Search History")

# # Display conversation
# for message in st.session_state.chat_history:
#     st.write(message)

# # Clear chat button
# if st.button("Clear Chat"):
#     # Reset all session state variables related to the chat
#     st.session_state.chat_history = []
#     st.session_state.last_keywords = []
#     st.session_state.selected_problem = None
#     st.session_state.pending_feedback = False

# # User input at the bottom
# user_input = st.text_input("Your message", key="user_input")

# if user_input:
#     st.session_state.chat_history.append(user_input)
    
#     ai_response = get_response(user_input)

#     if isinstance(ai_response, list) and ai_response:
#         # Display the problems as radio buttons
#         selected_problem = st.radio("Select a problem:", options=ai_response, index=0)  # Default selection to first problem
        
#         # Update selected problem
#         st.session_state.selected_problem = selected_problem
        
#         # Ask for feedback after selection
#         st.session_state.chat_history.append(f"Do you want the root cause and solution for '{selected_problem}'?")

#         # Option to get root cause and solution
#         if st.button("Get Root Cause and Solution"):
#             root_cause, solution = get_root_cause_and_solution(selected_problem)
#             if root_cause and solution:
#                 st.write(f"**Root Cause:** {root_cause}")
#                 st.write(f"**Solution:** {solution}")
#                 st.session_state.chat_history.append(f"Root Cause: {root_cause}\nSolution: {solution}")
#             else:
#                 st.write("No root cause or solution found.")
#                 st.session_state.chat_history.append("No root cause or solution found.")
#     else:
#         st.write(ai_response)
#         st.session_state.chat_history.append(ai_response)

# import streamlit as st
# import pandas as pd
# import re

# # Initialize session state variables
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
# if "last_keywords" not in st.session_state:
#     st.session_state.last_keywords = []
# if "selected_problem" not in st.session_state:
#     st.session_state.selected_problem = None
# if "pending_feedback" not in st.session_state:
#     st.session_state.pending_feedback = False

# # Set up the Streamlit app
# st.set_page_config(page_title="HitLit", page_icon="🤖", initial_sidebar_state="expanded")

# # Load the CSV file
# @st.cache_data
# def load_csv(file_path):
#     return pd.read_csv(file_path)

# # Replace with your CSV file path
# csv_file_path = r"\\kor2fs03\V-V--Testing$\03_Validation_Software\LLBP\VALSW_LL_BP_SPL_V1.1.csv"
# csv_data = load_csv(csv_file_path)

# def clean_and_split_query(query):
#     filler_words = {'um', 'like', 'you', 'know', 'so', 'well', 'actually', 'basically', 'just', 'really'}
#     stop_words = {'is', 'are', 'was', 'were', 'what', 'who', 'how', 'where', 'when', 'why',
#                   'i', 'me', 'you', 'his', 'her', 'ok', 'bye', 'i am sorry', 'it is what it is', 'it','is','on','over','under','inside','an','a','the', 'does','con',
#                   'get', 'got', 'have', 'had', 'has', 'should', 'not', 'use', 'mobile','team','Team','Verdict','an','no','not','but','T','15','with','off','issues','issue','is','in','the','problems','are','what','why','when','flt','flashing'}
#     cleaned_query = re.sub(r'[^\w\s]', '', query)
#     words = cleaned_query.lower().split()
#     filtered_words = [word for word in words if word not in filler_words and word not in stop_words]
#     return filtered_words

# # Function to get problems based on keyword search
# def get_problems_by_keyword(keywords):
#     search_columns = ['Keywords(One word)', 'ASIC/Module']
#     problem_column = 'Problem'
    
#     # Match the query keywords in the 'Keywords' and 'ASIC/Module' columns
#     matched_problems = pd.DataFrame()
#     for keyword in keywords:
#         matches = csv_data[csv_data[search_columns].apply(lambda row: row.astype(str).str.contains(keyword, case=False).any(), axis=1)]
#         matched_problems = pd.concat([matched_problems, matches])

#     matched_problems = matched_problems.drop_duplicates()
    
#     if not matched_problems.empty:
#         return matched_problems[problem_column].tolist()  # Return a list of problems
#     else:
#         return []

# # Function to get root cause and solution based on the selected problem
# def get_root_cause_and_solution(problem):
#     problem_row = csv_data[csv_data['Problem'] == problem]
#     if not problem_row.empty:
#         root_cause = problem_row['Root cause'].values[0]
#         solution = problem_row['Solution'].values[0]
#         return root_cause, solution
#     return None, None

# def query_csv(query):
#     keywords = clean_and_split_query(query)
#     st.session_state.last_keywords = keywords
#     problems = get_problems_by_keyword(keywords)
    
#     if problems:
#         st.session_state.pending_feedback = True
#         return problems
#     else:
#         return "No problems found for the given keyword."

# # Detect greetings and inappropriate language
# def detect_greeting(query):
#     greetings = {
#         "hi": "Hello! How can I assist you today?",
#         "hello": "Hello! Have a great day.",
#         "hey": "Hello! How can I assist you today?",
#         "good morning": "Good morning! Have a nice day.",
#         "good afternoon": "Good afternoon! Have a great day.",
#         "good evening": "Good evening! Go and have snacks.",
#         "good night": "Good night! Sleep well."
#     }
#     for key, value in greetings.items():
#         if key in query.lower():
#             return value
#     return None

# def detect_inappropriate_language(query):
#     inappropriate_phrases = ["brutal", "badword", "i hate you", "fuck you", "i love you", "i want to marry you"]
#     return any(phrase in query.lower() for phrase in inappropriate_phrases)

# # Function to get problems based on keyword search
# def get_problems_by_keyword(keywords):
#     search_columns = ['Keywords(One word)', 'ASIC/Module']
#     problem_column = 'Problem'
    
#     # Match the query keywords in the 'Keywords' and 'ASIC/Module' columns
#     matched_problems = pd.DataFrame()
#     for keyword in keywords:
#         matches = csv_data[csv_data[search_columns].apply(lambda row: row.astype(str).str.contains(keyword, case=False).any(), axis=1)]
#         matched_problems = pd.concat([matched_problems, matches])

#     matched_problems = matched_problems.drop_duplicates()
    
#     if not matched_problems.empty:
#         return matched_problems[problem_column].dropna().astype(str).tolist()  # Convert to string and return a list of problems
#     else:
#         return []

# # Modify get_response function for better type handling
# def get_response(query):
#     greeting_response = detect_greeting(query)
#     if greeting_response:
#         return greeting_response

#     if detect_inappropriate_language(query):
#         return "I didn't get you..."

#     if "problems" in query.lower() or "issues" in query.lower():
#         problems = query_csv(query)
#         if isinstance(problems, list) and problems:
#             st.session_state.pending_feedback = True
#             return problems
#         return "No problems found for the given keyword."

#     return "What do you want to know about this?"

# # Clear chat button logic
# if st.button("Clear Chat"):
#     # Reset all session state variables related to the chat
#     st.session_state.chat_history = []
#     st.session_state.last_keywords = []
#     st.session_state.selected_problem = None
#     st.session_state.pending_feedback = False

# # User input at the bottom
# user_input = st.text_input("Your message", key="user_input")

# if user_input:
#     st.session_state.chat_history.append(user_input)
    
#     ai_response = get_response(user_input)

#     if isinstance(ai_response, list) and ai_response:
#         # Ensure all problems are strings
#         ai_response = [str(problem) for problem in ai_response]
        
#         # Display the problems as radio buttons
#         selected_problem = st.radio("Select a problem:", options=ai_response, index=0)  # Default selection to first problem
        
#         # Update selected problem
#         st.session_state.selected_problem = selected_problem
        
#         # Ask for feedback after selection
#         st.session_state.chat_history.append(f"Do you want the root cause and solution for '{selected_problem}'?")

#         # Option to get root cause and solution
#         if st.button("Get Root Cause and Solution"):
#             root_cause, solution = get_root_cause_and_solution(selected_problem)
#             if root_cause and solution:
#                 st.write(f"**Root Cause:** {root_cause}")
#                 st.write(f"**Solution:** {solution}")
#                 st.session_state.chat_history.append(f"Root Cause: {root_cause}\nSolution: {solution}")
#             else:
#                 st.write("No root cause or solution found.")
#                 st.session_state.chat_history.append("No root cause or solution found.")
#     else:
#         st.write(ai_response)
#         st.session_state.chat_history.append(ai_response)

# import streamlit as st
# import pandas as pd
# import re

# # Initialize session state variables
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
# if "search_history" not in st.session_state:
#     st.session_state.search_history = {}
# if "last_keywords" not in st.session_state:
#     st.session_state.last_keywords = []
# if "selected_problem" not in st.session_state:
#     st.session_state.selected_problem = None
# if "pending_feedback" not in st.session_state:
#     st.session_state.pending_feedback = False

# # Set up the Streamlit app
# st.set_page_config(page_title="HitLit", page_icon="🤖", initial_sidebar_state="expanded")

# # Load the CSV file
# @st.cache_data
# def load_csv(file_path):
#     return pd.read_csv(file_path)

# # Replace with your CSV file path
# csv_file_path = r"\\kor2fs03\V-V--Testing$\03_Validation_Software\LLBP\VALSW_LL_BP_SPL_V1.1.csv"
# csv_data = load_csv(csv_file_path)

# def clean_and_split_query(query):
#     filler_words = {'um', 'like', 'you', 'know', 'so', 'well', 'actually', 'basically', 'just', 'really'}
#     stop_words = {'is', 'are', 'was', 'were', 'what', 'who', 'how', 'where', 'when', 'why',
#                   'i', 'me', 'you', 'his', 'her', 'ok', 'bye', 'i am sorry', 'it is what it is', 'it','is','on','over','under','inside','an','a','the', 'does','con',
#                   'get', 'got', 'have', 'had', 'has', 'should', 'not', 'use', 'mobile','team','Team','Verdict','an','no','not','but','T','15','with','off'}
#     cleaned_query = re.sub(r'[^\w\s]', '', query)
#     words = cleaned_query.lower().split()
#     filtered_words = [word for word in words if word not in filler_words and word not in stop_words]
#     return filtered_words

# # Function to get problems based on keyword search
# def get_problems_by_keyword(keywords):
#     search_columns = ['Keywords(One word)', 'ASIC/Module']
#     problem_column = 'Problem'
    
#     # Prepare a boolean mask to filter rows
#     mask = pd.Series([False] * len(csv_data))

#     for keyword in keywords:
#         # Check for matches in both columns
#         matches = csv_data[search_columns].apply(lambda row: row.astype(str).str.contains(keyword, case=False).any(), axis=1)
#         mask = mask | matches  # Update the mask to include matches

#     matched_problems = csv_data[mask]  # Get rows that matched the keywords

#     if not matched_problems.empty:
#         return matched_problems[problem_column].dropna().astype(str).tolist()  # Convert to string and return a list of problems
#     else:
#         return []

# # Detect greetings and inappropriate language
# def detect_greeting(query):
#     greetings = {
#         "hi": "Hello! How can I assist you today?",
#         "hello": "Hello! Have a great day.",
#         "hey": "Hello! How can I assist you today?",
#         "good morning": "Good morning! Have a nice day.",
#         "good afternoon": "Good afternoon! Have a great day.",
#         "good evening": "Good evening! Go and have snacks.",
#         "good night": "Good night! Sleep well."
#     }
#     for key, value in greetings.items():
#         if key in query.lower():
#             return value
#     return None

# def detect_inappropriate_language(query):
#     inappropriate_phrases = ["brutal", "badword", "i hate you", "fuck you", "i love you", "i want to marry you"]
#     return any(phrase in query.lower() for phrase in inappropriate_phrases)

# def get_response(query):
#     greeting_response = detect_greeting(query)
#     if greeting_response:
#         return greeting_response

#     if detect_inappropriate_language(query):
#         return "I didn't get you..."

#     if "problems" in query.lower() or "issues" in query.lower() or "difficulties" in query.lower():
#         keywords = clean_and_split_query(query)  # Clean and split the query into keywords
#         problems = get_problems_by_keyword(keywords)
#         if problems:
#             st.session_state.pending_feedback = True
#             return problems
#         return "No problems found for the given keyword."

#     return "What do you want to know about this?"

# # Clear chat button logic
# if st.button("Clear Chat"):
#     # Reset all session state variables related to the chat
#     st.session_state.chat_history = []
#     st.session_state.last_keywords = []
#     st.session_state.selected_problem = None
#     st.session_state.pending_feedback = False

# # Sidebar
# st.sidebar.title("Search History")

# # Display conversation
# for message in st.session_state.chat_history:
#     st.write(message)

# # User input at the bottom
# user_query = st.text_input("Your message", key="user_input")

# if user_query:
#     st.session_state.chat_history.append(user_query)

#     ai_response = get_response(user_query)

#     if isinstance(ai_response, list) and ai_response:
#         # Ensure all problems are strings
#         ai_response = [str(problem) for problem in ai_response]
        
#         # Display the problems as radio buttons
#         selected_problem = st.radio("Select a problem:", options=ai_response, index=0)  # Default selection to first problem
        
#         # Update selected problem
#         st.session_state.selected_problem = selected_problem
        
#         # Ask for feedback after selection
#         st.session_state.chat_history.append(f"Do you want the root cause and solution for '{selected_problem}'?")

#         # Option to get root cause and solution
#         if st.button("Get Root Cause and Solution"):
#             root_cause, solution = get_root_cause_and_solution(selected_problem)
#             if root_cause and solution:
#                 st.write(f"**Root Cause:** {root_cause}")
#                 st.write(f"**Solution:** {solution}")
#                 st.session_state.chat_history.append(f"Root Cause: {root_cause}\nSolution: {solution}")
#             else:
#                 st.write("No root cause or solution found.")
#                 st.session_state.chat_history.append("No root cause or solution found.")

#     else:
#         st.write(ai_response)
#         st.session_state.chat_history.append(ai_response)

# import streamlit as st
# import pandas as pd
# import re

# # Initialize session state variables
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
# if "search_history" not in st.session_state:
#     st.session_state.search_history = {}
# if "last_keywords" not in st.session_state:
#     st.session_state.last_keywords = []
# if "selected_problem" not in st.session_state:
#     st.session_state.selected_problem = None
# if "pending_feedback" not in st.session_state:
#     st.session_state.pending_feedback = False

# # Set up the Streamlit app
# st.set_page_config(page_title="HitLit", page_icon="🤖", initial_sidebar_state="expanded")

# # Load the CSV file
# @st.cache_data
# def load_csv(file_path):
#     return pd.read_csv(file_path)

# # Replace with your CSV file path
# csv_file_path = r"\\kor2fs03\V-V--Testing$\03_Validation_Software\LLBP\VALSW_LL_BP_SPL_V1.1.csv"
# csv_data = load_csv(csv_file_path)

# def clean_and_split_query(query):
#     filler_words = {'um', 'like', 'you', 'know', 'so', 'well', 'actually', 'basically', 'just', 'really'}
#     stop_words = {'is', 'are', 'was', 'were', 'what', 'who', 'how', 'where', 'when', 'why',
#                   'i', 'me', 'you', 'his', 'her', 'ok', 'bye', 'i am sorry', 'it is what it is', 'it','is','on','over','under','inside','an','a','the', 'does','con',
#                   'get', 'got', 'have', 'had', 'has', 'should', 'not', 'use', 'mobile','team','Team','Verdict','an','no','not','but','T','15','with','off','issues','in','problems','are','the','what'}
#     cleaned_query = re.sub(r'[^\w\s]', '', query)
#     words = cleaned_query.lower().split()
#     filtered_words = [word for word in words if word not in filler_words and word not in stop_words]
#     return filtered_words

# # Function to get problems based on keyword search
# def get_problems_by_keyword(keywords):
#     search_columns = ['Keywords(One word)', 'ASIC/Module']
#     problem_column = 'Problem'
    
#     # Prepare a boolean mask to filter rows
#     mask = pd.Series([False] * len(csv_data))

#     for keyword in keywords:
#         # Check for matches in both columns
#         matches = csv_data[search_columns].apply(lambda row: row.astype(str).str.contains(keyword, case=False).any(), axis=1)
#         mask = mask | matches  # Update the mask to include matches

#     matched_problems = csv_data[mask]  # Get rows that matched the keywords

#     if not matched_problems.empty:
#         return matched_problems[problem_column].dropna().astype(str).tolist()  # Convert to string and return a list of problems
#     else:
#         return []

# # Function to get root cause and solution for the selected problem
# def get_root_cause_and_solution(selected_problem):
#     root_cause_column = 'Root Cause'
#     solution_column = 'Solution'
    
#     # Check if the selected problem exists in the CSV data
#     matched_rows = csv_data[csv_data['Problem'].str.contains(selected_problem, case=False, na=False)]

#     if not matched_rows.empty:
#         root_causes = matched_rows[root_cause_column].dropna().unique()  # Get unique root causes
#         solutions = matched_rows[solution_column].dropna().unique()  # Get unique solutions
        
#         if root_causes.size > 0 and solutions.size > 0:
#             return root_causes[0], solutions[0]  # Return the first root cause and solution found
#         else:
#             return None, None  # Return None if no root cause or solution found
#     return None, None

# # Detect greetings and inappropriate language
# def detect_greeting(query):
#     greetings = {
#         "hi": "Hello! How can I assist you today?",
#         "hello": "Hello! Have a great day.",
#         "hey": "Hello! How can I assist you today?",
#         "good morning": "Good morning! Have a nice day.",
#         "good afternoon": "Good afternoon! Have a great day.",
#         "good evening": "Good evening! Go and have snacks.",
#         "good night": "Good night! Sleep well."
#     }
#     for key, value in greetings.items():
#         if key in query.lower():
#             return value
#     return None

# def detect_inappropriate_language(query):
#     inappropriate_phrases = ["brutal", "badword", "i hate you", "fuck you", "i love you", "i want to marry you"]
#     return any(phrase in query.lower() for phrase in inappropriate_phrases)

# def get_response(query):
#     greeting_response = detect_greeting(query)
#     if greeting_response:
#         return greeting_response

#     if detect_inappropriate_language(query):
#         return "I didn't get you..."

#     if "problems" in query.lower() or "issues" in query.lower() or "difficulties" in query.lower():
#         keywords = clean_and_split_query(query)  # Clean and split the query into keywords
#         problems = get_problems_by_keyword(keywords)
#         if problems:
#             st.session_state.pending_feedback = True
#             return problems
#         return "No problems found for the given keyword."

#     return "What do you want to know about this?"

# # Clear chat button logic
# if st.button("Clear Chat"):
#     # Reset all session state variables related to the chat
#     st.session_state.chat_history = []
#     st.session_state.last_keywords = []
#     st.session_state.selected_problem = None
#     st.session_state.pending_feedback = False

# # Sidebar
# st.sidebar.title("Search History")

# # Display conversation
# for message in st.session_state.chat_history:
#     st.write(message)

# # User input at the bottom
# user_query = st.text_input("Your message", key="user_input")

# if user_query:
#     st.session_state.chat_history.append(user_query)

#     ai_response = get_response(user_query)

#     if isinstance(ai_response, list) and ai_response:
#         # Ensure all problems are strings
#         ai_response = [str(problem) for problem in ai_response]
        
#         # Display the problems as radio buttons
#         selected_problem = st.radio("Select a problem:", options=ai_response, index=0)  # Default selection to first problem
        
#         # Update selected problem
#         st.session_state.selected_problem = selected_problem
        
#         # Ask for feedback after selection
#         st.session_state.chat_history.append(f"Do you want the root cause and solution for '{selected_problem}'?")

#         # Option to get root cause and solution
#         if st.button("Get Root Cause and Solution"):
#             root_cause, solution = get_root_cause_and_solution(selected_problem)
#             if root_cause and solution:
#                 st.write(f"**Root Cause:** {root_cause}")
#                 st.write(f"**Solution:** {solution}")
#                 st.session_state.chat_history.append(f"Root Cause: {root_cause}\nSolution: {solution}")
#             else:
#                 st.write("No root cause or solution found.")
#                 st.session_state.chat_history.append("No root cause or solution found.")

#     else:
#         st.write(ai_response)
#         st.session_state.chat_history.append(ai_response)


# import streamlit as st
# import pandas as pd
# import re

# # Initialize session state variables
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
# if "last_keywords" not in st.session_state:
#     st.session_state.last_keywords = []
# if "selected_problem" not in st.session_state:
#     st.session_state.selected_problem = None
# if "pending_feedback" not in st.session_state:
#     st.session_state.pending_feedback = False

# # Set up the Streamlit app
# st.set_page_config(page_title="HitLit", page_icon="🤖", initial_sidebar_state="expanded")

# # Load the CSV file
# @st.cache_data
# def load_csv(file_path):
#     return pd.read_csv(file_path)

# # Replace with your CSV file path
# csv_file_path = r"\\kor2fs03\V-V--Testing$\03_Validation_Software\LLBP\VALSW_LL_BP_SPL_V1.1.csv"
# csv_data = load_csv(csv_file_path)

# def clean_and_split_query(query):
#     filler_words = {'um', 'like', 'you', 'know', 'so', 'well', 'actually', 'basically', 'just', 'really'}
#     stop_words = {'is', 'are', 'was', 'were', 'what', 'who', 'how', 'where', 'when', 'why',
#                   'i', 'me', 'you', 'his', 'her', 'ok', 'bye', 'i am sorry', 'it is what it is', 'it','is','on','over','under','inside','an','a','the', 'does','con',
#                   'get', 'got', 'have', 'had', 'has', 'should', 'not', 'use', 'mobile','team','Team','Verdict','an','no','not','but','T','15','with','off','issues','issue','is','in','the','problems','are','what','why','when','flt','flashing'}
#     cleaned_query = re.sub(r'[^\w\s]', '', query)
#     words = cleaned_query.lower().split()
#     filtered_words = [word for word in words if word not in filler_words and word not in stop_words]
#     return filtered_words

# # Function to get problems based on keyword search
# def get_problems_by_keyword(keywords):
#     search_columns = ['Keywords(One word)', 'ASIC/Module']
#     problem_column = 'Problem'
    
#     # Match the query keywords in the 'Keywords' and 'ASIC/Module' columns
#     matched_problems = pd.DataFrame()
#     for keyword in keywords:
#         matches = csv_data[csv_data[search_columns].apply(lambda row: row.astype(str).str.contains(keyword, case=False).any(), axis=1)]
#         matched_problems = pd.concat([matched_problems, matches])

#     matched_problems = matched_problems.drop_duplicates()
    
#     if not matched_problems.empty:
#         return matched_problems[problem_column].tolist()  # Return a list of problems
#     else:
#         return []

# # Function to get root cause and solution based on the selected problem
# def get_root_cause_and_solution(problem):
#     problem_row = csv_data[csv_data['Problem'] == problem]
#     if not problem_row.empty:
#         root_cause = problem_row['Root cause'].values[0]
#         solution = problem_row['Solution'].values[0]
#         return root_cause, solution
#     return None, None

# def query_csv(query):
#     keywords = clean_and_split_query(query)
#     st.session_state.last_keywords = keywords
#     problems = get_problems_by_keyword(keywords)
    
#     if problems:
#         st.session_state.pending_feedback = True
#         return problems
#     else:
#         return "No problems found for the given keyword."

# # Detect greetings and inappropriate language
# def detect_greeting(query):
#     greetings = {
#         "hi": "Hello! How can I assist you today?",
#         "hello": "Hello! Have a great day.",
#         "hey": "Hello! How can I assist you today?",
#         "good morning": "Good morning! Have a nice day.",
#         "good afternoon": "Good afternoon! Have a great day.",
#         "good evening": "Good evening! Go and have snacks.",
#         "good night": "Good night! Sleep well."
#     }
#     for key, value in greetings.items():
#         if key in query.lower():
#             return value
#     return None

# def detect_inappropriate_language(query):
#     inappropriate_phrases = ["brutal", "badword", "i hate you", "fuck you", "i love you", "i want to marry you"]
#     return any(phrase in query.lower() for phrase in inappropriate_phrases)

# # Function to get problems based on keyword search
# def get_problems_by_keyword(keywords):
#     search_columns = ['Keywords(One word)', 'ASIC/Module']
#     problem_column = 'Problem'
    
#     # Match the query keywords in the 'Keywords' and 'ASIC/Module' columns
#     matched_problems = pd.DataFrame()
#     for keyword in keywords:
#         matches = csv_data[csv_data[search_columns].apply(lambda row: row.astype(str).str.contains(keyword, case=False).any(), axis=1)]
#         matched_problems = pd.concat([matched_problems, matches])

#     matched_problems = matched_problems.drop_duplicates()
    
#     if not matched_problems.empty:
#         return matched_problems[problem_column].dropna().astype(str).tolist()  # Convert to string and return a list of problems
#     else:
#         return []

# # Modify get_response function for better type handling
# def get_response(query):
#     greeting_response = detect_greeting(query)
#     if greeting_response:
#         return greeting_response

#     if detect_inappropriate_language(query):
#         return "I didn't get you..."

#     if "problems" in query.lower() or "issues" in query.lower():
#         problems = query_csv(query)
#         if isinstance(problems, list) and problems:
#             st.session_state.pending_feedback = True
#             return problems
#         return "No problems found for the given keyword."

#     return "What do you want to know about this?"

# # Add the title with fire symbol at the top
# st.markdown("<h1 style='text-align: center;'> HitLit 🔥 </h1>", unsafe_allow_html=True)

# # User input at the bottom
# user_input = st.text_input("Your message", key="user_input")

# if user_input:
#     st.session_state.chat_history.append(user_input)
    
#     ai_response = get_response(user_input)

#     if isinstance(ai_response, list) and ai_response:
#         # Ensure all problems are strings
#         ai_response = [str(problem) for problem in ai_response]
        
#         # Display the problems as radio buttons
#         selected_problem = st.radio("Select a problem:", options=ai_response, index=0)  # Default selection to first problem
        
#         # Update selected problem
#         st.session_state.selected_problem = selected_problem
        
#         # Ask for feedback after selection
#         st.session_state.chat_history.append(f"Do you want the root cause and solution for '{selected_problem}'?")

#         # Option to get root cause and solution
#         if st.button("Get Root Cause and Solution"):
#             root_cause, solution = get_root_cause_and_solution(selected_problem)
#             if root_cause and solution:
#                 st.write(f"**Root Cause:** {root_cause}")
#                 st.write(f"**Solution:** {solution}")
#                 st.session_state.chat_history.append(f"Root Cause: {root_cause}\nSolution: {solution}")
#             else:
#                 st.write("No root cause or solution found.")
#                 st.session_state.chat_history.append("No root cause or solution found.")
#     else:
#         st.write(ai_response)
#         st.session_state.chat_history.append(ai_response)

# # Clear chat button logic at the bottom of the page
# st.markdown("<br><hr>", unsafe_allow_html=True)
# if st.button("Clear Chat"):
#     # Reset all session state variables related to the chat
#     st.session_state.chat_history = []
#     st.session_state.last_keywords = []
#     st.session_state.selected_problem = None
#     st.session_state.pending_feedback = False

# import pandas as pd
# import streamlit as st

# # Load and Save CSV File
# @st.cache_data
# def load_csv(file_path):
#     return pd.read_csv(file_path)

# def save_csv(data, file_path):
#     data.to_csv(file_path, index=False)

# # Replace with your CSV file path
# csv_file_path = r"\\kor2fs03\V-V--Testing$\03_Validation_Software\LLBP\VALSW_LL_BP_SPL_V1.1.csv"
# csv_data = load_csv(csv_file_path)

# # Function to add new data to the CSV
# def add_to_csv(keyword, asic_module, problem, root_cause, solution):
#     global csv_data  # Use the global variable to keep track of the updated DataFrame
#     new_entry = {
#         "Keywords(One word)": keyword,
#         "ASIC/Module": asic_module,
#         "Problem": problem,
#         "Root cause": root_cause,
#         "Solution": solution
#     }
#     csv_data = csv_data.append(new_entry, ignore_index=True)
#     save_csv(csv_data, csv_file_path)  # Save the updated DataFrame back to the CSV

# # Function to detect greeting
# def detect_greeting(query):
#     greetings = ["hi", "hello", "good morning", "good afternoon", "good evening"]
#     if any(greet in query.lower() for greet in greetings):
#         return "Hello! How can I assist you today?"
#     return None

# # Function to detect inappropriate language
# def detect_inappropriate_language(query):
#     inappropriate_words = ["hate", "love", "marry", "fuck"]
#     return any(word in query.lower() for word in inappropriate_words)

# # Modify get_response function for better type handling
# def get_response(query):
#     greeting_response = detect_greeting(query)
#     if greeting_response:
#         return greeting_response

#     if detect_inappropriate_language(query):
#         return "I didn't get you..."

#     if "problems" in query.lower() or "issues" in query.lower():
#         problems = query_csv(query)
#         if isinstance(problems, list) and problems:
#             st.session_state.pending_feedback = True
#             return problems
#         return "No problems found for the given keyword."

#     return "What do you want to know about this?"

# # Function to query CSV for problems
# def query_csv(keyword):
#     keyword_match = csv_data[csv_data['Keywords(One word)'].str.contains(keyword, case=False, na=False)]
#     if not keyword_match.empty:
#         return keyword_match['Problem'].head(5).tolist()
#     return []

# # Function to get root cause and solution
# def get_root_cause_and_solution(selected_problem):
#     match = csv_data[csv_data['Problem'] == selected_problem]
#     if not match.empty:
#         root_cause = match.iloc[0]['Root cause']
#         solution = match.iloc[0]['Solution']
#         return root_cause, solution
#     return None, None

# # Streamlit App Layout
# # st.title("VALSW CHAT BOT")

# # Sidebar to switch between modes: Chat or Add Data
# mode = st.sidebar.radio("Select Mode:", ["Chat", "Add New Data"])

# # Chat Mode
# if mode == "Chat":
#     # Add the title with fire symbol at the top
#     st.markdown("<h1 style='text-align: center;'> HitLit 🔥 </h1>", unsafe_allow_html=True)

#     # User input at the bottom
#     user_input = st.text_input("Your message", key="user_input")

#     if user_input:
#         if 'chat_history' not in st.session_state:
#             st.session_state.chat_history = []
#         if 'pending_feedback' not in st.session_state:
#             st.session_state.pending_feedback = False

#         st.session_state.chat_history.append(user_input)
        
#         ai_response = get_response(user_input)

#         if isinstance(ai_response, list) and ai_response:
#             # Ensure all problems are strings
#             ai_response = [str(problem) for problem in ai_response]
            
#             # Display the problems as radio buttons
#             selected_problem = st.radio("Select a problem:", options=ai_response, index=0)  # Default selection to first problem
            
#             # Update selected problem
#             st.session_state.selected_problem = selected_problem
            
#             # Ask for feedback after selection
#             st.session_state.chat_history.append(f"Do you want the root cause and solution for '{selected_problem}'?")

#             # Option to get root cause and solution
#             if st.button("Get Root Cause and Solution"):
#                 root_cause, solution = get_root_cause_and_solution(selected_problem)
#                 if root_cause and solution:
#                     st.write(f"**Root Cause:** {root_cause}")
#                     st.write(f"**Solution:** {solution}")
#                     st.session_state.chat_history.append(f"Root Cause: {root_cause}\nSolution: {solution}")
#                 else:
#                     st.write("No root cause or solution found.")
#                     st.session_state.chat_history.append("No root cause or solution found.")
#         else:
#             st.write(ai_response)
#             st.session_state.chat_history.append(ai_response)

#     # Clear chat button logic at the bottom of the page
#     st.markdown("<br><hr>", unsafe_allow_html=True)
#     if st.button("Clear Chat"):
#         # Reset all session state variables related to the chat
#         st.session_state.chat_history = []
#         st.session_state.selected_problem = None
#         st.session_state.pending_feedback = False

# # Add New Data Mode
# elif mode == "Add New Data":
#     # User input to add new data
#     st.markdown("### Add New Problem Entry to the CSV")
#     keyword = st.text_input("Enter Keyword (One word):")
#     asic_module = st.text_input("Enter ASIC/Module:")
#     problem = st.text_area("Enter Problem Description:")
#     root_cause = st.text_area("Enter Root Cause:")
#     solution = st.text_area("Enter Solution:")
    
#     # Button to trigger adding the new data
#     if st.button("Add New Entry"):
#         if keyword and asic_module and problem and root_cause and solution:
#             add_to_csv(keyword, asic_module, problem, root_cause, solution)
#             st.success("New entry added successfully!")
#         else:
#             st.error("Please fill in all fields before adding the new entry.")


# import pandas as pd
# import streamlit as st

# # Load and Save CSV File
# @st.cache_data
# def load_csv(file_path):
#     return pd.read_csv(file_path)

# def save_csv(data, file_path):
#     data.to_csv(file_path, index=False)

# # Replace with your CSV file path
# csv_file_path = r"\\kor2fs03\V-V--Testing$\03_Validation_Software\LLBP\VALSW_LL_BP_SPL_V1.1.csv"
# csv_data = load_csv(csv_file_path)

# # Function to add new data to the CSV
# def add_to_csv(keyword, asic_module, problem, root_cause, solution):
#     global csv_data  # Use the global variable to keep track of the updated DataFrame
#     new_entry = {
#         "Keywords(One word)": keyword,
#         "ASIC/Module": asic_module,
#         "Problem": problem,
#         "Root cause": root_cause,
#         "Solution": solution
#     }
#     csv_data = csv_data.append(new_entry, ignore_index=True)
#     save_csv(csv_data, csv_file_path)  # Save the updated DataFrame back to the CSV

# # Function to detect greeting
# def detect_greeting(query):
#     greetings = ["hi", "hello", "good morning", "good afternoon", "good evening"]
#     if any(greet in query.lower() for greet in greetings):
#         return "Hello! How can I assist you today?"
#     return None

# # Function to detect inappropriate language
# def detect_inappropriate_language(query):
#     inappropriate_words = ["hate", "love", "marry", "fuck"]
#     return any(word in query.lower() for word in inappropriate_words)

# # Modify get_response function for better type handling
# def get_response(query):
#     greeting_response = detect_greeting(query)
#     if greeting_response:
#         return greeting_response

#     if detect_inappropriate_language(query):
#         return "I didn't get you..."

#     if "problems" in query.lower() or "issues" in query.lower():
#         problems = query_csv(query)
#         if isinstance(problems, list) and problems:
#             st.session_state.pending_feedback = True
#             return problems
#         return "No problems found for the given keyword."

#     return "What do you want to know about this?"

# # Function to query CSV for problems
# def query_csv(keyword):
#     keyword_match = csv_data[csv_data['Keywords(One word)'].str.contains(keyword, case=False, na=False)]
#     if not keyword_match.empty:
#         return keyword_match['Problem'].head(5).tolist()
#     return []

# # Function to get root cause and solution
# def get_root_cause_and_solution(selected_problem):
#     match = csv_data[csv_data['Problem'] == selected_problem]
#     if not match.empty:
#         root_cause = match.iloc[0]['Root cause']
#         solution = match.iloc[0]['Solution']
#         return root_cause, solution
#     return None, None

# # Streamlit App Layout
# # st.title("VALSW CHAT BOT")

# # Sidebar to switch between modes: Chat or Add Data
# mode = st.sidebar.radio("Select Mode:", ["Chat", "Add New Data"])

# # Chat Mode
# if mode == "Chat":
#     # Add the title with fire symbol at the top
#     st.markdown("<h1 style='text-align: center;'> HitLit 🔥 </h1>", unsafe_allow_html=True)

#     # User input at the bottom
#     user_input = st.text_input("Your message", key="user_input")

#     if user_input:
#         if 'chat_history' not in st.session_state:
#             st.session_state.chat_history = []
#         if 'pending_feedback' not in st.session_state:
#             st.session_state.pending_feedback = False

#         st.session_state.chat_history.append(user_input)
        
#         ai_response = get_response(user_input)

#         if isinstance(ai_response, list) and ai_response:
#             # Ensure all problems are strings
#             ai_response = [str(problem) for problem in ai_response]
            
#             # Display the problems as radio buttons
#             selected_problem = st.radio("Select a problem:", options=ai_response, index=0)  # Default selection to first problem
            
#             # Update selected problem
#             st.session_state.selected_problem = selected_problem
            
#             # Ask for feedback after selection
#             st.session_state.chat_history.append(f"Do you want the root cause and solution for '{selected_problem}'?")

#             # Option to get root cause and solution
#             if st.button("Get Root Cause and Solution"):
#                 root_cause, solution = get_root_cause_and_solution(selected_problem)
#                 if root_cause and solution:
#                     st.write(f"**Root Cause:** {root_cause}")
#                     st.write(f"**Solution:** {solution}")
#                     st.session_state.chat_history.append(f"Root Cause: {root_cause}\nSolution: {solution}")
#                 else:
#                     st.write("No root cause or solution found.")
#                     st.session_state.chat_history.append("No root cause or solution found.")
#         else:
#             st.write(ai_response)
#             st.session_state.chat_history.append(ai_response)

#     # Clear chat button logic at the bottom of the page
#     st.markdown("<br><hr>", unsafe_allow_html=True)
#     if st.button("Clear Chat"):
#         # Reset all session state variables related to the chat
#         st.session_state.chat_history = []
#         st.session_state.selected_problem = None
#         st.session_state.pending_feedback = False

# # Add New Data Mode
# elif mode == "Add New Data":
#     # User input to add new data
#     st.markdown("### Add New Problem Entry to the CSV")
#     keyword = st.text_input("Enter Keyword (One word):")
#     asic_module = st.text_input("Enter ASIC/Module:")
#     problem = st.text_area("Enter Problem Description:")
#     root_cause = st.text_area("Enter Root Cause:")
#     solution = st.text_area("Enter Solution:")
    
#     # Button to trigger adding the new data
#     if st.button("Add New Entry"):
#         if keyword and asic_module and problem and root_cause and solution:
#             add_to_csv(keyword, asic_module, problem, root_cause, solution)
#             st.success("New entry added successfully!")
#         else:
#             st.error("Please fill in all fields before adding the new entry.")


# import streamlit as st
# import pandas as pd
# import re

# # Initialize session state variables
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
# if "last_keywords" not in st.session_state:
#     st.session_state.last_keywords = []
# if "selected_problem" not in st.session_state:
#     st.session_state.selected_problem = None
# if "pending_feedback" not in st.session_state:
#     st.session_state.pending_feedback = False

# # Set up the Streamlit app
# st.set_page_config(page_title="HitLit", page_icon="🤖", initial_sidebar_state="expanded")

# # Load and Save CSV File
# @st.cache_data
# def load_csv(file_path):
#     return pd.read_csv(file_path)

# def save_csv(data, file_path):
#     data.to_csv(file_path, index=False)

# # Replace with your CSV file path
# csv_file_path = r"\\kor2fs03\V-V--Testing$\03_Validation_Software\LLBP\VALSW_LL_BP_SPL_V1.1.csv"
# csv_data = load_csv(csv_file_path)

# # Function to add new data to the CSV
# def add_to_csv(keyword, asic_module, problem, root_cause, solution):
#     global csv_data  # Use the global variable to keep track of the updated DataFrame
#     new_entry = {
#         "Keywords(One word)": keyword,
#         "ASIC/Module": asic_module,
#         "Problem": problem,
#         "Root cause": root_cause,
#         "Solution": solution
#     }
#     csv_data = csv_data.append(new_entry, ignore_index=True)
#     save_csv(csv_data, csv_file_path)  # Save the updated DataFrame back to the CSV

# def clean_and_split_query(query):
#     filler_words = {'um', 'like', 'you', 'know', 'so', 'well', 'actually', 'basically', 'just', 'really'}
#     stop_words = {'is', 'are', 'was', 'were', 'what', 'who', 'how', 'where', 'when', 'why',
#                   'i', 'me', 'you', 'his', 'her', 'ok', 'bye', 'i am sorry', 'it is what it is', 'it','is','on','over','under','inside','an','a','the', 'does','con',
#                   'get', 'got', 'have', 'had', 'has', 'should', 'not', 'use', 'mobile','team','Team','Verdict','an','no','not','but','T','15','with','off','issues','issue','is','in','the','problems','are','what','why','when','flt','flashing'}
#     cleaned_query = re.sub(r'[^\w\s]', '', query)
#     words = cleaned_query.lower().split()
#     filtered_words = [word for word in words if word not in filler_words and word not in stop_words]
#     return filtered_words

# # Function to get problems based on keyword search
# def get_problems_by_keyword(keywords):
#     search_columns = ['Keywords(One word)', 'ASIC/Module']
#     problem_column = 'Problem'
    
#     # Match the query keywords in the 'Keywords' and 'ASIC/Module' columns
#     matched_problems = pd.DataFrame()
#     for keyword in keywords:
#         matches = csv_data[csv_data[search_columns].apply(lambda row: row.astype(str).str.contains(keyword, case=False).any(), axis=1)]
#         matched_problems = pd.concat([matched_problems, matches])

#     matched_problems = matched_problems.drop_duplicates()
    
#     if not matched_problems.empty:
#         return matched_problems[problem_column].tolist()  # Return a list of problems
#     else:
#         return []

# # Function to get root cause and solution based on the selected problem
# def get_root_cause_and_solution(problem):
#     problem_row = csv_data[csv_data['Problem'] == problem]
#     if not problem_row.empty:
#         root_cause = problem_row['Root cause'].values[0]
#         solution = problem_row['Solution'].values[0]
#         return root_cause, solution
#     return None, None

# def query_csv(query):
#     keywords = clean_and_split_query(query)
#     st.session_state.last_keywords = keywords
#     problems = get_problems_by_keyword(keywords)
    
#     if problems:
#         st.session_state.pending_feedback = True
#         return problems
#     else:
#         return "No problems found for the given keyword."

# # Detect greetings and inappropriate language
# def detect_greeting(query):
#     greetings = {
#         "hi": "Hello! How can I assist you today?",
#         "hello": "Hello! Have a great day.",
#         "hey": "Hello! How can I assist you today?",
#         "good morning": "Good morning! Have a nice day.",
#         "good afternoon": "Good afternoon! Have a great day.",
#         "good evening": "Good evening! Go and have snacks.",
#         "good night": "Good night! Sleep well."
#     }
#     for key, value in greetings.items():
#         if key in query.lower():
#             return value
#     return None

# def detect_inappropriate_language(query):
#     inappropriate_phrases = ["brutal", "badword", "i hate you", "fuck you", "i love you", "i want to marry you"]
#     return any(phrase in query.lower() for phrase in inappropriate_phrases)

# # Function to get problems based on keyword search
# def get_problems_by_keyword(keywords):
#     search_columns = ['Keywords(One word)', 'ASIC/Module']
#     problem_column = 'Problem'
    
#     # Match the query keywords in the 'Keywords' and 'ASIC/Module' columns
#     matched_problems = pd.DataFrame()
#     for keyword in keywords:
#         matches = csv_data[csv_data[search_columns].apply(lambda row: row.astype(str).str.contains(keyword, case=False).any(), axis=1)]
#         matched_problems = pd.concat([matched_problems, matches])

#     matched_problems = matched_problems.drop_duplicates()
    
#     if not matched_problems.empty:
#         return matched_problems[problem_column].dropna().astype(str).tolist()  # Convert to string and return a list of problems
#     else:
#         return []

# # Modify get_response function for better type handling
# def get_response(query):
#     greeting_response = detect_greeting(query)
#     if greeting_response:
#         return greeting_response

#     if detect_inappropriate_language(query):
#         return "I didn't get you..."

#     if "problems" in query.lower() or "issues" in query.lower():
#         problems = query_csv(query)
#         if isinstance(problems, list) and problems:
#             st.session_state.pending_feedback = True
#             return problems
#         return "No problems found for the given keyword."

#     return "What do you want to know about this?"

# # Add the title with fire symbol at the top
# st.markdown("<h1 style='text-align: center;'> HitLit 🔥 </h1>", unsafe_allow_html=True)

# # User input at the bottom
# user_input = st.text_input("Your message", key="user_input")

# if user_input:
#     st.session_state.chat_history.append(user_input)
    
#     ai_response = get_response(user_input)

#     if isinstance(ai_response, list) and ai_response:
#         # Ensure all problems are strings
#         ai_response = [str(problem) for problem in ai_response]
        
#         # Display the problems as radio buttons
#         selected_problem = st.radio("Select a problem:", options=ai_response, index=0)  # Default selection to first problem
        
#         # Update selected problem
#         st.session_state.selected_problem = selected_problem
        
#         # Ask for feedback after selection
#         st.session_state.chat_history.append(f"Do you want the root cause and solution for '{selected_problem}'?")

#         # Option to get root cause and solution
#         if st.button("Get Root Cause and Solution"):
#             root_cause, solution = get_root_cause_and_solution(selected_problem)
#             if root_cause and solution:
#                 st.write(f"**Root Cause:** {root_cause}")
#                 st.write(f"**Solution:** {solution}")
#                 st.session_state.chat_history.append(f"Root Cause: {root_cause}\nSolution: {solution}")
#             else:
#                 st.write("No root cause or solution found.")
#                 st.session_state.chat_history.append("No root cause or solution found.")
#     else:
#         st.write(ai_response)
#         st.session_state.chat_history.append(ai_response)

# # Clear chat button logic at the bottom of the page
# st.markdown("<br><hr>", unsafe_allow_html=True)
# if st.button("Clear Chat"):
#     # Reset all session state variables related to the chat
#     st.session_state.chat_history = []
#     st.session_state.last_keywords = []
#     st.session_state.selected_problem = None
#     st.session_state.pending_feedback = False



# import streamlit as st
# import pandas as pd
# import re

# # Initialize session state variables
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
# if "last_keywords" not in st.session_state:
#     st.session_state.last_keywords = []
# if "selected_problem" not in st.session_state:
#     st.session_state.selected_problem = None
# if "pending_feedback" not in st.session_state:
#     st.session_state.pending_feedback = False

# # Set up the Streamlit app
# st.set_page_config(page_title="HitLit", page_icon="🤖", initial_sidebar_state="expanded")

# # Load and Save CSV File
# @st.cache_data
# def load_csv(file_path):
#     return pd.read_csv(file_path)

# def save_csv(data, file_path):
#     data.to_csv(file_path, index=False)

# # Replace with your CSV file path
# csv_file_path = r"\\kor2fs03\V-V--Testing$\03_Validation_Software\LLBP\VALSW_LL_BP_SPL_V1.1.csv"
# csv_data = load_csv(csv_file_path)

# # Function to add new data to the CSV
# def add_to_csv(keyword, asic_module, problem, root_cause, solution):
#     global csv_data  # Use the global variable to keep track of the updated DataFrame
#     new_entry = {
#         "Keywords(One word)": keyword,
#         "ASIC/Module": asic_module,
#         "Problem": problem,
#         "Root cause": root_cause,
#         "Solution": solution
#     }
#     csv_data = csv_data.append(new_entry, ignore_index=True)
#     save_csv(csv_data, csv_file_path)  # Save the updated DataFrame back to the CSV

# def clean_and_split_query(query):
#     filler_words = {'um', 'like', 'you', 'know', 'so', 'well', 'actually', 'basically', 'just', 'really'}
#     stop_words = {'is', 'are', 'was', 'were', 'what', 'who', 'how', 'where', 'when', 'why',
#                   'i', 'me', 'you', 'his', 'her', 'ok', 'bye', 'i am sorry', 'it is what it is', 'it','is','on','over','under','inside','an','a','the', 'does','con',
#                   'get', 'got', 'have', 'had', 'has', 'should', 'not', 'use', 'mobile','team','Team','Verdict','an','no','not','but','T','15','with','off','issues','issue','is','in','the','problems','are','what','why','when','flt','flashing'}
#     cleaned_query = re.sub(r'[^\w\s]', '', query)
#     words = cleaned_query.lower().split()
#     filtered_words = [word for word in words if word not in filler_words and word not in stop_words]
#     return filtered_words

# # Function to get problems based on keyword search
# def get_problems_by_keyword(keywords):
#     search_columns = ['Keywords(One word)', 'ASIC/Module']
#     problem_column = 'Problem'
    
#     matched_problems = pd.DataFrame()
#     for keyword in keywords:
#         matches = csv_data[csv_data[search_columns].apply(lambda row: row.astype(str).str.contains(keyword, case=False).any(), axis=1)]
#         matched_problems = pd.concat([matched_problems, matches])

#     matched_problems = matched_problems.drop_duplicates()
    
#     if not matched_problems.empty:
#         return matched_problems[problem_column].tolist()  # Return a list of problems
#     else:
#         return []

# # Function to get root cause and solution based on the selected problem
# def get_root_cause_and_solution(problem):
#     problem_row = csv_data[csv_data['Problem'] == problem]
#     if not problem_row.empty:
#         root_cause = problem_row['Root cause'].values[0]
#         solution = problem_row['Solution'].values[0]
#         return root_cause, solution
#     return None, None

# def query_csv(query):
#     keywords = clean_and_split_query(query)
#     st.session_state.last_keywords = keywords
#     problems = get_problems_by_keyword(keywords)
    
#     if problems:
#         st.session_state.pending_feedback = True
#         return problems
#     else:
#         return "No problems found for the given keyword."

# # Detect greetings and inappropriate language
# def detect_greeting(query):
#     greetings = {
#         "hi": "Hello! How can I assist you today?",
#         "hello": "Hello! Have a great day.",
#         "hey": "Hello! How can I assist you today?",
#         "good morning": "Good morning! Have a nice day.",
#         "good afternoon": "Good afternoon! Have a great day.",
#         "good evening": "Good evening! Go and have snacks.",
#         "good night": "Good night! Sleep well."
#     }
#     for key, value in greetings.items():
#         if key in query.lower():
#             return value
#     return None

# def detect_inappropriate_language(query):
#     inappropriate_phrases = ["brutal", "badword", "i hate you", "fuck you", "i love you", "i want to marry you"]
#     return any(phrase in query.lower() for phrase in inappropriate_phrases)

# # Modify get_response function for better type handling
# def get_response(query):
#     greeting_response = detect_greeting(query)
#     if greeting_response:
#         return greeting_response

#     if detect_inappropriate_language(query):
#         return "I didn't get you..."

#     if "problems" in query.lower() or "issues" in query.lower():
#         problems = query_csv(query)
#         if isinstance(problems, list) and problems:
#             st.session_state.pending_feedback = True
#             return problems
#         return "No problems found for the given keyword."

#     if "add data" in query.lower():
#         return "Please provide the following information to add new data: Keyword, ASIC/Module, Problem, Root Cause, Solution."

#     return "What do you want to know about this?"

# # Add the title with fire symbol at the top
# st.markdown("<h1 style='text-align: center;'> HitLit 🔥 </h1>", unsafe_allow_html=True)

# # User input at the bottom
# user_input = st.text_input("Your message", key="user_input")

# if user_input:
#     st.session_state.chat_history.append(user_input)
    
#     ai_response = get_response(user_input)

#     if isinstance(ai_response, list) and ai_response:
#         # Ensure all problems are strings
#         ai_response = [str(problem) for problem in ai_response]
        
#         # Display the problems as radio buttons
#         selected_problem = st.radio("Select a problem:", options=ai_response, index=0)  # Default selection to first problem
        
#         # Update selected problem
#         st.session_state.selected_problem = selected_problem
        
#         # Ask for feedback after selection
#         st.session_state.chat_history.append(f"Do you want the root cause and solution for '{selected_problem}'?")

#         # Option to get root cause and solution
#         if st.button("Get Root Cause and Solution"):
#             root_cause, solution = get_root_cause_and_solution(selected_problem)
#             if root_cause and solution:
#                 st.write(f"**Root Cause:** {root_cause}")
#                 st.write(f"**Solution:** {solution}")
#                 st.session_state.chat_history.append(f"Root Cause: {root_cause}\nSolution: {solution}")
#             else:
#                 st.write("No root cause or solution found.")
#                 st.session_state.chat_history.append("No root cause or solution found.")
#     elif "add data" in user_input.lower():
#         # Collect data for the new entry
#         keyword = st.text_input("Enter Keyword:")
#         asic_module = st.text_input("Enter ASIC/Module:")
#         problem = st.text_input("Enter Problem:")
#         root_cause = st.text_input("Enter Root Cause:")
#         solution = st.text_input("Enter Solution:")

#         if st.button("Submit New Data"):
#             add_to_csv(keyword, asic_module, problem, root_cause, solution)
#             st.success("Data added successfully!")
#             st.session_state.chat_history.append(f"Added new data: {keyword}, {asic_module}, {problem}, {root_cause}, {solution}")
#     else:
#         st.write(ai_response)
#         st.session_state.chat_history.append(ai_response)

# # Clear chat button logic at the bottom of the page
# st.markdown("<br><hr>", unsafe_allow_html=True)
# if st.button("Clear Chat"):
#     # Reset all session state variables related to the chat
#     st.session_state.chat_history = []
#     st.session_state.last_keywords = []
#     st.session_state.selected_problem = None
#     st.session_state.pending_feedback = False



# import streamlit as st
# import pandas as pd
# import re

# # Initialize session state variables
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
# if "last_keywords" not in st.session_state:
#     st.session_state.last_keywords = []
# if "selected_problem" not in st.session_state:
#     st.session_state.selected_problem = None
# if "pending_feedback" not in st.session_state:
#     st.session_state.pending_feedback = False

# # Set up the Streamlit app
# st.set_page_config(page_title="HitLit", page_icon="🤖", initial_sidebar_state="expanded")

# # Load and Save CSV File
# @st.cache_data
# def load_csv(file_path):
#     return pd.read_csv(file_path)

# def save_csv(data, file_path):
#     data.to_csv(file_path, index=False)

# # Replace with your CSV file path
# csv_file_path = r"\\kor2fs03\V-V--Testing$\03_Validation_Software\LLBP\VALSW_LL_BP_SPL_V1.1.csv"
# csv_data = load_csv(csv_file_path)

# # Function to add new data to the CSV
# def add_to_csv(keyword, asic_module, problem, root_cause, solution):
#     global csv_data  # Use the global variable to keep track of the updated DataFrame
#     new_entry = {
#         "Keywords(One word)": keyword,
#         "ASIC/Module": asic_module,
#         "Problem": problem,
#         "Root cause": root_cause,
#         "Solution": solution
#     }
#     csv_data = csv_data.append(new_entry, ignore_index=True)
#     save_csv(csv_data, csv_file_path)  # Save the updated DataFrame back to the CSV

# def clean_and_split_query(query):
#     filler_words = {'um', 'like', 'you', 'know', 'so', 'well', 'actually', 'basically', 'just', 'really'}
#     stop_words = {'is', 'are', 'was', 'were', 'what', 'who', 'how', 'where', 'when', 'why',
#                   'i', 'me', 'you', 'his', 'her', 'ok', 'bye', 'i am sorry', 'it is what it is', 'it','is','on','over','under','inside','an','a','the', 'does','con',
#                   'get', 'got', 'have', 'had', 'has', 'should', 'not', 'use', 'mobile','team','Team','Verdict','an','no','not','but','T','15','with','off','issues','issue','is','in','the','problems','are','what','why','when','flt','flashing'}
#     cleaned_query = re.sub(r'[^\w\s]', '', query)
#     words = cleaned_query.lower().split()
#     filtered_words = [word for word in words if word not in filler_words and word not in stop_words]
#     return filtered_words

# # Function to get problems based on keyword search
# def get_problems_by_keyword(keywords):
#     search_columns = ['Keywords(One word)', 'ASIC/Module']
#     problem_column = 'Problem'
    
#     # Match the query keywords in the 'Keywords' and 'ASIC/Module' columns
#     matched_problems = pd.DataFrame()
#     for keyword in keywords:
#         matches = csv_data[csv_data[search_columns].apply(lambda row: row.astype(str).str.contains(keyword, case=False).any(), axis=1)]
#         matched_problems = pd.concat([matched_problems, matches])

#     matched_problems = matched_problems.drop_duplicates()
    
#     if not matched_problems.empty:
#         return matched_problems[problem_column].tolist()  # Return a list of problems
#     else:
#         return []

# # Function to get root cause and solution based on the selected problem
# def get_root_cause_and_solution(problem):
#     problem_row = csv_data[csv_data['Problem'] == problem]
#     if not problem_row.empty:
#         root_cause = problem_row['Root cause'].values[0]
#         solution = problem_row['Solution'].values[0]
#         return root_cause, solution
#     return None, None

# def query_csv(query):
#     keywords = clean_and_split_query(query)
#     st.session_state.last_keywords = keywords
#     problems = get_problems_by_keyword(keywords)
    
#     if problems:
#         st.session_state.pending_feedback = True
#         return problems
#     else:
#         return "No problems found for the given keyword."

# # Detect greetings and inappropriate language
# def detect_greeting(query):
#     greetings = {
#         "hi": "Hello! How can I assist you today?",
#         "hello": "Hello! Have a great day.",
#         "hey": "Hello! How can I assist you today?",
#         "good morning": "Good morning! Have a nice day.",
#         "good afternoon": "Good afternoon! Have a great day.",
#         "good evening": "Good evening! Go and have snacks.",
#         "good night": "Good night! Sleep well."
#     }
#     for key, value in greetings.items():
#         if key in query.lower():
#             return value
#     return None

# def detect_inappropriate_language(query):
#     inappropriate_phrases = ["brutal", "badword", "i hate you", "fuck you", "i love you", "i want to marry you"]
#     return any(phrase in query.lower() for phrase in inappropriate_phrases)

# # Modify get_response function for better type handling
# def get_response(query):
#     greeting_response = detect_greeting(query)
#     if greeting_response:
#         return greeting_response

#     if detect_inappropriate_language(query):
#         return "I didn't get you..."

#     if "problems" in query.lower() or "issues" in query.lower():
#         problems = query_csv(query)
#         if isinstance(problems, list) and problems:
#             st.session_state.pending_feedback = True
#             return problems
#         return "No problems found for the given keyword."

#     if "add data" in query.lower():  # Trigger data addition
#         return "Please provide the following information to add new data."

#     return "What do you want to know about this?"

# # Add the title with fire symbol at the top
# st.markdown("<h1 style='text-align: center;'> HitLit 🔥 </h1>", unsafe_allow_html=True)

# # User input at the bottom
# user_input = st.text_input("Your message", key="user_input")

# if user_input:
#     st.session_state.chat_history.append(user_input)

#     ai_response = get_response(user_input)

#     if "add data" in user_input.lower():
#         # Collect data for the new entry
#         keyword = st.text_input("Enter Keyword:", key="keyword_input")
#         asic_module = st.text_input("Enter ASIC/Module:", key="asic_module_input")
#         problem = st.text_input("Enter Problem:", key="problem_input")
#         root_cause = st.text_input("Enter Root Cause:", key="root_cause_input")
#         solution = st.text_input("Enter Solution:", key="solution_input")

#         if st.button("Submit New Data"):
#             add_to_csv(keyword, asic_module, problem, root_cause, solution)
#             st.success("Data added successfully!")
#             st.session_state.chat_history.append(f"Added new data: {keyword}, {asic_module}, {problem}, {root_cause}, {solution}")

#     elif isinstance(ai_response, list) and ai_response:
#         # Ensure all problems are strings
#         ai_response = [str(problem) for problem in ai_response]
        
#         # Display the problems as radio buttons
#         selected_problem = st.radio("Select a problem:", options=ai_response, index=0)  # Default selection to first problem
        
#         # Update selected problem
#         st.session_state.selected_problem = selected_problem
        
#         # Ask for feedback after selection
#         st.session_state.chat_history.append(f"Do you want the root cause and solution for '{selected_problem}'?")

#         # Option to get root cause and solution
#         if st.button("Get Root Cause and Solution"):
#             root_cause, solution = get_root_cause_and_solution(selected_problem)
#             if root_cause and solution:
#                 st.write(f"**Root Cause:** {root_cause}")
#                 st.write(f"**Solution:** {solution}")
#                 st.session_state.chat_history.append(f"Root Cause: {root_cause}\nSolution: {solution}")
#             else:
#                 st.write("No root cause or solution found.")
#                 st.session_state.chat_history.append("No root cause or solution found.")
#     else:
#         st.write(ai_response)
#         st.session_state.chat_history.append(ai_response)

# # Clear chat button logic at the bottom of the page
# st.markdown("<br><hr>", unsafe_allow_html=True)
# if st.button("Clear Chat"):
#     # Reset all session state variables related to the chat
#     st.session_state.chat_history = []
#     st.session_state.last_keywords = []
#     st.session_state.selected_problem = None
#     st.session_state.pending_feedback = False



# import streamlit as st
# import pandas as pd
# import re

# # Initialize session state variables
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
# if "last_keywords" not in st.session_state:
#     st.session_state.last_keywords = []
# if "selected_problem" not in st.session_state:
#     st.session_state.selected_problem = None
# if "pending_feedback" not in st.session_state:
#     st.session_state.pending_feedback = False

# # Set up the Streamlit app
# st.set_page_config(page_title="HitLit", page_icon="🤖", initial_sidebar_state="expanded")

# # Load and Save CSV File
# @st.cache_data
# def load_csv(file_path):
#     return pd.read_csv(file_path)

# def save_csv(data, file_path):
#     data.to_csv(file_path, index=False)

# # Replace with your CSV file path
# csv_file_path = r"\\kor2fs03\V-V--Testing$\03_Validation_Software\LLBP\VALSW_LL_BP_SPL_V1.1.csv"
# csv_data = load_csv(csv_file_path)

# # Function to add new data to the CSV
# def add_to_csv(keyword, asic_module, problem, root_cause, solution):
#     global csv_data  # Use the global variable to keep track of the updated DataFrame
#     new_entry = pd.DataFrame({
#         "Keywords(One word)": [keyword],
#         "ASIC/Module": [asic_module],
#         "Problem": [problem],
#         "Root cause": [root_cause],
#         "Solution": [solution]
#     })
    
#     # Concatenate the new entry to the existing DataFrame
#     csv_data = pd.concat([csv_data, new_entry], ignore_index=True)
#     save_csv(csv_data, csv_file_path)  # Save the updated DataFrame back to the CSV

# def clean_and_split_query(query):
#     filler_words = {'um', 'like', 'you', 'know', 'so', 'well', 'actually', 'basically', 'just', 'really'}
#     stop_words = {'is', 'are', 'was', 'were', 'what', 'who', 'how', 'where', 'when', 'why',
#                   'i', 'me', 'you', 'his', 'her', 'ok', 'bye', 'i am sorry', 'it is what it is', 'it','is','on','over','under','inside','an','a','the', 'does','con',
#                   'get', 'got', 'have', 'had', 'has', 'should', 'not', 'use', 'mobile','team','Team','Verdict','an','no','not','but','T','15','with','off','issues','issue','is','in','the','problems','are','what','why','when','flt','flashing'}
#     cleaned_query = re.sub(r'[^\w\s]', '', query)
#     words = cleaned_query.lower().split()
#     filtered_words = [word for word in words if word not in filler_words and word not in stop_words]
#     return filtered_words

# # Function to get problems based on keyword search
# def get_problems_by_keyword(keywords):
#     search_columns = ['Keywords(One word)', 'ASIC/Module']
#     problem_column = 'Problem'
    
#     # Match the query keywords in the 'Keywords' and 'ASIC/Module' columns
#     matched_problems = pd.DataFrame()
#     for keyword in keywords:
#         matches = csv_data[csv_data[search_columns].apply(lambda row: row.astype(str).str.contains(keyword, case=False).any(), axis=1)]
#         matched_problems = pd.concat([matched_problems, matches])

#     matched_problems = matched_problems.drop_duplicates()
    
#     if not matched_problems.empty:
#         return matched_problems[problem_column].tolist()  # Return a list of problems
#     else:
#         return []

# # Function to get root cause and solution based on the selected problem
# def get_root_cause_and_solution(problem):
#     problem_row = csv_data[csv_data['Problem'] == problem]
#     if not problem_row.empty:
#         root_cause = problem_row['Root cause'].values[0]
#         solution = problem_row['Solution'].values[0]
#         return root_cause, solution
#     return None, None

# def query_csv(query):
#     keywords = clean_and_split_query(query)
#     st.session_state.last_keywords = keywords
#     problems = get_problems_by_keyword(keywords)
    
#     if problems:
#         st.session_state.pending_feedback = True
#         return problems
#     else:
#         return "No problems found for the given keyword."

# # Detect greetings and inappropriate language
# def detect_greeting(query):
#     greetings = {
#         "hi": "Hello! How can I assist you today?",
#         "hello": "Hello! Have a great day.",
#         "hey": "Hello! How can I assist you today?",
#         "good morning": "Good morning! Have a nice day.",
#         "good afternoon": "Good afternoon! Have a great day.",
#         "good evening": "Good evening! Go and have snacks.",
#         "good night": "Good night! Sleep well."
#     }
#     for key, value in greetings.items():
#         if key in query.lower():
#             return value
#     return None

# def detect_inappropriate_language(query):
#     inappropriate_phrases = ["brutal", "badword", "i hate you", "fuck you", "i love you", "i want to marry you"]
#     return any(phrase in query.lower() for phrase in inappropriate_phrases)

# # Modify get_response function for better type handling
# def get_response(query):
#     greeting_response = detect_greeting(query)
#     if greeting_response:
#         return greeting_response

#     if detect_inappropriate_language(query):
#         return "I didn't get you..."

#     if "problems" in query.lower() or "issues" in query.lower():
#         problems = query_csv(query)
#         if isinstance(problems, list) and problems:
#             st.session_state.pending_feedback = True
#             return problems
#         return "No problems found for the given keyword."

#     if "add data" in query.lower():  # Trigger data addition
#         return "Please provide the following information to add new data."

#     return "What do you want to know about this?"

# # Add the title with fire symbol at the top
# st.markdown("<h1 style='text-align: center;'> HitLit 🔥 </h1>", unsafe_allow_html=True)

# # User input at the bottom
# user_input = st.text_input("Your message", key="user_input")

# if user_input:
#     st.session_state.chat_history.append(user_input)

#     ai_response = get_response(user_input)

#     if "add data" in user_input.lower():
#         # Collect data for the new entry
#         keyword = st.text_input("Enter Keyword:", key="keyword_input")
#         asic_module = st.text_input("Enter ASIC/Module:", key="asic_module_input")
#         problem = st.text_input("Enter Problem:", key="problem_input")
#         root_cause = st.text_input("Enter Root Cause:", key="root_cause_input")
#         solution = st.text_input("Enter Solution:", key="solution_input")

#         if st.button("Submit New Data"):
#             add_to_csv(keyword, asic_module, problem, root_cause, solution)
#             st.success("Data added successfully!")
#             st.session_state.chat_history.append(f"Added new data: {keyword}, {asic_module}, {problem}, {root_cause}, {solution}")

#     elif isinstance(ai_response, list) and ai_response:
#         # Ensure all problems are strings
#         ai_response = [str(problem) for problem in ai_response]
        
#         # Display the problems as radio buttons
#         selected_problem = st.radio("Select a problem:", options=ai_response, index=0)  # Default selection to first problem
        
#         # Update selected problem
#         st.session_state.selected_problem = selected_problem
        
#         # Ask for feedback after selection
#         st.session_state.chat_history.append(f"Do you want the root cause and solution for '{selected_problem}'?")

#         # Option to get root cause and solution
#         if st.button("Get Root Cause and Solution"):
#             root_cause, solution = get_root_cause_and_solution(selected_problem)
#             if root_cause and solution:
#                 st.write(f"**Root Cause:** {root_cause}")
#                 st.write(f"**Solution:** {solution}")
#                 st.session_state.chat_history.append(f"Root Cause: {root_cause}\nSolution: {solution}")
#             else:
#                 st.write("No root cause and solution found.")

#     else:
#         st.session_state.chat_history.append(ai_response)

# # Display chat history
# for chat in st.session_state.chat_history:
#     st.write(chat)


# import streamlit as st
# import pandas as pd
# import re

# # Initialize session state variables
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
# if "last_keywords" not in st.session_state:
#     st.session_state.last_keywords = []
# if "selected_problem" not in st.session_state:
#     st.session_state.selected_problem = None
# if "pending_feedback" not in st.session_state:
#     st.session_state.pending_feedback = False

# # Set up the Streamlit app
# st.set_page_config(page_title="HitLit", page_icon="🤖", initial_sidebar_state="expanded")

# # Load and Save CSV File
# @st.cache_data
# def load_csv(file_path):
#     return pd.read_csv(file_path)

# def save_csv(data, file_path):
#     data.to_csv(file_path, index=False)

# # Replace with your CSV file path
# csv_file_path = r"\\kor2fs03\V-V--Testing$\03_Validation_Software\LLBP\VALSW_LL_BP_SPL_V1.1.csv"
# csv_data = load_csv(csv_file_path)

# # Function to add new data to the CSV
# def add_to_csv(keyword, asic_module, problem, root_cause, solution):
#     global csv_data  # Use the global variable to keep track of the updated DataFrame
#     new_entry = pd.DataFrame({
#         "Keywords(One word)": [keyword],
#         "ASIC/Module": [asic_module],
#         "Problem": [problem],
#         "Root cause": [root_cause],
#         "Solution": [solution]
#     })
    
#     # Concatenate the new entry to the existing DataFrame
#     csv_data = pd.concat([csv_data, new_entry], ignore_index=True)
#     save_csv(csv_data, csv_file_path)  # Save the updated DataFrame back to the CSV

# def clean_and_split_query(query):
#     filler_words = {'um', 'like', 'you', 'know', 'so', 'well', 'actually', 'basically', 'just', 'really'}
#     stop_words = {'is', 'are', 'was', 'were', 'what', 'who', 'how', 'where', 'when', 'why',
#                   'i', 'me', 'you', 'his', 'her', 'ok', 'bye', 'i am sorry', 'it is what it is', 'it','is','on','over','under','inside','an','a','the', 'does','con',
#                   'get', 'got', 'have', 'had', 'has', 'should', 'not', 'use', 'mobile','team','Team','Verdict','an','no','not','but','T','15','with','off','issues','issue','is','in','the','problems','are','what','why','when','flt','flashing'}
#     cleaned_query = re.sub(r'[^\w\s]', '', query)
#     words = cleaned_query.lower().split()
#     filtered_words = [word for word in words if word not in filler_words and word not in stop_words]
#     return filtered_words

# # Function to get problems based on keyword search
# def get_problems_by_keyword(keywords):
#     search_columns = ['Keywords(One word)', 'ASIC/Module']
#     problem_column = 'Problem'
    
#     # Match the query keywords in the 'Keywords' and 'ASIC/Module' columns
#     matched_problems = pd.DataFrame()
#     for keyword in keywords:
#         matches = csv_data[csv_data[search_columns].apply(lambda row: row.astype(str).str.contains(keyword, case=False).any(), axis=1)]
#         matched_problems = pd.concat([matched_problems, matches])

#     matched_problems = matched_problems.drop_duplicates()
    
#     if not matched_problems.empty:
#         return matched_problems[problem_column].tolist()  # Return a list of problems
#     else:
#         return []

# # Function to get root cause and solution based on the selected problem
# def get_root_cause_and_solution(problem):
#     problem_row = csv_data[csv_data['Problem'] == problem]
#     if not problem_row.empty:
#         root_cause = problem_row['Root cause'].values[0]
#         solution = problem_row['Solution'].values[0]
#         return root_cause, solution
#     return None, None

# def query_csv(query):
#     keywords = clean_and_split_query(query)
#     st.session_state.last_keywords = keywords
#     problems = get_problems_by_keyword(keywords)
    
#     if problems:
#         st.session_state.pending_feedback = True
#         return problems
#     else:
#         return "No problems found for the given keyword."

# # Detect greetings and inappropriate language
# def detect_greeting(query):
#     greetings = {
#         "hi": "Hello! How can I assist you today?",
#         "hello": "Hello! Have a great day.",
#         "hey": "Hello! How can I assist you today?",
#         "good morning": "Good morning! Have a nice day.",
#         "good afternoon": "Good afternoon! Have a great day.",
#         "good evening": "Good evening! Go and have snacks.",
#         "good night": "Good night! Sleep well."
#     }
#     for key, value in greetings.items():
#         if key in query.lower():
#             return value
#     return None

# def detect_inappropriate_language(query):
#     inappropriate_phrases = ["brutal", "badword", "i hate you", "fuck you", "i love you", "i want to marry you"]
#     return any(phrase in query.lower() for phrase in inappropriate_phrases)

# # Modify get_response function for better type handling
# def get_response(query):
#     greeting_response = detect_greeting(query)
#     if greeting_response:
#         return greeting_response

#     if detect_inappropriate_language(query):
#         return "I didn't get you..."

#     if "problems" in query.lower() or "issues" in query.lower():
#         problems = query_csv(query)
#         if isinstance(problems, list) and problems:
#             st.session_state.pending_feedback = True
#             return problems
#         return "No problems found for the given keyword."

#     if "add data" in query.lower():  # Trigger data addition
#         return "Please provide the following information to add new data."

#     return "What do you want to know about this?"

# # Add the title with fire symbol at the top
# st.markdown("<h1 style='text-align: center;'> HitLit 🔥 </h1>", unsafe_allow_html=True)

# # Clear chat option
# if st.button("Clear Chat"):
#     st.session_state.chat_history = []  # Reset chat history
#     st.success("Chat cleared!")

# # User input at the bottom
# user_input = st.text_input("Your message", key="user_input")

# if user_input:
#     st.session_state.chat_history.append(user_input)

#     ai_response = get_response(user_input)

#     if "add data" in user_input.lower():
#         # Collect data for the new entry
#         keyword = st.text_input("Enter Keyword:", key="keyword_input")
#         asic_module = st.text_input("Enter ASIC/Module:", key="asic_module_input")
#         problem = st.text_input("Enter Problem:", key="problem_input")
#         root_cause = st.text_input("Enter Root Cause:", key="root_cause_input")
#         solution = st.text_input("Enter Solution:", key="solution_input")

#         if st.button("Submit New Data"):
#             add_to_csv(keyword, asic_module, problem, root_cause, solution)
#             st.success("Data added successfully!")
#             st.session_state.chat_history.append(f"Added new data: {keyword}, {asic_module}, {problem}, {root_cause}, {solution}")

#     elif isinstance(ai_response, list) and ai_response:
#         # Ensure all problems are strings
#         ai_response = [str(problem) for problem in ai_response]
        
#         # Display the problems as radio buttons
#         selected_problem = st.radio("Select a problem:", options=ai_response, index=0)  # Default selection to first problem
        
#         # Update selected problem
#         st.session_state.selected_problem = selected_problem
        
#         # Ask for feedback after selection
#         st.session_state.chat_history.append(f"Do you want the root cause and solution for '{selected_problem}'?")

#         # Option to get root cause and solution
#         if st.button("Get Root Cause and Solution"):
#             root_cause, solution = get_root_cause_and_solution(selected_problem)
#             if root_cause and solution:
#                 st.write(f"**Root Cause:** {root_cause}")
#                 st.write(f"**Solution:** {solution}")
#                 st.session_state.chat_history.append(f"Root Cause: {root_cause}\nSolution: {solution}")
#             else:
#                 st.write("No root cause and solution found.")

#     else:
#         st.session_state.chat_history.append(ai_response)

# # Display chat history
# for chat in st.session_state.chat_history:
#     st.write(chat)


# import streamlit as st
# import pandas as pd
# import re

# # Initialize session state variables
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
# if "last_keywords" not in st.session_state:
#     st.session_state.last_keywords = []
# if "selected_problem" not in st.session_state:
#     st.session_state.selected_problem = None
# if "pending_feedback" not in st.session_state:
#     st.session_state.pending_feedback = False

# # Set up the Streamlit app
# st.set_page_config(page_title="HitLit", page_icon="🤖", initial_sidebar_state="expanded")

# # Load and Save CSV File
# @st.cache_data
# def load_csv(file_path):
#     return pd.read_csv(file_path)

# def save_csv(data, file_path):
#     data.to_csv(file_path, index=False)

# # Replace with your CSV file path
# csv_file_path = r"\\kor2fs03\V-V--Testing$\03_Validation_Software\LLBP\VALSW_LL_BP_SPL_V1.1.csv"
# csv_data = load_csv(csv_file_path)

# # Function to add new data to the CSV
# def add_to_csv(keyword, asic_module, problem, root_cause, solution):
#     global csv_data  # Use the global variable to keep track of the updated DataFrame
#     new_entry = pd.DataFrame({
#         "Keywords(One word)": [keyword],
#         "ASIC/Module": [asic_module],
#         "Problem": [problem],
#         "Root cause": [root_cause],
#         "Solution": [solution]
#     })
    
#     # Concatenate the new entry to the existing DataFrame
#     csv_data = pd.concat([csv_data, new_entry], ignore_index=True)
#     save_csv(csv_data, csv_file_path)  # Save the updated DataFrame back to the CSV

# def clean_and_split_query(query):
#     filler_words = {'um', 'like', 'you', 'know', 'so', 'well', 'actually', 'basically', 'just', 'really'}
#     stop_words = {'is', 'are', 'was', 'were', 'what', 'who', 'how', 'where', 'when', 'why',
#                   'i', 'me', 'you', 'his', 'her', 'ok', 'bye', 'i am sorry', 'it is what it is', 'it','is','on','over','under','inside','an','a','the', 'does','con',
#                   'get', 'got', 'have', 'had', 'has', 'should', 'not', 'use', 'mobile','team','Team','Verdict','an','no','not','but','T','15','with','off','issues','issue','is','in','the','problems','are','what','why','when','flt','flashing'}
#     cleaned_query = re.sub(r'[^\w\s]', '', query)
#     words = cleaned_query.lower().split()
#     filtered_words = [word for word in words if word not in filler_words and word not in stop_words]
#     return filtered_words

# # Function to get problems based on keyword search
# def get_problems_by_keyword(keywords):
#     search_columns = ['Keywords(One word)', 'ASIC/Module']
#     problem_column = 'Problem'
    
#     # Match the query keywords in the 'Keywords' and 'ASIC/Module' columns
#     matched_problems = pd.DataFrame()
#     for keyword in keywords:
#         matches = csv_data[csv_data[search_columns].apply(lambda row: row.astype(str).str.contains(keyword, case=False).any(), axis=1)]
#         matched_problems = pd.concat([matched_problems, matches])

#     matched_problems = matched_problems.drop_duplicates()
    
#     if not matched_problems.empty:
#         return matched_problems[problem_column].tolist()  # Return a list of problems
#     else:
#         return []

# # Function to get root cause and solution based on the selected problem
# def get_root_cause_and_solution(problem):
#     problem_row = csv_data[csv_data['Problem'] == problem]
#     if not problem_row.empty:
#         root_cause = problem_row['Root cause'].values[0]
#         solution = problem_row['Solution'].values[0]
#         return root_cause, solution
#     return None, None

# def query_csv(query):
#     keywords = clean_and_split_query(query)
#     st.session_state.last_keywords = keywords
#     problems = get_problems_by_keyword(keywords)
    
#     if problems:
#         st.session_state.pending_feedback = True
#         return problems
#     else:
#         return "No problems found for the given keyword."

# # Detect greetings and inappropriate language
# def detect_greeting(query):
#     greetings = {
#         "hi": "Hello! How can I assist you today?",
#         "hello": "Hello! Have a great day.",
#         "hey": "Hello! How can I assist you today?",
#         "good morning": "Good morning! Have a nice day.",
#         "good afternoon": "Good afternoon! Have a great day.",
#         "good evening": "Good evening! Go and have snacks.",
#         "good night": "Good night! Sleep well."
#     }
#     for key, value in greetings.items():
#         if key in query.lower():
#             return value
#     return None

# def detect_inappropriate_language(query):
#     inappropriate_phrases = ["brutal", "badword", "i hate you", "fuck you", "i love you", "i want to marry you"]
#     return any(phrase in query.lower() for phrase in inappropriate_phrases)

# # Modify get_response function for better type handling
# def get_response(query):
#     greeting_response = detect_greeting(query)
#     if greeting_response:
#         return greeting_response

#     if detect_inappropriate_language(query):
#         return "I didn't get you..."

#     if "problems" in query.lower() or "issues" in query.lower():
#         problems = query_csv(query)
#         if isinstance(problems, list) and problems:
#             st.session_state.pending_feedback = True
#             return problems
#         return "No problems found for the given keyword."

#     if "add data" in query.lower():  # Trigger data addition
#         return "Please provide the following information to add new data."

#     return "What do you want to know about this?"

# # Add the title with fire symbol at the top
# st.markdown("<h1 style='text-align: center;'> HitLit 🔥 </h1>", unsafe_allow_html=True)

# # User input at the bottom
# user_input = st.text_input("Your message", key="user_input")

# if user_input:
#     st.session_state.chat_history.append(user_input)

#     ai_response = get_response(user_input)

#     if "add data" in user_input.lower():
#         # Collect data for the new entry
#         keyword = st.text_input("Enter Keyword:", key="keyword_input")
#         asic_module = st.text_input("Enter ASIC/Module:", key="asic_module_input")
#         problem = st.text_input("Enter Problem:", key="problem_input")
#         root_cause = st.text_input("Enter Root Cause:", key="root_cause_input")
#         solution = st.text_input("Enter Solution:", key="solution_input")

#         if st.button("Submit New Data"):
#             add_to_csv(keyword, asic_module, problem, root_cause, solution)
#             st.success("Data added successfully!")
#             st.session_state.chat_history.append(f"Added new data: {keyword}, {asic_module}, {problem}, {root_cause}, {solution}")

#     elif isinstance(ai_response, list) and ai_response:
#         # Ensure all problems are strings
#         ai_response = [str(problem) for problem in ai_response]
        
#         # Display the problems as radio buttons
#         selected_problem = st.radio("Select a problem:", options=ai_response, index=0)  # Default selection to first problem
        
#         # Update selected problem
#         st.session_state.selected_problem = selected_problem
        
#         # Ask for feedback after selection
#         st.session_state.chat_history.append(f"Do you want the root cause and solution for '{selected_problem}'?")

#         # Option to get root cause and solution
#         if st.button("Get Root Cause and Solution"):
#             root_cause, solution = get_root_cause_and_solution(selected_problem)
#             if root_cause and solution:
#                 st.write(f"**Root Cause:** {root_cause}")
#                 st.write(f"**Solution:** {solution}")
#                 st.session_state.chat_history.append(f"Root Cause: {root_cause}\nSolution: {solution}")
#             else:
#                 st.write("No root cause and solution found.")

#     else:
#         st.session_state.chat_history.append(ai_response)

# # Display chat history
# for chat in st.session_state.chat_history:
#     st.write(chat)

# # Clear chat option at the bottom
# if st.button("Clear Chat"):
#     st.session_state.chat_history = []  # Reset chat history
    # st.success("Chat cleared!")


# import streamlit as st
# import pandas as pd
# import re
# from datetime import datetime

# # Initialize session state variables
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
# if "last_keywords" not in st.session_state:
#     st.session_state.last_keywords = []
# if "selected_problem" not in st.session_state:
#     st.session_state.selected_problem = None
# if "pending_feedback" not in st.session_state:
#     st.session_state.pending_feedback = False

# # Set up the Streamlit app
# st.set_page_config(page_title="HitLit", page_icon="🤖", initial_sidebar_state="expanded")

# # Load and Save CSV File
# @st.cache_data
# def load_csv(file_path):
#     return pd.read_csv(file_path)

# def save_csv(data, file_path):
#     data.to_csv(file_path, index=False)

# # Replace with your CSV file path
# csv_file_path = r"\\kor2fs03\V-V--Testing$\03_Validation_Software\LLBP\VALSW_LL_BP_SPL_V1.1.csv"
# csv_data = load_csv(csv_file_path)

# # Function to add new data to the CSV
# def add_to_csv(keyword, asic_module, problem, root_cause, solution, updater_name):
#     global csv_data  # Use the global variable to keep track of the updated DataFrame
#     serial_number = len(csv_data) + 1  # Create a new serial number based on current length
#     date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Get the current date and time
    
#     new_entry = pd.DataFrame({
#         "Serial Number": [serial_number],
#         "Date": [date],
#         "Updated By": [updater_name],
#         "Keywords(One word)": [keyword],
#         "ASIC/Module": [asic_module],
#         "Problem": [problem],
#         "Root cause": [root_cause],
#         "Solution": [solution]
#     })
    
#     # Concatenate the new entry to the existing DataFrame
#     csv_data = pd.concat([csv_data, new_entry], ignore_index=True)
#     save_csv(csv_data, csv_file_path)  # Save the updated DataFrame back to the CSV

# def clean_and_split_query(query):
#     filler_words = {'um', 'like', 'you', 'know', 'so', 'well', 'actually', 'basically', 'just', 'really'}
#     stop_words = {'is', 'are', 'was', 'were', 'what', 'who', 'how', 'where', 'when', 'why',
#                   'i', 'me', 'you', 'his', 'her', 'ok', 'bye', 'i am sorry', 'it is what it is', 'it','is','on','over','under','inside','an','a','the', 'does','con',
#                   'get', 'got', 'have', 'had', 'has', 'should', 'not', 'use', 'mobile','team','Team','Verdict','an','no','not','but','T','15','with','off','issues','issue','is','in','the','problems','are','what','why','when','flt','flashing'}
#     cleaned_query = re.sub(r'[^\w\s]', '', query)
#     words = cleaned_query.lower().split()
#     filtered_words = [word for word in words if word not in filler_words and word not in stop_words]
#     return filtered_words

# # Function to get problems based on keyword search
# def get_problems_by_keyword(keywords):
#     search_columns = ['Keywords(One word)', 'ASIC/Module']
#     problem_column = 'Problem'
    
#     # Match the query keywords in the 'Keywords' and 'ASIC/Module' columns
#     matched_problems = pd.DataFrame()
#     for keyword in keywords:
#         matches = csv_data[csv_data[search_columns].apply(lambda row: row.astype(str).str.contains(keyword, case=False).any(), axis=1)]
#         matched_problems = pd.concat([matched_problems, matches])

#     matched_problems = matched_problems.drop_duplicates()
    
#     if not matched_problems.empty:
#         return matched_problems[problem_column].tolist()  # Return a list of problems
#     else:
#         return []

# # Function to get root cause and solution based on the selected problem
# def get_root_cause_and_solution(problem):
#     problem_row = csv_data[csv_data['Problem'] == problem]
#     if not problem_row.empty:
#         root_cause = problem_row['Root cause'].values[0]
#         solution = problem_row['Solution'].values[0]
#         return root_cause, solution
#     return None, None

# def query_csv(query):
#     keywords = clean_and_split_query(query)
#     st.session_state.last_keywords = keywords
#     problems = get_problems_by_keyword(keywords)
    
#     if problems:
#         st.session_state.pending_feedback = True
#         return problems
#     else:
#         return "No problems found for the given keyword."

# # Detect greetings and inappropriate language
# def detect_greeting(query):
#     greetings = {
#         "hi": "Hello! How can I assist you today?",
#         "hello": "Hello! Have a great day.",
#         "hey": "Hello! How can I assist you today?",
#         "good morning": "Good morning! Have a nice day.",
#         "good afternoon": "Good afternoon! Have a great day.",
#         "good evening": "Good evening! Go and have snacks.",
#         "good night": "Good night! Sleep well."
#     }
#     for key, value in greetings.items():
#         if key in query.lower():
#             return value
#     return None

# def detect_inappropriate_language(query):
#     inappropriate_phrases = ["brutal", "badword", "i hate you", "fuck you", "i love you", "i want to marry you"]
#     return any(phrase in query.lower() for phrase in inappropriate_phrases)

# # Modify get_response function for better type handling
# def get_response(query):
#     greeting_response = detect_greeting(query)
#     if greeting_response:
#         return greeting_response

#     if detect_inappropriate_language(query):
#         return "I didn't get you..."

#     if "problems" in query.lower() or "issues" in query.lower():
#         problems = query_csv(query)
#         if isinstance(problems, list) and problems:
#             st.session_state.pending_feedback = True
#             return problems
#         return "No problems found for the given keyword."

#     if "add data" in query.lower():  # Trigger data addition
#         return "Please provide the following information to add new data."

#     return "What do you want to know about this?"

# # Add the title with fire symbol at the top
# st.markdown("<h1 style='text-align: center;'> HitLit 🔥 </h1>", unsafe_allow_html=True)

# # User input at the bottom
# user_input = st.text_input("Your message", key="user_input")

# if user_input:
#     st.session_state.chat_history.append(user_input)

#     ai_response = get_response(user_input)

#     if "add data" in user_input.lower():
#         # Collect data for the new entry
#         updater_name = st.text_input("Enter Your Name:", key="name_input")
#         keyword = st.text_input("Enter Keyword:", key="keyword_input")
#         asic_module = st.text_input("Enter ASIC/Module:", key="asic_module_input")
#         problem = st.text_input("Enter Problem:", key="problem_input")
#         root_cause = st.text_input("Enter Root Cause:", key="root_cause_input")
#         solution = st.text_input("Enter Solution:", key="solution_input")

#         if st.button("Submit New Data"):
#             add_to_csv(keyword, asic_module, problem, root_cause, solution, updater_name)
#             st.success("Data added successfully!")
#             st.session_state.chat_history.append(f"Added new data: {keyword}, {asic_module}, {problem}, {root_cause}, {solution}")

#     elif isinstance(ai_response, list) and ai_response:
#         # Ensure all problems are strings
#         ai_response = [str(problem) for problem in ai_response]
        
#         # Display the problems as radio buttons
#         selected_problem = st.radio("Select a problem:", options=ai_response, index=0)  # Default selection to first problem
        
#         # Update selected problem
#         st.session_state.selected_problem = selected_problem
        
#         # Ask for feedback after selection
#         st.session_state.chat_history.append(f"Do you want the root cause and solution for '{selected_problem}'?")

#         # Option to get root cause and solution
#         if st.button("Get Root Cause and Solution"):
#             root_cause, solution = get_root_cause_and_solution(selected_problem)
#             if root_cause and solution:
#                 st.write(f"**Root Cause:** {root_cause}")
#                 st.write(f"**Solution:** {solution}")
#                 st.session_state.chat_history.append(f"Root Cause: {root_cause}\nSolution: {solution}")
#             else:
#                 st.write("No root cause and solution found.")

#     else:
#         st.session_state.chat_history.append(ai_response)

# # Display chat history
# if st.session_state.chat_history:
#     for message in st.session_state.chat_history:
#         st.markdown(f"<div style='color: black;'>{message}</div>", unsafe_allow_html=True)

# # Footer message
# st.markdown("<hr><p style='text-align: center;'><small>Made with ❤️ by You</small></p>", unsafe_allow_html=True)


# import streamlit as st
# import pandas as pd
# import re
# from datetime import datetime

# # Initialize session state variables
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
# if "last_keywords" not in st.session_state:
#     st.session_state.last_keywords = []
# if "selected_problem" not in st.session_state:
#     st.session_state.selected_problem = None
# if "pending_feedback" not in st.session_state:
#     st.session_state.pending_feedback = False

# # Set up the Streamlit app
# st.set_page_config(page_title="HitLit", page_icon="🤖", initial_sidebar_state="expanded")

# # Load and Save CSV File
# @st.cache_data
# def load_csv(file_path):
#     return pd.read_csv(file_path)

# def save_csv(data, file_path):
#     data.to_csv(file_path, index=False)

# # Replace with your CSV file path
# csv_file_path = r"\\kor2fs03\V-V--Testing$\03_Validation_Software\LLBP\VALSW_LL_BP_SPL_V1.1.csv"
# csv_data = load_csv(csv_file_path)

# # Function to add new data to the CSV
# def add_to_csv(keyword, asic_module, problem, root_cause, solution, updater_name):
#     global csv_data  # Use the global variable to keep track of the updated DataFrame
#     serial_number = len(csv_data) + 1  # Create a new serial number based on current length
#     date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Get the current date and time
    
#     new_entry = pd.DataFrame({
#         "Serial Number": [serial_number],
#         "Date": [date],
#         "Updated By": [updater_name],
#         "Keywords(One word)": [keyword],
#         "ASIC/Module": [asic_module],
#         "Problem": [problem],
#         "Root cause": [root_cause],
#         "Solution": [solution]
#     })
    
#     # Concatenate the new entry to the existing DataFrame
#     csv_data = pd.concat([csv_data, new_entry], ignore_index=True)
#     save_csv(csv_data, csv_file_path)  # Save the updated DataFrame back to the CSV

# def clean_and_split_query(query):
#     filler_words = {'um', 'like', 'you', 'know', 'so', 'well', 'actually', 'basically', 'just', 'really'}
#     stop_words = {'is', 'are', 'was', 'were', 'what', 'who', 'how', 'where', 'when', 'why',
#                   'i', 'me', 'you', 'his', 'her', 'ok', 'bye', 'i am sorry', 'it is what it is', 'it','is','on','over','under','inside','an','a','the', 'does','con',
#                   'get', 'got', 'have', 'had', 'has', 'should', 'not', 'use', 'mobile','team','Team','Verdict','an','no','not','but','T','15','with','off','issues','issue','is','in','the','problems','are','what','why','when','flt','flashing'}
#     cleaned_query = re.sub(r'[^\w\s]', '', query)
#     words = cleaned_query.lower().split()
#     filtered_words = [word for word in words if word not in filler_words and word not in stop_words]
#     return filtered_words

# # Function to get problems based on keyword search
# def get_problems_by_keyword(keywords):
#     search_columns = ['Keywords(One word)', 'ASIC/Module']
#     problem_column = 'Problem'
    
#     # Match the query keywords in the 'Keywords' and 'ASIC/Module' columns
#     matched_problems = pd.DataFrame()
#     for keyword in keywords:
#         matches = csv_data[csv_data[search_columns].apply(lambda row: row.astype(str).str.contains(keyword, case=False).any(), axis=1)]
#         matched_problems = pd.concat([matched_problems, matches])

#     matched_problems = matched_problems.drop_duplicates()
    
#     if not matched_problems.empty:
#         return matched_problems[problem_column].tolist()  # Return a list of problems
#     else:
#         return []

# # Function to get root cause and solution based on the selected problem
# def get_root_cause_and_solution(problem):
#     problem_row = csv_data[csv_data['Problem'] == problem]
#     if not problem_row.empty:
#         root_cause = problem_row['Root cause'].values[0]
#         solution = problem_row['Solution'].values[0]
#         return root_cause, solution
#     return None, None

# def query_csv(query):
#     keywords = clean_and_split_query(query)
#     st.session_state.last_keywords = keywords
#     problems = get_problems_by_keyword(keywords)
    
#     if problems:
#         st.session_state.pending_feedback = True
#         return problems
#     else:
#         return "No problems found for the given keyword."

# # Detect greetings and inappropriate language
# def detect_greeting(query):
#     greetings = {
#         "hi": "Hello! How can I assist you today?",
#         "hello": "Hello! Have a great day.",
#         "hey": "Hello! How can I assist you today?",
#         "good morning": "Good morning! Have a nice day.",
#         "good afternoon": "Good afternoon! Have a great day.",
#         "good evening": "Good evening! Go and have snacks.",
#         "good night": "Good night! Sleep well."
#     }
#     for key, value in greetings.items():
#         if key in query.lower():
#             return value
#     return None

# def detect_inappropriate_language(query):
#     inappropriate_phrases = ["brutal", "badword", "i hate you", "fuck you", "i love you", "i want to marry you"]
#     return any(phrase in query.lower() for phrase in inappropriate_phrases)

# # Modify get_response function for better type handling
# def get_response(query):
#     greeting_response = detect_greeting(query)
#     if greeting_response:
#         return greeting_response

#     if detect_inappropriate_language(query):
#         return "I didn't get you..."

#     if "problems" in query.lower() or "issues" in query.lower():
#         problems = query_csv(query)
#         if isinstance(problems, list) and problems:
#             st.session_state.pending_feedback = True
#             return problems
#         return "No problems found for the given keyword."

#     if "add data" in query.lower():  # Trigger data addition
#         return "Please provide the following information to add new data."

#     return "What do you want to know about this?"

# # Add the title with fire symbol at the top
# st.markdown("<h1 style='text-align: center;'> HitLit 🔥 </h1>", unsafe_allow_html=True)

# # User input at the bottom
# user_input = st.text_input("Your message", key="user_input")

# if user_input:
#     st.session_state.chat_history.append(user_input)

#     ai_response = get_response(user_input)

#     if "add data" in user_input.lower():
#         # Collect data for the new entry
#         updater_name = st.text_input("Enter Your Name:", key="name_input")
#         keyword = st.text_input("Enter Keyword:", key="keyword_input")
#         asic_module = st.text_input("Enter ASIC/Module:", key="asic_module_input")
#         problem = st.text_input("Enter Problem:", key="problem_input")
#         root_cause = st.text_input("Enter Root Cause:", key="root_cause_input")
#         solution = st.text_input("Enter Solution:", key="solution_input")

#         if st.button("Submit New Data"):
#             add_to_csv(keyword, asic_module, problem, root_cause, solution, updater_name)
#             st.success("Data added successfully!")
#             st.session_state.chat_history.append(f"Added new data: {keyword}, {asic_module}, {problem}, {root_cause}, {solution}")

#     elif isinstance(ai_response, list) and ai_response:
#         # Ensure all problems are strings
#         ai_response = [str(problem) for problem in ai_response]
        
#         # Display the problems as radio buttons
#         selected_problem = st.radio("Select a problem:", options=ai_response, index=0)  # Default selection to first problem
        
#         # Update selected problem
#         st.session_state.selected_problem = selected_problem
        
#         # Ask for feedback after selection
#         st.session_state.chat_history.append(f"Do you want the root cause and solution for '{selected_problem}'?")

#         # Option to get root cause and solution
#         if st.button("Get Root Cause and Solution"):
#             root_cause, solution = get_root_cause_and_solution(selected_problem)
#             if root_cause and solution:
#                 st.write(f"**Root Cause:** {root_cause}")
#                 st.write(f"**Solution:** {solution}")
#                 st.session_state.chat_history.append(f"Root Cause: {root_cause}\nSolution: {solution}")
#             else:
#                 st.write("No root cause and solution found.")

#     else:
#         st.session_state.chat_history.append(ai_response)

# # Display chat history
# if st.session_state.chat_history:
#     for message in st.session_state.chat_history:
#         st.markdown(f"<div style='color: black;'>{message}</div>", unsafe_allow_html=True)

# # Clear chat button
# if st.button("Clear Chat"):
#     st.session_state.chat_history = []  # Clear chat history

# # Footer message
# st.markdown("<hr><p style='text-align: center;'><small>Made with ❤️ by You</small></p>", unsafe_allow_html=True)




# import streamlit as st
# import pandas as pd
# import re
# from datetime import datetime

# # Initialize session state variables
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
# if "last_keywords" not in st.session_state:
#     st.session_state.last_keywords = []
# if "selected_problem" not in st.session_state:
#     st.session_state.selected_problem = None
# if "pending_feedback" not in st.session_state:
#     st.session_state.pending_feedback = False
# if "last_entry_index" not in st.session_state:  # Track the last entry index
#     st.session_state.last_entry_index = None

# # Set up the Streamlit app
# st.set_page_config(page_title="HitLit", page_icon="🤖", initial_sidebar_state="expanded")

# # Load and Save CSV File
# @st.cache_data
# def load_csv(file_path):
#     return pd.read_csv(file_path)

# def save_csv(data, file_path):
#     data.to_csv(file_path, index=False)

# # Replace with your CSV file path
# csv_file_path = r"\\kor2fs03\V-V--Testing$\03_Validation_Software\LLBP\VALSW_LL_BP_SPL_V1.1.csv"
# csv_data = load_csv(csv_file_path)


# # Function to add new data to the CSV
# def add_to_csv(keyword, asic_module, problem, root_cause, solution, updater_name,project):
#     global csv_data  # Use the global variable to keep track of the updated DataFrame
#     serial_number = len(csv_data) + 1  # Create a new serial number based on current length
#     date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Get the current date and time
    
#     new_entry = pd.DataFrame({
#         "Sr. No": [serial_number],
#         "Year": [date],
#         "Author": [updater_name],
#         "Project":[project],
#         "Keywords(One word)": [keyword],
#         "ASIC/Module": [asic_module],
#         "Problem": [problem],
#         "Root cause": [root_cause],
#         "Solution": [solution]
#     })
    
#     # Concatenate the new entry to the existing DataFrame
#     csv_data = pd.concat([csv_data, new_entry], ignore_index=True)
#     save_csv(csv_data, csv_file_path)  # Save the updated DataFrame back to the CSV
#     st.session_state.last_entry_index = len(csv_data) - 1  # Store index of the last entry


# # def delete_last_entry():
# #     if st.session_state.last_entry_index is not None:
# #         # Check if the index is valid before attempting to drop it
# #         if st.session_state.last_entry_index < len(csv_data):
# #             # Remove the last entry based on the stored index
# #             csv_data.drop(csv_data.index[st.session_state.last_entry_index], inplace=True)
# #             save_csv(csv_data, csv_file_path)  # Save the updated DataFrame back to the CSV
# #             st.success("Last entry deleted successfully!")
# #             # Reset last entry index, since we have deleted it
# #             st.session_state.last_entry_index = len(csv_data) - 1 if len(csv_data) > 0 else None  
# #         else:
# #             st.warning("No entry to delete.")
# #     else:
# #         st.warning("No entry to delete.")
        

# def clean_and_split_query(query):
#     filler_words = {'um', 'like', 'you', 'know', 'so', 'well', 'actually', 'basically', 'just', 'really'}
#     stop_words = {'is', 'are', 'was', 'were', 'what', 'who', 'how', 'where', 'when', 'why',
#                   'i', 'me', 'you', 'his', 'her', 'ok', 'bye', 'i am sorry', 'it is what it is', 'it','is','on','over','under','inside','an','a','the', 'does','con',
#                   'get', 'got', 'have', 'had', 'has', 'should', 'not', 'use', 'mobile','team','Team','Verdict','an','no','not','but','T','15','with','off','issues','issue','is','in','the','problems','are','what','why','when','flt','flashing'}
#     cleaned_query = re.sub(r'[^\w\s]', '', query)
#     words = cleaned_query.lower().split()
#     filtered_words = [word for word in words if word not in filler_words and word not in stop_words]
#     return filtered_words

# # Function to get problems based on keyword search
# def get_problems_by_keyword(keywords):
#     search_columns = ['Keywords(One word)', 'ASIC/Module']
#     problem_column = 'Problem'
    
#     # Match the query keywords in the 'Keywords' and 'ASIC/Module' columns
#     matched_problems = pd.DataFrame()
#     for keyword in keywords:
#         matches = csv_data[csv_data[search_columns].apply(lambda row: row.astype(str).str.contains(keyword, case=False).any(), axis=1)]
#         matched_problems = pd.concat([matched_problems, matches])

#     matched_problems = matched_problems.drop_duplicates()
    
#     if not matched_problems.empty:
#         return matched_problems[problem_column].tolist()  # Return a list of problems
#     else:
#         return []

# # Function to get root cause and solution based on the selected problem
# def get_root_cause_and_solution(problem):
#     problem_row = csv_data[csv_data['Problem'] == problem]
#     if not problem_row.empty:
#         root_cause = problem_row['Root cause'].values[0]
#         solution = problem_row['Solution'].values[0]
#         return root_cause, solution
#     return None, None

# def query_csv(query):
#     keywords = clean_and_split_query(query)
#     st.session_state.last_keywords = keywords
#     problems = get_problems_by_keyword(keywords)
    
#     if problems:
#         st.session_state.pending_feedback = True
#         return problems
#     else:
#         return "No problems found for the given keyword."

# # Detect greetings and inappropriate language
# def detect_greeting(query):
#     greetings = {
#         "hi": "Hello! How can I assist you today?",
#         "hello": "Hello! Have a great day.",
#         "hey": "Hello! How can I assist you today?",
#         "good morning": "Good morning! Have a nice day.",
#         "good afternoon": "Good afternoon! Have a great day.",
#         "good evening": "Good evening! Go and have snacks.",
#         "good night": "Good night! Sleep well."
#     }
#     for key, value in greetings.items():
#         if key in query.lower():
#             return value
#     return None

# def detect_inappropriate_language(query):
#     inappropriate_phrases = ["brutal", "badword", "i hate you", "fuck you", "i love you", "i want to marry you"]
#     return any(phrase in query.lower() for phrase in inappropriate_phrases)

# # Modify get_response function for better type handling
# def get_response(query):
#     greeting_response = detect_greeting(query)
#     if greeting_response:
#         return greeting_response

#     if detect_inappropriate_language(query):
#         return "I didn't get you..."

#     if "problems" in query.lower() or "issues" in query.lower():
#         problems = query_csv(query)
#         if isinstance(problems, list) and problems:
#             st.session_state.pending_feedback = True
#             return problems
#         return "No problems found for the given keyword."

#     if "add data" in query.lower():  # Trigger data addition
#         return "Please provide the following information to add new data."

#     return "What do you want to know about this?"

# # Add the title with fire symbol at the top
# st.markdown("<h1 style='text-align: center;'> HitLit 🔥 </h1>", unsafe_allow_html=True)

# # User input at the bottom
# user_input = st.text_input("Your message", key="user_input")

# if user_input:
#     st.session_state.chat_history.append(user_input)

#     ai_response = get_response(user_input)

#     if "add data" in user_input.lower():
#         # Collect data for the new entry
#         updater_name = st.text_input("Enter Your Name:", key="name_input")
#         project = st.text_input("Enter Project Name:", key="project_input")
#         keyword = st.text_input("Enter Keyword:", key="keyword_input")
#         asic_module = st.text_input("Enter ASIC/Module:", key="asic_module_input")
#         problem = st.text_input("Enter Problem:", key="problem_input")
#         root_cause = st.text_input("Enter Root Cause:", key="root_cause_input")
#         solution = st.text_input("Enter Solution:", key="solution_input")

#         # Ensure all inputs are provided before allowing submission
#         if st.button("Submit New Data"):
#             add_to_csv(keyword, asic_module, problem, root_cause, solution, updater_name, project)
#             st.success("Data added successfully!")
#             st.session_state.chat_history.append(f"Added new data: {keyword}, {asic_module}, {problem}, {root_cause}, {solution}")

#         else:
#             st.warning("Please fill in all fields before submitting.")
    
#     elif isinstance(ai_response, list) and ai_response:
#         # Ensure all problems are strings
#         ai_response = [str(problem) for problem in ai_response]
        
#         # Display the problems as radio buttons
#         selected_problem = st.radio("Select a problem:", options=ai_response, key="problem_selection")
#         st.session_state.selected_problem = selected_problem
        
#         # Add thumbs up and down buttons
#         if st.button("👍"):
#             root_cause, solution = get_root_cause_and_solution(selected_problem)
#             if root_cause and solution:
#                 st.success(f"Root Cause: {root_cause}\nSolution: {solution}")
#                 st.session_state.chat_history.append(f"Selected Problem: {selected_problem}\nRoot Cause: {root_cause}\nSolution: {solution}")
#             else:
#                 st.warning("No root cause or solution found.")
#         elif st.button("👎"):
#             st.warning("Feedback noted. Please let me know what went wrong.")

#     st.session_state.chat_history.append(ai_response)

# # # Clear Chat Button at the bottom
# if st.button("Clear Chat"):
#     st.session_state.chat_history = []  # Clear chat history
#     st.success("Chat cleared successfully!")

# # Display chat history
# for msg in st.session_state.chat_history:
#     st.markdown(f"<div style='text-align: left;'>🤖: {msg}</div>", unsafe_allow_html=True)

# # Add a button to delete the last entry
# # if st.button("Delete Last Entry"):
# #     delete_last_entry()


# import streamlit as st
# import pandas as pd
# import re
# from datetime import datetime

# # Initialize session state variables
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
# if "last_keywords" not in st.session_state:
#     st.session_state.last_keywords = []
# if "selected_problem" not in st.session_state:
#     st.session_state.selected_problem = None
# if "pending_feedback" not in st.session_state:
#     st.session_state.pending_feedback = False

# # Set up the Streamlit app
# st.set_page_config(page_title="HitLit", page_icon="🤖", initial_sidebar_state="expanded")

# # Load and Save CSV File
# @st.cache_data
# def load_csv(file_path):
#     return pd.read_csv(file_path)

# def save_csv(data, file_path):
#     data.to_csv(file_path, index=False)

# # Replace with your CSV file path
# csv_file_path = r"\\kor2fs03\V-V--Testing$\03_Validation_Software\LLBP\VALSW_LL_BP_SPL_V1.1.csv"
# csv_data = load_csv(csv_file_path)

# # Function to add new data to the CSV
# def add_to_csv(keyword, asic_module, problem, root_cause, solution, updater_name):
#     global csv_data  # Use the global variable to keep track of the updated DataFrame
#     serial_number = len(csv_data) + 1  # Create a new serial number based on current length
#     date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Get the current date and time
    
#     new_entry = pd.DataFrame({
#         "Serial Number": [serial_number],
#         "Date": [date],
#         "Updated By": [updater_name],
#         "Keywords(One word)": [keyword],
#         "ASIC/Module": [asic_module],
#         "Problem": [problem],
#         "Root cause": [root_cause],
#         "Solution": [solution]
#     })
    
#     # Concatenate the new entry to the existing DataFrame
#     csv_data = pd.concat([csv_data, new_entry], ignore_index=True)
#     save_csv(csv_data, csv_file_path)  # Save the updated DataFrame back to the CSV

# def clean_and_split_query(query):
#     filler_words = {'um', 'like', 'you', 'know', 'so', 'well', 'actually', 'basically', 'just', 'really'}
#     stop_words = {'is', 'are', 'was', 'were', 'what', 'who', 'how', 'where', 'when', 'why',
#                   'i', 'me', 'you', 'his', 'her', 'ok', 'bye', 'i am sorry', 'it is what it is', 'it','is','on','over','under','inside','an','a','the', 'does','con',
#                   'get', 'got', 'have', 'had', 'has', 'should', 'not', 'use', 'mobile','team','Team','Verdict','an','no','not','but','T','15','with','off','issues','issue','is','in','the','problems','are','what','why','when','flt','flashing'}
#     cleaned_query = re.sub(r'[^\w\s]', '', query)
#     words = cleaned_query.lower().split()
#     filtered_words = [word for word in words if word not in filler_words and word not in stop_words]
#     return filtered_words

# # Function to get problems based on keyword search
# def get_problems_by_keyword(keywords):
#     search_columns = ['Keywords(One word)', 'ASIC/Module']
#     problem_column = 'Problem'
    
#     # Match the query keywords in the 'Keywords' and 'ASIC/Module' columns
#     matched_problems = pd.DataFrame()
#     for keyword in keywords:
#         matches = csv_data[csv_data[search_columns].apply(lambda row: row.astype(str).str.contains(keyword, case=False).any(), axis=1)]
#         matched_problems = pd.concat([matched_problems, matches])

#     matched_problems = matched_problems.drop_duplicates()
    
#     if not matched_problems.empty:
#         return matched_problems[problem_column].tolist()  # Return a list of problems
#     else:
#         return []

# # Function to get root cause and solution based on the selected problem
# def get_root_cause_and_solution(problem):
#     problem_row = csv_data[csv_data['Problem'] == problem]
#     if not problem_row.empty:
#         root_cause = problem_row['Root cause'].values[0]
#         solution = problem_row['Solution'].values[0]
#         return root_cause, solution
#     return None, None

# def query_csv(query):
#     keywords = clean_and_split_query(query)
#     st.session_state.last_keywords = keywords
#     problems = get_problems_by_keyword(keywords)
    
#     if problems:
#         st.session_state.pending_feedback = True
#         return problems
#     else:
#         return "No problems found for the given keyword."

# # Detect greetings and inappropriate language
# def detect_greeting(query):
#     greetings = {
#         "hi": "Hello! How can I assist you today?",
#         "hello": "Hello! Have a great day.",
#         "hey": "Hello! How can I assist you today?",
#         "good morning": "Good morning! Have a nice day.",
#         "good afternoon": "Good afternoon! Have a great day.",
#         "good evening": "Good evening! Go and have snacks.",
#         "good night": "Good night! Sleep well."
#     }
#     for key, value in greetings.items():
#         if key in query.lower():
#             return value
#     return None

# def detect_inappropriate_language(query):
#     inappropriate_phrases = ["brutal", "badword", "i hate you", "fuck you", "i love you", "i want to marry you"]
#     return any(phrase in query.lower() for phrase in inappropriate_phrases)

# # Modify get_response function for better type handling
# def get_response(query):
#     greeting_response = detect_greeting(query)
#     if greeting_response:
#         return greeting_response

#     if detect_inappropriate_language(query):
#         return "I didn't get you..."

#     if "problems" in query.lower() or "issues" in query.lower():
#         problems = query_csv(query)
#         if isinstance(problems, list) and problems:
#             st.session_state.pending_feedback = True
#             return problems
#         return "No problems found for the given keyword."

#     if "add data" in query.lower():  # Trigger data addition
#         return "Please provide the following information to add new data."

#     return "What do you want to know about this?"

# # Add the title with fire symbol at the top
# st.markdown("<h1 style='text-align: center;'> HitLit 🔥 </h1>", unsafe_allow_html=True)

# # User input at the bottom
# user_input = st.text_input("Your message", key="user_input")

# if user_input:
#     st.session_state.chat_history.append(user_input)

#     ai_response = get_response(user_input)

#     if "add data" in user_input.lower():
#         # Collect data for the new entry
#         updater_name = st.text_input("Enter Your Name:", key="name_input")
#         keyword = st.text_input("Enter Keyword:", key="keyword_input")
#         asic_module = st.text_input("Enter ASIC/Module:", key="asic_module_input")
#         problem = st.text_input("Enter Problem:", key="problem_input")
#         root_cause = st.text_input("Enter Root Cause:", key="root_cause_input")
#         solution = st.text_input("Enter Solution:", key="solution_input")

#         if st.button("Submit New Data"):
#             add_to_csv(keyword, asic_module, problem, root_cause, solution, updater_name)
#             st.success("Data added successfully!")
#             st.session_state.chat_history.append(f"Added new data: {keyword}, {asic_module}, {problem}, {root_cause}, {solution}")

#     elif isinstance(ai_response, list) and ai_response:
#         # Ensure all problems are strings
#         ai_response = [str(problem) for problem in ai_response]
        
#         # Display the problems as radio buttons
#         selected_problem = st.radio("Select a problem:", options=ai_response, index=0)  # Default selection to first problem
        
#         # Update selected problem
#         # st.session_state.selected_problem = selected_problem
        
#         # Ask for feedback after selection
#         # st.session_state.chat_history.append(f"Do you want the root cause and solution for '{selected_problem}'?")

#         # Option to get root cause and solution
#         if st.button("Get Root Cause and Solution"):
#             root_cause, solution = get_root_cause_and_solution(selected_problem)
#             if root_cause and solution:
#                 st.write(f"**Root Cause:** {root_cause}")
#                 st.write(f"**Solution:** {solution}")
#                 st.session_state.chat_history.append(f"Root Cause: {root_cause}\nSolution: {solution}")
#             else:
#                 st.write("No root cause and solution found.")

#     else:
#         st.session_state.chat_history.append(ai_response)

# # Display chat history
# # if st.session_state.chat_history:
#     # for message in st.session_state.chat_history:
#         # st.markdown(f"<div style='color: black;'>{message}</div>", unsafe_allow_html=True)

# # Clear Chat Button at the bottom
# if st.button("Clear Chat"):
#     st.session_state.chat_history = []  # Clear chat history
#     st.success("Chat cleared successfully!")

# st.markdown("<hr><p style='text-align: center;'><small>Made with ❤️ by You</small></p>", unsafe_allow_html=True)

# import streamlit as st
# import pandas as pd
# import re
# from datetime import datetime

# # Initialize session state variables
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
# if "last_keywords" not in st.session_state:
#     st.session_state.last_keywords = []
# if "selected_problem" not in st.session_state:
#     st.session_state.selected_problem = None
# if "pending_feedback" not in st.session_state:
#     st.session_state.pending_feedback = False

# # Set up the Streamlit app
# st.set_page_config(page_title="HitLit", page_icon="🤖", initial_sidebar_state="expanded")

# # Load and Save CSV File
# @st.cache_data
# def load_csv(file_path):
#     return pd.read_csv(file_path)

# def save_csv(data, file_path):
#     data.to_csv(file_path, index=False)

# # Replace with your CSV file path
# csv_file_path = r"\\kor2fs03\V-V--Testing$\03_Validation_Software\LLBP\VALSW_LL_BP_SPL_V1.1.csv"
# csv_data = load_csv(csv_file_path)

# # Function to add new data to the CSV
# def add_to_csv(keyword, asic_module, problem, root_cause, solution, updater_name):
#     global csv_data
#     serial_number = len(csv_data) + 1
#     date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
#     new_entry = pd.DataFrame({
#         "Serial Number": [serial_number],
#         "Date": [date],
#         "Updated By": [updater_name],
#         "Keywords(One word)": [keyword],
#         "ASIC/Module": [asic_module],
#         "Problem": [problem],
#         "Root cause": [root_cause],
#         "Solution": [solution]
#     })
    
#     csv_data = pd.concat([csv_data, new_entry], ignore_index=True)
#     save_csv(csv_data, csv_file_path)

# def clean_and_split_query(query):
#     filler_words = {'um', 'like', 'you', 'know', 'so', 'well', 'actually', 'basically', 'just', 'really'}
#     stop_words = {'is', 'are', 'was', 'were', 'what', 'who', 'how', 'where', 'when', 'why',
#                   'i', 'me', 'you', 'his', 'her', 'ok', 'bye', 'i am sorry', 'it is what it is', 'it','is','on','over','under','inside','an','a','the', 'does','con',
#                   'get', 'got', 'have', 'had', 'has', 'should', 'not', 'use', 'mobile','team','Team','Verdict','an','no','not','but','T','15','with','off','issues','issue','is','in','the','problems','are','what','why','when','flt','flashing'}
#     cleaned_query = re.sub(r'[^\w\s]', '', query)
#     words = cleaned_query.lower().split()
#     return [word for word in words if word not in filler_words and word not in stop_words]

# # Function to get problems based on keyword search
# def get_problems_by_keyword(keywords):
#     search_columns = ['Keywords(One word)', 'ASIC/Module']
#     problem_column = 'Problem'
#     matched_problems = pd.DataFrame()

#     for keyword in keywords:
#         matches = csv_data[csv_data[search_columns].apply(lambda row: row.astype(str).str.contains(keyword, case=False).any(), axis=1)]
#         matched_problems = pd.concat([matched_problems, matches])
    
#     matched_problems = matched_problems.drop_duplicates()
#     return matched_problems[problem_column].tolist() if not matched_problems.empty else []

# # Function to get root cause and solution based on the selected problem
# def get_root_cause_and_solution(problem):
#     problem_row = csv_data[csv_data['Problem'] == problem]
#     if not problem_row.empty:
#         return problem_row['Root cause'].values[0], problem_row['Solution'].values[0]
#     return None, None

# def query_csv(query):
#     keywords = clean_and_split_query(query)
#     st.session_state.last_keywords = keywords
#     problems = get_problems_by_keyword(keywords)
#     return problems if problems else "No problems found for the given keyword."

# def detect_greeting(query):
#     greetings = {
#         "hi": "Hello! How can I assist you today?",
#         "good morning": "Good morning! Have a nice day.",
#         "good afternoon": "Good afternoon! Have a great day.",
#         "good evening": "Good evening! Go and have snacks.",
#         "good night": "Good night! Sleep well."
#     }
#     for key, value in greetings.items():
#         if key in query.lower():
#             return value
#     return None

# def get_response(query):
#     greeting_response = detect_greeting(query)
#     if greeting_response:
#         return greeting_response

#     if "problems" in query.lower() or "issues" in query.lower():
#         return query_csv(query)

#     if "add data" in query.lower():
#         return "Please provide the following information to add new data."
    
#     return "What do you want to know about this?"

# st.markdown("<h1 style='text-align: center;'> HitLit 🔥 </h1>", unsafe_allow_html=True)

# # User input at the bottom
# user_input = st.text_input("Your message", key="user_input")

# if user_input:
#     st.session_state.chat_history.append(user_input)
#     ai_response = get_response(user_input)

#     if "add data" in user_input.lower():
#         updater_name = st.text_input("Enter Your Name:", placeholder="e.g. John Doe", key="name_input")
#         keyword = st.text_input("Enter Keyword:", placeholder="e.g. Error Code 123", key="keyword_input")
#         asic_module = st.text_input("Enter ASIC/Module:", placeholder="e.g. Module XYZ", key="asic_module_input")
#         problem = st.text_input("Enter Problem:", placeholder="Describe the issue", key="problem_input")
#         root_cause = st.text_input("Enter Root Cause:", placeholder="Explain the root cause", key="root_cause_input")
#         solution = st.text_input("Enter Solution:", placeholder="Provide the solution", key="solution_input")

#         if st.button("Submit New Data"):
#             add_to_csv(keyword, asic_module, problem, root_cause, solution, updater_name)
#             st.success("Data added successfully!")
#             st.session_state.chat_history.append(f"Added new data: {keyword}, {asic_module}, {problem}")

#     elif isinstance(ai_response, list):
#         selected_problem = st.selectbox("Select a problem:", options=ai_response)
#         if st.button("Get Root Cause and Solution"):
#             root_cause, solution = get_root_cause_and_solution(selected_problem)
#             if root_cause and solution:
#                 st.write(f"**Root Cause:** {root_cause}")
#                 st.write(f"**Solution:** {solution}")
#                 st.session_state.chat_history.append(f"Root Cause: {root_cause}\nSolution: {solution}")
#             else:
#                 st.write("No root cause and solution found.")

#     else:
#         st.session_state.chat_history.append(ai_response)

# # Clear Chat Button at the bottom
# if st.button("Clear Chat"):
#     st.session_state.chat_history = []
#     st.success("Chat cleared successfully!")

# st.markdown("<hr><p style='text-align: center;'><small>Made with ❤️ by You</small></p>", unsafe_allow_html=True)




# import streamlit as st
# import pandas as pd
# import re
# from datetime import datetime
# import fitz  # PyMuPDF for PDF handling

# # Initialize session state variables
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
# if "last_keywords" not in st.session_state:
#     st.session_state.last_keywords = []
# if "selected_problem" not in st.session_state:
#     st.session_state.selected_problem = None
# if "pdf_text" not in st.session_state:
#     st.session_state.pdf_text = ""

# # Set up the Streamlit app
# st.set_page_config(page_title="HitLit", page_icon="🤖", initial_sidebar_state="expanded")

# # Load and Save CSV File
# @st.cache_data
# def load_csv(file_path):
#     return pd.read_csv(file_path)

# def save_csv(data, file_path):
#     data.to_csv(file_path, index=False)

# # Replace with your CSV file path
# csv_file_path = r"\\kor2fs03\V-V--Testing$\03_Validation_Software\LLBP\VALSW_LL_BP_SPL_V1.1.csv"
# csv_data = load_csv(csv_file_path)

# # Function to read PDF
# def read_pdf(file_path):
#     pdf_text = ""
#     with fitz.open(file_path) as doc:
#         for page in doc:
#             pdf_text += page.get_text()
#     return pdf_text

# # Load PDF and store text in session state
# pdf_file_path = r"\\kor2fs03\V-V--Testing$\03_Validation_Software\LLBP\PDFs"  # Replace with the actual path to your PDF file
# if not st.session_state.pdf_text:
#     st.session_state.pdf_text = read_pdf(pdf_file_path)

# # Function to add new data to the CSV
# def add_to_csv(keyword, asic_module, problem, root_cause, solution, updater_name):
#     global csv_data
#     serial_number = len(csv_data) + 1
#     date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
#     new_entry = pd.DataFrame({
#         "Serial Number": [serial_number],
#         "Date": [date],
#         "Updated By": [updater_name],
#         "Keywords(One word)": [keyword],
#         "ASIC/Module": [asic_module],
#         "Problem": [problem],
#         "Root cause": [root_cause],
#         "Solution": [solution]
#     })
    
#     csv_data = pd.concat([csv_data, new_entry], ignore_index=True)
#     save_csv(csv_data, csv_file_path)

# def clean_and_split_query(query):
#     filler_words = {'um', 'like', 'you', 'know', 'so', 'well', 'actually', 'basically', 'just', 'really'}
#     stop_words = {'is', 'are', 'was', 'were', 'what', 'who', 'how', 'where', 'when', 'why',
#                   'i', 'me', 'you', 'his', 'her', 'ok', 'bye', 'i am sorry', 'it is what it is', 'it','is','on','over','under','inside','an','a','the', 'does','con',
#                   'get', 'got', 'have', 'had', 'has', 'should', 'not', 'use', 'mobile','team','Team','Verdict','an','no','not','but','T','15','with','off','issues','issue','is','in','the','problems','are','what','why','when','flt','flashing'}
#     cleaned_query = re.sub(r'[^\w\s]', '', query)
#     words = cleaned_query.lower().split()
#     return [word for word in words if word not in filler_words and word not in stop_words]

# # Function to get problems based on keyword search
# def get_problems_by_keyword(keywords):
#     search_columns = ['Keywords(One word)', 'ASIC/Module']
#     problem_column = 'Problem'
#     matched_problems = pd.DataFrame()

#     for keyword in keywords:
#         matches = csv_data[csv_data[search_columns].apply(lambda row: row.astype(str).str.contains(rf'\b{keyword}\b', case=False).any(), axis=1)]
#         matched_problems = pd.concat([matched_problems, matches])
    
#     matched_problems = matched_problems.drop_duplicates()
#     return matched_problems[problem_column].tolist() if not matched_problems.empty else []

# # Function to get root cause and solution based on the selected problem
# def get_root_cause_and_solution(problem):
#     problem_row = csv_data[csv_data['Problem'] == problem]
#     if not problem_row.empty:
#         return problem_row['Root cause'].values[0], problem_row['Solution'].values[0]
#     return None, None

# def query_csv(query):
#     keywords = clean_and_split_query(query)
#     st.session_state.last_keywords = keywords
#     problems = get_problems_by_keyword(keywords)
#     return problems if problems else "No problems found for the given keyword."

# def detect_greeting(query):
#     greetings = {
#         "hi": "Hello! How can I assist you today?",
#         "good morning": "Good morning! Have a nice day.",
#         "good afternoon": "Good afternoon! Have a great day.",
#         "good evening": "Good evening! Go and have snacks.",
#         "good night": "Good night! Sleep well."
#     }
#     for key, value in greetings.items():
#         if key in query.lower():
#             return value
#     return None

# def pdf_query_response(query):
#     # Search PDF text for the query
#     if query.lower() in st.session_state.pdf_text.lower():
#         return f"I found some information in the PDF regarding '{query}'."
#     return "Sorry, I couldn't find any relevant information in the PDF."

# def get_response(query):
#     greeting_response = detect_greeting(query)
#     if greeting_response:
#         return greeting_response

#     # First check the PDF for information
#     pdf_response = pdf_query_response(query)
#     if pdf_response:
#         return pdf_response

#     # Check for keywords directly if not a greeting
#     problems = query_csv(query)
#     if isinstance(problems, list) and problems:
#         return problems

#     if "add data" in query.lower():
#         return "Please provide the following information to add new data."
    
#     return "What do you want to know about this?"

# st.markdown("<h1 style='text-align: center;'> HitLit 🔥 </h1>", unsafe_allow_html=True)

# # User input at the bottom
# user_input = st.text_input("Your message", key="user_input")

# if user_input:
#     st.session_state.chat_history.append(user_input)
#     ai_response = get_response(user_input)

#     if "add data" in user_input.lower():
#         updater_name = st.text_input("Enter Your Name:", placeholder="e.g. John Doe", key="name_input")
#         keyword = st.text_input("Enter Keyword:", placeholder="e.g. Error Code 123", key="keyword_input")
#         asic_module = st.text_input("Enter ASIC/Module:", placeholder="e.g. Module XYZ", key="asic_module_input")
#         problem = st.text_input("Enter Problem:", placeholder="Describe the issue", key="problem_input")
#         root_cause = st.text_input("Enter Root Cause:", placeholder="Explain the root cause", key="root_cause_input")
#         solution = st.text_input("Enter Solution:", placeholder="Provide the solution", key="solution_input")

#         if st.button("Submit New Data"):
#             add_to_csv(keyword, asic_module, problem, root_cause, solution, updater_name)
#             st.success("Data added successfully!")
#             st.session_state.chat_history.append(f"Added new data: {keyword}, {asic_module}, {problem}")

#     elif isinstance(ai_response, list):
#         selected_problem = st.selectbox("Select a problem:", options=ai_response)
#         if st.button("Get Root Cause and Solution"):
#             root_cause, solution = get_root_cause_and_solution(selected_problem)
#             if root_cause and solution:
#                 st.write(f"**Root Cause:** {root_cause}")
#                 st.write(f"**Solution:** {solution}")
#                 st.session_state.chat_history.append(f"Root Cause: {root_cause}\nSolution: {solution}")
#             else:
#                 st.write("No root cause and solution found.")

#     else:
#         st.session_state.chat_history.append(ai_response)

# # Clear Chat Button at the bottom
# if st.button("Clear Chat"):
#     st.session_state.chat_history = []
#     st.success("Chat cleared successfully!")

# st.markdown("<hr><p style='text-align: center;'><small>Made with ❤️ by You</small></p>", unsafe_allow_html=True)


# # import os
# # import streamlit as st
# # import pandas as pd
# # import re
# # from datetime import datetime
# # import fitz  # PyMuPDF for PDF handling

# # # Initialize session state variables
# # if "chat_history" not in st.session_state:
# #     st.session_state.chat_history = []
# # if "last_keywords" not in st.session_state:
# #     st.session_state.last_keywords = []
# # if "selected_problem" not in st.session_state:
# #     st.session_state.selected_problem = None
# # if "pdf_text" not in st.session_state:
# #     st.session_state.pdf_text = ""

# # # Set up the Streamlit app
# # st.set_page_config(page_title="HitLit", page_icon="🤖", initial_sidebar_state="expanded")

# # # Load and Save CSV File
# # @st.cache_data
# # def load_csv(file_path):
# #     return pd.read_csv(file_path)

# # def save_csv(data, file_path):
# #     data.to_csv(file_path, index=False)

# # # Replace with your CSV file path
# # csv_file_path = r"\\kor2fs03\V-V--Testing$\03_Validation_Software\LLBP\VALSW_LL_BP_SPL_V1.1.csv"
# # csv_data = load_csv(csv_file_path)

# # # Function to read PDF
# # def read_pdf(file_path):
# #     pdf_text = ""
# #     with fitz.open(file_path) as doc:
# #         for page in doc:
# #             pdf_text += page.get_text()
# #     return pdf_text

# # # Function to find PDFs based on keyword
# # def find_pdf_by_keyword(keyword, pdf_directory):
# #     pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]
# #     matching_files = [f for f in pdf_files if keyword.lower() in f.lower()]
# #     return matching_files

# # # Load PDF and store text in session state
# # pdf_directory =r"\\kor2fs03\V-V--Testing$\03_Validation_Software\LLBP\PDFs"  # Replace with the actual path to your PDF file
# # selected_pdf_file = None

# # # Function to add new data to the CSV
# # def add_to_csv(keyword, asic_module, problem, root_cause, solution, updater_name):
# #     global csv_data
# #     serial_number = len(csv_data) + 1
# #     date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
# #     new_entry = pd.DataFrame({
# #         "Serial Number": [serial_number],
# #         "Date": [date],
# #         "Updated By": [updater_name],
# #         "Keywords(One word)": [keyword],
# #         "ASIC/Module": [asic_module],
# #         "Problem": [problem],
# #         "Root cause": [root_cause],
# #         "Solution": [solution]
# #     })
    
# #     csv_data = pd.concat([csv_data, new_entry], ignore_index=True)
# #     save_csv(csv_data, csv_file_path)

# # def clean_and_split_query(query):
# #     filler_words = {'um', 'like', 'you', 'know', 'so', 'well', 'actually', 'basically', 'just', 'really'}
# #     stop_words = {'is', 'are', 'was', 'were', 'what', 'who', 'how', 'where', 'when', 'why',
# #                   'i', 'me', 'you', 'his', 'her', 'ok', 'bye', 'i am sorry', 'it is what it is', 'it','is','on','over','under','inside','an','a','the', 'does','con',
# #                   'get', 'got', 'have', 'had', 'has', 'should', 'not', 'use', 'mobile','team','Team','Verdict','an','no','not','but','T','15','with','off','issues','issue','is','in','the','problems','are','what','why','when','flt','flashing'}
# #     cleaned_query = re.sub(r'[^\w\s]', '', query)
# #     words = cleaned_query.lower().split()
# #     return [word for word in words if word not in filler_words and word not in stop_words]

# # # Function to get problems based on keyword search
# # def get_problems_by_keyword(keywords):
# #     search_columns = ['Keywords(One word)', 'ASIC/Module']
# #     problem_column = 'Problem'
# #     matched_problems = pd.DataFrame()

# #     for keyword in keywords:
# #         matches = csv_data[csv_data[search_columns].apply(lambda row: row.astype(str).str.contains(rf'\b{keyword}\b', case=False).any(), axis=1)]
# #         matched_problems = pd.concat([matched_problems, matches])
    
# #     matched_problems = matched_problems.drop_duplicates()
# #     return matched_problems[problem_column].tolist() if not matched_problems.empty else []

# # # Function to get root cause and solution based on the selected problem
# # def get_root_cause_and_solution(problem):
# #     problem_row = csv_data[csv_data['Problem'] == problem]
# #     if not problem_row.empty:
# #         return problem_row['Root cause'].values[0], problem_row['Solution'].values[0]
# #     return None, None

# # def query_csv(query):
# #     keywords = clean_and_split_query(query)
# #     st.session_state.last_keywords = keywords
# #     problems = get_problems_by_keyword(keywords)
# #     return problems if problems else "No problems found for the given keyword."

# # def detect_greeting(query):
# #     greetings = {
# #         "hi": "Hello! How can I assist you today?",
# #         "good morning": "Good morning! Have a nice day.",
# #         "good afternoon": "Good afternoon! Have a great day.",
# #         "good evening": "Good evening! Go and have snacks.",
# #         "good night": "Good night! Sleep well."
# #     }
# #     for key, value in greetings.items():
# #         if key in query.lower():
# #             return value
# #     return None

# # def pdf_query_response(query):
# #     global selected_pdf_file
# #     if selected_pdf_file:
# #         pdf_text = read_pdf(os.path.join(pdf_directory, selected_pdf_file))
# #         if query.lower() in pdf_text.lower():
# #             return f"I found some information in the PDF regarding '{query}'."
# #     return "Sorry, I couldn't find any relevant information in the PDF."

# # def get_response(query):
# #     greeting_response = detect_greeting(query)
# #     if greeting_response:
# #         return greeting_response

# #     # Find matching PDF files based on the keywords
# #     keywords = clean_and_split_query(query)
# #     for keyword in keywords:
# #         matching_pdfs = find_pdf_by_keyword(keyword, pdf_directory)
# #         if matching_pdfs:
# #             selected_pdf_file = matching_pdfs[0]  # Select the first matching PDF
# #             break

# #     # First check the PDF for information
# #     pdf_response = pdf_query_response(query)
# #     if pdf_response:
# #         return pdf_response

# #     # Check for keywords directly if not a greeting
# #     problems = query_csv(query)
# #     if isinstance(problems, list) and problems:
# #         return problems

# #     if "add data" in query.lower():
# #         return "Please provide the following information to add new data."
    
# #     return "What do you want to know about this?"

# # st.markdown("<h1 style='text-align: center;'> HitLit 🔥 </h1>", unsafe_allow_html=True)

# # # User input at the bottom
# # user_input = st.text_input("Your message", key="user_input")

# # if user_input:
# #     st.session_state.chat_history.append(user_input)
# #     ai_response = get_response(user_input)

# #     if "add data" in user_input.lower():
# #         updater_name = st.text_input("Enter Your Name:", placeholder="e.g. John Doe", key="name_input")
# #         keyword = st.text_input("Enter Keyword:", placeholder="e.g. Error Code 123", key="keyword_input")
# #         asic_module = st.text_input("Enter ASIC/Module:", placeholder="e.g. Module XYZ", key="asic_module_input")
# #         problem = st.text_input("Enter Problem:", placeholder="Describe the issue", key="problem_input")
# #         root_cause = st.text_input("Enter Root Cause:", placeholder="Explain the root cause", key="root_cause_input")
# #         solution = st.text_input("Enter Solution:", placeholder="Provide the solution", key="solution_input")

# #         if st.button("Submit New Data"):
# #             add_to_csv(keyword, asic_module, problem, root_cause, solution, updater_name)
# #             st.success("Data added successfully!")
# #             st.session_state.chat_history.append(f"Added new data: {keyword}, {asic_module}, {problem}")

# #     elif isinstance(ai_response, list):
# #         selected_problem = st.selectbox("Select a problem:", options=ai_response)
# #         if st.button("Get Root Cause and Solution"):
# #             root_cause, solution = get_root_cause_and_solution(selected_problem)
# #             if root_cause and solution:
# #                 st.write(f"**Root Cause:** {root_cause}")
# #                 st.write(f"**Solution:** {solution}")
# #                 st.session_state.chat_history.append(f"Root Cause: {root_cause}\nSolution: {solution}")
# #             else:
# #                 st.write("No root cause and solution found.")

# #     else:
# #         st.session_state.chat_history.append(ai_response)

# # # # Clear Chat Button at the bottom
# # # if st.button("Clear Chat"):
# # #     st.session_state.chat_history = []
# # #     st.session_state.selected_problem = None

# # # Display chat history
# # # for message in st.session_state.chat_history:
# # #     st.write(message)

# # # Clear Chat Button at the bottom
# # if st.button("Clear Chat"):
# #     st.session_state.chat_history = []
# #     st.success("Chat cleared successfully!")

# # st.markdown("<hr><p style='text-align: center;'><small>Made with ❤️ by You</small></p>", unsafe_allow_html=True)


# import os
# import streamlit as st
# import pandas as pd
# import re
# from datetime import datetime
# import fitz  # PyMuPDF for PDF handling

# # Initialize session state variables
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
# if "last_keywords" not in st.session_state:
#     st.session_state.last_keywords = []
# if "selected_problem" not in st.session_state:
#     st.session_state.selected_problem = None
# if "pdf_text" not in st.session_state:
#     st.session_state.pdf_text = ""

# # Set up the Streamlit app
# st.set_page_config(page_title="HitLit", page_icon="🤖", initial_sidebar_state="expanded")

# # Load and Save CSV File
# @st.cache_data
# def load_csv(file_path):
#     return pd.read_csv(file_path)

# def save_csv(data, file_path):
#     data.to_csv(file_path, index=False)

# # Replace with your CSV file path
# csv_file_path = r"\\kor2fs03\V-V--Testing$\03_Validation_Software\LLBP\VALSW_LL_BP_SPL_V1.1.csv"
# csv_data = load_csv(csv_file_path)

# # Function to read PDF
# def read_pdf(file_path):
#     pdf_text = ""
#     with fitz.open(file_path) as doc:
#         for page in doc:
#             pdf_text += page.get_text()
#     return pdf_text

# # Function to find PDFs based on keyword
# def find_pdf_by_keyword(keyword, pdf_directory):
#     pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]
#     matching_files = [f for f in pdf_files if keyword.lower() in f.lower()]
#     return matching_files

# # Load PDF and store text in session state
# pdf_directory = r"\\kor2fs03\V-V--Testing$\03_Validation_Software\LLBP\PDFs"  # Replace with the actual path to your PDF file
# selected_pdf_file = None

# # Function to add new data to the CSV
# def add_to_csv(keyword, asic_module, problem, root_cause, solution, updater_name):
#     global csv_data
#     serial_number = len(csv_data) + 1
#     date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
#     new_entry = pd.DataFrame({
#         "Serial Number": [serial_number],
#         "Date": [date],
#         "Updated By": [updater_name],
#         "Keywords(One word)": [keyword],
#         "ASIC/Module": [asic_module],
#         "Problem": [problem],
#         "Root cause": [root_cause],
#         "Solution": [solution]
#     })
    
#     csv_data = pd.concat([csv_data, new_entry], ignore_index=True)
#     save_csv(csv_data, csv_file_path)

# def clean_and_split_query(query):
#     filler_words = {'um', 'like', 'you', 'know', 'so', 'well', 'actually', 'basically', 'just', 'really'}
#     stop_words = {'is', 'are', 'was', 'were', 'what', 'who', 'how', 'where', 'when', 'why',
#                   'i', 'me', 'you', 'his', 'her', 'ok', 'bye', 'i am sorry', 'it is what it is', 
#                   'it', 'is', 'on', 'over', 'under', 'inside', 'an', 'a', 'the', 'does', 'con',
#                   'get', 'got', 'have', 'had', 'has', 'should', 'not', 'use', 'mobile', 'team', 
#                   'Team', 'Verdict', 'an', 'no', 'not', 'but', 'T', '15', 'with', 'off', 
#                    'is', 'in', 'the', 'problems', 'are', 'what', 'why', 
#                   'when', 'flt', 'flashing'}
#     cleaned_query = re.sub(r'[^\w\s]', '', query)
#     words = cleaned_query.lower().split()
#     return [word for word in words if word not in filler_words and word not in stop_words]

# # Function to get problems based on keyword search
# def get_problems_by_keyword(keywords):
#     search_columns = ['Keywords(One word)', 'ASIC/Module']
#     problem_column = 'Problem'
#     matched_problems = pd.DataFrame()

#     for keyword in keywords:
#         matches = csv_data[csv_data[search_columns].apply(lambda row: row.astype(str).str.contains(rf'\b{keyword}\b', case=False).any(), axis=1)]
#         matched_problems = pd.concat([matched_problems, matches])
    
#     matched_problems = matched_problems.drop_duplicates()
#     return matched_problems[problem_column].tolist() if not matched_problems.empty else []

# # Function to get root cause and solution based on the selected problem
# def get_root_cause_and_solution(problem):
#     problem_row = csv_data[csv_data['Problem'] == problem]
#     if not problem_row.empty:
#         return problem_row['Root cause'].values[0], problem_row['Solution'].values[0]
#     return None, None

# def query_csv(query):
#     keywords = clean_and_split_query(query)
#     st.session_state.last_keywords = keywords
#     problems = get_problems_by_keyword(keywords)
#     return problems if problems else "No problems found for the given keyword."

# def detect_greeting(query):
#     greetings = {
#         "hi": "Hello! How can I assist you today?",
#         "good morning": "Good morning! Have a nice day.",
#         "good afternoon": "Good afternoon! Have a great day.",
#         "good evening": "Good evening! Go and have snacks.",
#         "good night": "Good night! Sleep well."
#     }
#     for key, value in greetings.items():
#         if key in query.lower():
#             return value
#     return None

# # Function to find PDFs based on keyword and set the selected PDF for searching
# def find_and_set_pdf_by_keyword(keyword, pdf_directory):
#     global selected_pdf_file
#     pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]
#     matching_files = [f for f in pdf_files if keyword.lower() in f.lower()]
#     if matching_files:
#         selected_pdf_file = matching_files[0]  # Select the first matching PDF
#         return True
#     return False

# # Function to refine the query response to extract selective information from PDF
# def pdf_query_response(query):
#     global selected_pdf_file
#     if selected_pdf_file:
#         pdf_text = ""
#         with fitz.open(os.path.join(pdf_directory, selected_pdf_file)) as doc:
#             for page_num, page in enumerate(doc):
#                 if page_num >= 15:  # Limit the search to the first 15 pages
#                     break
#                 pdf_text += page.get_text()

#         # Search for the keyword in the extracted text from the first 15 pages
#         matched_text = []
#         keyword_pattern = re.compile(re.escape(query), re.IGNORECASE)
#         for match in keyword_pattern.finditer(pdf_text):
#             start = max(0, match.start() - 50)  # Include some context before the match
#             end = min(len(pdf_text), match.end() + 50)  # Include some context after the match
#             matched_text.append(pdf_text[start:end])

#         # Return the matched excerpts if found, or an appropriate message if not
#         if matched_text:
#             return "\n\n".join(matched_text[:5])  # Provide the first 5 matched excerpts
#         else:
#             return f"Sorry, I couldn't find any relevant information about '{query}' in the first 15 pages of the PDF."
#     return "No PDF selected for searching."

# # Enhanced Response Handling Function
# def get_response(query):
#     greeting_response = detect_greeting(query)
#     if greeting_response:
#         return greeting_response

#     # Check for synonyms of "problems" or "issues" in the query
#     keywords = clean_and_split_query(query)
#     if any(keyword in ['problems', 'issues', 'difficulties', 'challenges'] for keyword in keywords):
#         # Prioritize CSV search for these queries
#         problems = query_csv(query)
#         if isinstance(problems, list) and problems:
#             return problems

#     # Prioritize finding a matching PDF datasheet based on keywords
#     for keyword in keywords:
#         if find_and_set_pdf_by_keyword(keyword, pdf_directory):
#             break

#     # Check if PDF information can be retrieved
#     pdf_response = pdf_query_response(query)
#     if pdf_response:
#         return pdf_response

#     # Fallback to searching CSV if no PDF matches were found
#     problems = query_csv(query)
#     if isinstance(problems, list) and problems:
#         return problems

#     if "add data" in query.lower():
#         return "Please provide the following information to add new data."
    
#     return "What do you want to know about this?"



# st.markdown("<h1 style='text-align: center;'> HitLit 🔥 </h1>", unsafe_allow_html=True)

# # User input at the bottom
# user_input = st.text_input("Your message", key="user_input")

# if user_input:
#     st.session_state.chat_history.append(user_input)
#     ai_response = get_response(user_input)

#     if "add data" in user_input.lower():
#         updater_name = st.text_input("Enter Your Name:", placeholder="e.g. John Doe", key="name_input")
#         keyword = st.text_input("Enter Keyword:", placeholder="e.g. Error Code 123", key="keyword_input")
#         asic_module = st.text_input("Enter ASIC/Module:", placeholder="e.g. Module XYZ", key="asic_module_input")
#         problem = st.text_input("Enter Problem:", placeholder="Describe the issue", key="problem_input")
#         root_cause = st.text_input("Enter Root Cause:", placeholder="Explain the root cause", key="root_cause_input")
#         solution = st.text_input("Enter Solution:", placeholder="Provide the solution", key="solution_input")

#         if st.button("Submit New Data"):
#             add_to_csv(keyword, asic_module, problem, root_cause, solution, updater_name)
#             st.success("Data added successfully!")
#             st.session_state.chat_history.append(f"Added new data: {keyword}, {asic_module}, {problem}")

#     elif isinstance(ai_response, list):
#         selected_problem = st.selectbox("Select a problem:", options=ai_response)
#         if st.button("Get Root Cause and Solution"):
#             root_cause, solution = get_root_cause_and_solution(selected_problem)
#             if root_cause and solution:
#                 st.write(f"**Root Cause:** {root_cause}")
#                 st.write(f"**Solution:** {solution}")
#                 st.session_state.chat_history.append(f"Root Cause: {root_cause}, Solution: {solution}")
#             else:
#                 st.write("No root cause or solution found for the selected problem.")

#     st.session_state.chat_history.append(ai_response)
    
# # Display chat history
# # for msg in st.session_state.chat_history:
# #     st.write(msg)

# # Clear Chat Button at the bottom
# if st.button("Clear Chat"):
#     st.session_state.chat_history = []
#     st.success("Chat cleared successfully!")

# st.markdown("<hr><p style='text-align: center;'><small>Made with ❤️ by You</small></p>", unsafe_allow_html=True)


# import streamlit as st
# import pandas as pd
# import re
# from datetime import datetime

# # Initialize session state variables
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
# if "last_keywords" not in st.session_state:
#     st.session_state.last_keywords = []
# if "selected_problem" not in st.session_state:
#     st.session_state.selected_problem = None
# if "pending_feedback" not in st.session_state:
#     st.session_state.pending_feedback = False

# # Set up the Streamlit app
# st.set_page_config(page_title="HitLit", page_icon="🤖", initial_sidebar_state="expanded")

# # Load and Save CSV File
# @st.cache_data
# def load_csv(file_path):
#     return pd.read_csv(file_path)

# def save_csv(data, file_path):
#     data.to_csv(file_path, index=False)

# # Replace with your CSV file path
# csv_file_path = r"\\kor2fs03\V-V--Testing$\03_Validation_Software\LLBP\VALSW_LL_BP_SPL_V1.1.csv"
# csv_data = load_csv(csv_file_path)

# # Function to add new data to the CSV
# def add_to_csv(keyword, asic_module, problem, root_cause, solution, updater_name):
#     global csv_data
#     serial_number = len(csv_data) + 1
#     date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
#     new_entry = pd.DataFrame({
#         "Serial Number": [serial_number],
#         "Date": [date],
#         "Updated By": [updater_name],
#         "Keywords(One word)": [keyword],
#         "ASIC/Module": [asic_module],
#         "Problem": [problem],
#         "Root cause": [root_cause],
#         "Solution": [solution]
#     })
    
#     csv_data = pd.concat([csv_data, new_entry], ignore_index=True)
#     save_csv(csv_data, csv_file_path)

# def clean_and_split_query(query):
#     filler_words = {'um', 'like', 'you', 'know', 'so', 'well', 'actually', 'basically', 'just', 'really'}
#     stop_words = {'is', 'are', 'was', 'were', 'what', 'who', 'how', 'where', 'when', 'why',
#                   'i', 'me', 'you', 'his', 'her', 'ok', 'bye', 'i am sorry', 'it is what it is', 'it','is','on','over','under','inside','an','a','the', 'does','con',
#                   'get', 'got', 'have', 'had', 'has', 'should', 'not', 'use', 'mobile','team','Team','Verdict','an','no','not','but','T','15','with','off','issues','issue','is','in','the','problems','are','what','why','when','flt','flashing'}
#     cleaned_query = re.sub(r'[^\w\s]', '', query)
#     words = cleaned_query.lower().split()
#     return [word for word in words if word not in filler_words and word not in stop_words]

# # Function to get problems based on keyword search
# def get_problems_by_keyword(keywords):
#     search_columns = ['Keywords(One word)', 'ASIC/Module']
#     problem_column = 'Problem'
#     matched_problems = pd.DataFrame()

#     for keyword in keywords:
#         matches = csv_data[csv_data[search_columns].apply(lambda row: row.astype(str).str.contains(rf'\b{keyword}\b', case=False).any(), axis=1)]
#         matched_problems = pd.concat([matched_problems, matches])
    
#     matched_problems = matched_problems.drop_duplicates()
#     return matched_problems[problem_column].tolist() if not matched_problems.empty else []

# # Function to get root cause and solution based on the selected problem
# def get_root_cause_and_solution(problem):
#     problem_row = csv_data[csv_data['Problem'] == problem]
#     if not problem_row.empty:
#         return problem_row['Root cause'].values[0], problem_row['Solution'].values[0]
#     return None, None

# def query_csv(query):
#     keywords = clean_and_split_query(query)
#     st.session_state.last_keywords = keywords
#     problems = get_problems_by_keyword(keywords)
#     return problems if problems else "No problems found for the given keyword."

# def detect_greeting(query):
#     greetings = {
#         "hi": "Hello! How can I assist you today?",
#         "good morning": "Good morning! Have a nice day.",
#         "good afternoon": "Good afternoon! Have a great day.",
#         "good evening": "Good evening! Go and have snacks.",
#         "good night": "Good night! Sleep well."
#     }
#     for key, value in greetings.items():
#         if key in query.lower():
#             return value
#     return None

# def get_response(query):
#     greeting_response = detect_greeting(query)
#     if greeting_response:
#         return greeting_response

#     # Check for keywords directly if not a greeting
#     problems = query_csv(query)
#     if isinstance(problems, list) and problems:
#         return problems

#     if "add data" in query.lower():
#         return "Please provide the following information to add new data."
    
#     return "What do you want to know about this?"

# st.markdown("<h1 style='text-align: center;'> HitLit 🔥 </h1>", unsafe_allow_html=True)

# # User input at the bottom
# user_input = st.text_input("Your message", key="user_input")

# if user_input:
#     st.session_state.chat_history.append(user_input)
#     ai_response = get_response(user_input)

#     if "add data" in user_input.lower():
#         updater_name = st.text_input("Enter Your Name:", placeholder="e.g. John Doe", key="name_input")
#         keyword = st.text_input("Enter Keyword:", placeholder="e.g. Error Code 123", key="keyword_input")
#         asic_module = st.text_input("Enter ASIC/Module:", placeholder="e.g. Module XYZ", key="asic_module_input")
#         problem = st.text_input("Enter Problem:", placeholder="Describe the issue", key="problem_input")
#         root_cause = st.text_input("Enter Root Cause:", placeholder="Explain the root cause", key="root_cause_input")
#         solution = st.text_input("Enter Solution:", placeholder="Provide the solution", key="solution_input")

#         if st.button("Submit New Data"):
#             add_to_csv(keyword, asic_module, problem, root_cause, solution, updater_name)
#             st.success("Data added successfully!")
#             st.session_state.chat_history.append(f"Added new data: {keyword}, {asic_module}, {problem}")

#     elif isinstance(ai_response, list):
#         selected_problem = st.selectbox("Select a problem:", options=ai_response)
#         if st.button("Get Root Cause and Solution"):
#             root_cause, solution = get_root_cause_and_solution(selected_problem)
#             if root_cause and solution:
#                 st.write(f"**Root Cause:** {root_cause}")
#                 st.write(f"**Solution:** {solution}")
#                 st.session_state.chat_history.append(f"Root Cause: {root_cause}\nSolution: {solution}")
#             else:
#                 st.write("No root cause and solution found.")

#     else:
#         st.session_state.chat_history.append(ai_response)

# # Clear Chat Button at the bottom
# if st.button("Clear Chat"):
#     st.session_state.chat_history = []
#     st.success("Chat cleared successfully!")

# st.markdown("<hr><p style='text-align: center;'><small>Made with ❤️ by You</small></p>", unsafe_allow_html=True)

# import streamlit as st
# import pandas as pd
# import re
# import requests  # Import requests to send HTTP requests
# from datetime import datetime

# # Initialize session state variables
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
# if "last_keywords" not in st.session_state:
#     st.session_state.last_keywords = []
# if "selected_problem" not in st.session_state:
#     st.session_state.selected_problem = None
# if "pending_feedback" not in st.session_state:
#     st.session_state.pending_feedback = False

# # Set up the Streamlit app
# st.set_page_config(page_title="HitLit", page_icon="🤖", initial_sidebar_state="expanded")

# # Load and Save CSV File
# @st.cache_data
# def load_csv(file_path):
#     return pd.read_csv(file_path)

# def save_csv(data, file_path):
#     data.to_csv(file_path, index=False)

# # Replace with your CSV file path
# csv_file_path = r"\\kor2fs03\V-V--Testing$\03_Validation_Software\LLBP\VALSW_LL_BP_SPL_V1.1.csv"
# csv_data = load_csv(csv_file_path)

# # # Function to send a message to Microsoft Teams
# # def send_to_teams(message):
# #     webhook_url = 'https://bosch.webhook.office.com/webhookb2/059bb68d-dcd9-4dec-95f0-18ee4c243253@0ae51e19-07c8-4e4b-bb6d-648ee58410f4/IncomingWebhook/dbdbe67775b24fdbab636521871165a0/e5f583a8-3294-4ff6-a219-a889116f5710/V2GdSH6m36m4x5wIYF42QFEulD-tO6WdamjuMZYhnVegE1'  # Replace with your Teams webhook URL
# #     payload = {
# #         "text": message
# #     }
# #     requests.post(webhook_url, json=payload)

# def add_to_csv(keyword, asic_module, problem, root_cause, solution, updater_name, project):
#     global csv_data
#     # Determine the highest serial number and increment it
#     if csv_data.empty:
#         serial_number = 1
#     else:
#         serial_number = csv_data["Sr. No"].max() + 1
        
#     date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
#     new_entry = pd.DataFrame({
#         "Sr. No": [serial_number],
#         "Year": [date],
#         "Author": [updater_name],
#         "Project": [project],
#         "Keywords(One word)": [keyword.strip()],
#         "ASIC/Module": [asic_module.strip()],
#         "Problem": [problem.strip()],
#         "Root cause": [root_cause.strip()],
#         "Solution": [solution.strip()]
#     })

#     # Remove any unwanted columns from the current DataFrame if they exist
#     csv_data = csv_data.loc[:, ~csv_data.columns.isin(['Updated By', 'Date', 'Serial Number'])]
    
#     # Concatenate the new entry with the existing DataFrame
#     csv_data = pd.concat([csv_data, new_entry], ignore_index=True)

#     # Remove unwanted lines from the DataFrame
#     unwanted_lines_condition = csv_data.apply(lambda row: row.astype(str).str.contains(r"dlkd'als|fhpiq\[oe\[|oqpoeq-2pw|w219e-=210=|1ue2oqwp", case=False).any(), axis=1)
#     csv_data = csv_data[~unwanted_lines_condition]

#     # Save the updated DataFrame to the CSV file
#     save_csv(csv_data, csv_file_path)


# # def add_to_csv(keyword, asic_module, problem, root_cause, solution, updater_name, project):
# #     global csv_data
# #     # Determine the highest serial number and increment it
# #     if csv_data.empty:
# #         serial_number = 1
# #     else:
# #         serial_number = csv_data["Sr. No"].max() + 1
        
# #     date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
# #     new_entry = pd.DataFrame({
# #         "Sr. No": [serial_number],
# #         "Year": [date],
# #         "Author": [updater_name],
# #         "Project": [project],
# #         "Keywords(One word)": [keyword.strip()],
# #         "ASIC/Module": [asic_module.strip()],
# #         "Problem": [problem.strip()],
# #         "Root cause": [root_cause.strip()],
# #         "Solution": [solution.strip()]
# #     })

# #     # Remove any unwanted columns from the current DataFrame if they exist
# #     csv_data = csv_data.loc[:, ~csv_data.columns.isin(['Updated By', 'Date', 'Serial Number'])]
    
# #     # Concatenate the new entry with the existing DataFrame
# #     csv_data = pd.concat([csv_data, new_entry], ignore_index=True)
    
# #     # Save the updated DataFrame to the CSV file
# #     save_csv(csv_data, csv_file_path)

#     # Notify Teams (optional, commented out for now)
#     # send_to_teams(f"New data added by {updater_name}: {keyword}, {asic_module}, {problem}, {project}")


# # def add_to_csv(keyword, asic_module, problem, root_cause, solution, updater_name, project):
# #     global csv_data
# #     # Determine the highest serial number and increment it
# #     if csv_data.empty:
# #         serial_number = 1
# #     else:
# #         serial_number = csv_data["Sr. No"].max() + 1
        
# #     date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
# #     new_entry = pd.DataFrame({
# #         "Sr. No": [serial_number],
# #         "Year": [date],
# #         "Author": [updater_name],
# #         "Project": [project],
# #         "Keywords(One word)": [keyword.strip()],
# #         "ASIC/Module": [asic_module.strip()],
# #         "Problem": [problem.strip()],
# #         "Root cause": [root_cause.strip()],
# #         "Solution": [solution.strip()]
# #     })
    
# #     # Remove any unwanted columns from the current DataFrame
# #     if 'Updated By' in csv_data.columns:
# #         csv_data = csv_data.drop(columns=['Updated By'])
# #     if 'Date' in csv_data.columns:
# #         csv_data = csv_data.drop(columns=['Date'])
# #     if 'Serial Number' in csv_data.columns:
# #         csv_data = csv_data.drop(columns=['Serial Number'])
    
# #     # Concatenate the new entry with the existing DataFrame
# #     csv_data = pd.concat([csv_data, new_entry], ignore_index=True)
    
# #     # Save the updated DataFrame to the CSV file
# #     save_csv(csv_data, csv_file_path)
    
#     # Notify Teams (optional, commented out for now)
#     # send_to_teams(f"New data added by {updater_name}: {keyword}, {asic_module}, {problem}, {project}")


# # def add_to_csv(keyword, asic_module, problem, root_cause, solution, updater_name, project):
# #     global csv_data
# #     # Determine the highest serial number and increment it
# #     if csv_data.empty:
# #         serial_number = 1
# #     else:
# #         serial_number = csv_data["Sr. No"].max() + 1
        
# #     date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
# #     new_entry = {
# #         "Sr. No": serial_number,
# #         "Year": date,
# #         "Author": updater_name,
# #         "Project": project,
# #         "Keywords(One word)": keyword.strip(),
# #         "ASIC/Module": asic_module.strip(),
# #         "Problem": problem.strip(),
# #         "Root cause": root_cause.strip(),
# #         "Solution": solution.strip()
# #     }
    
# #     # Remove any columns that shouldn't be there (e.g., 'Updated By') from the current DataFrame
# #     if 'Updated By' in csv_data.columns:
# #         csv_data = csv_data.drop(columns=['Updated By'])
# #     if 'Date' in csv_data.columns:
# #         csv_data = csv_data.drop(columns=['Date'])
# #     if 'Serial Number' in csv_data.columns:
# #         csv_data = csv_data.drop(columns=['Serial Number'])
        
# #     # Append the new entry as a row to the existing DataFrame
# #     csv_data = csv_data.append(new_entry, ignore_index=True)

#     # Save the updated DataFrame to the CSV file
#     save_csv(csv_data, csv_file_path)

#     # Notify Teams (optional, commented out for now)
#     # send_to_teams(f"New data added by {updater_name}: {keyword}, {asic_module}, {problem}, {project}")


# # def add_to_csv(keyword, asic_module, problem, root_cause, solution, updater_name, project):
# #     global csv_data
# #     # Determine the highest serial number and increment it
# #     if csv_data.empty:
# #         serial_number = 1
# #     else:
# #         serial_number = csv_data["Sr. No"].max() + 1
        
# #     date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
# #     new_entry = pd.DataFrame({
# #         "Sr. No": [serial_number],
# #         "Year": [date],
# #         "Author": [updater_name],
# #         "Project": [project],
# #         "Keywords(One word)": [keyword.strip()],
# #         "ASIC/Module": [asic_module.strip()],
# #         "Problem": [problem.strip()],
# #         "Root cause": [root_cause.strip()],
# #         "Solution": [solution.strip()],
# #         "Author": [updater_name.strip()],
# #         "Project": [project.strip()]
# #     })
    
    
    
#     # # Ensure no unwanted rows or strings are added
#     # csv_data = pd.concat([csv_data, new_entry], ignore_index=True)
#     # save_csv(csv_data, csv_file_path)
#     # Notify Teams
#     # send_to_teams(f"New data added by {updater_name}: {keyword}, {asic_module}, {problem}, {project}")



# def clean_and_split_query(query):
#     filler_words = {'um', 'like', 'you', 'know', 'so', 'well', 'actually', 'basically', 'just', 'really'}
#     stop_words = {'is', 'are', 'was', 'were', 'what', 'who', 'how', 'where', 'when', 'why',
#                   'i', 'me', 'you', 'his', 'her', 'ok', 'bye', 'i am sorry', 'it is what it is', 'it','is','on','over','under','inside','an','a','the', 'does','con',
#                   'get', 'got', 'have', 'had', 'has', 'should', 'not', 'use', 'mobile','team','Team','Verdict','an','no','not','but','T','15','with','off','issues','issue','is','in','the','problems','are','what','why','when','flt','flashing'}
#     cleaned_query = re.sub(r'[^\w\s]', '', query)
#     words = cleaned_query.lower().split()
#     return [word for word in words if word not in filler_words and word not in stop_words]

# # Function to get problems based on keyword search
# def get_problems_by_keyword(keywords):
#     search_columns = ['Keywords(One word)', 'ASIC/Module']
#     problem_column = 'Problem'
#     matched_problems = pd.DataFrame()

#     for keyword in keywords:
#         matches = csv_data[csv_data[search_columns].apply(lambda row: row.astype(str).str.contains(rf'\b{keyword}\b', case=False).any(), axis=1)]
#         matched_problems = pd.concat([matched_problems, matches])
    
#     matched_problems = matched_problems.drop_duplicates()
#     return matched_problems[problem_column].tolist() if not matched_problems.empty else []

# # Function to get root cause and solution based on the selected problem
# def get_root_cause_and_solution(problem):
#     problem_row = csv_data[csv_data['Problem'] == problem]
#     if not problem_row.empty:
#         return problem_row['Root cause'].values[0], problem_row['Solution'].values[0]
#     return None, None

# def query_csv(query):
#     keywords = clean_and_split_query(query)
#     st.session_state.last_keywords = keywords
#     problems = get_problems_by_keyword(keywords)
#     return problems if problems else "No problems found for the given keyword."

# def detect_greeting(query):
#     greetings = {
#         "hi": "Hello! How can I assist you today?",
#         "good morning": "Good morning! Have a nice day.",
#         "good afternoon": "Good afternoon! Have a great day.",
#         "good evening": "Good evening! Go and have snacks.",
#         "good night": "Good night! Sleep well."
#     }
#     for key, value in greetings.items():
#         if key in query.lower():
#             return value
#     return None

# def get_response(query):
#     greeting_response = detect_greeting(query)
#     if greeting_response:
#         return greeting_response

#     # Check for keywords directly if not a greeting
#     problems = query_csv(query)
#     if isinstance(problems, list) and problems:
#         return problems

#     if "add data" in query.lower():
#         return "Please provide the following information to add new data."
    
#     return "What do you want to know about this?"

# st.markdown("<h1 style='text-align: center;'> HitLit 🔥 </h1>", unsafe_allow_html=True)

# # User input at the bottom
# user_input = st.text_input("Your message", key="user_input")

# if user_input:
#     st.session_state.chat_history.append(user_input)
#     ai_response = get_response(user_input)

#     if "add data" in user_input.lower():
#         updater_name = st.text_input("Enter Your Name:", placeholder="e.g. John Doe", key="name_input")
#         keyword = st.text_input("Enter Keyword:", placeholder="e.g. Error Code 123", key="keyword_input")
#         asic_module = st.text_input("Enter ASIC/Module:", placeholder="e.g. Module XYZ", key="asic_module_input")
#         problem = st.text_input("Enter Problem:", placeholder="Describe the issue", key="problem_input")
#         root_cause = st.text_input("Enter Root Cause:", placeholder="Explain the root cause", key="root_cause_input")
#         solution = st.text_input("Enter Solution:", placeholder="Provide the solution", key="solution_input")
#         project = st.text_input("Enter Project:", placeholder="e.g. Project ABC", key="project_input")

#         if st.button("Submit New Data"):
#             if all([updater_name, keyword, asic_module, problem, root_cause, solution, project]):
#                 add_to_csv(keyword, asic_module, problem, root_cause, solution, updater_name, project)
#                 st.success("Data added successfully!")
#                 st.session_state.chat_history.append(f"Added new data: {keyword}, {asic_module}, {problem}")
#         else:
#             st.error("Please fill in all fields before submitting.")

#     elif isinstance(ai_response, list):
#         selected_problem = st.selectbox("Select a problem:", options=ai_response)
#         if st.button("Get Root Cause and Solution"):
#             root_cause, solution = get_root_cause_and_solution(selected_problem)
#             if root_cause and solution:
#                 st.write(f"**Root Cause:** {root_cause}")
#                 st.write(f"**Solution:** {solution}")
#                 st.session_state.chat_history.append(f"Root Cause: {root_cause}\nSolution: {solution}")
#             else:
#                 st.write("No root cause and solution found.")

#     else:
#         st.session_state.chat_history.append(ai_response)

# # Clear Chat Button at the bottom
# if st.button("Clear Chat"):
#     st.session_state.chat_history = []
#     st.success("Chat cleared successfully!")

# st.markdown("<hr><p style='text-align: center;'><small>Made with ❤️ by You</small></p>", unsafe_allow_html=True)


# import streamlit as st
# import pandas as pd
# import re
# import requests
# from datetime import datetime

# # Initialize session state variables
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
# if "last_keywords" not in st.session_state:
#     st.session_state.last_keywords = []
# if "selected_problem" not in st.session_state:
#     st.session_state.selected_problem = None
# if "pending_feedback" not in st.session_state:
#     st.session_state.pending_feedback = False

# # Set up the Streamlit app
# st.set_page_config(page_title="HitLit", page_icon="🤖", initial_sidebar_state="expanded")

# @st.cache_data
# def load_csv(file_path):
#     return pd.read_csv(file_path)

# def save_csv(data, file_path):
#     data.to_csv(file_path, index=False)

# csv_file_path = r"\\kor2fs03\V-V--Testing$\03_Validation_Software\LLBP\VALSW_LL_BP_SPL_V1.1.csv"
# csv_data = load_csv(csv_file_path)

# def add_to_csv(entries):
#     global csv_data
#     new_entries = []

#     for entry in entries:
#         keyword, asic_module, problem, root_cause, solution, updater_name, project = entry
#         if csv_data.empty:
#             serial_number = 1
#         else:
#             serial_number = csv_data["Sr. No"].max() + 1
            
#         date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
#         new_entry = {
#             "Sr. No": serial_number,
#             "Year": date,
#             "Author": updater_name,
#             "Project": project,
#             "Keywords(One word)": keyword.strip(),
#             "ASIC/Module": asic_module.strip(),
#             "Problem": problem.strip(),
#             "Root cause": root_cause.strip(),
#             "Solution": solution.strip()
#         }

#         new_entries.append(new_entry)

#     # Create DataFrame for new entries
#     new_entries_df = pd.DataFrame(new_entries)

# #   # Remove any unwanted columns from the current DataFrame if they exist
#     csv_data = csv_data.loc[:, ~csv_data.columns.isin(['Updated By', 'Date', 'Serial Number'])]
    
# #   # Concatenate the new entry with the existing DataFrame
#     csv_data = pd.concat([csv_data, new_entry], ignore_index=True)

#     # Remove unwanted lines from the DataFrame
#     unwanted_lines_condition = csv_data.apply(lambda row: row.astype(str).str.contains(r"dlkd'als|fhpiq\[oe\[|oqpoeq-2pw|w219e-=210=|1ue2oqwp", case=False).any(), axis=1)
#     csv_data = csv_data[~unwanted_lines_condition]

#     # Save the updated DataFrame to the CSV file
#     save_csv(csv_data, csv_file_path)

# def clean_and_split_query(query):
#     filler_words = {'um', 'like', 'you', 'know', 'so', 'well', 'actually', 'basically', 'just', 'really'}
#     stop_words = {'is', 'are', 'was', 'were', 'what', 'who', 'how', 'where', 'when', 'why','to','know','would','like','about',
#                   'i', 'me', 'you', 'his', 'her', 'ok', 'bye', 'i am sorry', 'it is what it is', 'it','is','on','over','under','inside','an','a','the', 'does','con',
#                   'get', 'got', 'have', 'had', 'has', 'should', 'not', 'use', 'mobile','team','Team','Verdict','an','no','not','but','T','15','with','off','issues','issue','is','in','the','problems','are','what','why','when','flt','flashing'}
#     cleaned_query = re.sub(r'[^\w\s]', '', query)
#     words = cleaned_query.lower().split()
#     return [word for word in words if word not in filler_words and word not in stop_words]

# def get_problems_by_keyword(keywords):
#     search_columns = ['Keywords(One word)', 'ASIC/Module']
#     problem_column = 'Problem'
#     matched_problems = pd.DataFrame()

#     for keyword in keywords:
#         matches = csv_data[csv_data[search_columns].apply(lambda row: row.astype(str).str.contains(rf'\b{keyword}\b', case=False).any(), axis=1)]
#         matched_problems = pd.concat([matched_problems, matches])
    
#     matched_problems = matched_problems.drop_duplicates()
#     return matched_problems[problem_column].tolist() if not matched_problems.empty else []

# def get_root_cause_and_solution(problem):
#     problem_row = csv_data[csv_data['Problem'] == problem]
#     if not problem_row.empty:
#         return problem_row['Root cause'].values[0], problem_row['Solution'].values[0]
#     return None, None

# def query_csv(query):
#     keywords = clean_and_split_query(query)
#     st.session_state.last_keywords = keywords
#     problems = get_problems_by_keyword(keywords)
#     return problems if problems else "No problems found for the given keyword."

# def detect_greeting(query):
#     greetings = {
#         "hi": "Hello! How can I assist you today?",
#         "good morning": "Good morning! Have a nice day.",
#         "good afternoon": "Good afternoon! Have a great day.",
#         "good evening": "Good evening! Go and have snacks.",
#         "good night": "Good night! Sleep well."
#     }
#     for key, value in greetings.items():
#         if key in query.lower():
#             return value
#     return None

# def get_response(query):
#     greeting_response = detect_greeting(query)
#     if greeting_response:
#         return greeting_response

#     problems = query_csv(query)
#     if isinstance(problems, list) and problems:
#         return problems

#     if "add data" in query.lower():
#         return "Please provide the following information to add new data."
    
#     return "What do you want to know about this?"

# st.markdown("<h1 style='text-align: center;'> HitLit 🔥 </h1>", unsafe_allow_html=True)

# user_input = st.text_input("Your message", key="user_input")

# if user_input:
#     st.session_state.chat_history.append(user_input)
#     ai_response = get_response(user_input)

#     if "add data" in user_input.lower():
#         entries = []
#         num_entries = st.number_input("How many entries do you want to add?", min_value=1, max_value=10, value=1)
        
#         for i in range(num_entries):
#             st.markdown(f"### Entry {i + 1}")
#             updater_name = st.text_input(f"Enter Your Name for Entry {i + 1}:", key=f"name_input_{i}")
#             keyword = st.text_input(f"Enter Keyword for Entry {i + 1}:", placeholder="e.g. Error Code 123", key=f"keyword_input_{i}")
#             asic_module = st.text_input(f"Enter ASIC/Module for Entry {i + 1}:", placeholder="e.g. Module XYZ", key=f"asic_module_input_{i}")
#             problem = st.text_input(f"Enter Problem for Entry {i + 1}:", placeholder="Describe the issue", key=f"problem_input_{i}")
#             root_cause = st.text_input(f"Enter Root Cause for Entry {i + 1}:", placeholder="Explain the root cause", key=f"root_cause_input_{i}")
#             solution = st.text_input(f"Enter Solution for Entry {i + 1}:", placeholder="Provide the solution", key=f"solution_input_{i}")
#             project = st.text_input(f"Enter Project for Entry {i + 1}:", placeholder="e.g. Project ABC", key=f"project_input_{i}")

#             if st.button(f"Submit Entry {i + 1}", key=f"submit_entry_{i}"):
#                 if all([updater_name, keyword, asic_module, problem, root_cause, solution, project]):
#                     entries.append((keyword, asic_module, problem, root_cause, solution, updater_name, project))
#                 else:
#                     st.error("Please fill in all fields before submitting.")

#         if entries:
#             add_to_csv(entries)
#             st.success("Data added successfully!")
#             for entry in entries:
#                 st.session_state.chat_history.append(f"Added new data: {entry[0]}, {entry[1]}, {entry[2]}")

#     elif isinstance(ai_response, list):
#         selected_problem = st.selectbox("Select a problem:", options=ai_response)
#         if st.button("Get Root Cause and Solution"):
#             root_cause, solution = get_root_cause_and_solution(selected_problem)
#             if root_cause and solution:
#                 st.write(f"**Root Cause:** {root_cause}")
#                 st.write(f"**Solution:** {solution}")
#                 st.session_state.chat_history.append(f"Root Cause: {root_cause}\nSolution: {solution}")
#             else:
#                 st.write("No root cause and solution found.")

#     else:
#         st.session_state.chat_history.append(ai_response)

# if st.button("Clear Chat"):
#     st.session_state.chat_history = []
#     st.success("Chat cleared successfully!")

# st.markdown("<hr><p style='text-align: center;'><small>Made with ❤️ by You</small></p>", unsafe_allow_html=True)


# import streamlit as st
# import pandas as pd
# import re
# from datetime import datetime

# # Initialize session state variables
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
# if "last_keywords" not in st.session_state:
#     st.session_state.last_keywords = []
# if "selected_problem" not in st.session_state:
#     st.session_state.selected_problem = None
# if "pending_feedback" not in st.session_state:
#     st.session_state.pending_feedback = False

# # Set up the Streamlit app
# st.set_page_config(page_title="HitLit", page_icon="🤖", initial_sidebar_state="expanded")

# @st.cache_data
# def load_csv(file_path):
#     return pd.read_csv(file_path)

# def save_csv(data, file_path):
#     data.to_csv(file_path, index=False)

# csv_file_path = r"\\kor2fs03\V-V--Testing$\03_Validation_Software\LLBP\VALSW_LL_BP_SPL_V1.1.csv"
# csv_data = load_csv(csv_file_path)

# def add_to_csv(entries):
#     global csv_data
#     new_entries = []

#     for entry in entries:
#         keyword, asic_module, problem, root_cause, solution, updater_name, project = entry
#         serial_number = csv_data["Sr. No"].max() + 1 if not csv_data.empty else 1
        
#         date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
#         new_entry = {
#             "Sr. No": serial_number,
#             "Year": date,
#             "Author": updater_name,
#             "Project": project,
#             "Keywords(One word)": keyword.strip(),
#             "ASIC/Module": asic_module.strip(),
#             "Problem": problem.strip(),
#             "Root cause": root_cause.strip(),
#             "Solution": solution.strip()
#         }

#         new_entries.append(new_entry)

#     new_entries_df = pd.DataFrame(new_entries)
    
#     # Clean existing data
#     csv_data.drop(columns=['Updated By', 'Date', 'Serial Number'], errors='ignore', inplace=True)
    
#     # Append new entries
#     csv_data = pd.concat([csv_data, new_entries_df], ignore_index=True)

#     # Save the updated DataFrame to the CSV file
#     save_csv(csv_data, csv_file_path)

# def clean_and_split_query(query):
#     filler_words = {'um', 'like', 'you', 'know', 'so', 'well', 'actually', 'basically', 'just', 'really'}
#     stop_words = {'is', 'are', 'was', 'were', 'what', 'who', 'how', 'where', 'when', 'why', 'to', 'know', 'would', 'like',
#                   'i', 'me', 'you', 'his', 'her', 'ok', 'bye', 'i am sorry', 'it is what it is', 'it', 'is', 'on', 'over',
#                   'under', 'inside', 'an', 'a', 'the', 'does', 'con', 'get', 'got', 'have', 'had', 'has', 'should', 
#                   'not', 'use', 'mobile', 'team', 'Team', 'Verdict', 'an', 'no', 'not', 'but', 'T', '15', 'with', 
#                   'off', 'issues', 'issue', 'is', 'in', 'the', 'problems', 'are', 'what', 'why', 'when', 'flt', 
#                   'flashing'}
    
#     cleaned_query = re.sub(r'[^\w\s]', '', query)
#     words = cleaned_query.lower().split()
#     return [word for word in words if word not in filler_words and word not in stop_words]

# def get_problems_by_keyword(keywords):
#     search_columns = ['Keywords(One word)', 'ASIC/Module']
#     matched_problems = pd.DataFrame()

#     for keyword in keywords:
#         matches = csv_data[csv_data[search_columns].apply(lambda row: row.astype(str).str.contains(rf'\b{keyword}\b', case=False).any(), axis=1)]
#         matched_problems = pd.concat([matched_problems, matches])
    
#     matched_problems = matched_problems.drop_duplicates()
#     return matched_problems['Problem'].tolist() if not matched_problems.empty else []

# def get_root_cause_and_solution(problem):
#     problem_row = csv_data[csv_data['Problem'] == problem]
#     if not problem_row.empty:
#         return problem_row['Root cause'].values[0], problem_row['Solution'].values[0]
#     return None, None

# def query_csv(query):
#     keywords = clean_and_split_query(query)
#     st.session_state.last_keywords = keywords
#     problems = get_problems_by_keyword(keywords)
#     return problems if problems else "No problems found for the given keyword."

# def detect_greeting(query):
#     greetings = {
#         "hi": "Hello! How can I assist you today?",
#         "good morning": "Good morning! Have a nice day.",
#         "good afternoon": "Good afternoon! Have a great day.",
#         "good evening": "Good evening! Go and have snacks.",
#         "good night": "Good night! Sleep well."
#     }
#     for key, value in greetings.items():
#         if key in query.lower():
#             return value
#     return None

# def get_response(query):
#     greeting_response = detect_greeting(query)
#     if greeting_response:
#         return greeting_response

#     problems = query_csv(query)
#     if isinstance(problems, list) and problems:
#         return problems

#     if "add data" in query.lower():
#         return "Please provide the information to add new data."

#     return "What do you want to know about this?"

# st.markdown("<h1 style='text-align: center;'> HitLit 🔥 </h1>", unsafe_allow_html=True)

# user_input = st.text_input("Your message", key="user_input")

# if user_input:
#     st.session_state.chat_history.append(user_input)
#     ai_response = get_response(user_input)

#     if "add data" in user_input.lower():
#         entries = []
#         num_entries = st.number_input("How many entries do you want to add?", min_value=1, max_value=10, value=1)
        
#         for i in range(num_entries):
#             st.markdown(f"### Entry {i + 1}")
#             updater_name = st.text_input(f"Enter Your Name for Entry {i + 1}:", key=f"name_input_{i}")
#             keyword = st.text_input(f"Enter Keyword for Entry {i + 1}:", placeholder="e.g. Error Code 123", key=f"keyword_input_{i}")
#             asic_module = st.text_input(f"Enter ASIC/Module for Entry {i + 1}:", placeholder="e.g. Module XYZ", key=f"asic_module_input_{i}")
#             problem = st.text_input(f"Enter Problem for Entry {i + 1}:", placeholder="Describe the issue", key=f"problem_input_{i}")
#             root_cause = st.text_input(f"Enter Root Cause for Entry {i + 1}:", placeholder="Explain the root cause", key=f"root_cause_input_{i}")
#             solution = st.text_input(f"Enter Solution for Entry {i + 1}:", placeholder="Provide the solution", key=f"solution_input_{i}")
#             project = st.text_input(f"Enter Project for Entry {i + 1}:", placeholder="e.g. Project ABC", key=f"project_input_{i}")

#             if st.button(f"Submit Entry {i + 1}", key=f"submit_entry_{i}"):
#                 if all([updater_name, keyword, asic_module, problem, root_cause, solution, project]):
#                     entries.append((keyword, asic_module, problem, root_cause, solution, updater_name, project))
#                     st.success(f"Entry {i + 1} submitted!")
#                 else:
#                     st.error("Please fill in all fields before submitting.")

#         if entries:
#             add_to_csv(entries)
#             st.success("All entries added successfully!")
#             for entry in entries:
#                 st.session_state.chat_history.append(f"Added new data: {entry[0]}, {entry[1]}, {entry[2]}")

#     elif isinstance(ai_response, list):
#         selected_problem = st.selectbox("Select a problem:", options=ai_response)
#         if st.button("Get Root Cause and Solution"):
#             root_cause, solution = get_root_cause_and_solution(selected_problem)
#             if root_cause and solution:
#                 st.write(f"**Root Cause:** {root_cause}")
#                 st.write(f"**Solution:** {solution}")
#                 st.session_state.chat_history.append(f"Root Cause: {root_cause}\nSolution: {solution}")
#             else:
#                 st.write("No root cause and solution found.")

#     else:
#         st.session_state.chat_history.append(ai_response)

# if st.button("Clear Chat"):
#     st.session_state.chat_history = []
#     st.success("Chat cleared successfully!")

# st.markdown("<hr><p style='text-align: center;'><small>Made with ❤️ by You</small></p>", unsafe_allow_html=True)


# import streamlit as st
# import pandas as pd
# import re
# from datetime import datetime
# from nltk.corpus import wordnet as wn

# # Initialize session state variables
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
# if "last_keywords" not in st.session_state:
#     st.session_state.last_keywords = []
# if "selected_problem" not in st.session_state:
#     st.session_state.selected_problem = None
# if "pending_feedback" not in st.session_state:
#     st.session_state.pending_feedback = False

# # Set up the Streamlit app
# st.set_page_config(page_title="HitLit", page_icon="🤖", initial_sidebar_state="expanded")

# @st.cache_data
# def load_csv(file_path):
#     return pd.read_csv(file_path)

# def save_csv(data, file_path):
#     data.to_csv(file_path, index=False)

# csv_file_path = r"\\kor2fs03\V-V--Testing$\03_Validation_Software\LLBP\VALSW_LL_BP_SPL_V1.1.csv"
# csv_data = load_csv(csv_file_path)

# def add_to_csv(entries):
#     global csv_data
#     new_entries = []

#     for entry in entries:
#         keyword, asic_module, problem, root_cause, solution, updater_name, project = entry
#         serial_number = csv_data["Sr. No"].max() + 1 if not csv_data.empty else 1
        
#         date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
#         new_entry = {
#             "Sr. No": serial_number,
#             "Year": date,
#             "Author": updater_name,
#             "Project": project,
#             "Keywords(One word)": keyword.strip(),
#             "ASIC/Module": asic_module.strip(),
#             "Problem": problem.strip(),
#             "Root cause": root_cause.strip(),
#             "Solution": solution.strip()
#         }

#         new_entries.append(new_entry)

#     new_entries_df = pd.DataFrame(new_entries)
    
#     # Clean existing data
#     csv_data.drop(columns=['Updated By', 'Date', 'Serial Number'], errors='ignore', inplace=True)
    
#     # Append new entries
#     csv_data = pd.concat([csv_data, new_entries_df], ignore_index=True)

#     # Save the updated DataFrame to the CSV file
#     save_csv(csv_data, csv_file_path)

# def clean_and_split_query(query):
#     filler_words = {'um', 'like', 'you', 'know', 'so', 'well', 'actually', 'basically', 'just', 'really'}
#     stop_words = {'is', 'are', 'was', 'were', 'what', 'who', 'how', 'where', 'when', 'why', 'to', 'know', 'would', 
#                   'like', 'i', 'me', 'you', 'his', 'her', 'ok', 'bye', 'i am sorry', 'it is what it is', 'it', 
#                   'is', 'on', 'over', 'under', 'inside', 'an', 'a', 'the', 'does', 'con', 'get', 'got', 'have', 
#                   'had', 'has', 'should', 'not', 'use', 'mobile', 'team', 'Team', 'Verdict', 'an', 'no', 
#                   'not', 'but', 'T', '15', 'with', 'off', 'issues', 'issue', 'is', 'in', 'the', 'problems', 
#                   'are', 'what', 'why', 'when', 'flt', 'flashing'}
    
#     cleaned_query = re.sub(r'[^\w\s]', '', query)
#     words = cleaned_query.lower().split()
#     return [word for word in words if word not in filler_words and word not in stop_words]

# def get_problems_by_keyword(keywords):
#     search_columns = ['Keywords(One word)', 'ASIC/Module']
#     matched_problems = pd.DataFrame()

#     for keyword in keywords:
#         matches = csv_data[csv_data[search_columns].apply(lambda row: row.astype(str).str.contains(rf'\b{keyword}\b', case=False).any(), axis=1)]
#         matched_problems = pd.concat([matched_problems, matches])
    
#     matched_problems = matched_problems.drop_duplicates()
#     return matched_problems['Problem'].tolist() if not matched_problems.empty else []

# def get_root_cause_and_solution(problem):
#     problem_row = csv_data[csv_data['Problem'] == problem]
#     if not problem_row.empty:
#         return problem_row['Root cause'].values[0], problem_row['Solution'].values[0]
#     return None, None

# def is_adding_data_query(query):
#     add_data_phrases = [
#         "add data", "I want to add", "please add", "let's add", "adding data",
#         "I need to add", "can you add", "add new entry", "new entry",
#         "submit data", "want to input", "enter data"
#     ]
    
#     return any(phrase in query.lower() for phrase in add_data_phrases)

# def is_deleting_data_query(query):
#     delete_data_phrases = [
#         "delete data", "remove entry", "can you delete", "please remove",
#         "I want to delete", "how do I delete", "remove record"
#     ]
    
#     return any(phrase in query.lower() for phrase in delete_data_phrases)

# def detect_keyword_type(keyword):
#     """ Determine if the keyword is a verb, adjective, or a known term. """
#     if len(keyword) == 0:
#         return None

#     synsets = wn.synsets(keyword)
    
#     if not synsets:
#         return "unknown"
    
#     # Check the first synset for its part of speech
#     pos = synsets[0].pos()
#     if pos in ['v']:  # Verb
#         return "verb"
#     elif pos in ['a']:  # Adjective
#         return "adjective"
#     else:  # Assuming it's a noun or other types
#         return "known_term"

# def get_response(query):
#     greeting_response = detect_greeting(query)
#     if greeting_response:
#         return greeting_response

#     keywords = clean_and_split_query(query)
#     if len(keywords) == 1:
#         keyword_type = detect_keyword_type(keywords[0])
#         if keyword_type == "verb" or keyword_type == "adjective":
#             return "Please provide more details; your input is too vague."
#         elif keyword_type == "known_term":
#             problems = get_problems_by_keyword(keywords)
#             if problems:
#                 return problems
#             else:
#                 return "No problems found related to that keyword."
#         else:
#             return "I'm not sure what you mean by that. Could you elaborate?"

#     # Handle multiple keywords
#     problems = get_problems_by_keyword(keywords)
#     if problems:
#         return problems

#     if is_adding_data_query(query):
#         return "Please provide the information to add new data."

#     if is_deleting_data_query(query):
#         return "Please specify which entry you want to delete."

#     return "What do you want to know about this?"

# def detect_greeting(query):
#     greetings = {
#         "hi": "Hello! How can I assist you today?",
#         "good morning": "Good morning! Have a nice day.",
#         "good afternoon": "Good afternoon! Have a great day.",
#         "good evening": "Good evening! Go and have snacks.",
#         "good night": "Good night! Sleep well."
#     }
#     for key, value in greetings.items():
#         if key in query.lower():
#             return value
#     return None

# st.markdown("<h1 style='text-align: center;'> HitLit 🔥 </h1>", unsafe_allow_html=True)

# user_input = st.text_input("Your message", key="user_input")

# if user_input:
#     st.session_state.chat_history.append(user_input)
#     ai_response = get_response(user_input)

#     if is_adding_data_query(user_input):
#         entries = []
#         num_entries = st.number_input("How many entries do you want to add?", min_value=1, max_value=10, value=1)
        
#         for i in range(num_entries):
#             st.markdown(f"### Entry {i + 1}")
#             updater_name = st.text_input(f"Enter Your Name for Entry {i + 1}:", key=f"name_input_{i}")
#             keyword = st.text_input(f"Enter Keyword for Entry {i + 1}:", placeholder="e.g. Error Code 123", key=f"keyword_input_{i}")
#             asic_module = st.text_input(f"Enter ASIC/Module for Entry {i + 1}:", placeholder="e.g. Module XYZ", key=f"asic_module_input_{i}")
#             problem = st.text_input(f"Enter Problem for Entry {i + 1}:", placeholder="Describe the issue", key=f"problem_input_{i}")
#             root_cause = st.text_input(f"Enter Root Cause for Entry {i + 1}:", placeholder="Explain the root cause", key=f"root_cause_input_{i}")
#             solution = st.text_input(f"Enter Solution for Entry {i + 1}:", placeholder="Provide the solution", key=f"solution_input_{i}")
#             project = st.text_input(f"Enter Project for Entry {i + 1}:", placeholder="e.g. Project ABC", key=f"project_input_{i}")

#             if st.button(f"Submit Entry {i + 1}", key=f"submit_entry_{i}"):
#                 if all([updater_name, keyword, asic_module, problem, root_cause, solution, project]):
#                     entries.append((keyword, asic_module, problem, root_cause, solution, updater_name, project))
#                     st.success(f"Entry {i + 1} submitted!")
#                 else:
#                     st.error("Please fill in all fields before submitting.")

#         if entries:
#             add_to_csv(entries)
#             st.success("All entries added successfully!")
#             for entry in entries:
#                 st.session_state.chat_history.append(f"Added new data: {entry[0]}, {entry[1]}, {entry[2]}")

#     elif is_deleting_data_query(user_input):
#         # Implement deletion logic here as needed
#         st.write("Deletion feature is not yet implemented.")

#     elif isinstance(ai_response, list):
#         selected_problem = st.selectbox("Select a problem:", options=ai_response)
#         if st.button("Get Root Cause and Solution"):
#             root_cause, solution = get_root_cause_and_solution(selected_problem)
#             if root_cause and solution:
#                 st.write(f"**Root Cause:** {root_cause}")
#                 st.write(f"**Solution:** {solution}")
#                 st.session_state.chat_history.append(f"Root Cause: {root_cause}\nSolution: {solution}")
#             else:
#                 st.write("No root cause and solution found.")

#     else:
#         st.session_state.chat_history.append(ai_response)

# if st.button("Clear Chat"):
#     st.session_state.chat_history = []
#     st.success("Chat cleared successfully!")

# st.markdown("<hr><p style='text-align: center;'><small>Made with ❤️ by You</small></p>", unsafe_allow_html=True)



# import streamlit as st
# import pandas as pd
# import re
# from datetime import datetime
# from nltk.corpus import wordnet as wn

# # Initialize session state variables
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
# if "last_keywords" not in st.session_state:
#     st.session_state.last_keywords = []
# if "selected_problem" not in st.session_state:
#     st.session_state.selected_problem = None
# if "pending_feedback" not in st.session_state:
#     st.session_state.pending_feedback = False

# # Set up the Streamlit app
# st.set_page_config(page_title="HitLit", page_icon="🤖", initial_sidebar_state="expanded")

# @st.cache_data
# def load_csv(file_path):
#     return pd.read_csv(file_path)

# def save_csv(data, file_path):
#     data.to_csv(file_path, index=False)

# csv_file_path = r"\\kor2fs03\V-V--Testing$\03_Validation_Software\LLBP\VALSW_LL_BP_SPL_V1.1.csv"
# csv_data = load_csv(csv_file_path)

# def add_to_csv(entries):
#     global csv_data
#     new_entries = []

#     for entry in entries:
#         keyword, asic_module, problem, root_cause, solution, updater_name, project = entry
#         serial_number = csv_data["Sr. No"].max() + 1 if not csv_data.empty else 1
        
#         date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
#         new_entry = {
#             "Sr. No": serial_number,
#             "Year": date,
#             "Author": updater_name,
#             "Project": project,
#             "Keywords(One word)": keyword.strip(),
#             "ASIC/Module": asic_module.strip(),
#             "Problem": problem.strip(),
#             "Root cause": root_cause.strip(),
#             "Solution": solution.strip()
#         }

#         new_entries.append(new_entry)

#     new_entries_df = pd.DataFrame(new_entries)
    
#     # Clean existing data
#     csv_data.drop(columns=['Updated By', 'Date', 'Serial Number'], errors='ignore', inplace=True)
    
#     # Remove unwanted lines from the DataFrame
#     unwanted_lines_condition = csv_data.apply(lambda row: row.astype(str).str.contains(r"dlkd'als|fhpiq\[oe\[|oqpoeq-2pw|w219e-=210=|1ue2oqwp", case=False).any(), axis=1)
#     csv_data = csv_data[~unwanted_lines_condition]

#     # Append new entries
#     csv_data = pd.concat([csv_data, new_entries_df], ignore_index=True)

#     # Save the updated DataFrame to the CSV file
#     save_csv(csv_data, csv_file_path)

# def clean_and_split_query(query):
#     filler_words = {'um', 'like', 'you', 'know', 'so', 'well', 'actually', 'basically', 'just', 'really'}
#     stop_words = {'is', 'are', 'was', 'were', 'what', 'who', 'how', 'where', 'when', 'why', 'to', 'know', 'would', 
#                   'like', 'i', 'me', 'you', 'his', 'her', 'ok', 'bye', 'i am sorry', 'it is what it is', 'it', 
#                   'is', 'on', 'over', 'under', 'inside', 'an', 'a', 'the', 'does', 'con', 'get', 'got', 'have', 
#                   'had', 'has', 'should', 'not', 'use', 'mobile', 'team', 'Team', 'Verdict', 'an', 'no', 
#                   'not', 'but', 'T', '15', 'with', 'off', 'issues', 'issue', 'is', 'in', 'the', 'problems', 
#                   'are', 'what', 'why', 'when', 'flt', 'flashing'}
    
#     cleaned_query = re.sub(r'[^\w\s]', '', query)
#     words = cleaned_query.lower().split()
#     return [word for word in words if word not in filler_words and word not in stop_words]

# def get_problems_by_keyword(keywords):
#     search_columns = ['Keywords(One word)', 'ASIC/Module']
#     matched_problems = pd.DataFrame()

#     for keyword in keywords:
#         matches = csv_data[csv_data[search_columns].apply(lambda row: row.astype(str).str.contains(rf'\b{keyword}\b', case=False).any(), axis=1)]
#         matched_problems = pd.concat([matched_problems, matches])
    
#     matched_problems = matched_problems.drop_duplicates()
#     return matched_problems['Problem'].tolist() if not matched_problems.empty else []

# def get_root_cause_and_solution(problem):
#     problem_row = csv_data[csv_data['Problem'] == problem]
#     if not problem_row.empty:
#         return problem_row['Root cause'].values[0], problem_row['Solution'].values[0]
#     return None, None

# def is_adding_data_query(query):
#     add_data_phrases = [
#         "add data", "I want to add", "please add", "let's add", "adding data",
#         "I need to add", "can you add", "add new entry", "new entry",
#         "submit data", "want to input", "enter data"
#     ]
    
#     return any(phrase in query.lower() for phrase in add_data_phrases)

# def is_deleting_data_query(query):
#     delete_data_phrases = [
#         "delete data", "remove entry", "can you delete", "please remove",
#         "I want to delete", "how do I delete", "remove record"
#     ]
    
#     return any(phrase in query.lower() for phrase in delete_data_phrases)

# def detect_keyword_type(keyword):
#     """ Determine if the keyword is a verb, adjective, or known term. """
#     if len(keyword) == 0:
#         return None

#     synsets = wn.synsets(keyword)
    
#     if not synsets:
#         return "unknown"
    
#     # Check the first synset for its part of speech
#     pos = synsets[0].pos()
#     if pos in ['v']:  # Verb
#         return "verb"
#     elif pos in ['a']:  # Adjective
#         return "adjective"
#     elif pos in ['n', 's']:  # Noun
#         return "noun"
#     elif pos in ['r']:  # Adverb
#         return "adverb"
#     else:  # Other types
#         return "unknown"

# def get_response(query):
#     greeting_response = detect_greeting(query)
#     if greeting_response:
#         return greeting_response

#     keywords = clean_and_split_query(query)
#     if len(keywords) == 1:
#         keyword_type = detect_keyword_type(keywords[0])
#         if keyword_type in ["verb", "adjective"]:
#             return "Please provide more details; your input is too vague."
#         elif keyword_type in ["noun", "pronoun"]:
#             return f"What do you want to know about '{keywords[0]}'?"
#         else:
#             return "I'm not sure what you mean by that. Could you elaborate?"

#     # Handle multiple keywords
#     problems = get_problems_by_keyword(keywords)
#     if problems:
#         return problems

#     if is_adding_data_query(query):
#         return "Please provide the information to add new data."

#     if is_deleting_data_query(query):
#         return "Please specify which entry you want to delete."

#     return "What do you want to know about this?"

# def detect_greeting(query):
#     greetings = {
#         "hi": "Hello! How can I assist you today?",
#         "good morning": "Good morning! Have a nice day.",
#         "good afternoon": "Good afternoon! Have a great day.",
#         "good evening": "Good evening! Go and have snacks.",
#         "good night": "Good night! Sleep well."
#     }
#     for key, value in greetings.items():
#         if key in query.lower():
#             return value
#     return None

# st.markdown("<h1 style='text-align: center;'> HitLit 🔥 </h1>", unsafe_allow_html=True)

# user_input = st.text_input("Your message", key="user_input")

# if user_input:
#     st.session_state.chat_history.append(user_input)
#     ai_response = get_response(user_input)

#     if is_adding_data_query(user_input):
#         entries = []
#         num_entries = st.number_input("How many entries do you want to add?", min_value=1, max_value=10, value=1)
        
#         for i in range(num_entries):
#             st.markdown(f"### Entry {i + 1}")
#             updater_name = st.text_input(f"Enter Your Name for Entry {i + 1}:", key=f"name_input_{i}")
#             keyword = st.text_input(f"Enter Keyword for Entry {i + 1}:", placeholder="e.g. Error Code 123", key=f"keyword_input_{i}")
#             asic_module = st.text_input(f"Enter ASIC/Module for Entry {i + 1}:", placeholder="e.g. Module XYZ", key=f"asic_module_input_{i}")
#             problem = st.text_input(f"Enter Problem for Entry {i + 1}:", placeholder="Describe the issue", key=f"problem_input_{i}")
#             root_cause = st.text_input(f"Enter Root Cause for Entry {i + 1}:", placeholder="Explain the root cause", key=f"root_cause_input_{i}")
#             solution = st.text_input(f"Enter Solution for Entry {i + 1}:", placeholder="Provide the solution", key=f"solution_input_{i}")
#             project = st.text_input(f"Enter Project for Entry {i + 1}:", placeholder="e.g. Project ABC", key=f"project_input_{i}")

#             if st.button(f"Submit Entry {i + 1}", key=f"submit_entry_{i}"):
#                 if all([updater_name, keyword, asic_module, problem, root_cause, solution, project]):
#                     entries.append((keyword, asic_module, problem, root_cause, solution, updater_name, project))
#                     st.success(f"Entry {i + 1} submitted!")
#                 else:
#                     st.error("Please fill in all fields before submitting.")

#         if entries:
#             add_to_csv(entries)
#             st.success("All entries added successfully!")
#             for entry in entries:
#                 st.session_state.chat_history.append(f"Added new data: {entry[0]}, {entry[1]}, {entry[2]}")

#     elif is_deleting_data_query(user_input):
#         # Implement deletion logic here as needed
#         st.write("Deletion feature is not yet implemented.")

#     elif isinstance(ai_response, list):
#         selected_problem = st.selectbox("Select a problem:", options=ai_response)
#         if st.button("Get Root Cause and Solution"):
#             root_cause, solution = get_root_cause_and_solution(selected_problem)
#             if root_cause and solution:
#                 st.write(f"**Root Cause:** {root_cause}")
#                 st.write(f"**Solution:** {solution}")
#                 st.session_state.chat_history.append(f"Root Cause: {root_cause}\nSolution: {solution}")
#             else:
#                 st.write("No root cause and solution found.")

#     else:
#         st.session_state.chat_history.append(ai_response)

# if st.button("Clear Chat"):
#     st.session_state.chat_history = []
#     st.success("Chat cleared successfully!")

# st.markdown("<hr><p style='text-align: center;'><small>Made with ❤️ by You</small></p>", unsafe_allow_html=True)


# import streamlit as st
# import pandas as pd
# import re
# from datetime import datetime
# from nltk.corpus import wordnet as wn

# # Initialize session state variables
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
# if "last_keywords" not in st.session_state:
#     st.session_state.last_keywords = []
# if "selected_problem" not in st.session_state:
#     st.session_state.selected_problem = None
# if "pending_feedback" not in st.session_state:
#     st.session_state.pending_feedback = False

# # Set up the Streamlit app
# st.set_page_config(page_title="HitLit", page_icon="🤖", initial_sidebar_state="expanded")

# @st.cache_data
# def load_csv(file_path):
#     return pd.read_csv(file_path)

# def save_csv(data, file_path):
#     data.to_csv(file_path, index=False)

# csv_file_path = r"\\kor2fs03\V-V--Testing$\03_Validation_Software\LLBP\VALSW_LL_BP_SPL_V1.1.csv"
# csv_data = load_csv(csv_file_path)

# def add_to_csv(entries):
#     global csv_data
#     new_entries = []
    
#     for entry in entries:
#         keyword, asic_module, problem, root_cause, solution, updater_name, project = entry
#         serial_number = csv_data["Sr. No"].max() + 1 if not csv_data.empty else 1
#         date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
#         new_entry = {
#             "Sr. No": serial_number,
#             "Year": date,
#             "Author": updater_name,
#             "Project": project,
#             "Keywords(One word)": keyword.strip(),
#             "ASIC/Module": asic_module.strip(),
#             "Problem": problem.strip(),
#             "Root cause": root_cause.strip(),
#             "Solution": solution.strip()
#         }

#         new_entries.append(new_entry)

#     new_entries_df = pd.DataFrame(new_entries)
#     csv_data.drop(columns=['Updated By', 'Date', 'Serial Number'], errors='ignore', inplace=True)
#     csv_data = pd.concat([csv_data, new_entries_df], ignore_index=True)
    
#     # Remove unwanted lines from the DataFrame
#     unwanted_lines_condition = csv_data.apply(lambda row: row.astype(str).str.contains(r"dlkd'als|fhpiq\[oe\[|oqpoeq-2pw|w219e-=210=|1ue2oqwp", case=False).any(), axis=1)
#     csv_data = csv_data[~unwanted_lines_condition]


#     save_csv(csv_data, csv_file_path)

# def clean_and_split_query(query):
#     filler_words = {'um', 'like', 'you', 'know', 'so', 'well', 'actually', 'basically', 'just', 'really'}
#     stop_words = {'is', 'are', 'was', 'were', 'what', 'who', 'how', 'where', 'when', 'why', 'to', 'know', 
#                   'would', 'like', 'i', 'me', 'his', 'her', 'ok', 'bye', 'it', 'on', 'an', 'a', 'the', 
#                   'does', 'con', 'get', 'got', 'have', 'had', 'has', 'should', 'not', 'use', 'mobile', 
#                   'team', 'Verdict', 'no', 'but', 'with', 'off', 'issues', 'is', 'in', 'the', 'are',}
    
#     cleaned_query = re.sub(r'[^\w\s]', '', query)
#     words = cleaned_query.lower().split()
#     # Keep only non-filler and non-stop words
#     return [word for word in words if word not in filler_words and word not in stop_words]

# def get_problems_by_keyword(keyword):
#     search_columns = ['Keywords(One word)', 'ASIC/Module']
#     matches = csv_data[csv_data[search_columns].apply(lambda row: row.astype(str).str.contains(rf'\b{keyword}\b', case=False).any(), axis=1)]
#     return matches['Problem'].tolist() if not matches.empty else []

# def get_root_cause_and_solution(problem):
#     problem_row = csv_data[csv_data['Problem'] == problem]
#     if not problem_row.empty:
#         return problem_row['Root cause'].values[0], problem_row['Solution'].values[0]
#     return None, None

# def is_adding_data_query(query):
#     add_data_phrases = [
#         "add data", "i want to add", "please add", "let's add", "adding data",
#         "i need to add", "can you add", "add new entry", "new entry",
#         "submit data", "want to input", "enter data"
#     ]
    
#     return any(phrase in query.lower() for phrase in add_data_phrases)

# def is_deleting_data_query(query):
#     delete_data_phrases = [
#         "delete data", "remove entry", "can you delete", "please remove",
#         "i want to delete", "how do i delete", "remove record"
#     ]
    
#     return any(phrase in query.lower() for phrase in delete_data_phrases)
# def detect_keyword_type(keyword):
#     """ Always return 'keyword' since we want to search in the CSV without type restrictions. """
#     return "keyword"

# def get_response(query):
#     greeting_response = detect_greeting(query)
#     if greeting_response:
#         return greeting_response

#     keywords = clean_and_split_query(query)

#     if len(keywords) == 1:
#         keyword = keywords[0]
#         problems = get_problems_by_keyword(keyword)
        
#         if problems:
#             return list(set(problems))  # Return unique problems
#         else:
#             return "No related problems found for that keyword."

#     # Handle multiple keywords
#     problems = []
#     for keyword in keywords:
#         problems += get_problems_by_keyword(keyword)

#     if problems:
#         return list(set(problems))  # Return unique problems

#     if is_adding_data_query(query):
#         return "Please provide the information to add new data."

#     if is_deleting_data_query(query):
#         return "Please specify which entry you want to delete."

#     return "What do you want to know about this?"

# def detect_greeting(query):
#     greetings = {
#         "hi": "Hello! How can I assist you today?",
#         "good morning": "Good morning! Have a nice day.",
#         "good afternoon": "Good afternoon! Have a great day.",
#         "good evening": "Good evening! Go and have snacks.",
#         "good night": "Good night! Sleep well."
#     }
#     for key, value in greetings.items():
#         if key in query.lower():
#             return value
#     return None

# st.markdown("<h1 style='text-align: center;'> HitLit 🔥 </h1>", unsafe_allow_html=True)

# user_input = st.text_input("Your message", key="user_input")

# if user_input:
#     st.session_state.chat_history.append(user_input)
#     ai_response = get_response(user_input)

#     if is_adding_data_query(user_input):
#         entries = []
#         num_entries = st.number_input("How many entries do you want to add?", min_value=1, max_value=10, value=1)
        
#         for i in range(num_entries):
#             st.markdown(f"### Entry {i + 1}")
#             updater_name = st.text_input(f"Enter Your Name for Entry {i + 1}:", key=f"name_input_{i}")
#             keyword = st.text_input(f"Enter Keyword for Entry {i + 1}:", placeholder="e.g. Error Code 123", key=f"keyword_input_{i}")
#             asic_module = st.text_input(f"Enter ASIC/Module for Entry {i + 1}:", placeholder="e.g. Module XYZ", key=f"asic_module_input_{i}")
#             problem = st.text_input(f"Enter Problem for Entry {i + 1}:", placeholder="Describe the issue", key=f"problem_input_{i}")
#             root_cause = st.text_input(f"Enter Root Cause for Entry {i + 1}:", placeholder="Explain the root cause", key=f"root_cause_input_{i}")
#             solution = st.text_input(f"Enter Solution for Entry {i + 1}:", placeholder="Provide the solution", key=f"solution_input_{i}")
#             project = st.text_input(f"Enter Project for Entry {i + 1}:", placeholder="e.g. Project ABC", key=f"project_input_{i}")

#             if st.button(f"Submit Entry {i + 1}", key=f"submit_entry_{i}"):
#                 if all([updater_name, keyword, asic_module, problem, root_cause, solution, project]):
#                     entries.append((keyword, asic_module, problem, root_cause, solution, updater_name, project))
#                     st.success(f"Entry {i + 1} submitted!")
#                 else:
#                     st.error("Please fill in all fields before submitting.")

#         if entries:
#             add_to_csv(entries)
#             st.success("All entries added successfully!")
#             for entry in entries:
#                 st.session_state.chat_history.append(f"Added new data: {entry[0]}, {entry[1]}, {entry[2]}")

#     elif is_deleting_data_query(user_input):
#         # Implement deletion logic here as needed
#         st.write("Deletion feature is not yet implemented.")

#     elif isinstance(ai_response, list):
#         selected_problem = st.selectbox("Select a problem:", options=ai_response)
#         if st.button("Get Root Cause and Solution"):
#             root_cause, solution = get_root_cause_and_solution(selected_problem)
#             if root_cause and solution:
#                 st.write(f"**Root Cause:** {root_cause}")
#                 st.write(f"**Solution:** {solution}")
#                 st.session_state.chat_history.append(f"Root Cause: {root_cause}\nSolution: {solution}")
#             else:
#                 st.write("No root cause and solution found.")

#     else:
#         st.session_state.chat_history.append(ai_response)

# if st.button("Clear Chat"):
#     st.session_state.chat_history = []
#     st.success("Chat cleared successfully!")

# st.markdown("<hr><p style='text-align: center;'><small>Made with ❤️ by You</small></p>", unsafe_allow_html=True)


import streamlit as st
import pandas as pd
import re
from datetime import datetime
from nltk.corpus import wordnet as wn

# Initialize session state variables
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_keywords" not in st.session_state:
    st.session_state.last_keywords = []
if "selected_problem" not in st.session_state:
    st.session_state.selected_problem = None
if "pending_feedback" not in st.session_state:
    st.session_state.pending_feedback = False

# Set up the Streamlit app
st.set_page_config(page_title="HitLit", page_icon="🤖", initial_sidebar_state="expanded")

@st.cache_data
def load_csv(file_path):
    return pd.read_csv(file_path)

def save_csv(data, file_path):
    data.to_csv(file_path, index=False)

csv_file_path = r"\\kor2fs03\V-V--Testing$\03_Validation_Software\LLBP\VALSW_LL_BP_SPL_V1.1.csv"
csv_data = load_csv(csv_file_path)

def add_to_csv(entries):
    global csv_data
    new_entries = []
    
    for entry in entries:
        keyword, asic_module, problem, root_cause, solution, updater_name, project = entry
        serial_number = csv_data["Sr. No"].max() + 1 if not csv_data.empty else 1
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        new_entry = {
            "Sr. No": serial_number,
            "Year": date,
            "Author": updater_name,
            "Project": project,
            "Keywords(One word)": keyword.strip(),
            "ASIC/Module": asic_module.strip(),
            "Problem": problem.strip(),
            "Root cause": root_cause.strip(),
            "Solution": solution.strip()
        }

        new_entries.append(new_entry)

    new_entries_df = pd.DataFrame(new_entries)
    csv_data.drop(columns=['Updated By', 'Date', 'Serial Number'], errors='ignore', inplace=True)
    csv_data = pd.concat([csv_data, new_entries_df], ignore_index=True)
    
    # Remove unwanted lines from the DataFrame
    unwanted_lines_condition = csv_data.apply(lambda row: row.astype(str).str.contains(r"dlkd'als|fhpiq\[oe\[|oqpoeq-2pw|w219e-=210=|1ue2oqwp", case=False).any(), axis=1)
    csv_data = csv_data[~unwanted_lines_condition]

    save_csv(csv_data, csv_file_path)

def clean_and_split_query(query):
    filler_words = {
        'um', 'like', 'you', 'know', 'so', 'well', 'actually', 'basically', 'a',
        'just', 'really', 'the', 'an', 'is', 'are', 'was', 'were',
        'what', 'who', 'how', 'where', 'when', 'why', 'to', 'would',
        'i', 'me', 'his', 'her', 'ok', 'bye', 'it', 'on', 'and', 'but',
        'with', 'off', 'not', 'does', 'get', 'have', 'had', 'has', 'should',
        'this', 'that', 'these', 'those', 'my', 'your', 'our', 'his', 'her',
        'its', 'they', 'them', 'he', 'she', 'him', 'it', 'which', 'who',
        'whom', 'if', 'as', 'because', 'while', 'until', 'whereas', 'since',
        'for', 'nor', 'or', 'yet', 'so', 'both', 'either', 'neither',
        'not', 'just', 'always', 'often', 'sometimes', 'rarely', 'never'
    }

    cleaned_query = re.sub(r'[^\w\s]', '', query)
    words = cleaned_query.lower().split()
    return [word for word in words if word not in filler_words]


# def clean_and_split_query(query):
#     filler_words = {'um', 'like', 'you', 'know', 'so', 'well', 'actually', 'basically', 'just', 'really'}
#     stop_words = {'is', 'are', 'was', 'were', 'what', 'who', 'how', 'where', 'when', 'why', 'to', 'know', 
#                   'would', 'like', 'i', 'me', 'his', 'her', 'ok', 'bye', 'it', 'on', 'an', 'a', 'the', 
#                   'does', 'con', 'get', 'got', 'have', 'had', 'has', 'should', 'not', 'use', 'mobile', 
#                   'team', 'Verdict', 'no', 'but', 'with', 'off', 'issues', 'is', 'in', 'the', 'are', 'do','for','looking','look'}
    
#     cleaned_query = re.sub(r'[^\w\s]', '', query)
#     words = cleaned_query.lower().split()
#     # Keep only non-filler and non-stop words
#     return [word for word in words if word not in filler_words and word not in stop_words]

def get_problems_by_keyword(keyword):
    search_columns = ['Keywords(One word)', 'ASIC/Module']
    matches = csv_data[csv_data[search_columns].apply(lambda row: row.astype(str).str.contains(rf'\b{keyword}\b', case=False).any(), axis=1)]
    return matches['Problem'].tolist() if not matches.empty else []

def get_root_cause_and_solution(problem):
    problem_row = csv_data[csv_data['Problem'] == problem]
    if not problem_row.empty:
        return problem_row['Root cause'].values[0], problem_row['Solution'].values[0]
    return None, None

def is_adding_data_query(query):
    add_data_phrases = [
        "add data", "i want to add", "please add", "let's add", "adding data",
        "i need to add", "can you add", "add new entry", "new entry",
        "submit data", "want to input", "enter data",
        "i would like to do data entry", "i would like to add", "i want to input data",
        "can you help me add", "how do I add data", "i need to do data entry",
        "need to add information", "i want to submit","can i","can we add"
    ]
    
    return any(phrase in query.lower() for phrase in add_data_phrases)
def is_data_entry_query(query):
    data_entry_phrases = [
        "do a new data entry", "make a new entry", "create a new entry",
        "want to add an entry", "i want to input", "can i add",
        "i need to do data entry", "new data entry"
    ]
    
    return any(phrase in query.lower() for phrase in data_entry_phrases)

def is_deleting_data_query(query):
    delete_data_phrases = [
        "delete data", "remove entry", "can you delete", "please remove",
        "i want to delete", "how do i delete", "remove record"
    ]
    
    return any(phrase in query.lower() for phrase in delete_data_phrases)

def detect_keyword_type(keyword):
    """ Always return 'keyword' since we want to search in the CSV without type restrictions. """
    return "keyword"

def get_response(query):
    greeting_response = detect_greeting(query)
    if greeting_response:
        return greeting_response

    keywords = clean_and_split_query(query)

    if is_data_entry_query(query):
        return "Please provide the information to add a new data entry."

    if len(keywords) == 1:
        keyword = keywords[0]
        problems = get_problems_by_keyword(keyword)
        
        if problems:
            return list(set(problems))  # Return unique problems
        else:
            return "No related problems found for that keyword."

    # Handle multiple keywords
    problems = []
    for keyword in keywords:
        problems += get_problems_by_keyword(keyword)

    if problems:
        return list(set(problems))  # Return unique problems

    if is_adding_data_query(query):
        return "Please provide the information to add new data."

    if is_deleting_data_query(query):
        return "Please specify which entry you want to delete."

    return "What do you want to know about this?"

def detect_greeting(query):
    greetings = {
        "hi": "Hello! How can I assist you today?",
        "good morning": "Good morning! Have a nice day.",
        "good afternoon": "Good afternoon! Have a great day.",
        "good evening": "Good evening! Go and have snacks.",
        "good night": "Good night! Sleep well."
    }
    for key, value in greetings.items():
        if key in query.lower():
            return value
    return None

st.markdown("<h1 style='text-align: center;'> HitLit 🔥 </h1>", unsafe_allow_html=True)

# Add space between the title and the input
# st.markdown("<div style='height: 350px;'></div>", unsafe_allow_html=True)

# Refresh button in the top right corner
# if st.button("Refresh", key="refresh_button", help="Clear chat history", on_click=lambda: st.session_state.clear_chat()):
#     st.session_state.chat_history = []
#     st.success("Chat cleared successfully!")

user_input = st.text_input("Type your message", key="user_input")

if user_input:
    st.session_state.chat_history.append(user_input)
    ai_response = get_response(user_input)

    if is_adding_data_query(user_input):
        entries = []
        num_entries = st.number_input("How many entries do you want to add?", min_value=1, max_value=10, value=1)
        
        for i in range(num_entries):
            st.markdown(f"### Entry {i + 1}")
            updater_name = st.text_input(f"Enter Your Name for Entry {i + 1}:", key=f"name_input_{i}")
            keyword = st.text_input(f"Enter Keyword for Entry {i + 1}:", placeholder="e.g. Error Code 123", key=f"keyword_input_{i}")
            asic_module = st.text_input(f"Enter ASIC/Module for Entry {i + 1}:", placeholder="e.g. Module XYZ", key=f"asic_module_input_{i}")
            problem = st.text_input(f"Enter Problem for Entry {i + 1}:", placeholder="Describe the issue", key=f"problem_input_{i}")
            root_cause = st.text_input(f"Enter Root Cause for Entry {i + 1}:", placeholder="Explain the root cause", key=f"root_cause_input_{i}")
            solution = st.text_input(f"Enter Solution for Entry {i + 1}:", placeholder="Provide the solution", key=f"solution_input_{i}")
            project = st.text_input(f"Enter Project for Entry {i + 1}:", placeholder="e.g. Project ABC", key=f"project_input_{i}")

            if st.button(f"Submit Entry {i + 1}", key=f"submit_entry_{i}"):
                if all([updater_name, keyword, asic_module, problem, root_cause, solution, project]):
                    entries.append((keyword, asic_module, problem, root_cause, solution, updater_name, project))
                    st.success(f"Entry {i + 1} submitted!")
                else:
                    st.error("Please fill in all fields before submitting.")

        if entries:
            add_to_csv(entries)
            st.success("All entries added successfully!")
            for entry in entries:
                st.session_state.chat_history.append(f"Added new data: {entry[0]}, {entry[1]}, {entry[2]}")

    elif is_deleting_data_query(user_input):
        # Implement deletion logic here as needed
        st.write("Deletion feature is not yet implemented.")

    elif isinstance(ai_response, list):
        selected_problem = st.selectbox("Select a problem:", options=ai_response)
        if st.button("Get Root Cause and Solution"):
            root_cause, solution = get_root_cause_and_solution(selected_problem)
            if root_cause and solution:
                st.write(f"**Root Cause:** {root_cause}")
                st.write(f"**Solution:** {solution}")
                st.session_state.chat_history.append(f"Root Cause: {root_cause}\nSolution: {solution}")
            else:
                st.write("No root cause and solution found.")

    else:
        st.session_state.chat_history.append(ai_response)

if st.button("Clear Chat"):
    st.session_state.chat_history = []
    st.success("Chat cleared successfully!")

st.markdown("<hr><p style='text-align: center;'><small>Made with ❤️ by Me</small></p>", unsafe_allow_html=True)
