# Import relevant libraries
import streamlit as st
import pandas as pd
import streamlit_dataframe_editor as sde

# Function to demonstrate resetting to a dataframe's default contents
def reset_dataframe_content_callback(data_editor_key):
    st.session_state[data_editor_key].reset_dataframe_content()

# Function to demonstrate changing of a dataframe's contents
def update_editor_contents_callback(data_editor_key, new_df_contents):
    st.session_state[data_editor_key].update_editor_contents(new_df_contents=new_df_contents)

# Main function
def main():

    # Run streamlit-dataframe-editor library initialization tasks at the top of the page
    st.session_state = sde.initialize_session_state(st.session_state)

    # Constants
    default_df_contents3 = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
    default_df_contents4 = pd.DataFrame({'c': [11, 13], 'd': [14, 16]}, index=['hello', 'there']).reset_index()  # resetting index because it's probably best practice for the data editor df to have a reset index so the changes dictionary corresponds to a range index... maybe not totally necessary but it's clearer and more unified that way anyway

    # Initialize some variables in the session state
    if 'de3' not in st.session_state:
        st.session_state['de3'] = sde.DataframeEditor(df_name='df3', default_df_contents=default_df_contents3)
    if 'de4' not in st.session_state:
        st.session_state['de4'] = sde.DataframeEditor(df_name='df4', default_df_contents=default_df_contents4)

    # Create columns for displaying the editable dataframes
    demo_cols = st.columns(2)
    
    # Display one sample dataframe
    with demo_cols[0]:
        st.header('Dataframe 3')
        st.session_state['de3'].dataframe_editor(dynamic_rows=False)

    # Display another sample dataframe
    with demo_cols[1]:
        st.header('Dataframe 4')
        st.session_state['de4'].dataframe_editor(reset_data_editor_button=False)

    # Demonstrate additional usage scenarios
    st.header('Additional examples')

    # Demonstrate scraping of current contents of a dataframe
    # Note that since the dataframe is displayed (via st.dataframe()) *after* its contents are scraped, it is fine to call this within the "if st.button():" block
    if st.button('Show current dataframe 3 contents'):
        st.dataframe(st.session_state['de3'].reconstruct_edited_dataframe())

    # Demonstrate resetting to a dataframe's default contents
    # Note that per Streamlit's top-down operation, in order to display the reset dataframe *above*, a callback must be used to reset the dataframe content *before* displaying it. This typical Sreamlit behavior and if the resetting was done in an "if st.button():" block, then the change would only appear upon page refresh
    st.button('Reset Dataframe 4 to default values', on_click=reset_dataframe_content_callback, args=('de4',))

    # Demonstrate modification of a dataframe's contents
    # Same note as above (resetting of the dataframe to a default value) applies here: a callback must be used in Streamlit in general to update code higher up in the .py file
    st.button('Modify Dataframe 3 contents', on_click=update_editor_contents_callback, args=('de3', pd.DataFrame({99: ['a', 'b', 'c', 'd'], 200: ['aa', 'bb', 'cc', 'dd'], 101: ['aaa', 'bbb', 'ccc', 'ddd']})))

    # Run streamlit-dataframe-editor library finalization tasks at the bottom of the page
    st.session_state = sde.finalize_session_state(st.session_state)

# Call the main function
if __name__ == '__main__':
    main()
