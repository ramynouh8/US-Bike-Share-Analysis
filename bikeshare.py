import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chi': 'chicago.csv', 'chicago': 'chicago.csv',
              'nyc': 'new_york_city.csv','new york city': 'new_york_city.csv',
              'wa': 'washington.csv', 'washington': 'washington.csv' }

def check_input(input_str,input_type):
    while True:
        input_read=input(input_str).lower()
        try:
            if input_read in ['chi','chicago','nyc','new york city','washington','wa'] and input_type==1:
                break
            elif input_read in ['january','february','march','april','may','june','all'] and input_type==2:
                break
            elif input_read in ['sunday','monday','tuesday','wednesday','thursday','friday','saturday','all'] and input_type==3:
                break
            else:
                if input_type==1:
                    print('wrong city dear :)\n your input should be [chi or chicago, nyc or new york city, wa or washington]')
                if input_type==2:
                    print('wrong month dear :)\n your input should be [january, february, march, april, may, june, all]')
                if input_type==3:
                    print('wrong day dear :)\n your input should be [sunday, monday, tuesday, wednesday, thursday, friday, saturday, all]')
        except ValueError:
            print('sorry dear, your input not valid dear ^^')
    return input_read

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello Dear! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = check_input("Would you like to see the data for chi or chicago, nyc or new york city, wa or washington?",1).lower()

    # get user input for month (all, january, february, ..(until).. , june)
    month = check_input("Which Month (all, january, ... june)?", 2).lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = check_input("Which day? (all, monday,... sunday)", 3).lower()

    print('<>'*20)
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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week, hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

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

    # display the most common month
    print(df['month'].mode()[0])

    # display the most common day of week
    print(df['day_of_week'].mode()[0])


    # display the most common start hour
    print(df['hour'].mode()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print(df['Start Station'].mode()[0])


    # display most commonly used end station
    print(df['End Station'].mode()[0])


    # display most frequent combination of start station and end station trip
    group_station=df.groupby(['Start Station','End Station'])
    print(group_station.size().sort_values(ascending=False).head(1))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('<>'*20)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print(df['Trip Duration'].sum())

    # display mean travel time
    print(df['Trip Duration'].mean())


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    print('User Type Stats:')
    print(df['User Type'].value_counts())
    if city != 'wa' and'washington':
        print('Gender Stats:')
        print(df['Gender'].value_counts())

        print('Birth Year Stats:')
        most_common_year = df['Birth Year'].mode()[0]
        
        print('Most Common Year:',most_common_year)
        most_recent_year = df['Birth Year'].max()
        
        print('Most Recent Year:',most_recent_year)
        earliest_year = df['Birth Year'].min()
        
        print('Earliest Year:',earliest_year)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('<>'*20)

def display_raw(df):

    raw_list = ['yes', 'no']
    rwdata = ''
    counter = 0
    while rwdata not in raw_list:
        print("\nDo you wish to view the raw data?")
        print("\nYes or yes\nNo or no")
        rwdata = input().lower()
        if rwdata == "yes":
            print(df.head())
        elif rwdata not in raw_list:
            print("\nWrong,Check your input dear :)")

    while rwdata == 'yes':
        print("Do you wish to view more raw data?")
        counter += 5
        rwdata = input().lower()
        if rwdata == "yes":
             print(df[counter:counter+5])
        elif rwdata != "yes":
             break


    print('<>'*20)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        display_raw(df)

        restart = input('\nWould you like to restart?\n Enter yes or no.\n')
        if restart.lower() != 'yes':
            print('Have a nice day ^^\n bye bye..')
            break


if __name__ == "__main__":
        main()
