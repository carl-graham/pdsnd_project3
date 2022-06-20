import time
import pandas as pd
import numpy as np
import tabulate as tb

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months_list = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november','december']

def get_city():
    """
    Asks user to specify a month, and day to analyze.
    Provides list of available options from CITY_DATA

    Returns:
        (str) city - name of the city to analyze
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities = list(CITY_DATA.keys())
    
    string_cities=""
    
    for city in cities:
        string_cities = string_cities + city + ", " 

    string_cities = string_cities[:-2]
    
    while True:
        city = input("Which city would you like to see the data for? Select from " + string_cities + "\n").lower()
        #could try if any(city in s for s in CITY_DATA), which would allow part strings to be found??
        if city not in CITY_DATA:
            print("This city was not recognised, please try again\n")
        else:
            break
            
    return city

def get_filters(month_options):
    """
    Asks user to specify a month, and day to analyze.
    Provides list of available options from CITY_DATA

    Returns:
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    # TO DO: get user input for month (all, january, february, ... , june)
    #could get month & day lists from data, to allow easy reusing
    while True:
        month = input("Which month would you like to see the data for? Use \'All\' to see all data available \n").lower()

        if month in month_options:
            break
        elif month == 'all':
            break
        else:
            print("This response was not recognised or the month selected is not in the data, please try again\n")
            continue
            
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Which day of the week would you like to see the data for? Use \'All\' to see all data available \n").lower()
        if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            break
        elif day == 'all':
            break
        else:
            print("This response was not recognised, please try again\n")
            continue

    print('-'*40)
    return month, day


def load_data(city):
    """
    Loads data for the specified city 

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
        # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    return df

def get_month_options(df):
    
    months_in_data = list(set(df['month']))
    
    month_options=[]
    
    for m in months_in_data:
        month_options.append(months_list[m-1])
    
    return month_options


def filter_data(df, month, day):
    """
    Filters the data by month and day if applicable.
    
    Args:
        (dataframe) df - Pandas dataframe containing city data
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
        # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    month_mode=int(df['month'].mode())
    month_name = months_list[month_mode-1].title()
    # TO DO: display the most common day of week
    day_mode=str(df['day_of_week'].mode())

    # TO DO: display the most common start hour
    time_mode=df['Start Time'].dt.hour.mode()

    table_display = [["Month", "Day", "Start Time"],[month_name, day_mode, time_mode]]
    
    print("--------Most frequent--------")
    print(tb.tabulate(table_display, headers="firstrow", tablefmt="simple"))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    print('\n')

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print("The most commonly used start station is:\n{}".format(df['Start Station'].value_counts().idxmax()))
    #mode_start_station = df['Start Station'].mode()

    # TO DO: display most commonly used end station
    print("The most commonly used end station is:\n{}".format(df['End Station'].value_counts().idxmax()))

    # TO DO: display most frequent combination of start station and end station trip
    
    most_freq_combo = df.groupby(["Start Station", "End Station"]).size().sort_values(ascending= False)
    print("The most frequent combination is:\n{}".format(most_freq_combo.head(1)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    print('\n')

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    travel_total = df['Trip Duration'].sum()

    # TO DO: display mean travel time
    travel_mean = df['Trip Duration'].mean()
    
    table_ttimes = [['Total Travel Time', 'Average Trip Duration (mins)'], [travel_total, travel_mean]]
    
    print("------------Trip Statistics------------")
    print(tb.tabulate(table_ttimes, headers="firstrow", tablefmt="simple"))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    print('\n')


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()

    # TO DO: Display counts of gender
    gender_count = df['Gender'].value_counts()

    # TO DO: Display earliest, most recent, and most common year of birth
    today = pd.to_datetime("today")
    this_year = today.year
    
    birth_year_mode = df['Birth Year'].mode()
    age_mode = this_year - birth_year_mode
    
    birth_year_latest = df['Birth Year'].max()
    age_latest = this_year - birth_year_latest
    
    birth_year_oldest = df['Birth Year'].min()
    age_oldest = this_year - birth_year_oldest
    
    table_dob = [['Most Common Birth Year', birth_year_mode, age_mode], ['Youngest birth year', birth_year_latest, age_latest],['Oldest birth year', birth_year_oldest, age_oldest]]
    
    table_user_data = [["User Types Count", "Gender Count"],[user_types, gender_count]]
    
    print("--------User Count Statistics--------")
    print(tb.tabulate(table_user_data, headers="firstrow", tablefmt="simple"))
    
    print("--------User Age Statistics--------")
    print(tb.tabulate(table_dob, headers=[" ", "Year", "Current Age"], tablefmt="simple"))
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    print('\n')

def view_data(df):
    """Displays data to the user on request"""
    continue_loop = True

    while continue_loop:

        show_data = input("Would you like to see the first 5 rows of data? Enter yes or no\n").lower()
    
        if show_data == 'yes':
            start_row=0
            continue_loop = False
            
            while show_data == 'yes':
                print (df.iloc[start_row:start_row+5])
                show_data = input("Would you like to see the next 5 rows of data? Enter yes or no\n").lower()
                start_row=start_row+5

        elif show_data = 'no':
            continue_loop = False
    

    

def main():
    while True:
        
        city = get_city()
        
        df = load_data(city)
        
        month_options = get_month_options(df)
        
        month, day = get_filters(month_options)
        
        df = filter_data(df, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        
        if city.lower() != 'washington':
            user_stats(df)

        view_data(df)    
            
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
