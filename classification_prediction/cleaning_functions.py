import pandas as pd

def weekdays(v):
    """
    This is a supporting function to cleaning(), to be used inside the latter. 
    Meant to be applied to each value of the weekdays variable.
    """
    if 'wed' in v:
        v = 'wednesday'
    elif 'thu' in v:
        v = 'thursday'
    elif 'fri' in v:
        v = 'friday'
        
    return v


# Combining all cleaning steps in a function
def cleaning(data):
    """
    This function is specific to 'Code_challenge_train.csv' and 'Code_challenge_test.csv'
    
    Parameters:
    -----------
    data: the data frame to clean. 
    """
    # numerical variables with strange characters and nulls: replace missing value with '9999'
    data[['x41', 'x45']] = data[['x41', 'x45']].fillna('9999')
    
    # strip the strange characters, and replace
    data['x41'] = data['x41'].map(lambda x: x.strip('$'))
    data['x45'] = data['x45'].map(lambda x: x.strip('%'))
    data[['x41', 'x45']] = data[['x41', 'x45']].astype('float')
    
    # filling nulls in rest of string variables with 'unknown'
    object_columns = data.select_dtypes(include='object').columns.to_list()
    data[object_columns] = data[object_columns].fillna('unknown')
    
    # weekdays variable is messy, cleaning it
    data['x35'] = data['x35'].map(lambda x: weekdays(x))
    
    # dropping 'x45'
    data.drop(['x45'], axis = 1, inplace = True)
    
    # changing months to numbers
    months_dict = {'January': 1, 'Feb': 2, 'Mar':3, 'Apr': 4, 'May': 5, 'Jun': 6, 'July': 7, 'Aug': 8, 'sept.': 9, 
                    'Oct': 10, 'Nov': 11, 'Dev': 12, 'unknown': 0}
    data['x68'] = data['x68'].map(months_dict)
    
    # one-hot encode the other string variables
    string_variables = data.select_dtypes(include='object').columns.to_list()
    string_dummies = pd.get_dummies(data[string_variables])
    data = pd.concat([data, string_dummies], axis = 1, sort = False)
    
    # dropping extra columns
    unknowns_columns = [n for n in data.columns if 'unknown' in n]
    data.drop(unknowns_columns, axis = 1, inplace = True)
    data.drop(['x34', 'x35', 'x93'], axis = 1, inplace = True)
    
    # filling missing values in the numerical variables
    numerical_columns = data.select_dtypes(exclude = 'object').columns.to_list()
    data[numerical_columns] = data[numerical_columns].fillna(method = 'bfill')
    
    return data