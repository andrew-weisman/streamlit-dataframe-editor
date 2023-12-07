# Import relevant libraries
import streamlit as st
import streamlit_dataframe_editor as sde

# Main function
def main():

    # Load the st.session_state from the previous page
    st.session_state = sde.load_session_state_from_previous_page(st.session_state)

    # Output something on the page
    st.write('Hi from home page')

    # If there are no data editors to be present on the page, save the page name like this before potentially leaving the page. This must be present on every page (per Zachary Blackwood at https://discuss.streamlit.io/t/how-can-i-learn-what-page-i-am-looking-at/56980)
    st.session_state['previous_page_name'] = sde.get_current_page_name()

# Call the main function
if __name__ == '__main__':
    main()
