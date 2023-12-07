# Import relevant libraries
import streamlit as st
from streamlit_javascript import st_javascript

# Reload everything in the session state except for widgets that cannot be so saved, which we manually ignore by appending "__do_not_persist" to the widget's key
for key, val in st.session_state.items():
    if (not key.endswith('__do_not_persist')) and (not key.startswith('FormSubmitter:')):
        st.session_state[key] = val
        
# Get the URL of the current page, per https://discuss.streamlit.io/t/what-is-the-current-page-in-use-multipage-app/41898, which we've used before but keeping the reference here anyway
curr_url = st_javascript("await fetch('').then(r => window.parent.location.href)")

# Initialize some variables in the session state
if 'previous_url' not in st.session_state:
    st.session_state['previous_url'] = curr_url

# Output something on the page
st.write('hi from home page')

# Save the URL of the current page before we potentially leave the page. This must be present on every page
st.session_state['previous_url'] = curr_url
