# streamlit-dataframe-editor

The [st.data_editor()](https://docs.streamlit.io/library/advanced-features/dataframes) widget is a great way to interact with dataframes in Streamlit, but common problems include:

1. Retrieving the contents of the edited dataframe (the robust way to do it is to use `st.session_state` and not the output from the widget)
1. Losing changes made to dataframes on multi-page apps after leaving and coming back to the page
1. Unresponsive resetting of the contents of the dataframe back to the original contents

This `streamlit-dataframe-editor` package allows you to perform all these tasks efficiently and easily.

## Usage

### Old data editor setup

```python
st.session_state['my_dataframe_edited'] = st.data_editor(st.session_state['my_dataframe'], num_rows='dynamic')
```

### New data editor setup

#### Same page as the data editor

Instantiate a member of the `DataframeEditor` class like:

```python
import streamlit_dataframe_editor as sde
st.session_state['dataframe_editor'] = sde.DataframeEditor(df_name='my_dataframe', default_df_contents=pd.DataFrame())
```

Then replace the usual call to `st.data_editor()` (including any return values as in the example above) with:

```python
st.session_state['dataframe_editor'].process_data_editor(current_page_id=current_page_name, previous_page_key='previous_page_name')
```

At the top of the page where you've done this, include:

```python
st.session_state = sde.load_session_state_from_previous_page(st.session_state)  # load the st.session_state from the previous page
current_page_name = sde.get_current_page_name()  # get the current page name
```

At the bottom of the page, save the current page name to the session state:

```python
st.session_state['previous_page_name'] = current_page_name
```

#### Different page from the data editor (i.e., any other pages)

On pages different from where the data editor is located, you need to save the page name to the session state.

At the top of these pages, load the session state from the previous page:

```python
import streamlit_dataframe_editor as sde
st.session_state = sde.load_session_state_from_previous_page(st.session_state)
```

As before, save the current page name to the session state:

```python
st.session_state['previous_page_name'] = sde.get_current_page_name()
```

### Utilization of the `DataframeEditor` object

To get the current values of the data editor:

```python
current_contents = st.session_state['dataframe_editor'].reconstruct_edited_dataframe()
```

To reset the data editor to its default values:

```python
st.session_state['dataframe_editor'].reset_dataframe_content()
```

To modify the contents of the rendered data editor:

```python
st.session_state['dataframe_editor'].update_editor_contents(new_df_contents=pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}), reset_key=True)
```

## Notes

Whenever the contents of the data editor are updated to prior or new values, you should generally set `reset_key=True` (the default) so that the `st.data_editor()` widget obtains a new key in `st.session_state`. This forces the contents of the data editor to refresh even when the contents will be the same as prior contents, and this will cause brief "flashing" of the data editor when it's loaded. When you are confident that the content of the data editor will be unchanged--such as when leaving and then returning to the page containing the data editor--you don't expect the contents to be updated anyway, so setting `reset_key=False` will indeed retain the previous contents of the data editor and prevent any flashing upon reloading of the data editor.

This latter case is automatically handled by the `DataframeEditor` class. Since the default setting is `reset_key=True`, then this means that in practice, you should never really need to set the `reset_key` parameter.

## Example

To see the package in action, clone this repository and run:

```bash
streamlit run home.py
```

Don't forget to switch back and forth between the pages to see the saved edited dataframe contents.

## Dependencies

The only atypical dependency of this package is [st-pages](https://github.com/blackary/st_pages), which is needed to obtain the current page name.

Alternatively, the package [streamlit-javascript](https://github.com/thunderbug1/streamlit-javascript) could be used to obtain the current page name, but this package seems to cause the Streamlit script to run twice, whereas `st-pages` does not.

## TODO

* Post on Streamlit Community and link to [previous post](https://discuss.streamlit.io/t/simultaneous-multipage-widget-state-persistence-data-editors-with-identical-contents-and-multiprocessing-capability/52554)
* Add code from that post to this repository?
* Turn into a package?
