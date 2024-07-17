# This script was created for compatibility with the global state defined in global_state_lib.py and should eventually be updated to include all the features in streamlit_dataframe_editor.py.

# Import relevant libraries
import streamlit as st
import pandas as pd

# Define the prefix for the keys used in the state_holder on this page
st_key_prefix = 'streamlit_dataframe_editor_global__'


# From an original dataframe and its changes, construct the edited dataframe
def reconstruct_edited_dataframe(df_orig, changes_dict):

    # As long as there are changes to reconstruct...
    if changes_dict is not None:

        # Make a copy of the original dataframe with a reset, range index
        df_edited = df_orig.reset_index(drop=True)  # this resetting of the index is probably important because of how the indexing works below, which from https://docs.streamlit.io/library/advanced-features/dataframes#access-edited-data appears to be zero-based range indexing. Note this does not affect the indexing of the original dataframe, only the version of it (df_edited) that is input into the data_editor

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
    
    # If there are no changes to the original dataframe, just return the original dataframe
    else:
        return df_orig


# Set the original dataframe to the edited dataframe and empty the changes dictionary
def fast_forward_editable_dataframe_in_state(state_holder, key_df_orig, key_changes_dict):
    changes_dict = state_holder[key_changes_dict]
    if changes_dict is not None:
        df_orig = state_holder[key_df_orig]
        state_holder[key_df_orig] = reconstruct_edited_dataframe(df_orig, changes_dict)
        state_holder[key_changes_dict] = None


# Define a class to render editable dataframes in a robust way
class DataframeEditor:

    # Constructor
    def __init__(self, df_orig, df_description, state_holder):

        # Set the key names for the following editable dataframe
        key_df_orig = st_key_prefix + 'df_orig_' + df_description
        key_changes_dict = key_df_orig + '_changes_dict' + '__dataframe_editor'

        # Save attributes to the object
        self.df_orig = df_orig
        self.state_holder = state_holder
        self.key_df_orig = key_df_orig
        self.key_changes_dict = key_changes_dict


    # Render the editable dataframe using st.data_editor() with a dataframe as its input
    def render_data_editor(self, on_change=None, previous_page_name_key='previous_page_name', current_page_name_key='current_page_name', num_rows='fixed'):

        # Load attributes
        state_holder = self.state_holder
        key_df_orig = self.key_df_orig
        key_changes_dict = self.key_changes_dict
        df_orig = self.df_orig

        # If we are revisiting a previous page, fast forward the editable dataframe, otherwise we will recover the ground zero dataframe instead of the last edited state of it
        if (previous_page_name_key in state_holder) and (current_page_name_key in state_holder):
            if state_holder[previous_page_name_key] != state_holder[current_page_name_key]:
                fast_forward_editable_dataframe_in_state(state_holder, key_df_orig, key_changes_dict)

        # Data editor widget
        if key_df_orig not in state_holder:
            state_holder[key_df_orig] = df_orig
        st.data_editor(state_holder[key_df_orig], key=key_changes_dict, on_change=on_change, args=(state_holder, key_changes_dict), num_rows=num_rows)


    # Reconstruct the edited dataframe
    def reconstruct_edited_dataframe(self):

        # Load attributes
        state_holder = self.state_holder
        key_df_orig = self.key_df_orig
        key_changes_dict = self.key_changes_dict

        # Reconstruct the edited dataframe
        return reconstruct_edited_dataframe(state_holder[key_df_orig], state_holder[key_changes_dict])
    

    # Fast forward the two properties of an editable dataframe: (1) the original dataframe and (2) changes to it
    def fast_forward_editable_dataframe_in_state(self):

        # Load attributes
        state_holder = self.state_holder
        key_df_orig = self.key_df_orig
        key_changes_dict = self.key_changes_dict

        # Fast forward the editable dataframe
        fast_forward_editable_dataframe_in_state(state_holder, key_df_orig, key_changes_dict)
