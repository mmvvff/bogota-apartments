import numpy as np
import re

def check_jacuzzi(x):
    """
    Check if 'JACUZZI' is in the list x.

    Args:
    x (list): A list of amenities.

    Returns:
    int: 1 if 'JACUZZI' is in the list x, 0 otherwise.
    """
    if type(x) == list:
        return 1 if 'JACUZZI' in x else 0
    else:
        return 0

def extract_piso(x):
    """
    Extracts the floor number from a list of strings.

    Args:
    x (list): A list of strings.

    Returns:
    int: The floor number if found in the list, otherwise np.nan.
    """
    if type(x) == list:
        try:
            for item in x:
                if item.startswith('PISO '):
                    return int(item.split(' ')[1])
        except:
            return np.nan
    else:
        return np.nan

def extract_closets(x):
    """
    Extracts the number of closets from a list of apartment features.

    Args:
    x (list): A list of apartment features.

    Returns:
    int: The number of closets in the apartment, or np.nan if not found.
    """
    if type(x) == list:
        try:
            for item in x:
                if item.startswith('CLOSETS'):
                    return int(item.split(' ')[1])
        except:
            return np.nan
    else:
        return np.nan

def check_chimeny(x):
    """
    Check if a list contains the string 'CHIMENEA'.

    Args:
    x (list): A list to check for the presence of 'CHIMENEA'.

    Returns:
    int: 1 if 'CHIMENEA' is in the list, 0 otherwise.
    """
    if type(x) == list:
        return 1 if 'CHIMENEA' in x else 0
    else:
        return 0

def check_mascotas(x):
    if type(x) == list:
        # return 1 if 'PERMITE MASCOTAS' in x else 0
        if 'PERMITE MASCOTAS' in x:
            return 1
        elif 'ADMITE MASCOTAS' in x:
            return 1
        else:
            return 0
    else:
        return 0

def check_gimnasio(x):
    """
    Checks if 'GIMNASIO' is in the input list and returns 1 if it is, 0 otherwise.

    Args:
    x (list): The input list to check for 'GIMNASIO'.

    Returns:
    int: 1 if 'GIMNASIO' is in the input list, 0 otherwise.
    """
    if type(x) == list:
        return 1 if 'GIMNASIO' in x else 0
    else:
        return 0

def check_ascensor(x):
    """
    Check if 'ASCENSOR' is in the given list.

    Args:
    x (list): A list of strings.

    Returns:
    int: 1 if 'ASCENSOR' is in the list, 0 otherwise.
    """
    if type(x) == list:
        return 1 if 'ASCENSOR' in x else 0
    else:
        return 0

def check_conjunto_cerrado(x):
    """
    Check if a list contains the string 'CONJUNTO CERRADO'.

    Args:
    x (list): A list of strings.

    Returns:
    int: 1 if 'CONJUNTO CERRADO' is in the list, 0 otherwise.
    """
    if type(x) == list:
        return 1 if 'CONJUNTO CERRADO' in x else 0
    else:
        return 0
    
def check_piscina(x):
    """
    Check if a list contains the string 'PISCINA'.

    Args:
    x (list): A list of strings.

    Returns:
    int: 1 if 'PISCINA' is in the list, 0 otherwise.
    """
    if type(x) == list:
        return 1 if 'PISCINA' in x else 0
    else:
        return 0
    

def check_salon_comunal(x):
    """
    Check if a list contains the string 'SALÓN COMUNAL'.

    Args:
    x (list): A list of strings.

    Returns:
    int: 1 if 'SALÓN COMUNAL' is in the list, 0 otherwise.
    """
    if type(x) == list:
        return 1 if 'SALÓN COMUNAL' in x else 0
    else:
        return 0
    
def check_terraza(x):
    """
    Check if a list contains the string 'TERRAZA'.

    Args:
    x (list): A list of strings.

    Returns:
    int: 1 if 'TERRAZA' is in the list, 0 otherwise.
    """
    if type(x) == list:
        return 1 if 'TERRAZA' in x else 0
    else:
        return 0
    
def check_amoblado(x):
    """
    Check if a list contains the string 'AMOBLADO'.

    Args:
    x (list): A list of strings.

    Returns:
    int: 1 if 'AMOBLADO' is in the list, 0 otherwise.
    """
    if type(x) == list:
        return 1 if 'AMOBLADO' in x else 0
    else:
        return 0
    
def check_vigilancia(x):
    """
    Check if a list contains the string 'VIGILANCIA'.

    Args:
    x (list): A list of strings.

    Returns:
    int: 1 if 'VIGILANCIA' is in the list, 0 otherwise.
    """
    if type(x) == list:
        return 1 if any(re.findall(r'VIGILANCIA', str(x))) else 0
    else:
        return 0
    
    