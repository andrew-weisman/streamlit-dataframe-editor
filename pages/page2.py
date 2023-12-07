# This example shows two things: (1) how to persist data editor changes in a clean way (e.g., data_editor is smooth, no hesitations or scrollbar snapping) when switching between pages and (2) how to reset a data editor's contents back to its original contents

# Import relevant libraries
import streamlit as st
import pandas as pd
from streamlit_javascript import st_javascript
import streamlit_dataframe_editor

# Main function
def main():

    # Reload everything in the session state except for widgets that cannot be so saved, which we manually ignore by appending "__do_not_persist" to the widget's key
    for key, val in st.session_state.items():
        if (not key.endswith('__do_not_persist')) and (not key.startswith('FormSubmitter:')):
            st.session_state[key] = val

    # Get the URL of the current page, per https://discuss.streamlit.io/t/what-is-the-current-page-in-use-multipage-app/41898, which we've used before but keeping the reference here anyway. Remember something strange happens here, with the script running twice or the like and not picking up the session state fully or vice versa, so sometimes we see strange behavior as a result though it's usually not a bit deal. In this case I've taken care of it anyway below by resetting the index on default_df_contents2
    curr_url = st_javascript("await fetch('').then(r => window.parent.location.href)")

    # Constants
    default_df_contents3 = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
    default_df_contents4 = pd.DataFrame({'c': [11, 13], 'd': [14, 16]}, index=['hello', 'there']).reset_index()  # resetting index because it's probably best practice for the data editor df to have a reset index so the changes dictionary corresponds to a range index... maybe not totally necessary but it's clearer and more unified that way anyway

    # Initialize some variables in the session state
    if 'de3' not in st.session_state:
        st.session_state['de3'] = streamlit_dataframe_editor.DataframeEditor(df_name='df3', default_df_contents=default_df_contents3)
    if 'de4' not in st.session_state:
        st.session_state['de4'] = streamlit_dataframe_editor.DataframeEditor(df_name='df4', default_df_contents=default_df_contents4)
    if 'previous_url' not in st.session_state:
        st.session_state['previous_url'] = curr_url

    # Handle one sample dataframe
    st.session_state['de3'].process_data_editor(current_page_id=curr_url, previous_page_key='previous_url')

    # Handle another sample dataframe
    st.session_state['de4'].process_data_editor(current_page_id=curr_url, previous_page_key='previous_url')

    # Save the URL of the current page before we potentially leave the page. This must be present on every page
    st.session_state['previous_url'] = curr_url

# Call the main function
if __name__ == '__main__':
    main()
