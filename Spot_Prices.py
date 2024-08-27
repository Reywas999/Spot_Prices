#!/usr/bin/env python
# coding: utf-8

# In[1]:


'''
The purpose of this script (now) is to take a user specified string input of a selection of metals 
they would like to see the current spot price and day change for, and return a dict of the 
price per ounce PPO and the daily change.
'''


# In[2]:


# Necessary imports
import requests
import re
from bs4 import BeautifulSoup


# In[3]:


# A list of metals with associated websites -- Can update if more are added (or deleted)
Possible_responses = ['silver', 'gold', 'platinum']


# In[4]:


# User specified metals as a string input
def input_metals():
    input_string = input(f'\nPlease enter the metal(s) you would like to return separated by commas.\nHere is a list of options:\n{", ".join(Possible_responses)}\nYour selection: ')
    return input_string


# In[5]:


def metal_list(input_string):
    '''
    1) Taking the user input string as an argument, splitting the string at the commas making sure
    to account for any accidental spacing, 
    2) converting the split values into a list, 
    3) converting all values to lowercase,
    4) Creating a list of valid responses
    5) comparing the new list to the list of valid responses 
    6) returning the metal list and the number of mismatch errors
    '''
    # Using re.split() to create a list from the user-input string, separating the input string at the
    # commas, using r',\s*' to account for any spaces input after the comma(s)
    metals_unclean = re.split(r',\s*', input_string)
    # Stripping any accidental spaces
    # Converting all letters in the list to lowercase to check against the possible responses
    metals = [s.lower().strip() for s in metals_unclean]

    # Couting any mismatch errors
    errors = 0
    for item in metals:
        if item in Possible_responses:
            pass
        else:
            print(f'\n{item} is not an item on the list. Please review the list and double check spelling.')
            errors += 1
            
    return metals, errors


# In[6]:


def error_checks():
    # Setting the input string to variable 'x'
    input_string = input_metals()
    # Running the function to return the list of metals and number of errors as variables
    metals, errors = metal_list(input_string)
    
    # If there were any errors, the user will be asked to reinput their metal selections until their input
    # matches the valid input list.
    while errors > 0:
        input_string = input_metals()
        metals, errors = metal_list(input_string)
        
    return metals


# In[7]:


def Fetch_Results():
    '''
    a) Fetch the metals
    1) Creating an empty dictionary for all the metal PPO and changes to be entered
    2) Iterate through each metal in the list and perform the following:
        a) scrape the text data from the appropriate metal URL
        b) search for the price per ounce value in the extracted text
        c) convert the dollar values into two seperate values accompanied by a key
        d) update the empty dictionary with the new key:value paring
    3) Return the dict of all metal values
    '''
    # Fetching the user input metals
    metals = error_checks()
    
    # Creating an empty dictionary for all the metal PPO and changes to be entered
    metal_values_dict = {}
    
    # Iterate through each of the metals and perform the following
    for metal in metals:
        # URL of the page to scrape
        url = f'https://www.apmex.com/{metal}-price'

        # Send a GET request to the webpage
        response = requests.get(url)
        
        # Check if the webpage is valid
        if response.status_code == 200:
            status = True # if it is, set the status to True
            # Parse the content of the page with BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
        else:
            status = False
            status_response = response.status_code # if its not valid, save the status code as status_response
            soup = 'N/a'
        
        if status == True:
            # If the webpage is valid, search for the PPO term ignoring cases
            if re.search(f"{metal} Price Per Ounce", soup.text, re.IGNORECASE):
                # The specific string you're looking for, in lowercase using casefold for case-insensitive comparison
                # Setting the specific string to look for and renaming the scraped text for simplicity
                specific_string = f"{metal} price per ounce"
                scraped_text = soup.text.lower()

                # The number of characters you want to return after the specific string
                num_chars = 30 # 30 is arbitrary, I just wanted to make sure I capture what I need

                # Use partition to find the first occurrence of the specific string and return the text after it
                _, _, after_specific_string = scraped_text.partition(specific_string)

                # If the specific string is found, after_specific_string will not be empty
                if after_specific_string:
                    # Return the text that comes after the first occurrence of the specific string
                    result_text = after_specific_string[:num_chars]
                    # Regular expression to match dollar values
                    pattern = r'\$(\d{1,3}(?:,\d{3})*\.\d{2})'

                    # Find all matches in the string
                    matches = re.findall(pattern, result_text)
                    
                    # Remove commas from each string and convert to float
                    matches = [float(s.replace(',', '')) for s in matches]

                    # Convert matches to float and store in a dictionary
                    dollar_values = {f'{metal} PPO': matches[0], f'{metal} change': matches[1]}
                    # Update the empty dictionary
                    metal_values_dict.update(dollar_values)
                else:
                    print(f"{metal} price per ounce cannot be found at this time.")
        else:
            # If the webpage was invalid
            print(f"Failed to retrieve the webpage. Status code: {status_response}")
        
    return metal_values_dict


# In[ ]:





# In[ ]:





# In[8]:


Fetch_Results()

