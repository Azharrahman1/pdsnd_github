import time
import pandas as pd
import numpy as np
import datetime
#import matplotlib.pyplot as plt

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    """
    Brief, simple inner function to show error message.
    """
    
    # Define error function to handle invalid inputs
    def incorrect_input():
        print ("sorry, please rectify input and try again.")

    # Get user input for city (chicago, new york city, washington).
    while True:
        city = input("\nWhich city would you like to see data for? Chicago, New York, or Washington ?\n").lower()
        if city in ['chicago', 'new york', 'washington']:
            break
        else:
            incorrect_input()

    # Get user input for month (all, january, february, ... , june)
    while True:
        month = input("\nPlease specify the month from January to June or input 'all'.\n").lower()
        if month in ["january", "february", "march", "april", "may", "june", "all"]:
            break
        else:
            incorrect_input()

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("\nPlease specify the day from Monday to Sunday or input 'all'.\n").lower()
        if day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "all"]:
            break
        else:
            incorrect_input()

    print('-'*40)
    return city, month, day

    #load data process
def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    file_name = CITY_DATA[city]
    print ("Start to load data from " + file_name + " ...")
    df = pd.read_csv(file_name)

    # convert 'Star Time' to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # month filter
    if month != 'all':
        # extract month and day of week from Start Time to create new columns
        df['month'] = df['Start Time'].dt.month
        df['day_of_week'] = df['Start Time'].dt.weekday_name

        # Get the index for the corresponding month and then + 1 
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # create new df with the inputted month
        df = df[df['month'] == month]

    # day filter
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df
    

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # convert 'Start Time' to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

# Display the most common month
    common_month = df['month'].value_counts().idxmax()  #df['month'].mode()[0]
    print('Most Common Month;', common_month)
    
 # Display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('Most common day;', common_day)
    
 # Display the most common start hour

    df['hour'] = df['Start Time'].dt.hour
    common_hr = df['hour'].mode()[0]
    print('Most Common Hour;', common_hr)
   

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print ('Most Commonly Used Start Station;', df['Start Station'].value_counts().idxmax())

    # display most commonly used end station
    print ('Most Commonly Used End Station;', df['End Station'].value_counts().idxmax())

    # display most frequent combination of start station and end station trips
    grouped_stations = df.groupby(['Start Station', 'End Station'])
    
    max_combo = grouped_stations.size().sort_values(ascending = False).head(1)
    
    print('\nThe most commonly used combination of start and end stations;', max_combo)
   

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    # display total travel time
    total_travel = int(df['Trip Duration'].sum())
    
    total_time = str(datetime.timedelta(seconds = total_travel))
    
    print('\nThe total travel time is;', total_time)
                
                           
    # display mean travel time
    average = int(df['Trip Duration'].mean())
    
    mean_time = str(datetime.timedelta(seconds = average))
    
    print('\nThe mean travel time is;', mean_time)
   

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display user type count
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display gender type count
    try:
        genders = df['Gender'].value_counts()
        print("\nThe gender ratio is\n", genders)
    except KeyError:
        print("\nNo data available for selected month/city")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print("\nThe earliest year of birth is;", int(df['Birth Year'].min()))
        print("\nThe most year of birth is;", int(df['Birth Year'].max()))
        print("\nThe most common year of birth is;", int(df['Birth Year'].mode()[0])) 

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    #return raw data as per user request
    
def show_raw_data(df):
    user_input = input('Do you want to see raw data? Enter yes or no.\n')
    line_number = 0

    while True:
        if user_input.lower() != 'no':
            # Show specfic rows
            print(df.iloc[line_number : line_number+5])
            line_number +=5
            user_input = input('\nDo you want to see more raw data? Enter yes or no.\n')
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_raw_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break



if __name__ == "__main__":
	main()
