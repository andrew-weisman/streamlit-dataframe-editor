# This example shows two things: (1) how to persist data editor changes in a clean way (e.g., data_editor is smooth, no hesitations or scrollbar snapping) when switching between pages and (2) how to reset a data editor's contents back to its original contents

# Import relevant libraries
import streamlit as st
import pandas as pd
import streamlit_dataframe_editor as sde

# Main function
def main():

    # Load the st.session_state from the previous page
    st.session_state = sde.load_session_state_from_previous_page(st.session_state)

    # Get the current page name
    current_page_name = sde.get_current_page_name()

    # Constants
    default_df_contents3 = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
    default_df_contents4 = pd.DataFrame({'c': [11, 13], 'd': [14, 16]}, index=['hello', 'there']).reset_index()  # resetting index because it's probably best practice for the data editor df to have a reset index so the changes dictionary corresponds to a range index... maybe not totally necessary but it's clearer and more unified that way anyway

    # Initialize some variables in the session state
    if 'de3' not in st.session_state:
        st.session_state['de3'] = sde.DataframeEditor(df_name='df3', default_df_contents=default_df_contents3)
    if 'de4' not in st.session_state:
        st.session_state['de4'] = sde.DataframeEditor(df_name='df4', default_df_contents=default_df_contents4)
    if 'previous_page_name' not in st.session_state:
        st.session_state['previous_page_name'] = current_page_name

    # Handle one sample dataframe
    st.session_state['de3'].process_data_editor(current_page_id=current_page_name, previous_page_key='previous_page_name')

    # Handle another sample dataframe
    st.session_state['de4'].process_data_editor(current_page_id=current_page_name, previous_page_key='previous_page_name')

    # Save the name of the current page before we potentially leave the page. This must be present on every page
    st.session_state['previous_page_name'] = current_page_name

# Call the main function
if __name__ == '__main__':
    main()
