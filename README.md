# streamlit-dataframe-editor

The [st.data_editor()](https://docs.streamlit.io/library/advanced-features/dataframes) widget is a great way to interact with dataframes in Streamlit, but common problems include:

1. Retrieving the contents of the edited dataframe (the robust way to do it is to use `st.session_state` and not the output from the widget)
1. Losing changes made to dataframes on multi-page apps after leaving and coming back to the page
1. Unresponsive resetting of the contents of the dataframe back to the original contents

This `streamlit-dataframe-editor` package allows you to perform all these tasks efficiently and easily. Overall, whatever issues we've encountered with `st.data_editor()` for dataframes, we've addressed them with appropriate workarounds by abstracting them into a module.

## Setup

At the top of every page in the app, regardless of whether an editable dataframe will be included, add:

```python
import streamlit_dataframe_editor as sde
st.session_state = sde.initialize_session_state(st.session_state)
```

and add this to the bottom:

```python
st.session_state = sde.finalize_session_state(st.session_state)
```

**Only on a page where you would like to create an editable dataframe,** somewhere in between, instantiate the class for each desired editable dataframe using something like:

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

## Example

To see the package in action, clone this repository and run:

```bash
streamlit run home.py
```

Don't forget to switch back and forth between the pages to see the saved edited dataframe contents.

## Dependencies

The only atypical dependency of this package is [st-pages](https://github.com/blackary/st_pages), which is used only to obtain the current page name.
