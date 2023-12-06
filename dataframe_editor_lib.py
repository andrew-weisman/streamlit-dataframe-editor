# Import relevant libraries
import streamlit as st
import pandas as pd
import random

# Set the dataframe in the data editor to specific values robustly
def update_dataframe_editor_contents(df_name, new_df_contents):
    '''
      Example calls (below):
        * update_dataframe_editor_contents('df2', default_df_contents2)  # either (1) initialization at the top of the script or (2) resetting of the data editor back to the original contents
        * update_dataframe_editor_contents('df2', reconstruct_edited_dataframe(st.session_state['df2'], st.session_state['df2_changes_dict']))  # updating of the contents to the saved values from the previous run of the page
    '''
    st.session_state[df_name] = new_df_contents
    st.session_state[df_name + '_changes_dict'] = {'edited_rows': {}, 'added_rows': [], 'deleted_rows': []}
    st.session_state[df_name + '_key'] = df_name + '_' + get_random_integer() + '__do_not_persist'  # not strictly necessary to do every time, though it is in the case where the new data is exactly the same as the original data, so we may as well do it every time

# This function is necessary for retaining information in a data editor upon switching pages
def reconstruct_edited_dataframe(df, changes_dict):

    # Make a copy of the original dataframe with a reset, range index
    df_edited = df.reset_index(drop=True)  # this resetting of the index is probably important because of how the indexing works below, which from https://docs.streamlit.io/library/advanced-features/dataframes#access-edited-data appears to be zero-based range indexing. Note this does not affect the indexing of the original dataframe, only the version of it (df_edited) that is input into the data_editor

    # Update edited rows
    for idx in changes_dict['edited_rows']:
        for col in changes_dict['edited_rows'][idx]:
            df_edited.loc[idx, col] = changes_dict['edited_rows'][idx][col]

    # Update added rows
    df_edited = pd.concat([df_edited, pd.DataFrame(changes_dict['added_rows'])]).reset_index(drop=True)

    # Update deleted rows
    df_edited = df_edited.drop(index=changes_dict['deleted_rows']).reset_index(drop=True)

    # Return the updated dataframe
    return df_edited

# From the data editor key, which is a dictionary of changes to the input dataframe, save the changes dictionary to the session state
def save_data_editor_changes(key_for_changes_dict, key_for_data_editor_widget):
    st.session_state[key_for_changes_dict] = st.session_state[key_for_data_editor_widget]

# Using this to create a new data editor key which is the only way to reset an editable dataframe to its original contents, per https://discuss.streamlit.io/t/reset-experimental-data-editor-to-original-values/41618. We likely haven't run into this before because in our editable dataframes we generally have new contents within the dataframe which forces this. But to reset to the exact same contents, you need a different key
def get_random_integer(stop=1000000):
    return '{:06d}'.format(random.randrange(start=0, stop=stop))

# Function to perform all data editor functionalities for a dataframe that users should be able to manipulate
def handle_dataframe_editor(df_name, default_df_contents, current_page_id, previous_page_key='previous_url'):

    # If we've just switched to this page, then have the input to the data editor be the previously saved "output" from the data editor. Note doing this like this should make the data editor experience smooth and hiccup-free, e.g., no scrollbar snapping back to the topmost location
    if current_page_id != st.session_state[previous_page_key]:
        update_dataframe_editor_contents(df_name, reconstruct_edited_dataframe(st.session_state[df_name], st.session_state[df_name + '_changes_dict']))

    # Output a data editor for a dataframe of interest
    st.data_editor(st.session_state[df_name], key=st.session_state[df_name + '_key'], on_change=save_data_editor_changes, args=(df_name + '_changes_dict', st.session_state[df_name + '_key']), num_rows='dynamic')

    # Create a button to reset the data in the data editor
    st.button('Reset data editor', on_click=update_dataframe_editor_contents, args=(df_name, default_df_contents), key=(df_name + '_button__do_not_persist'))
