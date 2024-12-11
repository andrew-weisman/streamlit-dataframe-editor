# Import relevant libraries
import streamlit as st
import streamlit_dataframe_editor as sde

# Main function
def main():

    # Run streamlit-dataframe-editor library initialization tasks at the top of the page
    st.session_state = sde.initialize_session_state(st.session_state)

    # Output something on the page
    st.write('Hi from a page that does not contain a `DataframeEditor` object')

    # Run streamlit-dataframe-editor library finalization tasks at the bottom of the page
    st.session_state = sde.finalize_session_state(st.session_state)

# Call the main function
if __name__ == '__main__':
    main()
