# streamlit-dataframe-editor

The [st.data_editor()](https://docs.streamlit.io/library/advanced-features/dataframes) widget is a great way to interact with dataframes in Streamlit, but common problems include:

1. Retrieving the contents of the edited dataframe (the robust way to do it is to use `st.session_state` and not the output from the widget)
1. Losing changes made to dataframes on multi-page apps after leaving and coming back to the page
1. Unresponsive resetting of the contents of the dataframe back to the original contents

This `streamlit-dataframe-editor` package allows you to perform all these tasks efficiently and easily. Overall, whatever issues we've encountered with `st.data_editor()` for dataframes, we've addressed them with appropriate workarounds by abstracting them into a module.

## Setup

In the [new multipage structure](https://docs.streamlit.io/develop/concepts/multipage-apps/page-and-navigation) in Streamlit, a function called from the `if __name__ == '__main__':` (e.g. `main()`) should contain something like:

```python
# For widget persistence between pages, we need always copy the session state to itself, being careful with widgets that cannot be persisted, like st.data_editor() (where we use the "__do_not_persist" suffix to avoid persisting it)
for key in st.session_state.keys():
    if (not key.endswith('__do_not_persist')) and (not key.startswith('FormSubmitter:')):
        st.session_state[key] = st.session_state[key]

# This is needed for the st.dataframe_editor() class (https://github.com/andrew-weisman/streamlit-dataframe-editor) but is also useful for seeing where we are and where we've been
st.session_state['current_page_name'] = pg.url_path if pg.url_path != '' else 'Home'
if 'previous_page_name' not in st.session_state:
    st.session_state['previous_page_name'] = st.session_state['current_page_name']

# Render the select page
pg.run()

# Update the previous page location
st.session_state['previous_page_name'] = st.session_state['current_page_name']
```

On a page where you would like to create an editable dataframe, instantiate the class for each desired editable dataframe using something like:

```python
st.session_state['dataframe_editor'] = sde.DataframeEditor(df_name='my_dataframe', default_df_contents=pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}))
```

## Usage

### Editable dataframe creation

Where you used to create an editable dataframe like:

```python
st.session_state['my_dataframe_edited'] = st.data_editor(st.session_state['my_dataframe'])
```

now do so like:

```python
st.session_state['dataframe_editor'].dataframe_editor()  # note there is no return variable
```

### Display the contents of an editable dataframe

```python
current_contents = st.session_state['dataframe_editor'].reconstruct_edited_dataframe()
```

### Reset an editable dataframe to its default contents

```python
st.session_state['dataframe_editor'].reset_dataframe_content()
```

### Programmatically modify an editable dataframe's contents

```python
st.session_state['dataframe_editor'].update_editor_contents(new_df_contents=pd.DataFrame({'c': [11, 13], 'd': [14, 16]}))
```

### Completely reset a dataframe editor object

This essentially both updates what's in the dataframe editor (as above) *and* it's default contents, so e.g. when you hit the "Reset" button, the dataframe will be reset to a *new* dataframe:

```python
del st.session_state['dataframe_editor']
```
