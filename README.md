# streamlit-dataframe-editor

Module (with complete example) to robustly handle editable dataframes in Streamlit, showing (1) how to persist data editor changes for dataframes in a clean way (e.g., data_editor is smooth, no hesitations or scrollbar snapping) when switching between Streamlit pages and (2) how to reset a data editor's contents back to its original contents

## TODO

* Post on Streamlit Community and link to [previous post](https://discuss.streamlit.io/t/simultaneous-multipage-widget-state-persistence-data-editors-with-identical-contents-and-multiprocessing-capability/52554)
* Try not updating the key when copying values from previous page state to see if that helps with initial flashing
* Test a bit more
