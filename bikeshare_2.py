# this is the code I submitted for the bikesharing project on Udacity

import time
import pandas as pd
import numpy as np
import json

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


MONTHS = ['all', 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

DAYS = ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday' ]


def get_filters():

    # let's do this....  :-)
    # get user input (city, month, and day)

    print(MONTHS)

    print('Hello! Let\'s explore some US bikeshare data!')
    print('We have data for three major cities; Chicogo, New York, or Washington')

    while True:
        # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
        while True:
            city = input('Which city data do you want to view? \n> ').lower()
            if city in ['chicago', 'new york', 'washington']:
                break

        # get user input for month (all, january, february, ... , june)
        print('Which month would you like the data for? (enter ALL for all the data)')
        while True:
            month = input('Enter abreviated month (January = jan) \n>').lower()
            if month in MONTHS:
                break

        # get user input for day of week (all, monday, tuesday, ... sunday)
        print('Which day of the week would you like the data for? (enter ALL for all the data)')
        while True:
            day = input('Enter the day (i.e. Monday) \n>').lower()
            if day in DAYS:
                break

        print('And we are set!  So we are going to fetch the data for ' + city)
        print(' and filter ' + month.upper() + ' for the MONTHS field,')
        print(' and filter ' + day.upper() + ' for the DAYS field.')

        response = input('Is that correct? Y/N \n> ').lower()
        if response == 'y':
            break

    print('-'*40)
    return city, month, day


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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        month =  MONTHS.index(month)
        df = df[ df['month'] == month ]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[ df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].value_counts().idxmax()
    print("The most common month is :" + getFullMonth(most_common_month))

    # display the most common day of week
    most_common_day_of_week = df['day_of_week'].value_counts().idxmax()
    print("The most common day of week is :", most_common_day_of_week)

    # display the most common start hour

    most_common_start_hour = df['hour'].value_counts().idxmax()
    print("The most common start hour is :", most_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].value_counts().idxmax()
    print("The most commonly used start station :", most_common_start_station)

    # display most commonly used end station
    most_common_end_station = df['End Station'].value_counts().idxmax()
    print("The most commonly used end station :", most_common_end_station)

    # display most frequent combination of start station and end station trip
    most_common_start_end_station = df[['Start Station', 'End Station']].mode().loc[0]
    print("The most commonly used start station and end station : {}, {}"\
            .format(most_common_start_end_station[0], most_common_start_end_station[1]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

     # display total travel time
    total_travel = df['Trip Duration'].sum()
    print("Total travel time :", total_travel)

    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print("Mean travel time :", mean_travel)

    # display mean travel time
    max_travel = df['Trip Duration'].max()
    print("Max travel time :", max_travel)

    print("Travel time for each user type:\n")
    # display the total trip duration for each user type
    group_by_user_trip = df.groupby(['User Type']).sum()['Trip Duration']
    for index, user_trip in enumerate(group_by_user_trip):
        print("  {}: {}".format(group_by_user_trip.index[index], user_trip))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Counts of user types:\n")
    user_counts = df['User Type'].value_counts()

    # iteratively print out the total numbers of user types
    for index, user_count in enumerate(user_counts):
        print("  {}: {}".format(user_counts.index[index], user_count))

    print()

    # Display counts of gender
    if 'Gender' in df.columns:
        print("Counts of gender:\n")
        gender_counts = df['Gender'].value_counts()
        # iteratively print out the total numbers of genders
        for index,gender_count   in enumerate(gender_counts):
            print("  {}: {}".format(gender_counts.index[index], gender_count))

        print()

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        birth_year = df['Birth Year']
        # the most common birth year
        most_common_year = birth_year.value_counts().idxmax()
        print("The most common birth year:", most_common_year)
        # the most recent birth year
        most_recent = birth_year.max()
        print("The most recent birth year:", most_recent)
        # the most earliest birth year
        earliest_year = birth_year.min()
        print("The most earliest birth year:", earliest_year)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):

    """Displays raw bikeshare data."""

    response = input('\nWould you like to see the particular user trip data? Y/N \n> ')
    if response.lower() != 'n':
        number_of_rows = int(input('\nHow many rows of the data do you want to view (max 10) ? \n> '))
        if number_of_rows > 10:
            number_of_rows = 10

        # retrieve and convert data to json format
        # split each json row data
        row_data = df.iloc[0: number_of_rows].to_json(orient='records', lines=True).split('\n')
        for row in row_data:
            # pretty print each user data
            parsed_row = json.loads(row)
            json_row = json.dumps(parsed_row, indent=2)
            print(json_row)


def getFullMonth(most_common_month):
    full_month = {1: " January",
          2: " February",
          3: " March",
          4: " April",
          5: " May",
          6: " June",
          7: " July",
          8: " August",
          9: " September",
          10: " October",
          11: " November",
          12: " December"
          }
    return full_month.get(most_common_month, "All")

def main():

    # run through the rpogram as many times as the user wants
    while True:
        #go get the city, month and day that the user wants data for
        city, month, day = get_filters()
        #load that data into the variable df
        df = load_data(city, month, day)

        # go get statistics on the most frequent times of travel
        time_stats(df)

        #go get statistics on the most popular stations and trips
        station_stats(df)

        # go get statistics on the total and average trip durations
        trip_duration_stats(df)

        #go get stats on the bikeshare users
        user_stats(df)

        #see if the user wants to view some of the raw data - i mean, who wouldn't? right?
        display_data(df)

        #see if the user wants more data. if not end program
        restart = input('\n\n Would you like to restart? Y/N \n')
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
    main()
