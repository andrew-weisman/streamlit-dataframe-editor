# Import relevant libraries
import streamlit as st
import random
import pandas as pd
from st_pages import get_pages, get_script_run_ctx

def get_random_integer(stop=1000000):
    '''
    Use this to create a new data editor key which is the only way to reset 
    an editable dataframe to its original contents, per 
    https://discuss.streamlit.io/t/reset-experimental-data-editor-to-original-values/41618. 
    We likely haven't run into this before because in our editable dataframes 
    we generally have new contents within the dataframe which forces this. 
    But to reset to the exact same contents, you need a different key.
    '''
    return '{:06d}'.format(random.randrange(start=0, stop=stop))

def reconstruct_edited_dataframe(df, changes_dict):
    '''
    Retaining information in a data editor upon switching pages
    '''

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

def save_data_editor_changes(key_for_changes_dict, key_for_data_editor_widget, additional_callback):
    '''
    From the data editor key, which is a dictionary of changes to the input dataframe, save the changes 
    dictionary to the session state
    This should probably be renamed as I've generalized it to include optional additional callbacks
    '''
    st.session_state[key_for_changes_dict] = st.session_state[key_for_data_editor_widget]
    if additional_callback is not None:
        additional_callback()

def get_current_page_name():
    '''This is a snippet from Zachary Blackwood using his st_pages package per 
    https://discuss.streamlit.io/t/how-can-i-learn-what-page-i-am-looking-at/56980 
    for getting the page name without having the script run twice as it does using 
    the st_javascript package with curr_url = st_javascript("await fetch('').then(r => window.parent.location.href)").
    # Note that you can also import these from streamlit directly
    '''
    pages = get_pages("")
    ctx = get_script_run_ctx()
    try:
        current_page = pages[ctx.page_script_hash]
    except KeyError:
        current_page = [
            p for p in pages.values() if p["relative_page_hash"] == ctx.page_script_hash
        ][0]
    return current_page['page_name']

def load_session_state_from_previous_page(session_state):
    '''
    Reload everything in session_state except for widgets that cannot be so saved, 
    which are manually ignore by appending "__do_not_persist" to the widget's key
    '''
    for key, val in session_state.items():
        if (not key.endswith('__do_not_persist')) and (not key.startswith('FormSubmitter:')):
            session_state[key] = val
    return session_state

def initialize_previous_page_name(current_page_name, session_state):
    '''
    Define the previous page name if it hasn't already been initialized
    '''
    if 'previous_page_name' not in session_state:
        session_state['previous_page_name'] = current_page_name
    return session_state

def initialize_session_state(session_state):
    '''
    Run common things at the top of the page in a single function
    '''
    session_state = load_session_state_from_previous_page(session_state)  # load the st.session_state from the previous page
    session_state['current_page_name'] = get_current_page_name()  # get the current page name, saving it to the session state
    session_state = initialize_previous_page_name(session_state['current_page_name'], session_state)  # initialize the previous page name to the current page name if it's not already defined. This is unnecessary to do on pages not containing any dataframe editor objects, but for uniformity in "decorating" all pages, it shouldn't hurt to include this here and to call top_matter() on all pages
    return session_state

def finalize_session_state(session_state):
    '''
    Set the old page name to the current page name
    '''
    session_state['previous_page_name'] = session_state['current_page_name']
    return session_state

def cast_column_labels_to_strings(df):
    '''
    Run a check on dataframe columns labels and convert them to strings if they're not already strings
    '''
    cols = df.columns
    non_str_cols = [col for col in cols if not isinstance(col, str)]
    non_str_cols_string_versions = [str(col) for col in non_str_cols]
    mapper = dict(zip(non_str_cols, non_str_cols_string_versions))
    if len(non_str_cols) > 0:
        st.warning('Columns with non-string labels have been detected, and Streamlit internally casts [columns names to strings](https://docs.streamlit.io/library/advanced-features/dataframes#limitations), a known limitation. This causes problems when data is edited in such columns, so we\'re now casting these column names to strings: {}.'.format(non_str_cols), icon='⚠️')
    return df.rename(columns=mapper)

class DataframeEditor:
    '''
    Define the DataframeEditor class
    '''

    def __init__(self, df_name, default_df_contents):
        '''
        Object instantiation
        '''
        self.df_name = df_name
        self.default_df_contents = cast_column_labels_to_strings(default_df_contents)
        self.reset_dataframe_content()

    def reset_dataframe_content(self, additional_callback=None):
        '''
        Initialize the editor contents to its default dataframe
        '''
        self.update_editor_contents(new_df_contents=self.default_df_contents, additional_callback=additional_callback)  # reset_key must = True (the default) here or else the resetting will not happen per nuances of Streamlit, due to the desired dataframe contents being the same as they once were with the same key I believe

    def update_editor_contents(self, new_df_contents, reset_key=True, additional_callback=None):
        '''
        Set the dataframe in the data editor to specific values robustly
        Note reset_key=True has some flicker but is necessary in case the data editor contents are ever the same, in which case they wouldn't update. So reset_key=False may lead to non-updates, but no flicker, and is the right option for e.g. leaving and coming back to the page containing the data editor as long as the contents were not expected to have changed in the interim, so there's no need to force a refresh using reset_key=True.
        '''

        df_name = self.df_name

        st.session_state[df_name] = cast_column_labels_to_strings(new_df_contents)
        st.session_state[df_name + '_changes_dict'] = {'edited_rows': {}, 'added_rows': [], 'deleted_rows': []}

        # This step causes brief flashing of the dataframe so it's best to not run this unless required. A good time to not run this is when a dataframe is reloaded after leaving and coming back to the page it's on
        if reset_key:
            st.session_state[df_name + '_key'] = df_name + '_' + get_random_integer() + '__do_not_persist'  # not strictly necessary to do every time, though it is in the case where the new data is exactly the same as the original data, so we may as well do it every time

        # Allow extra functionality to be run if the data editor contents are programmatically changed
        if additional_callback is not None:
            additional_callback()

    def reconstruct_edited_dataframe(self):
        '''
        Method version of same-named function
        '''
        df_name = self.df_name
        return reconstruct_edited_dataframe(st.session_state[df_name], st.session_state[df_name + '_changes_dict'])

    def dataframe_editor(self, current_page_key='current_page_name', previous_page_key='previous_page_name', dynamic_rows=True, reset_data_editor_button=True, reset_data_editor_button_text='Reset data editor', on_change=None, hide_index=None, column_config=None):
        '''
        Function to perform all data editor functionalities for a dataframe that users should be able to manipulate
        '''
        df_name = self.df_name
        current_page_name = st.session_state[current_page_key]
        previous_page_name = st.session_state[previous_page_key]

        # If the user switches to this page, then 
        # have the data editor input be the previously saved data editor "output". 
        # Note doing this provide a smooth and hiccup-free experience
        # e.g., no scrollbar snapping back to the topmost location
        if current_page_name != previous_page_name:
            self.update_editor_contents(new_df_contents=self.reconstruct_edited_dataframe(), reset_key=False)

        # Output a data editor for a dataframe of interest
        if dynamic_rows:
            num_rows='dynamic'
        else:
            num_rows='fixed'
        st.data_editor(st.session_state[df_name], key=st.session_state[df_name + '_key'], on_change=save_data_editor_changes, args=(df_name + '_changes_dict', st.session_state[df_name + '_key'], on_change), num_rows=num_rows, hide_index=hide_index, column_config=column_config)
        # st.write(f'st.data_editor() key for the dataframe {df_name}: {st.session_state[df_name + "_key"]}')

        # Create a button to reset the data in the data editor
        if reset_data_editor_button:
            st.button(reset_data_editor_button_text, on_click=self.reset_dataframe_content, key=(df_name + '_button__do_not_persist'), kwargs={'additional_callback': on_change})
